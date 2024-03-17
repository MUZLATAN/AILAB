
import json
import os
import time
import jwt

def generate_token(api_key:str, exp_seconds:int):
    try:
        id, secret = api_key.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key":id,
        "exp":int(round(time.time() * 1000)) + exp_seconds*1000,
        "timestamp": int(round(time.time()*1000)),
    }

    jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg":"HS256", "sign_type":"SIGN"},
    )
