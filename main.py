from fastapi import FastAPI
import requests
import os

app = FastAPI()

RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")
SERVICE_ID    = os.getenv("SERVICE_ID")
ENV_ID        = os.getenv("ENVIRONMENT_ID")
ADMIN_KEY     = os.getenv("ADMIN_KEY")

GRAPHQL_URL = "https://backboard.railway.app/graphql/v2"

def call_railway(query, variables):
    r = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {RAILWAY_TOKEN}"}
    )
    print("RAW:", r.text)
    return r.text


@app.get("/start")
def start(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation($serviceId: String!, $environmentId: String!) {
      deploymentCreate(
        input: {
          serviceId: $serviceId,
          environmentId: $environmentId,
          action: START
        }
      ) {
        id
      }
    }
    """

    return call_railway(query, {
        "serviceId": SERVICE_ID,
        "environmentId": ENV_ID
    })


@app.get("/stop")
def stop(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation($serviceId: String!, $environmentId: String!) {
      deploymentCreate(
        input: {
          serviceId: $serviceId,
          environmentId: $environmentId,
          action: STOP
        }
      ) {
        id
      }
    }
    """

    return call_railway(query, {
        "serviceId": SERVICE_ID,
        "environmentId": ENV_ID
    })
