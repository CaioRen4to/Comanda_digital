from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os
import supabase


produtos_bp = Blueprint('produtos', __name__)

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

@produtos_bp.route("/produtos", methods=["POST"])
def cadastrar_produto():

    dados = request.json

    supabase.table("produtos").insert({
        "nome": dados['nome'],
        "descricao": dados['descricao'],
        "preco": dados['preco'],
        "imagem_url": dados['imagem_url']
    }).execute()

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    })
