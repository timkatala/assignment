import uvicorn
from fastapi import FastAPI

from src.api.message_router import message_router
from src.api.user_router import user_router

# Define FastAPI app
app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(message_router, prefix="/messages", tags=["messages"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
