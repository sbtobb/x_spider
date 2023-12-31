from fastapi import FastAPI
import uvicorn
from application.routers import auth, tweets

app = FastAPI()

app.include_router(auth.router)
app.include_router(tweets.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
