from enum import Enum


class ReleaseType(Enum):
  ALPHA = "alpha"
  BETA = "beta"
  RELEASE = "release"


class VersionIncrementType(Enum):
  MAJOR = "major"
  MINOR = "minor"
  PATCH = "patch"