import requests

def verifyToken(token) :
    result = requests.post("http://127.0.0.1:5001/verify",json={"token":token})
    if(result.status_code != 401) :
        return True
    else :
        return False
    