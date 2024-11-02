import requests
import csv

GITHUB_TOKEN = "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"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_users_in_singapore(min_followers=100, location="Singapore"):
    users=[]
    page=1
    while True:
        url = f"https://api.github.com/search/users?q=location:{location}+followers:>{min_followers}&per_page=100&page={page}"
        response=requests.get(url, headers=headers)
        if response.status_code==200:
            items=response.json().get("items", [])
            if not items: 
                break
            users.extend(items)
            page += 1
        else:
            print(f"Failed {response.status_code}")
            break
    return users


def get_user_details(username):
    url=f"https://api.github.com/users/{username}"
    response=requests.get(url, headers=headers)
    if response.status_code==200:
        return response.json()
    return {}


def clean_company_name(company):
    if company:
        company=company.strip().lstrip('@').upper()
    return company


def get_user_repos(username):
    repos=[]
    page=1
    while True:
        url=f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response=requests.get(url, headers=headers)
        if response.status_code==200:
            items = response.json()
            if not items:  
                break
            repos.extend(items)
            page += 1
        else:
            print(f"Failed to fetch repositories for {username}: {response.status_code}")
            break
    return repos


with open("users.csv", "w", newline="") as users_file:
    user_writer=csv.writer(users_file)
    user_writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])

    users=get_users_in_singapore()
    for user in users:
        details=get_user_details(user["login"])
        user_writer.writerow([
            details.get("login"),
            details.get("name", ""),
            clean_company_name(details.get("company", "")),
            details.get("location", ""),
            details.get("email", ""),
            details.get("hireable", ""),
            details.get("bio", ""),
            details.get("public_repos", ""),
            details.get("followers", ""),
            details.get("following", ""),
            details.get("created_at", "")
        ])

with open("repositories.csv", "w", newline="") as repos_file:
    repo_writer=csv.writer(repos_file)
    repo_writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"])

    for user in users:
        repos=get_user_repos(user["login"])
        for repo in repos:
            repo_writer.writerow([
                user["login"],
                repo.get("full_name"),
                repo.get("created_at"),
                repo.get("stargazers_count", ""),
                repo.get("watchers_count", ""),
                repo.get("language", ""),
                repo.get("has_projects", False),
                repo.get("has_wiki", False),
                repo.get("license", {}).get("key", "") if repo.get("license") else ""
            ])
