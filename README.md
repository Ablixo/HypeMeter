HypeMeter — Trailer Hype Voting (MVP)

Small FastAPI backend where users vote HYPED or NAH on trailers and view a leaderboard.
Data is in-memory (resets on restart) to keep the MVP simple.

Run (dev)
uvicorn api.app:app --reload
# Docs: http://localhost:8000/docs

Endpoints
GET
GET /health

Returns app status.

{ "status": "ok" }

GET /trailers

List all trailers.

[
  { "id": "tt-superman", "title": "Superman Movie", "platform": "Youtube" }
]

GET /leaderboard?limit=10

Top trailers sorted by score = hypedCount - nahCount.

[
  { "trailerId": "tt-superman", "title": "Superman Movie", "hypedCount": 3, "nahCount": 1, "score": 2 }
]

POST
POST /trailers

Create a trailer.
Body

{
  "id": "tt-oppenheimer",
  "title": "Oppenheimer Trailer",
  "platform": "Youtube"
}


Responses

201 Created — returns created trailer

409 Conflict — id already exists

422 Unprocessable Content — bad/missing fields

POST /vote

Cast a vote (one vote per user per trailer).
Body

{
  "trailerId": "tt-superman",
  "userId": "anon-123",
  "vote": "HYPED"
}


Success

{ "trailerId": "tt-superman", "hypedCount": 4, "nahCount": 1, "score": 3 }