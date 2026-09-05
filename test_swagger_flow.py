import requests

BASE_URL = "http://127.0.0.1:8000"

# Test 1: Call login
print("=== Test 1: Login ===")
login_response = requests.post(f"{BASE_URL}/login")
print(f"Status: {login_response.status_code}")
print(f"Response: {login_response.json()}")
token = login_response.json()["access_token"]
print(f"Token: {token[:50]}...")

# Test 2: Try to create blog WITHOUT token
print("\n=== Test 2: Create blog WITHOUT token ===")
blog_data = {"title": "Test", "content": "Content"}
response = requests.post(f"{BASE_URL}/blogs", json=blog_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 3: Try to create blog WITH token
print("\n=== Test 3: Create blog WITH token ===")
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/blogs", json=blog_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 4: Check what token Swagger UI might be sending
print("\n=== Test 4: Try with just token (no Bearer prefix) ===")
headers_no_bearer = {"Authorization": token}
response = requests.post(f"{BASE_URL}/blogs", json=blog_data, headers=headers_no_bearer)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
