import semver
import requests
import os
import re
import logging
from build_version.common.interfaces import ReleaseType
from build_version.common.utils import check_release_type
from build_version.lib.interfaces import VersionIncrementType
from build_version.lib.utils import generate_random_string
from build_version.common.process_base import ProcessBase

logger = logging.getLogger(__name__)
log_level = os.environ.get("LOG_LEVEL", "INFO")

class ProcessSemVer(ProcessBase):
  def __init__(self, **data):
    super().__init__(**data)

  def get_increment_type(self) -> VersionIncrementType:
    repo = os.environ.get("GITHUB_REPOSITORY")
    
    if not (repo and self._ref_name and self._private_token):
      return VersionIncrementType.PATCH
    headers = {
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {self._private_token}",
      "X-GitHub-Api-Version": "2022-11-28"
    }
    base_url = f"https://api.github.com/repos/{repo}"

    if re.fullmatch(r"^[0-9]+/merge$", ref_name):
      return VersionIncrementType.PATCH
    commit_sha = os.environ.get("GITHUB_SHA", "")
    if not commit_sha:
      return VersionIncrementType.PATCH
    url = f"{base_url}/commits/{commit_sha}"
    commit_response = requests.get(url, headers=headers)
    if commit_response.status_code != 200:
      return VersionIncrementType.PATCH
    commit_data = commit_response.json()
    message = commit_data["commit"]["message"]
    message_match = re.search(r"\(#[0-9]+\)", message)
    if not message_match:
      return VersionIncrementType.PATCH
    matched_group = message_match.group(0)
    matched_number = re.search(r"[0-9]+", matched_group)
    if not matched_number:
      return VersionIncrementType.PATCH
    pr_id = matched_number.group(0)
    if not pr_id:
      return VersionIncrementType.PATCH
    url = f"{base_url}/pulls/{pr_id}"
    
    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      retrieved_labels = response.json().get("labels", [])
      highest_increment = VersionIncrementType.PATCH
      for label in retrieved_labels:
        label_name = label["name"].lower()
        if label_name == "major":
          highest_increment = VersionIncrementType.MAJOR
          break
        elif (
          label_name == "minor"
          and highest_increment != VersionIncrementType.MAJOR 
        ):
          highest_increment = VersionIncrementType.MINOR
      return highest_increment
    except (requests.RequestException, ValueError):
      return VersionIncrementType.PATCH
  
  def get_current_version(self) -> str:
    tags = self._repo.tags
    version_tags = [tag for tag in tags if re.match(r"v\d+\.\d+\.\d+$", tag.name)]
    if not version_tags:
      return "0.0.0"
    latest_tag = sorted(
      version_tags, key=lambda t: list(map(int, t.name.strip("v").split(".")))
    )[-1]
    return latest_tag.name.strip("v")
  
  def generate_version(self, release_type: ReleaseType, increment_type: VersionIncrementType) -> str:
    current_version = self.get_current_version()
    pipeline_id = os.environ.get("GITHUB_RUN_ID", generate_random_string(8))
    if release_type == ReleaseType.ALPHA:
      if current_version == "0.0.0":
        current_version = "0.0.1"
      return f"{current_version}-alpha.{pipeline_id}"
    elif release_type == ReleaseType.BETA:
      if current_version == "0.0.0":
        current_version = "0.0.1"
        return f"{current_version}-beta.{pipeline_id}"
    elif release_type == ReleaseType.RELEASE:
      parsed_version = semver.Version.parse(current_version)
      if increment_type == VersionIncrementType.MAJOR:
        return parsed_version.bump_major().__str__()
      elif increment_type == VersionIncrementType.MINOR:
        return parsed_version.bump_minor().__str__()
      else:
        return parsed_version.bump_patch().__str__()
    else:
      logger.error(f"Invalid release type: {release_type}")
      raise ValueError(f"Invalid release type: {release_type}")

  def run(self) -> str:
    release_type = check_release_type(self._ref_name)
    increment_type = self.get_increment_type()
    version = self.generate_version(release_type, increment_type)
    logger.debug(f"Release type: {release_type}")
    logger.debug(f"Generated Version: {version}")
    print(f"Writing result to file: {self._output_file}")
    print(f"Version: {version}")
    self.write_to_file(version)
    return version
