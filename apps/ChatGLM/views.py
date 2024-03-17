import asyncio
from collections import defaultdict
from typing import Dict, List

from fastapi import APIRouter
from fastapi import Query, WebSocket, Body
from starlette.websockets import WebSocketDisconnect
from zhipuai.types.chat.chat_completion_chunk import ChoiceDelta

from .utils import generate_token

from zhipuai import ZhipuAI

router = APIRouter(prefix="/chatglm")

@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    client = ZhipuAI(api_key="8d102f5e48b2c04fccc669b8d90be27e.XBMIbE8LHh6hA7lU")  # 请填写您自己的APIKey
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
            response =client.chat.completions.create(
                        model="glm-3-turbo",  # 填写需要调用的模型名称
                        messages=[
                            {"role": "user", "content": data},
                        ],
                        stream=True,
                    )
            # result = dict()
            for line in response:
                res_str = line.choices[0].delta
                if isinstance(res_str, ChoiceDelta):
                    content = res_str.content
                    print(content)
                    await websocket.send_text(content)

    except WebSocketDisconnect:
        return



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
