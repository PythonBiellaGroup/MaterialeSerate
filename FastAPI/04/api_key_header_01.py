from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uvicorn

API_TOKEN = "PythonBiellaGroup"

app = FastAPI(title="Sicurezza")
api_key_header = APIKeyHeader(name="Token")


@app.get("/protected-route")
async def protected_route(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"hello": "world"}


"""
Main
"""
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload
