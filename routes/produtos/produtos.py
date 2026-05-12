from supabase import create_client, Client
from flask import Flask, app, jsonify, redirect, request
import os
import supabase


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
