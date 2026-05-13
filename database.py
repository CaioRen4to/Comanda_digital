from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

"""
Cria e retorna um cliente Supabase usando variáveis de ambiente.
Lança ValueError se as variáveis não estiverem definidas.
"""

def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY precisam estar definidos no .env")

    return create_client(url, key)

# Instância global do cliente Supabase
supabase = get_supabase()
