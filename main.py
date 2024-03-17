import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.users import router as users_router
from apps.openai import router as openai_router
from apps.ChatGLM import router as chatglm_router

app = FastAPI()
app.include_router(users_router)
app.include_router(openai_router)
app.include_router(chatglm_router)

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv(), verbose=True)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def get_env():
    app.state.api_key = os.getenv("API_KEY")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=12003)
