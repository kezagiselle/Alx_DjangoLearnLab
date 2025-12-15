import requests
import time
import sys

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api():
    print("Waiting for server to start...")
    time.sleep(5)
    
    # 1. Register
    print("Testing Registration...")
    reg_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "bio": "I am a test user"
    }
    try:
        response = requests.post(f"{BASE_URL}/register/", data=reg_data)
        if response.status_code == 201:
            print("Registration Successful!")
            print(response.json())
        else:
            print(f"Registration Failed: {response.status_code}")
            print(response.text)
            # If user already exists (from previous run), try login
            if "username" in response.text and "already exists" in response.text:
                 print("User likely already exists, proceeding to login...")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Login
    print("\nTesting Login...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    token = None
    response = requests.post(f"{BASE_URL}/login/", data=login_data)
    if response.status_code == 200:
        print("Login Successful!")
        data = response.json()
        token = data.get('token')
        print(f"Token: {token}")
    else:
        print(f"Login Failed: {response.status_code}")
        print(response.text)
        return

    # 3. Profile
    if token:
        print("\nTesting Profile Access...")
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        if response.status_code == 200:
            print("Profile Access Successful!")
            print(response.json())
        else:
            print(f"Profile Access Failed: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_api()
