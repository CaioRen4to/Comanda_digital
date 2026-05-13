from flask import Blueprint, request, jsonify
from database import supabase

itemCardapio_bp = Blueprint('itemCardapio', __name__)

@itemCardapio_bp.route("/cadastrarCardapio", mehotds=["POST"])
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
            "imagem_url": dados.get('imagem.url', ''),
            "categoria_id": dados.get('categorias_id')
        }).execute()
        
        return jsonify({
            "mensagem": "Item cadastrado com sucesso!",
            "Item": response.data[0] if response.data else None
        }), 201
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar item: {str(e)}"}), 500
    
@itemCardapio_bp.route ("/itensCardapio", methods=["GET"])
def listar_item_cardapio():
    try:
        response = supabase.table("itens_cardapio").select("*").execute()
        return jsonify({"itens": response.data}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar itens: {str(e)}"}), 500

@itemCardapio_bp.route ("/itensCardapio/<int:item_id>", methods=["PUT"])
def atualizar_item_cardapio (item_id):
    try:
        dados = request.json
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 500
        
        update_data = {}
        
        campos_permitidos = ["nome", "descricao", "preco", "imagem_url", "categoria"]
        for campo in campos_permitidos:
            if campo in dados:
                update_data[campo] = dados[campo]
                
        if not update_data:
            return jsonify({"erro": "Nenhum campo válido para atualização"}), 400
                
        response = supabase.table("itens_cardapio").update(update_data).eq("id", item_id).execute()
            
        if not response.data:
            return jsonify({"erro": "Item não encontrado"}), 404
            
        return jsonify({
            "mensagem": "Item atualizado com sucesso",
            "item": response.data[0]
        }), 200
            
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar item: {str(e)}"}), 500
    
@itemCardapio_bp.route ("/itensCardapio/<int:item_id>", methods=["DELETE"])
def deletar_item_cardapio (item_id):
    try:
        response = supabase.table("itens_cardapio").delete().eq("id", item_id).execute()
        
        if not response.data:
            return jsonify({"erro": "Item não encontrado"}), 404
        
        return jsonify({"mensagem": "Item deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar o item: {str(e)}" }), 500