from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.agent.agent import run_sql_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório de templates
templates_path = Path(__file__).parent / "templates"
app.mount("/static", StaticFiles(directory=str(templates_path)), name="static")

@app.get("/")
def home():
    return FileResponse(str(templates_path / "index.html"))

@app.get("/query")
def query(q: str):
    response = run_sql_agent(q)
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
