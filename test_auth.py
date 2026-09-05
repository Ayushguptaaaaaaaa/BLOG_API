import requests

# Base URL
BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login to get token
print("Step 1: Getting token...")
login_response = requests.post(
    f"{BASE_URL}/login",
    data={"username": "admin", "password": "password"}
)
print(f"Login Status: {login_response.status_code}")
print(f"Login Response: {login_response.json()}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"\nToken: {token}\n")

    # Step 2: Create a blog with the token
    print("Step 2: Creating blog with token...")
    headers = {"Authorization": f"Bearer {token}"}
    blog_data = {
        "title": "Test Blog",
        "content": "This is a test blog post"
    }

    create_response = requests.post(
        f"{BASE_URL}/blogs",
        json=blog_data,
        headers=headers
    )
    print(f"Create Blog Status: {create_response.status_code}")
    print(f"Create Blog Response: {create_response.json()}")
else:
    print("Login failed!")
