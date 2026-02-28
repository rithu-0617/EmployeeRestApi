"""
Quick manual test script – exercises every API endpoint.
Run while the server is up: python test_api_manual.py
"""
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:5000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def req(method, path, body=None, token=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if token:
        r.add_header("Authorization", f"Bearer {token}")
    try:
        resp = urllib.request.urlopen(r)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def pp(label, status, data):
    print(f"\n{'='*50}")
    print(f"  {label}  [HTTP {status}]")
    print(f"{'='*50}")
    print(json.dumps(data, indent=2))


# ── 1. Health ────────────────────────────────────
status, data = req("GET", "/health")
pp("1. GET /health", status, data)

# ── 2. Register ──────────────────────────────────
status, data = req("POST", "/auth/register", {
    "username": "demo_admin",
    "password": "Demo@123"
})
pp("2. POST /auth/register", status, data)

# ── 3. Login ─────────────────────────────────────
status, data = req("POST", "/auth/login", {
    "username": "demo_admin",
    "password": "Demo@123"
})
pp("3. POST /auth/login", status, data)
TOKEN = data.get("access_token", "")

# ── 4. Create Student ────────────────────────────
status, data = req("POST", "/students", {
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@university.com",
    "course": "Computer Science"
}, token=TOKEN)
pp("4. POST /students (create)", status, data)
STUDENT_ID = data.get("student", {}).get("id", "")

# ── 5. Create Another Student ────────────────────
status, data = req("POST", "/students", {
    "first_name": "Bob",
    "last_name": "Jones",
    "email": "bob@university.com",
    "course": "Mathematics"
}, token=TOKEN)
pp("5. POST /students (create #2)", status, data)

# ── 6. List All Students ─────────────────────────
status, data = req("GET", "/students", token=TOKEN)
pp("6. GET /students (list all)", status, data)

# ── 7. Get Single Student ────────────────────────
status, data = req("GET", f"/students/{STUDENT_ID}", token=TOKEN)
pp("7. GET /students/<id> (single)", status, data)

# ── 8. Update Student ────────────────────────────
status, data = req("PUT", f"/students/{STUDENT_ID}", {
    "course": "Data Science",
    "last_name": "Smith-Updated"
}, token=TOKEN)
pp("8. PUT /students/<id> (update)", status, data)

# ── 9. Delete Student ────────────────────────────
status, data = req("DELETE", f"/students/{STUDENT_ID}", token=TOKEN)
pp("9. DELETE /students/<id>", status, data)

# ── 10. Verify Deletion ──────────────────────────
status, data = req("GET", f"/students/{STUDENT_ID}", token=TOKEN)
pp("10. GET deleted student (expect 404)", status, data)

# ── 11. Access without token (expect 401) ────────
status, data = req("GET", "/students")
pp("11. GET /students without token (expect 401)", status, data)

print(f"\n{'='*50}")
print("  ✅ All API endpoints tested!")
print(f"{'='*50}\n")
