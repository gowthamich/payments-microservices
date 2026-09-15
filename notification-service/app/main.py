from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")

class Notification(BaseModel):
    user_id: int
    message: str

@app.get("/health")
def health():
    return {"status": "UP", "service": "notification-service"}

@app.post("/notifications")
def send_notification(notification: Notification):
    print(f"Notification sent to user {notification.user_id}: {notification.message}")
    return {
        "status": "SENT",
        "user_id": notification.user_id,
        "message": notification.message,
    }
