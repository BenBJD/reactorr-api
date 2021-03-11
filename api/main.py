from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from api import database, xmltojson


app = FastAPI()


global config
config = {
    "jackett_url": database.read_config("jackett_url"),
    "jackett_apikey": database.read_config("jackett_apikey")
}


@app.get("/search/{indexer}")
async def read_users(indexer: str, category:int, q:str):
    params = {
        "apikey": config["jackett_apikey"],
        "q": q
    }
    results = requests.request("get", (config["jackett_url"] + f"/api/v2.0/indexers/{indexer}/results/torznab/api"), params=params)
    return JSONResponse(xmltojson.parse(results.content))