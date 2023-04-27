import requests


def request_png(request: str) -> bytes:
    response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{request}')
    return response.content


def request_svg(request: str) -> bytes:
    response = requests.get(f'https://www.plantuml.com/plantuml/svg/~h{request}')
    return response.content
