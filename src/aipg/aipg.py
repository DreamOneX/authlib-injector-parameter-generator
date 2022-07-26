import requests, json, base64
__all__ = ["get_tokens", "get_metadata"]

def get_tokens(api: str, username: str, password: str) -> dict:
    data = json.dumps({'username': username, 'password': password, 'requestUser': False, 'agent': {'name': 'Minecraft', 'version': 1}})
    header = {'Content-Type': 'application/json'}
    return json.loads(requests.post(f"{api}/authserver/authenticate", headers=header, data=data).text)

def get_metadata(api: str) -> str:
    return str(base64.b64encode(requests.get(api).text.encode('ascii')))
