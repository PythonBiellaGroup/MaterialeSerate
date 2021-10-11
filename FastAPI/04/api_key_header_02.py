from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uvicorn

API_TOKEN = "PythonBiellaGroup"

app = FastAPI(title="Sicurezza")


async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.get("/protected-route", dependencies=[Depends(api_token)])
async def protected_route():
    return {"hello": "world"}


"""
Main
"""
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload

