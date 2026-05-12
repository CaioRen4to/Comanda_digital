from flask import Flask, Blueprint, request, jsonify
from supabase import create_client, Client
import os
import uuid


mesas_bp = Blueprint('mesas', __name__)
def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)


@mesas_bp.route("/mesas", methods=["POST"])
def criar_mesa():
    
    supabase = get_supabase()
    numero = request.json.get("numero")
    token = str(uuid.uuid4())  #Gerar um token único para a mesa
    
    mesa = supabase.table("mesas").insert({
        "numero": numero,
        "status": "livre",
        "qr_code_token": token
    }).execute()
    
    url_qrcode = f"http://localhost:3000/mesa/{token}"  #URL para acessar a mesa via QR code
    
    if not numero:
        return jsonify({"erro": "Número da mesa é obrigatório"}), 400
    
    return jsonify({
        "mensagem": "Mesa criada com sucesso",
        "id": mesa.data[0]['id'],
        "url_qrcode": url_qrcode  #essa URL vira o QR Code
    })



@mesas_bp.route("/mesas", methods=["GET"])
def listar_mesas():
    supabase = get_supabase()
    mesas = supabase.table("mesas").select("*").execute()
    return jsonify(mesas.data)



@mesas_bp.route("/mesas/<int:id>", methods=["PUT"])
def atualizar_mesa(id):
    status = request.json.get("status")
    supabase = get_supabase()
    supabase.table("mesas").update({
        "status": status
    }).eq("id", id).execute()
    
    return jsonify({
        "mensagem": "Mesa atualizada com sucesso"
    })
    


@mesas_bp.route("/mesas/<int:id>", methods=["DELETE"])
def deletar_mesa(id):
    supabase = get_supabase()
    supabase.table("mesas").delete().eq("id", id).execute()
    return jsonify({
        "mensagem": "Mesa deletada com sucesso"
    })
    
