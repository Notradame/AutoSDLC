Steps to run: 
1. have python installed in your computer
2. open command promt
3. run "python -m pip install pip install requests pandas bandit"
4. Now, open the compliance_check.py and update line no 63 to a repo of your choice, it is currently set to "https://api.github.com/repos/Notradame/AutoSDLC/contents/"
5. Update it to the repo of your choice, the new repo_url should look like "https://api.github.com/repos/<username_of_the_github_user>/<target_repo_name>/contents/"
6. Now, the compliance_report.csv will be generated. and then import it in a power bi project. 
