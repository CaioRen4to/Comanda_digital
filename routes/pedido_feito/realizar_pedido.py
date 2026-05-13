from flask import app
from database import supabase
from flask import Blueprint, request, jsonify, render_template
from routes.mesas.mesas import mesas_bp


pedidos_realizado_bp = Blueprint('pedidos_realizado', __name__, template_folder='../../templates')



@pedidos_realizado_bp.route('/mesa/<token>/pedido', methods=['POST'])
def pedidos_realizado(token):
    
    mesa = supabase.table("mesas").select("*").eq("qr_code_token", token).execute()
    if not mesa.data:
        return jsonify({"erro": "Mesa não encontrada"}), 404
    
    mesa_id = mesa.data[0]['id']
    
    
    produtos = supabase.table("produtos").select("*").execute()
    produtos_dict = {produto['id']: produto for produto in produtos.data}
    
    pedido = supabase.table("pedidos").insert({
        'fk_mesa_id': mesa_id,
        'status': 'recebido',
        'valor_total': 0,
        'solicitar_conta': False
    }).execute()
    
    pedido_id = pedido.data[0]['id']
    
    valor_total = 0
    itens = []
    
    
    for produto_id, produto in produtos_dict.items():
        quantidade = int(request.form.get(f'quantidade_{produto_id}', 0))
        if quantidade > 0:
            subtotal = quantidade * float(produto['preco'])
            valor_total += subtotal
            itens.append({
                'fk_pedido_id': pedido_id,
                'fk_produto_id': produto_id,
                'quantidade': quantidade,
                'valor_unitario': produto['preco'],
                'subtotal': subtotal
            })
            
    # Salvar os itens do pedido no banco de dados        
    if itens:
        supabase.table("itens_pedido").insert(itens).execute()
    
    # Atualizar o valor total do pedido
    supabase.table("pedidos").update({
        'valor_total': valor_total
        }).eq('id', pedido_id).execute()
    
    return render_template("pedido_confirmado.html", mesa=mesa.data[0], valor_total=valor_total)

