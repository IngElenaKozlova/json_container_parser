import os

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.container_parser import pars_container
from models.db_models import Container, base

import logging

import time

CURRENT_TIME = time.strftime("%H_%M_%S", time.localtime())
LOG_FILE_NAME = f'{CURRENT_TIME}.log'
FULL_PATH_TO_LOG_FILE = os.path.join('logs', LOG_FILE_NAME)

logging.basicConfig(filename=FULL_PATH_TO_LOG_FILE,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

POSTGRES_URL = r'postgresql://root:root@localhost:5432/data_json'

engine = create_engine(POSTGRES_URL)
Session = sessionmaker(bind=engine)


def create_db():
    logger.info("Creating a database")
    base.metadata.create_all(engine)


def read_json(path_to_file: json) -> dict:
    logger.info("Start to read from json file to python format dictionary")
    with open(path_to_file, 'r') as f:
        containers_data_dict = json.load(f)
    logger.info("Reading json to python was finished successfully")
    return containers_data_dict



if __name__ == '__main__':
    db_is_created = os.path.exists("pg-data")
    if not db_is_created:
        create_db()
    session = Session()
    all_containers = read_json(os.path.join('json_template', 'sample_data.json'))
    for container in all_containers:
        data_for_sql = pars_container(container)
        if data_for_sql is None:
            logger.warning(f"Unable to parse container. More information is in logs {FULL_PATH_TO_LOG_FILE}")
            continue
        d = Container(name=data_for_sql.name, cpu=data_for_sql.cpu, memory=data_for_sql.memory,
                      create_at=data_for_sql.create_at, status=data_for_sql.status,
                      ip_addresses=', '.join(data_for_sql.ip_addresses) if data_for_sql.ip_addresses else None)
        session.add(d)
        session.commit()

