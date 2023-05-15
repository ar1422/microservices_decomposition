import git
from pathlib import Path

directories_to_ignore = [".git", ".idea"]


def clone_repository(public_repository, local_path):
    """
    Function to clone the repository.
    :param public_repository: URL for the public repository which needs to be cloned.
    :param local_path: local path to make the copy of the project.
    :return: Cloned Repo object.
    """

    return git.Repo.clone_from(public_repository, local_path)


def get_all_file_names(local_path):
    """
    Function to get all the python files from the given local path of the project.
    :param local_path: Local path of the project
    :return: List of all the *.py files in the project.
    """
    all_files = []
    for filename in Path(local_path).glob('**/*.py'):
        all_files.append(filename.absolute())

    return all_files


def get_contributors_map(local_path, files):
    """
    Function to get the contributors information for the given file(s).
    :param local_path: Local path of the project.
    :param files: a String representing the filename or list of strings representing the filename.
    :return: Dictionary with key and filename(s) and values as the set of contributors for the file.
    """
    repository = git.Repo(local_path)
    contributors_map = {}
    if not isinstance(files, (list, tuple, set)):
        files = [files]

    for filename in files:
        blame_command_output = repository.git.blame('--', filename).split('\n')
        contributors = set()
        for bl in blame_command_output:
            contributor = bl.split('(')[1].split()[0]
            contributors.add(contributor)
        contributors_map[filename] = contributors
    return contributors_map


def get_commits(local_path):
    unique_files = set()

    # Open the repository
    repo = git.Repo(local_path)
    commits = []
    commit_history = list(repo.iter_commits())
    for commit in commit_history[:-1]:
        files = repo.git.diff(
            "--name-only", f"{commit.hexsha}^", commit.hexsha
        ).splitlines()
        commits.append({"commit": commit.hexsha, "changes": files})
        for file in files:
            unique_files.add(file)

    return commits


if __name__ == '__main__':
    get_contributors_map("", [""])
