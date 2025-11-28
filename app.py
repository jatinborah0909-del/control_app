from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")
SERVICE_ID    = os.getenv("SERVICE_ID")
ADMIN_KEY     = os.getenv("ADMIN_KEY")   # secret key for dashboard

GRAPHQL_URL = "https://backboard.railway.app/graphql"

def railway_call(query, variables):
    return requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={
            "Authorization": f"Bearer {RAILWAY_TOKEN}",
            "Content-Type": "application/json"
        }
    ).json()

def get_status():
    query = """
    query Status($serviceId: String!) {
      service(id: $serviceId) {
        deployments {
          status
        }
      }
    }
    """
    resp = railway_call(query, {"serviceId": SERVICE_ID})
    
    try:
        status = resp["data"]["service"]["deployments"][0]["status"]
    except:
        status = "unknown"
        
    return status


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, key: str):
    if key != ADMIN_KEY:
        return "Unauthorized"

    status = get_status()
    css_class = "running" if status == "SUCCESS" else "stopped"

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "status": status,
        "status_class": css_class,
        "key": key
    })


@app.get("/start")
def start_service(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation ServiceStart($serviceId: String!) {
      serviceStart(id: $serviceId)
    }
    """

    return railway_call(query, {"serviceId": SERVICE_ID})


@app.get("/stop")
def stop_service(key: str):
    if key != ADMIN_KEY:
        return {"error": "unauthorized"}

    query = """
    mutation ServiceStop($serviceId: String!) {
      serviceStop(id: $serviceId)
    }
    """

    return railway_call(query, {"serviceId": SERVICE_ID})
