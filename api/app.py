from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal


# Creates my webapp
app = FastAPI(title="HypeMeter API", version="0.0.1")

# Who voted what 

VOTED = set()
COUNTS = {}

#test data db

TRAILERS = {
    "tt-superman": {
        "id": "tt-superman",
        "title": "Superman Movie",
        "platform": "Youtube"
    },
    "tt-f1": {
        "id": "tt-f1",
        "title": "F1 Movie",
        "platform": "Youtube"
    }
}

for tid in TRAILERS.keys():
    if tid not in COUNTS:
        COUNTS[tid] = {"HYPED": 0, "NAH": 0}


# SCHEMAS (Using them to validate incoming JSON)
# Trailer request schema 
class TrailerRequest(BaseModel):
    id: str
    title: str
    platform: str = "Youtube"

# Vote request schema
class VoteRequest(BaseModel):
    trailerId: str
    userId: str
    vote: Literal["HYPED", "NAH"]

# Check if app is responding
@app.get("/")
def root():
    return {"message": "Hello from HypeMeter"}

# Monitoring and uptime check to see if server is alive
@app.get("/health") 
def health():
    return {"status": "ok"}

# when GET request hits /trailers run list_trailers()
@app.get("/trailers")
def list_trailers():
    return list(TRAILERS.values())

# Creates a new trailer
@app.post("/trailers", status_code=201)
def add_trailer(t: TrailerRequest):
    if t.id in TRAILERS:
        raise HTTPException(status_code=409, detail="Trailer ID already exists")
    
    data = t.model_dump()
    
    TRAILERS[t.id] = data
    COUNTS.setdefault(t.id, {"HYPED": 0, "NAH": 0})

    return data

# creates a new vote 
@app.post("/vote")
def cast_vote(v: VoteRequest):

    if v.trailerID not in TRAILERS:
        raise HTTPException(status_code=404, detail="Trailer not found")
    
    key = (v.trailerID, v.userID)
    if key in VOTED:
        raise HTTPException(status_code=409, detail="User already voted")
    
    VOTED.add(key)

    COUNTS[v.trailerID][v.vote] += 1

    hyped = COUNTS[v.trailerID]["HYPED"]
    nah = COUNTS[v.trailerID]["NAH"]
    score = hyped - nah

    return {
        "trailerId": v.trailerID,
        "hypedCount": hyped,
        "nahCount": nah,
        "score": score
    }


# returns a sorted list of trailers by score
@app.get("/leaderboard")
def leaderboard(limit: int = 10):
    rows = []

    for tid , trailer in TRAILERS.items():
        counts = COUNTS.get(tid, {"HYPED": 0, "NAH": 0})
        hyped = counts.get("HYPED", 0)
        nah = counts.get("NAH", 0)
        score = hyped - nah

        rows.append({
            "trailerID": tid,
            "title": trailer["title"],
            "hypedCount": hyped,
            "nahCount": nah,
            "score": score
        })

    rows.sort(key = lambda r: (r["score"], r["hypedCount"]), reverse=True)

    return rows[:limit]