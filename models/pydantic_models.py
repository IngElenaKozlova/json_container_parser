import datetime

from pydantic import BaseModel


class ParsingInformationPydantic(BaseModel):
    name: str
    cpu: None | int
    memory: None | int
    create_at: datetime.datetime
    status: str
    ip_addresses: None | list
