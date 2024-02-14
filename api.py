import uvicorn
from fastapi import FastAPI
from api_auth import auth

app = FastAPI()
app.include_router(auth.auth_router)

@app.get("/")
async def root():
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run(app='api:app')