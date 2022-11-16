from sqlalchemy import DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


base = declarative_base()


class Container(base):

    __tablename__ = 'container'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpu = Column(Integer)
    memory = Column(Integer)
    create_at = DateTime()
    status = Column(String)
    ip_addresses = Column(Text)


    def __repr__(self):
        info: str = f'Container [Name: {self.name}, CPU: {self.cpu}, Memory: {self.memory}, ' \
                    f'Create_at: {self.create_at}, Status: {self.status}, IP_addresses: {self.ip_addresses}]'
        return info
