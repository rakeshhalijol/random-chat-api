from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from models import SignupModel, LoginModel
from database import (
    create_user,
    fetch_user,
    update_online,
    fetch_user_on_username,
    get_all_user,
    add_followers,
    add_following
)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.post("/random-chat/signin", tags=["user credentials"])
def signin(signupData: SignupModel):
    userId = create_user(signupData)
    return {"status": "OK", "userid": userId}


@app.patch("/random-chat/login", tags=["user credentials"])
def login(loginData: LoginModel):
    user = fetch_user(dict(loginData))
    if user:
        update_status = update_online(user.get("email"), True)
        return {"status": "OK", "data": "Login Successfull"}
    else:
        return {"status": "FAIL", 'data': "Invalid credentials"}


@app.patch("/random-chat/logout", tags=["user credentials"])
def logout(name: str):
    user = fetch_user_on_username(name)
    if user:
        update_status = update_online(user.get("email"), False)
        return {"status": "OK", "data": "Logout Successfull"}
    else:
        return {"status": "FAIL", 'data': "Invalid credentials"}


@app.get("/random-chat/friends")
def get_all_users(name: str = Query(None)):
    users = get_all_user(name)
    data = []
    for user in users:
        user["_id"] = str(user["_id"])
        data.append(user)
    return {"users": data}


@app.patch("/random-chat/add-following/{user}")
def add_followingfriend(user, friend_name):
    userId = fetch_user_on_username(user).get("_id")
    count = add_following(userId, friend_name)
    return {"data": "friend added"}


@app.patch("/random-chat/add-follower/{user}")
def add_followingfriend(user, friend_name):
    userId = fetch_user_on_username(user).get("_id")
    count = add_followers(userId, friend_name)
    return {"data": "friend added"}


########################################## -- WEBSOCKETS -- ####################################################
connections = {}


@app.websocket("/ws/{username}/{reciver}")
async def mutual_chat(ws: WebSocket, username: str, reciver: str):
    print("Accepting...")
    await ws.accept()
    print("Accepted...")
    connections[username] = [ws, reciver]
    while True:
        try:
            data = await ws.receive_json()
            for name, connection in connections.items():
                if (name == username and connection[1] == reciver) or name == reciver and connection[1] == username:
                    await connection[0].send_json(data)
        except:
            del connections[username]
            break
