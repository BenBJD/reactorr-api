from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import os.path
from api import database, xmltojson


if not os.path.exists("db.sqlite"):
    print("No database detected - Running setup.py")
    database.create_db()
    database.set_config("jackett_url", input("Enter Jackett URL: "))
    database.set_config("jackett_apikey", input("Enter Jackett API key: "))
    print("Done!")
else:
    pass

app = FastAPI()


global config
config = {
    "jackett_url": database.get_config("jackett_url"),
    "jackett_apikey": database.get_config("jackett_apikey")
}

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def get_users(indexer: str, category: int, q: str):
    params = {
        "apikey": config["jackett_apikey"],
        "q": q,
        "cat": category,
        "t": "search"
    }
    database.add_recent(q)
    results = requests.request(
        "get", (config["jackett_url"] + f"/api/v2.0/indexers/{indexer}/results/torznab/api"), params=params)
    return JSONResponse(xmltojson.parse_results(results.content))


@app.get("/indexers")
async def get_indexers():
    params = {
        "apikey": config["jackett_apikey"],
        "t": "indexers",
        "configured": "true"
    }
    indexers = requests.request(
        "get", config["jackett_url"] + f"/api/v2.0/indexers/all/results/torznab/api", params=params)
    return JSONResponse(xmltojson.parse_indexers(indexers.content))


@app.get("/recents")
async def get_recents(number: int):
    recents = database.get_recents(number)
    return recents


@app.post("/recents")
async def remove_recents(id: int, all: bool):
    database.remove_recent(id, all)
    return "success"


@app.get("/config")
async def get_config(key: str):
    config = database.get_config(key)
    print(config)
    return config


@app.post("/config")
async def set_config(key: str, value: str):
    database.set_config(key, value)
    return "success"
