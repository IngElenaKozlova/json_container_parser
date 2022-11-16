# json_container_parser

Program reads data from JSON file (list of lxc containers from testing server)
then parses them into pydantic BaseModel. 
I parse only these data for each container: 
name, cpu a memory usage, created_at (converted to UTC timestamp), status, all asigned IP addresses.
Finally program stores these certain data to SQLite using SQLAlchemy.