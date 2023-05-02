from flask import render_template, request, jsonify
from models import app, db, Game, Review
import sqlalchemy
from flask_cors import CORS
from datetime import datetime

db.init_app(app)
CORS(app)


# ページ遷移
@app.route("/")
def index():
    games = Game.query.all()
    return render_template("index.html", games=games)


# ゲーム一覧を取得
@app.route("/game_list", methods=["GET"])
def get_games():
    games = Game.query.all()
    games_json = [game.to_dict() for game in games]
    return jsonify(games=games_json)


# レビュー登録ページ
@app.route("/review")
def review():
    games = Game.query.all()
    reviews = Review.query.all()
    return render_template("review.html", games=games, reviews=reviews)


# 機能系
# ゲーム登録
@app.route("/add_game", methods=["POST"])
def add_game():
    data = request.get_json()
    game_id = data.get("game_id")
    game_name = data.get("game_name")
    game = Game(game_id, game_name)
    try:
        db.session.add(game)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")
    return render_template("confirm_added_game.html", game=game)


# レビュー登録
@app.route("/add_review", methods=["POST"])
def add_review():
    data = request.get_json()
    game_name = data.get("game_name")
    play_status = data.get("play_status")
    evaluation = data.get("evaluation")
    category = data.get("category")
    impression = data.get("impression")
    register_date = data.get("register_date")
    register_date = datetime.strptime(register_date, "%Y-%m-%d")
    game = Game.query.filter_by(game_name=game_name).first()
    review = Review(
        game.game_id,
        play_status,
        evaluation,
        category,
        impression,
        register_date,
    )
    try:
        db.session.add(review)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")

    return render_template("confirm_added_review.html", review=review)


# レビュー削除
@app.route("/delete_review", methods=["POST"])
def delete_review():
    review_id = request.form["input-review-id"]
    review = Game.query.filter_by(review_id=review_id).first()
    try:
        db.session.delete(review)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")

    return render_template("confirm_deleted_review.html", review=review)


if __name__ == "__main__":
    app.run(debug=True)
