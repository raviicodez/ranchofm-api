from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI(
    title="RanchoFM API",
    description="Servidor de scrobbling do RanchoFM",
    version="0.1.0"
)


@app.get("/")
async def home():
    return {
        "project": "RanchoFM",
        "version": "0.1.0",
        "status": "online"
    }


@app.post("/webhook")
async def webhook(request: Request):
    """
    Endpoint utilizado pelo Web Scrobbler.
    """

    payload = await request.json()

    print("\n========== WEB SCROBBLER ==========")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("===================================\n")

    return JSONResponse({
        "success": True
    })

@app.post("/webhook/{username}")
async def webhook(username: str, request: Request):
    data = await request.json()

    print("========== WEB SCROBBLER ==========")
    print(f"USER: {username}")
    print(json.dumps(data, indent=2))
    print("===================================")

    return {
        "status": "ok",
        "user": username
    }

@app.post("/2.0/")
async def pano(request: Request):
    """
    Endpoint compatível com clientes Last.fm-like.
    Inicialmente apenas registra tudo o que receber.
    """

    form = await request.form()
    data = dict(form)

    print("\n========== PANO ==========")

    for key, value in data.items():
        print(f"{key}: {value}")

    print("===================================\n")

    method = data.get("method")

    #
    # Login
    #
    if method == "auth.getMobileSession":
        return JSONResponse({
            "session": {
                "name": data.get("username"),
                "key": "ranchofm-session",
                "subscriber": 0
            }
        })

    #
    # Todos os outros métodos
    #
    return JSONResponse({
        "status": "received",
        "method": method
    })