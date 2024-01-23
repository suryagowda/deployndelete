# main_script.py
from github import Github
import os
import requests
from config import GITHUB_USERNAME, GITHUB_PASSWORD

def deploy_to_github(username, password, repository_name, local_folder_path):
    try:
        g = Github(username, password)
        user = g.get_user()

        repo = next((r for r in user.get_repos() if r.name == repository_name), None)

        if repo is None:
            repo = user.create_repo(repository_name)
            print(f"Repository '{repository_name}' created on GitHub.")

        os.chdir(local_folder_path)

        if not os.path.exists(".git"):
            os.system("git init")

        os.system("git add .")
        os.system("git commit -m 'Initial commit'")
        os.system("git branch -M main")
        os.system(f"git remote add origin https://github.com/{username}/{repository_name}.git")
        os.system("git pull origin main")
        os.system("git push -u --force origin main")

        print("Local folder successfully pushed to GitHub on the 'main' branch.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_github_repo(username, token, repository_name):
    try:
        url = f"https://api.github.com/repos/{username}/{repository_name}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Repository '{repository_name}' deleted successfully.")
        elif response.status_code == 404:
            print(f"Repository '{repository_name}' not found.")
        else:
            print(f"Failed to delete repository. Status code: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        print("Options:")
        print("1. Deploy local folder to GitHub")
        print("2. Delete an existing repository")

        option = input("Enter the option number: ")

        if option == "1":
            repo_name = input("Enter the repository name: ")
            local_folder = input("Enter the local folder path: ")
            deploy_to_github(GITHUB_USERNAME, GITHUB_PASSWORD, repo_name, local_folder)

        elif option == "2":
            repo_name_to_delete = input("Enter the name of the repository to delete: ")
            delete_github_repo(GITHUB_USERNAME, GITHUB_PASSWORD, repo_name_to_delete)

        else:
            print("Invalid option.")
    except Exception as e:
        print(f"An error occurred: {e}")
