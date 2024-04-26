from fastapi import Depends, FastAPI, Body, HTTPException, Header, Request, Response, Cookie, status
from fastapi.responses import JSONResponse
import jwt
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from App.output_ports.db.Connexion import SessionLocal
from App.inputs.routes import LoginRoute, RegisterRoute
from index import router as index_router



app = FastAPI(title="Vues Js Test Api", description="Testing vuejs and fastapi",docs_url="/Test/docs")

origins = [
    "http://localhost:5173",
    "http://localhost:4000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )





@app.get("/")
async def main():
    return {"welcom":"welcome to my test"}


##
app.include_router(LoginRoute.router)
app.include_router(RegisterRoute.router)
app.include_router(index_router)



# if __name__ == '__main__':
#     uvicorn.run(app, host="192.168.100.7", port=8000)