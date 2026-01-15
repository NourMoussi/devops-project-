import requests
import uuid

URL = "http://localhost:5000/health"

print("--- 1. Test génération automatique ID ---")
r = requests.get(URL)
req_id = r.headers.get("X-Request-ID")
print(f"Status: {r.status_code}")
print(f"X-Request-ID: {req_id}")

if not req_id:
    raise Exception("Header X-Request-ID manquant !")

print("\n--- 2. Test propagation ID existant ---")
custom_id = str(uuid.uuid4())
headers = {"X-Request-ID": custom_id}
r = requests.get(URL, headers=headers)
returned_id = r.headers.get("X-Request-ID")
print(f"Sent ID: {custom_id}")
print(f"Received ID: {returned_id}")

if custom_id != returned_id:
    raise Exception("L'ID envoyé n'a pas été propagé !")

print("\n✅ TRACING SUCCESS")
