async def login(username: str, password: str):
    return {"message": "User logged in"}

async def logout():
    return {"message": "User logged out"}

async def user_create(username: str, email: str, password: str):
    return {"message": "User created"}
