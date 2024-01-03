import csv
import requests
import os

github_token = 'your_github_access_token'

csv_file_path = 'path_to_your_csv_file.csv'

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': f'token {github_token}'  
}

with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    logins = [row['login'] for row in reader]

users_info = []

for login in logins:
    url = f'https://api.github.com/users/{login}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        # 提取指定的字段
        user_info = {
            'login': user_data.get('login', ''),
            'name': user_data.get('name', ''),
            'location': user_data.get('location', ''),
            'html_url': user_data.get('html_url', ''),
            'avatar_url': user_data.get('avatar_url', '')
        }
        users_info.append(user_info)
    else:
        print(f"Unable to obtain user {login} Data, status code：{response.status_code}")

# Specify the path to output CSV files
output_csv_path = os.path.join(os.path.expanduser("~"), "Desktop", "github_users_info.csv")

with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['login', 'name', 'location', 'html_url', 'avatar_url'])
    writer.writeheader()
    writer.writerows(users_info)

print(f"All user information has been saved to: {output_csv_path}")
