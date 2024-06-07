import os
import re
import json
import pickle
import sqlite3
from cryptography.fernet import Fernet

# Hardcoded key (High Severity)
SECRET_KEY = b'mysecretkey1234567890abcdef'

# Weak encryption algorithm (High Severity)
def encrypt_data(data):
    cipher = Fernet(SECRET_KEY)
    return cipher.encrypt(data.encode())

def decrypt_data(token):
    cipher = Fernet(SECRET_KEY)
    return cipher.decrypt(token).decode()

# SQL Injection Vulnerability (High Severity)
def get_user_info(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Direct use of user input in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# Deserialization of untrusted data (High Severity)
def load_user_preferences(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)

# Command injection vulnerability (High Severity)
def run_os_command(command):
    return os.system(command)

# Insufficient logging (Medium Severity)
def log_event(event):
    with open('events.log', 'a') as log_file:
        log_file.write(event + '\n')

# Missing input sanitization (Medium Severity)
def process_user_input(user_input):
    # Accepts input without sanitization
    if re.match(r'^[a-zA-Z0-9_]+$', user_input):
        return f"Processing input: {user_input}"
    else:
        return "Invalid input!"

# Hardcoded configuration file (Low Severity)
def load_config():
    # Loading configuration from a hardcoded path
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    user_command = "ls -l"
    user_file = "preferences.pkl"
    user_input = "admin"

    print(f"Running OS command: {user_command}")
    run_os_command(user_command)  # Command Injection

    print(f"Loading user preferences from {user_file}")
    preferences = load_user_preferences(user_file)  # Untrusted Deserialization

    print(f"Getting info for user: {user_input}")
    user_info = get_user_info(user_input)  # SQL Injection
    print(user_info)

    encrypted_data = encrypt_data("Sensitive data")
    print(f"Encrypted data: {encrypted_data}")
    decrypted_data = decrypt_data(encrypted_data)
    print(f"Decrypted data: {decrypted_data}")

    print(process_user_input(user_input))  # Missing input sanitization

    log_event("Script executed")  # Insufficient logging

    config = load_config()  # Hardcoded configuration path
    print(f"Loaded configuration: {config}")
