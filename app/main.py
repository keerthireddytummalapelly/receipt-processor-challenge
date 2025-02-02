from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.routes import router

app = FastAPI(title="Receipt Processor")

# Default route
@app.get("/")
def home():
    return {"message": "A simple receipt processor"}

# Exception Handler to change validation error status code from 422 to 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(status_code=400, detail="The receipt is invalid.") 


app.include_router(router)