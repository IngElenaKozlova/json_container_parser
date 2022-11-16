import os

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.container_parser import pars_container
from models.db_models import Container, base

DATABASE_NAME = 'application.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)


def create_db():
    base.metadata.create_all(engine)


def read_json(path_to_file: json) -> dict:
    with open(path_to_file, 'r') as f:
        containers_data_dict = json.load(f)
    return containers_data_dict



if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()
    session = Session()
    all_containers = read_json(os.path.join('json_template', 'sample_data.json'))
    for container in all_containers:
        data_for_sql = pars_container(container)
        d = Container(name=data_for_sql.name, cpu=data_for_sql.cpu, memory=data_for_sql.memory,
                      create_at=data_for_sql.create_at, status=data_for_sql.status,
                      ip_addresses=', '.join(data_for_sql.ip_addresses) if data_for_sql.ip_addresses else None)
        session.add(d)
        session.commit()

