from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui():
    return FileResponse("index.html")

# Game state
game = {
    "players": {},
    "race_started": False,
    "winner": None
}

TRACK_LENGTH = 100

@app.post("/join/{dog_name}")
def join_game(dog_name: str):
    if game["race_started"]:
        return {"error": "Race already started"}

    game["players"][dog_name] = {
        "position": 0,
        "status": "running"
    }

    return {"message": f"{dog_name} joined the race 🐶"}

@app.post("/start")
def start_race():
    game["race_started"] = True
    return {"message": "Race started 🚕💨"}

@app.post("/move")
def move():
    if not game["race_started"]:
        return {"error": "Start the race first"}

    for dog in game["players"]:
        if game["players"][dog]["status"] == "running":
            step = random.randint(1, 10)
            game["players"][dog]["position"] += step

    # Collision logic
    positions = {}
    for dog, data in game["players"].items():
        pos = data["position"]
        if pos in positions:
            game["players"][dog]["status"] = "toppled"
            game["players"][positions[pos]]["status"] = "toppled"
        else:
            positions[pos] = dog

    # Check winner
    for dog, data in game["players"].items():
        if data["position"] >= TRACK_LENGTH:
            game["winner"] = dog
            game["race_started"] = False
            return {"winner": dog}

    return game

@app.get("/state")
def get_state():
    return game


# 🔄 RESET API (added here)
@app.post("/reset")
def reset_game():
    game["players"].clear()
    game["race_started"] = False
    game["winner"] = None
    return {"message": "Game reset 🔄"}
