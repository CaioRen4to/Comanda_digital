from supabase import create_client, Client
from flask import Flask, redirect
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


@app.route('/')
def seed():

    categorias = [
    ]

    response = supabase.table("categorias").insert(categorias).execute()

    return {
        "mensagem": "Inserido",
        "dados": response.data
    }




if __name__ == '__main__':
    conectDB()
    app.run(debug=True)