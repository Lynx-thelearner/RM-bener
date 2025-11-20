from fastapi import FastAPI
from app.api.v1.meja import meja_router
from app.api.v1.feedback import feedback_router
from app.api.v1.reservation import reservation_router
from app.api.v1.user import user_router
from app.api.v1.payment import payment_router
from app.api.v1.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI

class UUIDJsonResponse(JSONResponse):
    def render(self, content):
        return super().render(jsonable_encoder(content))

app = FastAPI(
    title="NER API Service",
    version="1.0.0",
    description="A FastAPI service for New Entry Reservation (NER)" 
    )
#Cors middleware protection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],

)


"""ROOT ENDPOINT"""
@app.get("/")
async def read_root():
    return {"message": "Welcome to the NER API Service!"}

app.include_router(auth_router.router)

app.include_router(meja_router.router)
app.include_router(user_router.router)
app.include_router(reservation_router.router)
app.include_router(payment_router.router)
app.include_router(feedback_router.router)