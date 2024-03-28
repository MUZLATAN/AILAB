import asyncio
from collections import defaultdict
from typing import Dict, List
from fastapi import APIRouter
from fastapi import Query, WebSocket, Body
from starlette.websockets import WebSocketDisconnect
from zhipuai.types.chat.chat_completion_chunk import ChoiceDelta
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json
from zhipuai import ZhipuAI
import os

router = APIRouter()
# 获取'API_KEY'的环境变量
glm_key = os.getenv("API_KEY")

@router.websocket("/chat_websocket")
async def websocket_chat(websocket: WebSocket):
    client = ZhipuAI(api_key=glm_key)  # 请填写您自己的APIKey
    try:
        await websocket.accept()
        message = list()
        while True:
            # await 将这个函数变成一个task， 然后event loop 会执行websocket.receive_text()
            # websocket.receive_text()执行完成之后，await显式地将程序控制权还给event loop
            data = await websocket.receive_text()
            if data == "quit":
                await websocket.close()
                break

            response =client.chat.completions.create(
                model="glm-3-turbo",  # 填写需要调用的模型名称
                messages=[
                    {"role": "user", "content": data},
                ],
                stream=True)
            
            await websocket.send_text("[BEG]")
            for line in response:
                res_str = line.choices[0].delta
                if isinstance(res_str, ChoiceDelta):
                    content = res_str.content
                    print(content)
                    await websocket.send_text(content)
            await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
        return


class RequestProps(BaseModel):
    prompt: str
    options: dict = {}
    systemMessage: str = ""
    temperature: float = 0.7
    top_p: float = 0.9

@router.post("/chat-process")
async def process_chat(props: RequestProps):
    async def generate_stream(props:RequestProps):
        first_chunk = True
        local_dict = await chat_reply_process(**props.dict())
        for chat_message in local_dict:
            if first_chunk:
                yield bytes(json.dumps("hahah \n"), "utf-8")
                first_chunk = False
            else:
                yield bytes("\n" + json.dumps("hahah lue lue lue \n"), "utf-8")

    return StreamingResponse(generate_stream(props), media_type="application/octet-stream")

# 这个例子中没有异常处理，你可以根据实际情况添加
@router.get("/translate")
async def translate(inp: str = Query(...), lang: str = Query("en")):
    """翻译"""
    url = "https://api.openai.com/v1/completions"
    data = {
        "stream": False,
        "prompt": "translate '" + inp + "' to " + lang,
        "temperature": 0.9,
        "max_tokens": 3000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "model": "text-davinci-002"
    }
    
    return (await request(url, data)).get("choices")[0]


res_arr=[
    "[BEG]",
    "您好！看来您可能是想输入数字“111”。",
"这个数字",
"在",
"不同的",
"上下",
"文中",
"可能有",
"不同的",
"含义",
"。",
"如果您",
"有",
"其他",
"问题",
"或",
"需要",
"帮助",
"，",
"请",
"随时",
"告诉我",
"[DONE]"
]



@router.websocket("/chat_websocket1")
async def chat_websocket(websocket: WebSocket):
    try:
        await websocket.accept()
        message = list()
        while True:
            # await 将这个函数变成一个task， 然后event loop 会执行websocket.receive_text()
            # websocket.receive_text()执行完成之后，await显示的将程序控制权还给event loop
            data = await websocket.receive_text()
            print(data)

            if data == "quit":
                await websocket.close()
                break

            for line in res_arr:
                print(line)
                await websocket.send_text(line)


    except WebSocketDisconnect:
        return
