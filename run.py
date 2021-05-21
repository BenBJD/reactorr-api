import uvicorn
import api

if __name__ == "__main__":
    uvicorn.run("api:app", port=5010)
