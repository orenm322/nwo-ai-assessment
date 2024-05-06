from flask import Blueprint, jsonify, request
from models import User, Sector, Source, Subcategory, UserSubscription
from database import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash

bp = Blueprint('bp', __name__)

@bp.route("/v1/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).filter(User.deleted_at.is_(None)).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})

@bp.route("/v1/user/subscription", methods=["POST"])
@jwt_required()
def save_user_subscription():
    user_id = get_jwt_identity()
    
    data = request.json
    sector_id = data["sector_id"]
    source_id = data["source_id"]
    subcategory_id = data["subcategory_id"]

    user = User.query.filter_by(id=user_id).filter(User.deleted_at.is_(None)).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_subscription = UserSubscription.query.filter_by(user_id=user_id).first()
    sector = Sector.query.filter_by(id=sector_id).filter(Sector.deleted_at.is_(None)).first()
    if not sector:
        return jsonify({"error": "Sector not found"}), 404
    source = Source.query.filter_by(id=source_id).filter(Source.deleted_at.is_(None)).first()
    if not source:
        return jsonify({"error": "Source not found"}), 404
    subcategory = Subcategory.query.filter_by(id=subcategory_id).filter(Subcategory.deleted_at.is_(None)).first()
    if not subcategory:
        return jsonify({"error": "Subcategory not found"}), 404
    
    try:
        if user_subscription:
            user_subscription.sector_id = sector_id
            user_subscription.source_id = source_id
            user_subscription.subcategory_id = subcategory_id
            user_subscription.deleted_at = None
            db.session.add(user_subscription)
            db.session.commit()
            return jsonify(user_subscription.serialize())
        else:
            user_subscription = UserSubscription(user_id=user_id, sector_id=sector_id, source_id=source_id, subcategory_id=subcategory_id)
        db.session.add(user_subscription)
        db.session.commit()
        return jsonify(user_subscription.serialize(user=user, sector=sector, source=source, subcategory=subcategory))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/v1/user/subscription", methods=["GET"])
@jwt_required()
def get_user_subscription():
    user_id = get_jwt_identity()
    user_subscription = UserSubscription.query.filter_by(user_id=user_id).filter(UserSubscription.deleted_at.is_(None)).first()
    if not user_subscription:
        return jsonify({"error": "User not subscribed"}), 404
    return jsonify(user_subscription.serialize())

@bp.route("/v1/user/subscription", methods=["DELETE"])
@jwt_required()
def delete_user_subscription():
    user_id = get_jwt_identity()
    user_subscription = UserSubscription.query.filter_by(user_id=user_id).filter(UserSubscription.deleted_at.is_(None)).first()
    if not user_subscription:
        return jsonify({"error": "User is not currently subscribed"}), 404
    try:
        user_subscription.deleted_at = db.func.now()
        db.session.add(user_subscription)
        db.session.commit()
        return jsonify({"result": "User has been unsubscribed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400