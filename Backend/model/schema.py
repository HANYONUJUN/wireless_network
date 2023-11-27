from pydantic import BaseModel
from datetime import datetime

class Logs(BaseModel):
    seq: int
    administrator: str
    phone: str
    logtime: datetime
    logpath: str
    smsflag: bool