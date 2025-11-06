from fastapi import FastAPI
from app.api.v1.meja import meja_router
from app.api.v1.feedback import feedback_router
from app.api.v1.reservation import reservation_router
from app.api.v1.user import user_router
from app.api.v1.payment import payment_router


app = FastAPI(
    title="NER API Service",
    version="1.0.0",
    description="A FastAPI service for New Entry Reservation (NER)" 
    )



"""ROOT ENDPOINT"""
@app.get("/")
async def read_root():
    return {"message": "Welcome to the NER API Service!"}



app.include_router(meja_router.router, prefix="/meja", tags=["Meja"])
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(reservation_router.router, prefix="/reservation", tags=["Reservation"])
app.include_router(payment_router.router, prefix="/payment", tags=["Payment"])
app.include_router(feedback_router.router, prefix="/feedback", tags=["Feedback"])