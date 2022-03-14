from pydantic import BaseModel
from rest_framework.views import APIView

# pydantic is used for data validation
class MessageQuery(BaseModel):
    subject: str
    sender: str
    recipients: list
    html: str
    cc: list
    bcc: list 
    attachments: list