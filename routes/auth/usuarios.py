from flask import Blueprint, request, jsonify
from database import supabase
import bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route("/usuarios", methods=["POST"])
def criar_usuario():

    dados = request.json

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")
    cargo = dados.get("cargo")

    if not nome or not email or not senha or not cargo:

        return jsonify({
            "erro": "Todos os campos são obrigatórios"
        }), 400

    senha_hash = bcrypt.hashpw(

        senha.encode('utf-8'),
        bcrypt.gensalt()

    ).decode('utf-8')

    usuario = supabase.table("usuarios").insert({

        "nome": nome,
        "email": email,
        "senha_hash": senha_hash,
        "cargo": cargo

    }).execute()

    return jsonify({

        "mensagem": "Usuário criado com sucesso",
        "usuario": usuario.data

    })


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():

    usuarios = supabase.table("usuarios").select("*").execute()

    return jsonify(usuarios.data)


@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):

    dados = request.json

    supabase.table("usuarios").update({

        "nome": dados.get("nome"),
        "email": dados.get("email"),
        "cargo": dados.get("cargo")

    }).eq("id", id).execute()

    return jsonify({
        "mensagem": "Usuário atualizado com sucesso"
    })


@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):

    supabase.table("usuarios").delete().eq("id", id).execute()

    return jsonify({
        "mensagem": "Usuário deletado com sucesso"
    })