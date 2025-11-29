from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Environment variables (must be set in Railway)
RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")
SERVICE_ID    = os.getenv("SERVICE_ID")      # example: service_xxxxxxx
ADMIN_KEY     = os.getenv("ADMIN_KEY")       # example: tinku123

GRAPHQL_URL = "https://backboard.railway.app/graphql/v2"


@app.get("/")
def root():
    return {
        "usage": {
            "start_service": "/start?key=YOUR_ADMIN_KEY",
            "stop_service": "/stop?key=YOUR_ADMIN_KEY"
        }
    }


@app.get("/start")
def start_service(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation($id: String!) {
      serviceStart(id: $id)
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"id": SERVICE_ID}},
        headers={"Authorization": f"Bearer {RAILWAY_TOKEN}"}
    )

    return {"action": "start", "response": response.text}


@app.get("/stop")
def stop_service(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation($id: String!) {
      serviceStop(id: $id)
    }
    """

    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"id": SERVICE_ID}},
        headers={"Authorization": f"Bearer {RAILWAY_TOKEN}"}
    )

    return {"action": "stop", "response": response.text}
