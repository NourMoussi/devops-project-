import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_api():
    print("--- 1. GET /tasks (Initial) ---")
    r = requests.get(f"{BASE_URL}/tasks")
    print(f"Status: {r.status_code}")
    print(f"Count: {len(r.json())}")
    
    print("\n--- 2. POST /tasks ---")
    payload = {
        "title": "Tâche API Test",
        "description": "Créée via script python",
        "status": "TODO"
    }
    r = requests.post(f"{BASE_URL}/tasks", json=payload)
    print(f"Status: {r.status_code}")
    if r.status_code == 201:
        new_task = r.json()
        print(f"Created ID: {new_task['id']}")
        task_id = new_task['id']
    else:
        print(f"Error: {r.text}")
        sys.exit(1)

    print(f"\n--- 3. GET /tasks/{task_id} ---")
    r = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {r.status_code}")
    print(f"Title: {r.json()['title']}")

    print(f"\n--- 4. PUT /tasks/{task_id} ---")
    update_payload = {"status": "IN_PROGRESS", "title": "Tâche API Updated"}
    r = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_payload)
    print(f"Status: {r.status_code}")
    print(f"New Status: {r.json()['status']}")

    print(f"\n--- 5. DELETE /tasks/{task_id} ---")
    r = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {r.status_code}")

    print("\n--- 6. GET /tasks/{task_id} (Verify Delete) ---")
    r = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {r.status_code} (Expected 404)")

if __name__ == "__main__":
    try:
        test_api()
        print("\n✅ GLOBAL TEST SUCCESS")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
