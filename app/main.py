from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
# cd fantasy-basketball-frontend
# npm start
# python -m app.main

app = FastAPI(
    title="Fantasy Basketball Wrapped API",
    description="API for retrieving ESPN Fantasy Basketball season statistics",
    version="1.0.0"
)

# for front end requests? 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)