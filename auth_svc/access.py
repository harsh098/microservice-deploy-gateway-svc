import os, requests
from flask import Request


def login(request: Request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuthcreds = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuthcreds
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)



