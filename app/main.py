from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import time


app = FastAPI(
    title="RanchoFM API",
    version="0.1.0"
)


# -------------------------
# Health check
# -------------------------

@app.get("/")
async def root():
    return {
        "project": "RanchoFM",
        "version": "0.1.0",
        "status": "online"
    }


# -------------------------
# WEB SCROBBLER
# -------------------------

@app.post("/webhook/{username}")
async def web_scrobbler(username: str, request: Request):

    data = await request.json()

    print("\n========== WEB SCROBBLER ==========")
    print(f"USER: {username}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("===================================\n")


    event = data.get("eventName")

    if event == "scrobble":
        print("🎵 SCROBBLE RECEBIDO")

    elif event == "nowplaying":
        print("▶️ NOW PLAYING RECEBIDO")


    return {
        "status": "ok",
        "user": username,
        "event": event
    }



# -------------------------
# PANO SCROBBLER
# LAST.FM LIKE API
# -------------------------

@app.api_route(
    "/2.0/",
    methods=["GET", "POST"]
)
async def pano_scrobbler(request: Request):


    # =========================
    # GET REQUESTS
    # =========================

    if request.method == "GET":

        params = request.query_params

        method = params.get("method")
        user = params.get("user")


        print("\n========== PANO GET ==========")
        print(dict(params))
        print("==============================\n")


        # User info

        if method == "user.getInfo":

            return {
                "user": {
                    "name": user,
                    "realname": user,
                    "playcount": 0,
                    "registered": {
                        "unixtime": int(time.time())
                    }
                }
            }


        # Top tracks

        if method == "user.getTopTracks":

            return {
                "toptracks": {
                    "track": []
                }
            }


        # Top artists

        if method == "user.getTopArtists":

            return {
                "topartists": {
                    "artist": []
                }
            }


        return {
            "error": 6,
            "message": "Invalid method"
        }



    # =========================
    # POST REQUESTS
    # =========================


    form = await request.form()

    params = dict(form)


    print("\n========== PANO POST ==========")
    print(json.dumps(params, indent=2))
    print("===============================\n")


    method = params.get("method")


    # -------------------------
    # LOGIN
    # -------------------------

    if method == "auth.getMobileSession":

        username = params.get("username")


        print(
            f"PANO LOGIN: {username}"
        )


        return {
            "session": {
                "name": username,
                "key": "ranchofm-session",
                "subscriber": 0
            }
        }


    # -------------------------
    # NOW PLAYING
    # -------------------------

    if method == "track.updateNowPlaying":

        print("▶️ PANO NOW PLAYING")

        return {
            "nowplaying": {
                "ignoredMessage": {
                    "code": 0,
                    "explanation": ""
                }
            }
        }



    # -------------------------
    # SCROBBLE
    # -------------------------

    if method == "track.scrobble":

        print("🎵 PANO SCROBBLE")

        return {
            "scrobbles": {
                "@attr": {
                    "accepted": 1,
                    "ignored": 0
                },
                "scrobble": []
            }
        }


    # -------------------------
    # FALLBACK
    # -------------------------

    return {
        "error": 6,
        "message": "Unknown method"
    }