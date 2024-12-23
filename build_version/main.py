import argparse
import os

from build_version.lib.custom_semver import ProcessSemVer

def main():
  parser = argparse.ArgumentParser(
    description="Parse Build Version inputs"
  )
  parser.add_argument(
    "--output-file",
    help="Path to the output file",
    type=str,
    required=False,
    default="./build.env"
  )
  parser.add_argument(
    "--repo-path",
    help="Path to the repository",
    type=str,
    required=False,
    default="./"
  )
  parser.add_argument(
    "--token",
    help="Private PAT, Installation Token or GitHub Actions Token to access the repository",
    type=str,
    required=False,
    default=os.getenv("GITHUB_TOKEN", "")
  )
  
  args = parser.parse_args()
  build_version = ProcessSemVer(
    repo_path=args.repo_path,
    output_file=args.output_file,
    token=args.token
  )
  build_version.run()