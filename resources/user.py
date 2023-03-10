import requests
import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema, UserRegisterSchema


blp = Blueprint("Users", "users", description="Operations on users")


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    mailgun_address = f"https://api.mailgun.net/v3/{domain}/messages"
    return requests.post(
        f"{mailgun_address}",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Christopher Austin <mailgun@{domain}>",
              "to": [to],
              "subject": subject,
              "text": body})


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):                                                         # Create a user
        if UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"]
                )
        ).first():
            abort(409, message="A user with that username or email already exists.")   # 409 means "conflict"

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        send_simple_message(
            to=user.email,
            subject="Successfully signed up.",
            body=f"Hi {user.username}!  You have successfully signed up to Digiwares REST API."
        )
        print(f"{user.email}, {user.username}, TESTING")            # test for user creation
        return {"message": "User created successfully."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/user")                                  # http://127.0.0.1:5000/user
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):                                   # Retrieve all users
        return UserModel.query.all()
