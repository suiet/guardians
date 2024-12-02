import subprocess
import os

# Configure repository URL and local path
repo_url = 'https://github.com/suiet/guardians.git'
local_path = './guardians'  # Path to clone to locally
save_path = os.getcwd()
n = 10  # Compare the last n versions

# Clone the repository
if os.path.exists(local_path):
    print(f"Directory {local_path} already exists, proceed directly.")
else:
    print(f"Directory {local_path} does not exist, start cloning.")
    subprocess.run(['git', 'clone', repo_url, local_path], check=True)

# Enter the local repository path
os.chdir(local_path)

# Update to the latest version
subprocess.run(['git', 'pull'], check=True)

# Find the last n versions
commits = subprocess.run(['git', 'log', '--format=%H', '-n', str(n)], capture_output=True, text=True).stdout.splitlines()
commits.reverse()

new_add = []
new_remove = []

for i in range(len(commits) - 1):
    base_commit = commits[i]
    head_commit = commits[i + 1]

    # Get the differences
    diff_output = subprocess.run(['git', 'diff', f'{base_commit}..{head_commit}', '--', 'dist/domain-list.json'], capture_output=True, text=True).stdout
    # Extract new additions and deletions
    for line in diff_output.splitlines():
        if line.startswith('+++') or line.startswith('---'):
            continue
        if line.startswith('+'):
            new_add.append(line[1:])
        elif line.startswith('-'):
            new_remove.append(line[1:])

os.chdir(save_path)
# Write to files
with open('./new_add.txt', 'w') as f:
    f.writelines('\n'.join(new_add))

with open('./new_remove.txt', 'w') as f:
    f.writelines('\n'.join(new_remove))

print("Operation completed, new additions have been saved to new_add.txt, and deletions have been saved to new_remove.txt")
