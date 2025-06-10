import requests

BASE_URL = "http://127.0.0.1:8000"

print("\nCreating students:")
r1 = requests.post(f"{BASE_URL}/students/", json={"name": "Laura", "age": 21})
r2 = requests.post(f"{BASE_URL}/students/", json={"name": "Joan", "age": 24})
print(r1.json())
print(r2.json())

print("\nListing all students:")
students = requests.get(f"{BASE_URL}/students/").json()
print(students)

print("\nGetting student 1:")
print(requests.get(f"{BASE_URL}/students/1").json())

print("\nUpdating student 1:")
u = requests.put(f"{BASE_URL}/students/1", json={"name": "Laura Updated", "age": 22})
print(u.json())

print("\nDeleting student 2:")
print(requests.delete(f"{BASE_URL}/students/2").json())