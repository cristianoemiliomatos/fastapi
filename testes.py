import requests

headrs = {
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzkwMTY4NjY1fQ.4GK2VbBbNiI2D-OvkXuLGMC-CD7vrdOrFA1duVwKszM"
}
requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headrs)
print(requisicao)
print(requisicao.json())