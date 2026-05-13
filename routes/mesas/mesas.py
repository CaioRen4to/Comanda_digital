from flask import Blueprint, request, jsonify, render_template
from database import supabase
import uuid


mesas_bp = Blueprint('mesas', __name__, template_folder='../../templates')


@mesas_bp.route("/mesas", methods=["POST"])
def criar_mesa():

    numero = request.json.get("numero")

    if not numero:
        return jsonify({"erro": "Número da mesa é obrigatório"}), 400

    token = str(uuid.uuid4())  #Gerar um token único para a mesa

    mesa = supabase.table("mesas").insert({
        "numero": numero,
        "status": "livre",
        "qr_code_token": token
    }).execute()

    url_qrcode = f"http://localhost:3000/mesa/{token}"  #URL para acessar a mesa via QR code

    return jsonify({
        "mensagem": "Mesa criada com sucesso",
        "id": mesa.data[0]['id'],
        "url_qrcode": url_qrcode  #essa URL vira o QR Code
    })


@mesas_bp.route("/mesa/<token>", methods=["GET"])
def abrir_cardapio(token):
    
    mesa = supabase.table("mesas").select("*").eq("qr_code_token", token).execute()
    
    if not mesa.data:
        return jsonify({"erro": "Mesa não encontrada"}), 404
    
    produtos = supabase.table("produtos").select("*").execute()
    categorias = supabase.table("categorias").select("*").execute()

    return render_template(
        "cardapio.html",
        mesa=mesa.data[0],
        produtos=produtos.data or [],
        categorias=categorias.data or [],
    )
    
    
@mesas_bp.route("/mesas", methods=["GET"])
def listar_mesas():
    mesas = supabase.table("mesas").select("*").execute()
    return jsonify(mesas.data)



@mesas_bp.route("/mesas/<int:id>", methods=["PUT"])
def atualizar_mesa(id):
    status = request.json.get("status")
    supabase.table("mesas").update({
        "status": status
    }).eq("id", id).execute()
    
    return jsonify({
        "mensagem": "Mesa atualizada com sucesso"
    })
    


@mesas_bp.route("/mesas/<int:id>", methods=["DELETE"])
def deletar_mesa(id):
    supabase.table("mesas").delete().eq("id", id).execute()
    return jsonify({
        "mensagem": "Mesa deletada com sucesso"
    })
    
