from flask import Blueprint, request, jsonify
from database import supabase

itemCardapio_bp = Blueprint('itemCardapio', __name__)

@itemCardapio_bp.route("/cadastrarCardapio", methods=["POST"])
def criar_item_cardapio():
    try:
        dados = request.json
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        campos_obrigatorios = ['nome', 'preco']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400
        
        response = supabase.table("itens_cardapio").insert({
            "nome": dados['nome'], 
            "descricao": dados.get('descricao', ''),
            "preco": dados['preco'],
            "imagem_url": dados.get('imagem_url', ''),
            "categoria_id": dados.get('categorias_id')
        }).execute()
        
        return jsonify({
            "mensagem": "Item cadastrado com sucesso!",
            "Item": response.data[0] if response.data else None
        }), 201
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar item: {str(e)}"}), 500
