from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from io import BytesIO
from models import User, SessionLocal, init_db
from kmz_utils import build_corrected_kmz

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "troque-por-uma-chave-forte"
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
init_db()

def _db():
    return SessionLocal()

@app.post("/signup")
def signup():
    data = request.json
    db = _db()
    if db.query(User).filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email já cadastrado"}), 400
    hashed = bcrypt.generate_password_hash(data["password"]).decode()
    db.add(User(email=data["email"], password=hashed))
    db.commit()
    return jsonify({"msg": "ok"})

@app.post("/login")
def login():
    data = request.json
    db = _db()
    user = db.query(User).filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Credenciais inválidas"}), 401
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)

@app.post("/process")
@jwt_required()
def process_kmz():
    if "file" not in request.files:
        return jsonify({"msg": "Arquivo ausente"}), 400
    kmz_bytes = request.files["file"].read()
    out_kmz = build_corrected_kmz(kmz_bytes)
    return send_file(
        BytesIO(out_kmz),
        download_name="corrigido.kmz",
        mimetype="application/vnd.google-earth.kmz"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
