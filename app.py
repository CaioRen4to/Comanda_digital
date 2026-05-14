from supabase import create_client, Client
from flask import Flask, jsonify, redirect, request
import os
from dotenv import load_dotenv

load_dotenv()

from routes.produtos.produtos import produtos_bp
from routes.produtos.cardapio.itemCardapio import itemCardapio_bp
from routes.mesas.mesas import mesas_bp
from routes.auth.usuarios import usuarios_bp
from database import supabase


# Teste de leitura do .env
print(f"--- DEBUG ENV ---")
print(f"SUPABASE_URL: {'Carregado' if os.getenv('SUPABASE_URL') else 'NÃO CARREGADO'}")
print(f"SUPABASE_KEY: {'Carregado' if os.getenv('SUPABASE_KEY') else 'NÃO CARREGADO'}")
print(f"-----------------")


app = Flask(__name__)
app.register_blueprint(produtos_bp)
app.register_blueprint(itemCardapio_bp)
app.register_blueprint(mesas_bp)
app.register_blueprint(usuarios_bp)



if __name__ == '__main__':
    app.run(debug=True)