from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router
import os

app = FastAPI(
    title="Fantasy Basketball Wrapped API",
    description="API for retrieving ESPN Fantasy Basketball season statistics",
    version="1.0.0"
)

# Allow frontend access (adjust domain in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve React static build files (must run `npm run build` first)
app.mount("/static", StaticFiles(directory="fantasy-frontend/build/static"), name="static")

# Catch-all route to serve index.html for React SPA
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    file_path = f"fantasy-frontend/build/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("fantasy-frontend/build/index.html")

# Run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
