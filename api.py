from flask import Flask, jsonify, request
from datetime import datetime
from firebase_config import db  # Importa apenas a instância já configurada do Firestore

app = Flask(__name__)

# Função para converter qualquer formato de data para ISO 8601
def formatar_data_para_iso(data_hora_str):
    try:
        return datetime.fromisoformat(data_hora_str).strftime("%Y-%m-%dT%H:%M:%S")  # Já está no formato correto
    except ValueError:
        try:
            data_hora_obj = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            return data_hora_obj.strftime("%Y-%m-%dT%H:%M:%S")  # Converte para ISO 8601
        except ValueError:
            return None  # Se falhar, retorna None


@app.route("/clima", methods=["POST"])
def adicionar_clima():
    data = request.json  # Recebe os dados do corpo da requisição
    
    # Converte e valida a data antes de salvar
    data_hora_formatada = formatar_data_para_iso(data.get("data_hora"))
    if not data_hora_formatada:
        return jsonify({"error": "Formato de data inválido! Use 'YYYY-MM-DDTHH:MM:SS' ou 'dd/MM/yyyy HH:MM'."}), 400
    
    data["data_hora"] = data_hora_formatada  # Atualiza o campo com a data formatada
    db.collection("clima").add(data)
    
    return jsonify({"mensagem": "Registro adicionado com sucesso!"}), 201


@app.route("/clima", methods=["GET"])
def get_clima():
    clima_ref = db.collection("clima")
    docs = clima_ref.stream()
    
    clima_data = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id  # 🔹 Adiciona o ID do documento 🔹
        clima_data.append(data)
        
        # Trata qualquer formato de data salvo no Firestore
        try:
            data["data_hora"] = formatar_data_para_iso(data["data_hora"])
            if not data["data_hora"]:
                raise ValueError("Formato inválido")

            # Retorna a data formatada para um formato legível
            data["data_hora"] = datetime.fromisoformat(data["data_hora"]).strftime("%d/%m/%Y %H:%M")
        
        except ValueError:
            return jsonify({"error": f"Erro ao formatar data: {data['data_hora']}"}), 400

        clima_data.append(data)
    
    return jsonify(clima_data)


@app.route("/clima/<cidade>", methods=["GET"])
def get_clima_por_cidade(cidade):
    clima_ref = db.collection("clima").where("cidade", "==", cidade)
    docs = clima_ref.stream()

    clima_data = []
    for doc in docs:
        data = doc.to_dict()
        
        try:
            data["data_hora"] = formatar_data_para_iso(data["data_hora"])
            if not data["data_hora"]:
                raise ValueError("Formato inválido")

            data["data_hora"] = datetime.fromisoformat(data["data_hora"]).strftime("%d/%m/%Y %H:%M")
        
        except ValueError:
            return jsonify({"error": f"Erro ao formatar data: {data['data_hora']}"}), 400

        clima_data.append(data)
    
    return jsonify(clima_data)

@app.route("/clima/<id>", methods=["PUT"])
def atualizar_clima(id):
    data = request.json  # Pega os novos dados do request

    doc_ref = db.collection("clima").document(id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update(data)
        return jsonify({"mensagem": "Registro atualizado com sucesso!"})
    else:
        return jsonify({"erro": "Registro não encontrado!"}), 404
    

@app.route("/clima/<id>", methods=["DELETE"])
def deletar_clima(id):
    doc_ref = db.collection("clima").document(id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.delete()
        return jsonify({"mensagem": "Registro deletado com sucesso!"})
    else:
        return jsonify({"erro": "Registro não encontrado!"}), 404
    
@app.route("/clima/media/<cidade>", methods=["GET"])
def media_temperatura(cidade):
    clima_ref = db.collection("clima").where("cidade", "==", cidade)
    docs = clima_ref.stream()

    temperaturas = [doc.to_dict()["temperatura"] for doc in docs]

    if temperaturas:
        media = sum(temperaturas) / len(temperaturas)
        return jsonify({"cidade": cidade, "temperatura_media": round(media, 2)})
    else:
        return jsonify({"erro": "Nenhum dado encontrado para essa cidade!"}), 404





if __name__ == "__main__":
    app.run(debug=True)
