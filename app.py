from flask import Flask, request, jsonify
import mercadopago # type: ignore

app = Flask(__name__)

# ✅ Tu Access Token real de prueba
ACCESS_TOKEN = "APP_USR-4695665624566666-052514-85780921cbf91c5ba4f7d76d76c67d48-1378222190"

sdk = mercadopago.SDK(ACCESS_TOKEN)

@app.route("/pago-automatico", methods=["POST"])
def pago_automatico():
    data = request.get_json()
    token = data.get("token")
    amount = float(data.get("amount", 0))
    email = data.get("email", "comprador@example.com")
    payment_method_id = data.get("payment_method_id", "visa")

    if not token or amount <= 0:
        return jsonify({"error": "Faltan datos o monto inválido"}), 400

    payment_data = {
        "transaction_amount": amount,
        "token": token,
        "description": "Pago automático",
        "installments": 1,
        "payment_method_id": payment_method_id,
        "payer": {
            "email": email
        }
    }

    result = sdk.payment().create(payment_data)
    return jsonify(result["response"])

@app.route("/")
def index():
    return open("index.html").read()

if __name__ == "__main__":
    app.run(debug=True)
