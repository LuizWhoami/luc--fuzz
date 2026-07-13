#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Directory Fuzzer - Ferramenta de Descoberta de Diretórios
Uso educacional e testes de autorização autorizados.

AVISO DE SEGURANÇA:
Esta ferramenta deve ser utilizada APENAS em sistemas onde você possui
autorização explícita para realizar testes. O uso não autorizado é
ilegal e antiético. O autor não se responsabiliza por uso indevido.

Como funciona a assincronia:
- O asyncio permite que múltiplas requisições sejam "disparadas" sem bloquear
  a execução do programa enquanto espera respostas.
- Enquanto uma requisição aguarda resposta, outras são iniciadas, aproveitando
  ao máximo o tempo de latência da rede.
- O aiohttp gerencia conexões HTTP de forma assíncrona, permitindo centenas
  de requisições simultâneas com baixo overhead de recursos.
- O Semaphore controla o número máximo de requisições concorrentes, evitando
  sobrecarga do sistema e do servidor alvo.
"""


import asyncio
import aiohttp
import argparse
import sys
from urllib.parse import urlparse


class DirectoryFuzzer:
    def __init__(self, target_url, wordlist_path, max_concurrent, hide_status, timeout):
        self.target_url = target_url
        self.wordlist_path = wordlist_path
        self.max_concurrent = max_concurrent
        self.hide_status = hide_status
        self.timeout = timeout
        self.found_dirs = []
        
    async def fuzz(self, session, path, semaphore):
        """
        Função assíncrona que realiza uma requisição para um caminho específico.
        
        Args:
            session: Sessão aiohttp
            path: Caminho a ser testado
            semaphore: Semáforo para controle de concorrência
            
        Returns:
            bool: True se o caminho foi encontrado, False caso contrário
        """
        # Usa o semáforo para limitar requisições simultâneas
        async with semaphore:
            # Substitui a palavra FUZZ pela palavra atual
            url = self.target_url.replace('FUZZ', path)
            
            try:
                # Realiza a requisição GET com timeout configurado
                async with session.get(url, timeout=self.timeout) as response:
                    status_code = response.status
                    
                    # Verifica se deve mostrar ou esconder o resultado
                    if status_code not in self.hide_status:
                        # Obtém tamanho da resposta (útil para identificar falsos positivos)
                        content_length = len(await response.text())
                        
                        # Exibe informações relevantes
                        print(f"[{status_code}] {url} (Tamanho: {content_length} bytes)")
                        self.found_dirs.append((url, status_code, content_length))
                        return True
                    
            except asyncio.TimeoutError:
                # Timeout da requisição - silencioso para não poluir output
                pass
                
            except aiohttp.ClientError as e:
                # Erros de conexão - silencioso para evitar ruído
                pass
                
            except Exception as e:
                # Outros erros inesperados - apenas registra em debug
                # print(f"Erro inesperado em {path}: {e}")
                pass
                
            return False
    
    async def run(self):
        """
        Função principal que gerencia o processo de fuzzing.
        """
        # Lê a wordlist
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8') as f:
                # Remove linhas vazias e espaços em branco
                paths = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Erro: Wordlist '{self.wordlist_path}' não encontrada.")
            return
        except Exception as e:
            print(f"Erro ao ler wordlist: {e}")
            return
        
        print(f"\n[INFO] Iniciando fuzzing em: {self.target_url}")
        print(f"[INFO] Wordlist: {len(paths)} palavras carregadas")
        print(f"[INFO] Concorrência máxima: {self.max_concurrent}")
        print(f"[INFO] Ocultando status: {self.hide_status}")
        print(f"[INFO] Timeout por requisição: {self.timeout} segundos")
        print("-" * 60)
        
        # Configura o connector com limites de conexão
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,  # Limite total de conexões
            limit_per_host=self.max_concurrent,  # Limite por host
            ttl_dns_cache=300  # Cache de DNS para performance
        )
        
        # Configura timeout da sessão (global)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        # Cria o semáforo para controlar concorrência real
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        # Cria a sessão aiohttp com configurações otimizadas
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Directory-Fuzzer/1.0 (Educational)'
            }
        ) as session:
            
            # Cria tarefas assíncronas para cada caminho
            tasks = [
                self.fuzz(session, path, semaphore) 
                for path in paths
            ]
            
            # Executa todas as tarefas concorrentemente
            # gather permite executar múltiplas coroutines em paralelo
            await asyncio.gather(*tasks)
        
        # Exibe resumo final
        print("-" * 60)
        print(f"\n[RESUMO] Diretórios/arquivos encontrados: {len(self.found_dirs)}")
        if self.found_dirs:
            print("\nDetalhes:")
            for url, status, size in self.found_dirs[:10]:  # Mostra apenas 10 primeiros
                print(f"  [{status}] {url} ({size} bytes)")
            if len(self.found_dirs) > 10:
                print(f"  ... e mais {len(self.found_dirs) - 10} itens")


def validate_url(url):
    """
    Valida se a URL é válida e contém a palavra 'FUZZ'.
    """
    if 'FUZZ' not in url:
        print("Erro: A URL deve conter a palavra 'FUZZ' para substituição.")
        print("Exemplo: https://exemplo.com/FUZZ")
        sys.exit(1)
    
    # Verifica se a URL é válida
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print("Erro: URL inválida. Use o formato: https://exemplo.com/FUZZ")
        sys.exit(1)
    
    return url


def main():
    """
    Função principal com parsing de argumentos.
    """
    parser = argparse.ArgumentParser(
        description='Directory Fuzzer - Ferramenta de descoberta de diretórios',
        epilog='AVISO: Use apenas em sistemas com autorização explícita.'
    )
    
    parser.add_argument(
        '-u', 
        '--url',
        required=True,
        help='URL alvo (deve conter FUZZ para substituição)'
    )
    
    parser.add_argument(
        '-w',
        '--wordlist',
        required=True,
        help='Caminho para o arquivo de wordlist'
    )
    
    parser.add_argument(
        '-t',
        '--threads',
        type=int,
        default=200,
        help='Número máximo de requisições simultâneas (padrão: 200)'
    )
    
    parser.add_argument(
        '-fc',
        '--hide-status',
        nargs='+',
        type=int,
        default=[404],
        help='Códigos de status para esconder (padrão: 404)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Timeout por requisição em segundos (padrão: 10)'
    )
    
    # Exibe aviso de segurança
    print("""
 _
