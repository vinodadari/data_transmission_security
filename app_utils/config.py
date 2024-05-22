from yaml import safe_load
from pathlib import Path
from pydantic import BaseModel
from typing import Union


config_path = Path(__file__).absolute().parent.parent.joinpath("config.yaml").as_posix()


class ClientConfig(BaseModel):
    user_id: Union[int, None] = None
    gateway_id: Union[int, None] = None
    vault_url: str = "http://localhost:8000"
    vault_username: str = "admin"
    vault_password: str = "password"
    target_host: str = "localhost"
    target_port: int = 8001


class ServerConfig(BaseModel):
    user_id: Union[int, None] = None
    gateway_id: Union[int, None] = None
    vault_url: str = "http://localhost:8000"
    vault_username: str = "admin"
    vault_password: str = "password"
    bind_host: str = "localhost"
    bind_port: int = 8001


def client_config() -> ClientConfig:
    with open(config_path, "r") as file:
        return ClientConfig(**safe_load(file)["client"])


def server_config() -> ServerConfig:
    with open(config_path, "r") as file:
        return ServerConfig(**safe_load(file)["server"])


class VaultConfig:
    def __init__(self, config):
        self.config = config

    def get_server_public_key(self):
        return self.config["server_public_key"]

    def get_client_private_key(self):
        return self.config["client_private_key"]
