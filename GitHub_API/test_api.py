import requests
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()


base_url = "https://api.github.com"


def create_repo(access_token, repo_name, repo_descr=None):
    url = f"{base_url}/user/repos"

    headers = {
        "Authorization": f"token {access_token}",
    }

    # create json data to send using the post request
    data = {
        "name": repo_name,
        "description": repo_descr,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        repo_data = response.json()
        return repo_data
    else:
        return None


def delete_repo(access_token, username, repo_name):
    url = f"{base_url}/repos/{username}/{repo_name}"

    headers = {
        "Authorization": f"token {access_token}",
    }
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Repository has been deleted successfully. Status code: {response.status_code}")
    elif response.status_code == 404:
        print(f"Repository not found or already deleted. Status code: {response.status_code}")
    else:
        print(f"Failed to delete repository. Status code: {response.status_code}")


def get_user_repos(username):
    url = f"{base_url}/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories_data = response.json()
        return repositories_data
    else:
        return None


access_token = os.getenv("access_token")
repo_name = os.getenv("repo_name")
username = os.getenv("user")

#Создать новый репозиторий
new_repo = create_repo(access_token, repo_name)

if new_repo:
    print(f"New public repo created successfully!")
    user_repos = get_user_repos(username)
    if user_repos:
        print(f"Repositories of {username}:")
        for repo in user_repos:
            #Проверить наличие репозитория
            if repo['name'] == repo_name:
                print('The repository has already been created')
                #Удалить репозиторий
                delete_repo(access_token, username, repo_name)
                break
            else:
                print('The repository has not yet been created')
            print(repo["name"])
    else:
        print(f"Failed to retrieve repositories.")


else:
    print("Failed to create a new repo.")
