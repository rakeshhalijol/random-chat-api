from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://rakeshhalijol:Rakesh123@cluster0.inydvtx.mongodb.net/test")

# Database created
db = client["RANDOM-CHAT"]

# User table created here
User = db["User"]
Followers = db["Followers"]
Following = db["Following"]


def create_user(signupData: dict):
    response = User.insert_one(dict(signupData))
    followers_list = {
        "userId": response.inserted_id, "friends": []
    }
    following_list = {
        "userId": response.inserted_id, "friends": []
    }
    Followers.insert_one(followers_list)
    Following.insert_one(following_list)
    return str(response.inserted_id)


def fetch_user(loginData: dict):
    user = User.find_one({"name": loginData.get(
        "name"), "password": loginData.get("password")})
    return user


def fetch_user_on_username(name: str):
    user = User.find_one({"name": name})
    return user


def update_online(email: str, isActive: bool):
    user = User.update_one({"email": email}, {"$set": {"isActive": isActive}})
    return user.modified_count


def get_all_user(username: str):
    users = User.find({"name": {"$ne": username}}, {})
    return users


def add_following(userid, friend_name):
    friend = Following.update_one(
        {"userId": userid}, {"$push": {"friends": friend_name}})
    return friend.modified_count


def add_followers(userid, friend_name):
    friend = Followers.update_one(
        {"userId": userid}, {"$push": {"friends": friend_name}})
    return friend.modified_count
