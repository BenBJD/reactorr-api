# reactorr-api
Backend API for Reactorr based on FastAPI. To be run on the same machine as the front-end and served by the same NGinx instance

## Features
- Interacts with Jackett's Torznab API
- Translates XML to more friendly JSON with only relevent information
- Manages a database of recent searches and settings
- Autogenerated docs available

## To-Do
- Finish it
- Make a meta repo to setup an instance in a Docker contrainer for the frontend, backend and an instance of NGinx
- Get it on Docker Hub
- Testing
- Better security (CORS, SQL injection etc.)
- Maybe switch to an ORM such as SQLalchemy
