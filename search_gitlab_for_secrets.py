# Import the required libraries
import os
import re
import gitlab

# Set the GitLab API access token
GITLAB_TOKEN = "YOUR_TOKEN_HERE"

# Set the GitLab server URL
GITLAB_URL = "https://gitlab.com"

# Set the regular expression pattern for the secret search
SECRET_PATTERN = r"(?i)(password|secret|key|token)"

# Set the repository name and branch name for the secret search
REPOSITORY_NAME = "YOUR_REPO_NAME_HERE"
BRANCH_NAME = "YOUR_BRANCH_NAME_HERE"

# Authenticate to the GitLab API using the access token
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

# Get the repository by its name
repository = gl.projects.get(REPOSITORY_NAME)

# Get the branch by its name
branch = repository.branches.get(BRANCH_NAME)

# Get the commit that the branch points to
commit = repository.commits.get(branch.commit['id'])

# Get the tree that the commit points to
tree = repository.repository_tree(commit.tree['id'])

# Iterate over the tree entries
for entry in tree:
  # Check if the entry is a file
  if entry['type'] == "blob":
    # Get the file content
    content = repository.files.get(entry['id'], file_path=entry['path'])

    # Check if the file content matches the secret pattern
    if re.search(SECRET_PATTERN, content.decoded, re.IGNORECASE):
      # Print the secret file path and content
      print("Secret found in file: " + entry['path'])
      print("Secret content: " + content.decoded)
