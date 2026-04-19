from fastapi import FastAPI
from app.agent.agent import run_sql_agent

app = FastAPI()

@app.get("/query")
def query(q: str):
    response = run_sql_agent(q)
    print("Resposta do agente:", response)
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
