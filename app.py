from supabase import create_client, Client
from flask import Flask, jsonify, redirect, request
import os
from dotenv import load_dotenv
from routes.produtos.produtos import produtos_bp

load_dotenv()

# Teste de leitura do .env
print(f"--- DEBUG ENV ---")
print(f"SUPABASE_URL: {'Carregado' if os.getenv('SUPABASE_URL') else 'NÃO CARREGADO'}")
print(f"SUPABASE_KEY: {'Carregado' if os.getenv('SUPABASE_KEY') else 'NÃO CARREGADO'}")
print(f"-----------------")

app = Flask(__name__)
app.register_blueprint(produtos_bp)

def conectDB() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY precisam estar definidos no .env")

    supabase: Client = create_client(url, key)
    return supabase

supabase = conectDB()


if __name__ == '__main__':
    supabase = conectDB()
    app.run(debug=True)