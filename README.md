# Luc Fuzz

O **Luc Fuzz** é uma ferramenta de descoberta de diretórios rápida, assíncrona e eficiente, desenvolvida em Python. Projetado para auxiliar em testes de segurança e reconhecimento, o Luc Fuzz permite identificar arquivos e pastas ocultos em servidores web através de *brute-force* baseado em uma wordlist.

## ⚠️ Aviso de Segurança
> **IMPORTANTE:** Esta ferramenta foi criada para fins puramente **educacionais e testes de penetração autorizados**. O uso desta ferramenta contra sistemas sem permissão expressa do proprietário é **ilegal e antiético**. O autor não assume responsabilidade por qualquer uso indevido ou danos causados pelo software.

---

## 🚀 Funcionalidades
*   **Alta Performance:** Utiliza `asyncio` e `aiohttp` para realizar centenas de requisições simultâneas de forma assíncrona.
*   **Controle de Concorrência:** Implementação de `Semaphore` para evitar sobrecarga no servidor alvo e na sua rede.
*   **Filtragem de Respostas:** Permite definir quais códigos de status HTTP ignorar (ex: ocultar `404 Not Found`).
*   **Timeout Personalizável:** Evita que requisições travadas consumam recursos desnecessários.
*   **Leve e Eficiente:** Baixo consumo de recursos, ideal para rodar em ambientes de teste.

---

## 📋 Pré-requisitos
Certifique-se de ter o Python 3.7+ instalado. Você precisará instalar as dependências necessárias:

```bash
pip install aiohttp

🛠 Como usar

O uso é simples. Você deve fornecer a URL alvo contendo a palavra-chave FUZZ (onde as palavras da wordlist serão injetadas) e o caminho para a sua wordlist.
Sintaxe básica:
Bash

python3 fuzzer.py -u [http://exemplo.com/FUZZ](http://exemplo.com/FUZZ) -w wordlist.txt

Opções disponíveis:
Flag	Descrição	Padrão
-u, --url	URL alvo (deve conter a string FUZZ)	Obrigatório
-w, --wordlist	Caminho para o arquivo da wordlist	Obrigatório
-t, --threads	Número de requisições simultâneas	200
-fc, --hide-status	Códigos HTTP para ocultar	404
--timeout	Tempo limite por requisição (segundos)	10
Exemplo avançado:

Para realizar o fuzzing com 100 threads, ignorando status 404 e 403:
Bash

python3 fuzzer.py -u [http://exemplo.com/FUZZ](http://exemplo.com/FUZZ) -w lista.txt -t 100 -fc 404 403

🧠 Como funciona a assincronia

O Luc Fuzz utiliza o ecossistema asyncio do Python:

    Non-blocking I/O: Enquanto aguarda a resposta de uma requisição, o programa inicia outras, maximizando a largura de banda.

    Semaphore: Controla o fluxo, garantindo que o limite de threads especificado pelo usuário não seja ultrapassado.

    DNS Cache: Configurado para otimizar o tempo de consulta em grandes wordlists.

🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request ou abrir uma Issue para sugerir melhorias ou reportar bugs.
📝 Licença

Este projeto é de código aberto. Sinta-se livre para estudar e modificar o código.


Links darkweb:
- Verified Hacking Links List
http://njxlpsukc52svveeehbortqep52c4toh3ayi5bwae4aaw2bs46d4g7ad.onion/  
- The Island
http://53gsgrg4h4pllwmndk3zska3be6vffp5lqoxf46tmnu7z7pll3affyid.onion  
- Qilin Group
http://ijzn3sicrcy7guixkzjkib4ukbiilwc3xhnmby4mcbccnsd7j2rekvqd.onion/?page=1  
- Ahmia Search Engine
http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/  
- DeepSearch
http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/ 
- ShadowX 
http://shadowxn3o3kvvkbjyaoe33emqxrtadijp7xybizbht2thb6x5dvfhad.onion/
- Everest Ransomware Group
http://ransomocmou6mnbquqz44ewosbkjk3o5qjsl3orawojexfook2j7esad.onion/news
- Ragnar Locker
http://rgleaktxuey67yrgspmhvtnrqtgogur35lwdrup4d3igtbm3pupc4lyd.onion/
- O LockBit 5.0 (Next-Gen) opera em modelo RaaS (Ransomware-as-a-Service).
http://lockbitapt67g6rwzjbcxnww5efpg4qok6vpfeth7wx3okj52ks4wtad.onion/




