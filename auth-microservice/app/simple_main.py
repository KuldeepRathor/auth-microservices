from fastapi import FastAPI

app = FastAPI(title="Auth Microservice", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Auth Microservice is running!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "auth-microservice"}
