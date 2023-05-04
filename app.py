from flask import render_template, request, jsonify
from models import app, db, Game, Review
import sqlalchemy
from flask_cors import CORS
from datetime import datetime
import traceback

db.init_app(app)
CORS(app)


# ページ遷移
@app.route("/")
def index():
    return "This is the index page"


# ゲーム一覧を取得
@app.route("/game_list", methods=["GET"])
def get_games():
    games = Game.query.all()
    games_json = [game.to_dict() for game in games]
    return jsonify(games_json)


@app.route("/game_list/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game is None:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(game.to_dict())


# 機能系
# ゲーム登録
@app.route("/add_game", methods=["POST"])
def add_game():
    data = request.get_json()
    game_name = data.get("game_name")
    game = Game(game_name=game_name)
    try:
        db.session.add(game)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as sqlalchemy_error:
        db.session.rollback()
        return jsonify({"error": str(sqlalchemy_error.orig)}), 400
    return jsonify({"game": game.to_dict()})


# レビュー登録
@app.route("/add_review", methods=["POST"])
def add_review():
    data = request.get_json()
    game_id = data.get("game_id")
    if game_id is None:
        return jsonify({"error": "game_id is missing"}), 400
    game = Game.query.get(game_id)
    if game is None:
        return jsonify({"error": "game_id does not exist"}), 400
    play_status = data.get("play_status")
    play_status = int(play_status)
    evaluation = data.get("evaluation")
    if evaluation is not None:
        evaluation = int(evaluation)
    category = data.get("category")
    impression = data.get("impression")
    register_date = data.get("register_date")
    register_date = datetime.fromisoformat(register_date).date()
    review = Review(
        game_id=game_id,
        play_status=play_status,
        evaluation=evaluation,
        category=category,
        impression=impression,
        register_date=register_date,
    )
    try:
        print("通過")
        db.session.add(review)
        print("通過2")
        db.session.commit()
        print("通過3")
    except sqlalchemy.exc.IntegrityError as sqlalchemy_error:
        db.session.rollback()
        print("通過４")
        print(str(sqlalchemy_error.orig))
        return jsonify({"error": str(sqlalchemy_error.orig)}), 400
    return jsonify({"review": review.to_dict()})


# レビュー削除
@app.route("/delete_review", methods=["POST"])
def delete_review():
    review_id = request.form["input-review-id"]
    review = Game.query.filter_by(review_id=review_id).first()
    try:
        db.session.delete(review)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as sqlalchemy_error:
        db.session.rollback()
        return jsonify({"error": str(sqlalchemy_error.orig)}), 400

    return jsonify({"レビューを削除しました": review.to_dict()})


@app.errorhandler(Exception)
def handle_exception(error):
    tb = traceback.format_exc()
    return jsonify({"error": str(error), "traceback": tb}), 400


if __name__ == "__main__":
    app.run(debug=True)
