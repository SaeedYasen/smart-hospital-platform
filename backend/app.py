from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["JWT_SECRET_KEY"] = "super-secret"

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="patient")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Smart Hospital Platform API"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return {"msg": "User created"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    if not user:
        return {"msg": "Bad credentials"}, 401
    token = create_access_token(identity=user.id)
    return {"token": token}

if __name__ == "__main__":
    app.run(debug=True)
