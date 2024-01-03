import requests
import json

def get_top_starred_projects():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "stars:>10000",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": 1
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Replace with your own TOKEN"
    }
    projects = []
    while len(projects) < 1000:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                project_name = item["full_name"]
                project_url = item["html_url"]
                project_has_discussions = item["has_discussions"]
                projects.append({"name": project_name, "url": project_url, "has_discussions": project_has_discussions})
            if "next" in response.links:
                params["page"] += 1
            else:
                break
        else:
            print("Failed to retrieve top projects.")
            break
    return projects

def save_to_json(projects):
    filename = "top_1k_projects.json"
    with open(filename, mode='w') as file:
        json.dump(projects, file)
    print(f"Projects saved to {filename}.")

top_projects = get_top_starred_projects()
save_to_json(top_projects)
