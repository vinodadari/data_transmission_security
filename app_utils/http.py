import requests
from requests import Response
from app_utils.config import ClientConfig, ServerConfig, client_config, server_config

from pydantic import BaseModel
from typing_extensions import Union


class TokenResponse(BaseModel):
    token_type: str
    access_token: str


class Http:
    token: Union[str, None] = None
    username: str
    password: str

    def __init__(self):
        self.client_config: ClientConfig = client_config()
        self.server_uri = client_config.vault_url

        self.server_config: ServerConfig = server_config()

    def login(self):
        login_request = requests.post(
            f"{self.server_uri}/token",
            data={"username": self.username, "password": self.password},
        )
        token_response = TokenResponse(**login_request.json())
        self.token = token_response.access_token
        return self.token

    def get(self, url, **kwargs) -> Union[Response, None]:
        if not self.token:
            self.login()
        try:
            client_request = requests.get(
                url, headers={"Authorization": f"Bearer {self.token}"}, **kwargs
            )
            if client_request and client_request.status_code == 200:
                return client_request
            else:
                raise Exception("Failed to get request")

        except Exception as e:
            print(e)

    def post(self, url, data=None, json=None, **kwargs) -> Union[Response, None]:
        self.login()
        try:
            return requests.post(
                url,
                data=data,
                json=json,
                headers={"Authorization": f"Bearer {self.token}"},
                **kwargs,
            )
        except Exception as e:
            print(e)

    def put(self, url, data=None, **kwargs) -> Union[Response, None]:
        self.login()
        try:
            return requests.put(
                url,
                data=data,
                headers={"Authorization": f"Bearer {self.token}"},
                **kwargs,
            )
        except Exception as e:
            print(e)


class ClientHttp(Http):
    def __init__(self):
        super().__init__()
        self.user_id = self.client_config.user_id
        self.client_gateway_id = self.client_config.gateway_id
        self.server_gateway_id = self.server_config.gateway_id

        self.username = self.client_config.vault_username
        self.password = self.client_config.vault_password

    def get_client_info(self):
        url = f"{self.client_config.vault_url}/users/me"
        users_me_request = self.get(url)
        if users_me_request and users_me_request.status_code == 200:
            return users_me_request.json()
        else:
            raise Exception("Failed to get client info")

    def get_client_private_key(self):
        url = f"{self.client_config.vault_url}/gateways/get_gateway/{self.client_gateway_id}"
        private_secret_request = self.get(url)
        if private_secret_request and private_secret_request.status_code == 200:
            return private_secret_request.json()["private_key"]
        else:
            raise Exception("Failed to get client private secret")

    def get_server_public_key(self):
        url = f"{self.client_config.vault_url}/gateways/get_gateway/{self.server_gateway_id}"
        private_secret_request = self.get(url)
        if private_secret_request and private_secret_request.status_code == 200:
            return private_secret_request.json()["public_key"]
        else:
            raise Exception("Failed to get server public secret")


class ServerHttp(Http):
    def __init__(self):
        super().__init__()
        self.user_id = self.server_config.user_id
        self.client_gateway_id = self.client_config.gateway_id
        self.server_gateway_id = self.server_config.gateway_id

        self.username = self.server_config.vault_username
        self.password = self.server_config.vault_password

    def get_server_info(self):
        url = f"{self.client_config.vault_url}/users/me"
        users_me_request = self.get(url)
        if users_me_request and users_me_request.status_code == 200:
            return users_me_request.json()
        else:
            raise Exception("Failed to get client info")

    def get_client_public_key(self):
        url = f"{self.client_config.vault_url}/gateways/get_gateway/{self.client_gateway_id}"
        private_secret_request = self.get(url)
        if private_secret_request and private_secret_request.status_code == 200:
            return private_secret_request.json()["public_key"]
        else:
            raise Exception("Failed to get client private secret")

    def get_server_private_key(self):
        url = f"{self.client_config.vault_url}/gateways/get_gateway/{self.server_gateway_id}"
        private_secret_request = self.get(url)
        if private_secret_request and private_secret_request.status_code == 200:
            return private_secret_request.json()["private_key"]
        else:
            raise Exception("Failed to get server public secret")
