import requests

def get_headers(github_token: str) -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def get_repository_commits(repository_name: str, commit_sha: str, ref_name: str, headers: dict):
    url = f"https://api.github.com/repos/{repository_name}/commits/{commit_sha}"
    commit_response = requests.get(url, headers=headers)