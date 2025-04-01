import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv("api.env")
API_KEY = os.getenv("API_KEY")
print("Chave da API:", API_KEY)  # Isso deve imprimir a chave



# Configurar Firebase
cred = credentials.Certificate("clima-19bf4-firebase-adminsdk-fbsvc-2c9dd49d62.json")  # Caminho do arquivo JSON do Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuração da API
CITY = "Florianópolis"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Faz a requisição
response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    
    # Extrai os dados
    cidade = data["name"]
    temperatura = data["main"]["temp"]
    descricao = data["weather"][0]["description"]
    data_hora = datetime.now().isoformat()

    # Cria um documento no Firestore
    doc_ref = db.collection("clima").add({
        "cidade": cidade,
        "temperatura": temperatura,
        "descricao": descricao,
        "data_hora": data_hora
    })

    print("Dados inseridos com sucesso no Firebase!")
else:
    print("Erro ao acessar a API:", response.status_code)
