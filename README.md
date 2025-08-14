# Envio de mensagens com Python, Supabase e Z-API

Projeto que busca contatos no Supabase e envia mensagens no WhatsApp via Z-API.

## ✅ Objetivo
- Buscar contatos salvos em uma tabela do Supabase.
- Enviar mensagem personalizada (nome) para até 3 números diferentes via Z-API.

## 🧩 O que tem aqui
- `main.py` — script principal (busca contatos e envia mensagens).
- `requirements.txt` — dependências (veja sugestão abaixo).
- `.env` — variáveis de ambiente (não comitar).

## 🛠️ Pré-requisitos
- Conta no Supabase 
- Conta/instância na Z-API
- Python 3.9+ instalado.

## 🗂️ Tabela no Supabase
Crie uma tabela (ex.: `contatos`) com pelo menos estas colunas:
- `name` (text) — nome do contato
- `number` (text) — telefone em formato internacional, ex: `5511999999999`

## 🔐 Variáveis de ambiente (.env)
Crie um arquivo `.env` na raiz com estas chaves (substitua os valores pela sua configuração):

```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=suachavesupabase
SUPABASE_TABLE=contatos
SUPABASE_NAME_FIELD=name
SUPABASE_NUMBER_FIELD=number
ZAPI_INSTANCE=seu_id_da_instancia
ZAPI_TOKEN=seu_token_da_zapi
ZAPI_CLIENT_TOKEN=seu_client_token (esse deve ser ativado no painel de segurança)
```

Notas rápidas:
- `SUPABASE_TABLE`, `SUPABASE_NAME_FIELD` e `SUPABASE_NUMBER_FIELD` têm valores padrão no código.
- Telefone deve estar no formato internacional (sem `+`, ex.: `55` + DDD + número). # sem espaços

## 📦 requirements.txt
Adicione esse conteúdo ao `requirements.txt`:

```
supabase-py==0.2.6
requests==2.31.0
python-dotenv==1.0.0
```

Se preferir, instale e gere automaticamente com:

```powershell
# instala dependências listadas
pip install -r requirements.txt
```

## ▶️ Como rodar (ex.: PowerShell)

1. Configure o `.env` e confirme que a tabela `contatos` tem 1–3 números.
2. Instale as dependências.
3. Rode o script:

```powershell
pip install -r requirements.txt
python main.py
```

O script busca até 3 contatos e envia uma mensagem do tipo `Olá {nome}, tudo bem com você?` para cada número.

## ℹ️ Observações
- O `.env` não deve ser comitado — adicione-o ao `.gitignore`.
- Mensagens são enviadas usando o `Client-Token` no header da Z-API; confira o painel de segurança da Z-API.
- Se quiser personalizar a mensagem, edite `main.py` (função `enviar_mensagem`).


---
Feito para aprender e aplicar meu conhecimento na prática. 😊
