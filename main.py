import requests
#1 verifica se o site está online
#2 verifica se o site está offline
#3 fazer enumeração de diretórios e arquivos
wordlist = 'wordlist.txt'
url = input("Digite seu Site: ")
url = "http://" + url if not url.startswith("https://") else url

def verifica_site():
    request = requests.get(url)
    if request.status_code == 200:
        print(f"Status:{request.status_code} --> {url}")
    elif request.status_code == 404 or request.status_code == 443:
        print(f"Status:{request.status_code} --> {url}")
    else:
        print(f"Status:{request.status_code} --> {url}")
verifica_site()

print("+" * 50)
print("Do you want to perform directory enumeration? (yes/no)")
respose = input('Response: ').lower()

if respose == 'yes' or respose == 'y':
    print("+" * 50)
    print("Initializing Directory Enumeration...")
    print("+" * 50)

def enum_dir(url, wordlist):
    with open(wordlist, 'r') as file:
        for line in file:
            line = line.strip()
            full_url = f"{url}/{line}"
            response = requests.get(full_url)
            if response.status_code == 200:
                print(f"Found: {full_url} (Status: {response.status_code})")
            elif response.status_code == 403:
                print(f"Forbidden: {full_url} (Status: {response.status_code})")
            elif response.status_code == 404:
                print(f"Not Found: {full_url} (Status: {response.status_code})")
            else:
                print(f"Status: {response.status_code} --> {full_url}")
enum_dir(url, wordlist)