
from assertpy import assert_that
from build_version.lib.custom_semver import ProcessSemVer
from build_version.lib.interfaces import ReleaseType, VersionIncrementType
from tests.helpers.helper_test import validate_version_regex, mock_repo
import os
import pytest


@pytest.fixture(autouse=True)
def base_env(monkeypatch):
  monkeypatch.setenv("GITHUB_ACTIONS", "true")
  monkeypatch.setenv("GITHUB_RUN_ID", "123")
  

def test_generate_version_alpha(monkeypatch, mock_repo):
  mock_repo.active_branch.name = "feature/test"
  process_semver = ProcessSemVer(output_file="build.env", token="")
  monkeypatch.setattr(process_semver, "get_current_version", lambda: "1.0.0")
  version = process_semver.generate_version(ReleaseType.ALPHA, VersionIncrementType.PATCH)
  expected = f"1.0.0-alpha.{os.environ['GITHUB_RUN_ID']}"
  assert_that(version).is_equal_to(expected)
  validate_version_regex(version)