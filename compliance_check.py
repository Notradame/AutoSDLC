import os
import pandas as pd
import requests
from bandit.core import manager, config

def download_files(repo_url, local_dir):
    response = requests.get(repo_url)
    files = response.json()
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    for file in files:
        download_url = file['download_url']
        file_name = os.path.join(local_dir, file['name'])
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
    print(f"Issues saved to {output_file}")

def main():

    repo_url = "https://api.github.com/repos/Notradame/AutoSDLC/contents/"
    directory = "temp"
    
    download_files(repo_url, directory)
    issues = scan_directory(directory)
    for issue in issues:
        print(issue)
    if issues:
        save_compliance_report(issues, "compliance_report.csv")
    else:
        print("No issues found.")

if __name__ == "__main__":
    main()
