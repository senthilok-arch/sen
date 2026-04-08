from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

scores = []

class Score(BaseModel):
    score: int

@app.post("/score")
def save_score(s: Score):
    scores.append(s.score)
    return {"message": "Score saved"}

@app.get("/leaderboard")
def leaderboard():
    return {"top_scores": sorted(scores, reverse=True)[:5]}
