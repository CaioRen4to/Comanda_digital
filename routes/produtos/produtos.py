import flask
from database import supabase

produtos_bp = flask.Blueprint('produtos', __name__)

@produtos_bp.route("/produtos", methods=["POST"])
def cadastrar_produto():

    dados = flask.request.json

    supabase.table("produtos").insert({
        "nome": dados['nome'],
        "descricao": dados['descricao'],
        "preco": dados['preco'],
        "imagem_url": dados['imagem_url']
    }).execute()

    return flask.jsonify({
        "mensagem": "Produto cadastrado com sucesso"
    })
