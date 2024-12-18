from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

app = Flask(__name__)

# Configurações do Pub/Sub
PROJECT_ID = "stoked-virtue-321000"
TOPIC_ID = "transacoes-topico"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

# Rota principal
@app.route('/')
def home():
    return "API Pub/Sub está funcionando! Use a rota /enviar para enviar dados.", 200

@app.route('/enviar', methods=['POST'])
def enviar_dados():
    try:
        dados = request.json
        # Envia a mensagem ao Pub/Sub
        mensagem = str(dados).encode("utf-8")
        future = publisher.publish(topic_path, mensagem)
        future.result()  # Garante que a mensagem foi enviada
        return jsonify({"status": "sucesso", "message_id": future.result()}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
