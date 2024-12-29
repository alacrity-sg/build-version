from pydantic import BaseModel, Field
from git import Repo
from enum import Enum
import re
from os import environ



class ProcessBase(BaseModel):
    _repo: Repo = Field(frozen=True, min_length=1)
    _output_file: str = Field(frozen=True, min_length=1)
    _private_token: str = Field(frozen=True, min_length=1)
    _ref_name: str = Field(frozen=True, default=environ.get('GITHUB_REF'))

    def __init__(self, **data):
        super().__init__()
        if not data.get('repo') and not data.get('output_file'):
            raise ValueError("repo and output_file must not be empty.")

        self._repo = Repo(path=data.get('repo'))
        self._output_file = data.get('output_file')
        self._private_token = data.get('private_token')

    def write_to_file(self, version: str):
        with open(self._output_file, 'w') as f:
            if self._output_file.split('.')[-1] == "env":
                f.write(f"BUILD_VERSION={version}\n")

    def run(self) -> str:
        pass