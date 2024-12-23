from assertpy import assert_that
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_repo():
  with patch("build_version.lib.custom_semver.Repo") as MockRepo:
    mock_repo_instance = MagicMock()
    mock_repo_instance.active_branch.name = "main"
    with patch("git.Repo", return_value=mock_repo_instance):
      yield mock_repo_instance
      yield MockRepo
      

def validate_version_regex(version: str):
  assert_that(version).matches(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
  )
  

def validate_file_content(content: str, version: str):
  assert_that(content).is_not_empty()
  assert_that(content).is_equal_to(f"BUILD_VERSION={version}\n")