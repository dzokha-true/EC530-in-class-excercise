from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

users = []          # [{id, username}]
notes = []          # [{id, user_id, text}]
next_user_id = 1
next_note_id = 1


def find_user_by_id(user_id: int):
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def username_exists(username: str):
    return any(u["username"] == username for u in users)

@app.post("/users", status_code=201)
async def create_user(req: Request):
    global next_user_id

    body = await req.json()
    username = (body.get("username") or "").strip()

    if not username:
        raise HTTPException(status_code=400, detail="username is required")

    if username_exists(username):
        raise HTTPException(status_code=409, detail="username already exists")

    user = {"id": next_user_id, "username": username}
    next_user_id += 1
    users.append(user)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.get("/users")
def list_users():
    return users

@app.post("/users/{user_id}/notes", status_code=201)
async def add_note(user_id: int, req: Request):
    global next_note_id

    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    body = await req.json()
    text = (body.get("text") or "").strip()

    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note = {"id": next_note_id, "user_id": user_id, "text": text}
    next_note_id += 1
    notes.append(note)
    return note


@app.get("/users/{user_id}/notes")
def read_notes(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return [n for n in notes if n["user_id"] == user_id]
