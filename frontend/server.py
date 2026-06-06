"""
React-based Web UI for Prompt-to-Prod
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Prompt-to-Prod UI")

# Serve static files
@app.get("/")
async def read_root():
    """Serve index.html"""
    return FileResponse("public/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