| |_   _  ___ 
| | | | |/ __|
| | |_| | (__ 
|_|\__,_|\___|
""")
    print("\n" + "="*60)
    print("AVISO DE SEGURANÇA IMPORTANTE")
    print("="*60)
    print("Esta ferramenta deve ser usada APENAS em sistemas onde você")
    print("possui autorização explícita para realizar testes de segurança.")
    print("O uso não autorizado é ilegal e pode resultar em penalidades.")
    print("="*60 + "\n")
    
    # Processa os argumentos
    args = parser.parse_args()
    
    # Valida e ajusta argumentos
    target_url = validate_url(args.url)
    
    # Verifica se o número de threads é válido
    if args.threads < 1:
        print("Erro: Número de threads deve ser maior que 0.")
        sys.exit(1)
    
    # Verifica se a wordlist existe
    try:
        with open(args.wordlist, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Erro: Wordlist '{args.wordlist}' não encontrada.")
        sys.exit(1)
    
    # Cria e executa o fuzzer
    fuzzer = DirectoryFuzzer(
        target_url=target_url,
        wordlist_path=args.wordlist,
        max_concurrent=args.threads,
        hide_status=args.hide_status,
        timeout=args.timeout
    )
    
    # Executa o loop assíncrono
    try:
        asyncio.run(fuzzer.run())
    except KeyboardInterrupt:
        print("\n\n[!] Operação interrompida pelo usuário.")
        print(f"[RESUMO] Diretórios encontrados até o momento: {len(fuzzer.found_dirs)}")
        sys.exit(0)


if __name__ == '__main__':
    main()
