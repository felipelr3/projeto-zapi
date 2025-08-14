import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List
from schemas.contato import Contato

load_dotenv()

def conectar_supabase(url: str, key: str) -> Client:
    try:
        client = create_client(supabase_url = url, 
                               supabase_key = key)
        
        logging.info("A conexão com supabase foi sucedida.")
        
        return client
    
    except Exception as e:
        logging.error(f"Ocorreu um erro ao conectar no Supabase: {e}")
        raise ValueError(e) from e


def buscar_contatos(supabase: Client, 
                    tabela: str, 
                    nome: str, 
                    numero: str) -> List[Contato]:
    try:
        response = supabase.table(tabela).select(f"{nome},{numero}").limit(3).execute().data
                
        contatos: List[Contato] = [
            {"nome": data.get(nome), "numero": data.get(numero)}
            for data in response
            if data.get(numero)
        ]
        
        if contatos:
            logging.info(f"{len(contatos)} contatos encontrados")
        else:
            logging.warning("O telefone não foi encontrado no banco de dados")
        return contatos
    except Exception as error:
        logging.error(f"Erro ao buscar contatos: {error}")
        return []

# Utilização da Z API
def enviar_mensagem(instancia: str, api_token: str, client_token: str, numero: str, nome: str) -> bool:
    url = f"https://api.z-api.io/instances/{instancia}/token/{api_token}/send-text"
    payload = {"phone": str(numero), "message": f"Olá {nome}, tudo bem com você?"}
    headers = {
        "Client-Token": client_token,
        "Content-Type": "application/json"
    }

    if not client_token:
        logging.error("Client-Token não encontrado. Ative e copie no painel de segurança, e coloque=o no arquivo .env")
        return False

    for tentativa in range(1, 3):  # tenta 2 vezes
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            logging.info(f"O que a Z-API recebeu: {resp.status_code}: {resp.text[:160]}")

            if resp.status_code == 200:
                logging.info(f"Mensagem enviada para {nome} ({numero})")
                return True

            if resp.status_code == 403 and "null not allowed" in resp.text.lower():
                logging.error("A Z-API exigiu o Client-Token no header e não recebeu.")
                break

            if resp.status_code == 403 and "not allowed" in resp.text.lower():
                logging.error("Client-Token inválido para esta conta/instância. Verifique seu client_token no painel de segurança")
                break

            if resp.status_code in (404, 405):
                logging.error("Endpoint com falha. Use POST em vez de GET")
                break

        except requests.RequestException as errorro:
            logging.warning(f"Tentativa {tentativa} com erro de rede: {e}")

    return False


# Main
def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    config = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "TABELA": os.getenv("SUPABASE_TABLE", "contatos"),
        "nome": os.getenv("SUPABASE_NAME_FIELD", "name"),
        "numero": os.getenv("SUPABASE_NUMBER_FIELD", "number"),
        "ZAPI_INSTANCE": os.getenv("ZAPI_INSTANCE"),
        "ZAPI_TOKEN": os.getenv("ZAPI_TOKEN"),
        "ZAPI_CLIENT_TOKEN": os.getenv("ZAPI_CLIENT_TOKEN"),
    }

    try:
        supabase_client = conectar_supabase(config["SUPABASE_URL"], config["SUPABASE_KEY"])
    
        contatos = buscar_contatos(
        supabase_client,
        config["TABELA"],
        config["nome"],
        config["numero"],
    )
        qtd_enviados = sum(
            enviar_mensagem(
            config["ZAPI_INSTANCE"], 
            config["ZAPI_TOKEN"],
            config["ZAPI_CLIENT_TOKEN"],
            contato["numero"], 
            contato["nome"],
            ) for contato in contatos
        )
        logging.info(f"{qtd_enviados} Mensagens enviadas com sucesso.")

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()
