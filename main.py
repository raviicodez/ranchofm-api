from fastapi import FastAPI, Request

app = FastAPI(title="RanchoFM API")


@app.get("/")
async def root():
    return {"status": "RanchoFM API online"}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    print("\n========== WEBHOOK ==========")
    print(body)
    print("=============================\n")

    return {"success": True}
