import os
import sys
import pandas as pd
import requests
from bandit.core import manager, config

def get_file_list_recursive(url, file_list = []):
    response = requests.get(url)
    assert response.status_code == '200', response.text
    js_res = response.json()
    for item in js_res:
        if item['type'] == "file":
            print(item['download_url'])
            file_list.append(item['download_url'])
        elif item['type'] == "dir":
            file_list.extend(get_all_nested_files(item['url'])) 
        
    return file_list

def get_first_level_files(url):
    response = requests.get(url)
    assert response.status_code == '200', response.text
    files = response.json()
    file_list = [file['download_url'] for file in files if file['type'] == "file"]
    return file_list


def download_files(repo_url, local_dir):
    response = requests.get(repo_url)
    files = response.json()
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    for file in files:
        download_url = file['download_url']
        file_name = os.path.join(local_dir, file['name'])
        if not file_name.lower().endswith(".py"):
            print(f"Skipping file '{file_name}' as it is not a python file");
            continue
        print(f"Downloading to path '{file_name}'")
        file_content = requests.get(download_url).text
        with open(file_name, 'w') as f:
            f.write(file_content)


def download_(repo_url, local_dir):
    files = get_first_level_files(repo_url)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    for file in files:
        download_url = file['download_url']
        file_name = os.path.join(local_dir, file['name'])
        if not file_name.lower().endswith(".py"):
            print(f"Skipping file '{file_name}' as it is not a python file");
            continue
        print(f"Downloading to path '{file_name}'")
        file_content = requests.get(download_url).text
        with open(file_name, 'w') as f:
            f.write(file_content)

def run_bandit_on_file(b_mgr, file_path):
    """Run bandit on a single file and return issues found."""
    try:
        b_mgr.discover_files([file_path])
        b_mgr.run_tests()
        return b_mgr.results
    except Exception as e:
        print(f"Error running bandit on {file_path}: {e}")
        return []

def scan_directory(directory):
    """Scan all Python files in the directory using bandit."""
    conf = config.BanditConfig()
    b_mgr = manager.BanditManager(conf, "file")
    
    issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Scanning {file_path}...")
                results = run_bandit_on_file(b_mgr, file_path)
                issues.extend(results)
    
    return issues

def format_issue(issue):
    """Format the bandit issue into a dictionary for CSV output."""
    return {
        "File": issue.fname,
        "Line": issue.lineno,
        "Severity": issue.severity,
        "Confidence": issue.confidence,
        "Issue": issue.text,
    }

def save_compliance_report(issues, output_file):
    """Save the issues to a CSV file using pandas."""
    issues_data = [format_issue(issue) for issue in issues]
    df = pd.DataFrame(issues_data)
    df.to_csv(output_file, index=False)
    print(f"Issues saved to '{output_file}'")

def convert_github_url_to_api(url):
    if not url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub URL")
    repo_path = url[len("https://github.com/"):].split('/')
    assert len(repo_path) >= 2, "Looks like an invalid('/')"

    return f"https://api.github.com/repos/{repo_path[0]}/{repo_path[1]}/contents/"

def main(repo_url, directory="temp"):
    download_files(repo_url, directory)
    issues = scan_directory(directory)
    print("====================ISSUE_LIST====================")
    for issue in issues:
        print(f"{issue.text} '{issue.fname}'")
    print("====================XXXXXXXXXX====================")
    if issues:
        save_compliance_report(issues, "compliance_report.csv")
    else:
        print("No issues found.")

if __name__ == "__main__":
    api_url = None
    if len(sys.argv) != 2:
        print("Usage: python <file_name> <repo_url>")
    else:
        repo_url = sys.argv[1]
        try:
            api_url = convert_github_url_to_api(repo_url)
            print(api_url)
        except ValueError as e:
            print(e)
            
    main(api_url)
