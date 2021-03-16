from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import os.path
from api import database, xmltojson


app = FastAPI()


if not os.path.exists("db.sqlite"):
    print("No database detected - initialising")
    database.create_db()
else:
    pass


global config
config = {
    "jackett_url": database.get_config("jackett_url"),
    "jackett_apikey": database.get_config("jackett_apikey")
}


@app.get("/{indexer}/search")
async def get_users(indexer: str, category:int, q:str):
    params = {
        "apikey": config["jackett_apikey"],
        "q": q,
        "cat": category,
        "t": "search"
    }
    results = requests.request("get", (config["jackett_url"] + f"/api/v2.0/indexers/{indexer}/results/torznab/api"), params=params)
    return JSONResponse(xmltojson.parse_results(results.content))


@app.get("/{indexer}/categories")
async def get_categories(indexer: str):
    params = {
        "apikey": config["jackett_apikey"],
        "t": "caps"
    }
    categories = requests.request("get", (config["jackett_url"] + f"/api/v2.0/indexers/{indexer}/results/torznab/api"), params=params)
    return JSONResponse(xmltojson.parse_categories(categories.content))