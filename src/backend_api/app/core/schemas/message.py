from pydantic import BaseModel


# Generic message
# Used for sending message responses to the client
class Message(BaseModel):
    message: str
