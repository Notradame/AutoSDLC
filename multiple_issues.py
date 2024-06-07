import hashlib
import os
import subprocess
import sys

# Hardcoded credentials (High Severity)
USERNAME = "admin"
PASSWORD = "password123"

def weak_hash(password):
    # Use of weak cryptographic hash function (MD5) (High Severity)
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def insecure_run(command):
    # Use of insecure subprocess call (High Severity)
    return subprocess.call(command, shell=True)

def get_config():
    # Hardcoded sensitive information in code (High Severity)
    return {"db_user": "root", "db_pass": "toor"}

def open_file(filename):
    # Missing input validation (Medium Severity)
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None

def authenticate(user, password):
    # Hardcoded secret comparison (High Severity)
    if user == USERNAME and password == PASSWORD:
        return "Authenticated"
    else:
        return "Authentication Failed"

def run_server():
    # Use of exec to run server command (High Severity)
    server_cmd = "python -m http.server 8080"
    exec(server_cmd)

def save_user_info(user, password):
    # Saving sensitive info without encryption (High Severity)
    with open('user_info.txt', 'w') as file:
        file.write(f"User: {user}, Password: {password}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <command> <filename>")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    print(f"Weak hash of 'password': {weak_hash('password')}")
    print(f"Running command: {command}")
    insecure_run(command)

    print(f"Opening file: {filename}")
    content = open_file(filename)
    if content:
        print(content)

    print(authenticate("admin", "password123"))
    run_server()
    save_user_info("admin", "password123")
