from fastapi import FastAPI

app = FastAPI(
    title="NER API Service",
    version="1.0.0",
    description="A FastAPI service for New Entry Reservation (NER)" 
    )

"""ROOT ENDPOINT"""
@app.get("/")
async def read_root():
    return {"message": "Welcome to the NER API Service!"}