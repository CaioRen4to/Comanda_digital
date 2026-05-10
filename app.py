from supabase import create_client, Client
from flask import Flask, jsonify, redirect, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def conectDB() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY precisam estar definidos no .env")

    supabase: Client = create_client(url, key)
    return supabase

supabase = conectDB()


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():

    dados = request.json

    nome = dados['nome']
    descricao = dados['descricao']
    preco = dados['preco']
    imagem_url = dados['imagem_url']

    supabase.table("produtos").insert({
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "imagem_url": imagem_url
    }).execute()

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    })




if __name__ == '__main__':
    supabase = conectDB()
    app.run(debug=True)