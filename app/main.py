from fastapi import FastAPI
from app.agent.agent import run_sql_agent

app = FastAPI()

@app.get("/query")
def query(q: str):
    return run_sql_agent(q)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
