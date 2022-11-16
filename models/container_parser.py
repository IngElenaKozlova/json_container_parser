import datetime

from models.pydantic_models import ParsingInformationPydantic


def get_container_name(container: dict) -> str:
    name = container.get('name')
    return name


def get_container_memory_and_cpu_usage(container: dict) -> tuple:
    state = container.get('state')
    if state is None:
        return None, None
    else:
        memory_usage = state['memory']['usage']
        cpu_usage = state['cpu']['usage']
    return memory_usage, cpu_usage


def get_container_create_at(container: dict):
    create_at = container.get('created_at')
    return datetime.datetime.strptime(create_at, '%Y-%m-%dT%H:%M:%S%z')


def get_container_status(container: dict) -> str:
    status = container.get('status')
    return status


def process_network_item(network: dict) -> list:
    network_item_ip = []
    addresses = network['addresses']
    for address in addresses:
        network_item_ip.append(address['address'])
    return network_item_ip


def get_container_ip_addresses(container: dict) -> None | list:
    container_ip = []
    state = container.get('state')
    if state is None:
        return None
    else:
        network = container['state']['network']
        for network_value in network.values():
            network_ip = process_network_item(network_value)
            container_ip.extend(network_ip)
    return container_ip


def pars_container(container: dict) -> ParsingInformationPydantic:
    name = get_container_name(container)
    cpu, memory = get_container_memory_and_cpu_usage(container)
    create_at = get_container_create_at(container)
    status = get_container_status(container)
    ip_addresses = get_container_ip_addresses(container)

    container_pydantic = ParsingInformationPydantic(name=name, cpu=cpu, memory=memory,
                                                    create_at=create_at, status=status, ip_addresses=ip_addresses)
    return container_pydantic