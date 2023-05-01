from flask import render_template, request
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
    game_id = request.form["input-game-id"]
    game_name = request.form["input-game-name"]
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
    game_name = request.form["input-game-name"]
    play_status = request.form["input-play-status"]
    evaluation = request.form["input-evaluation"]
    category = request.form["input-category"]
    impression = request.form["input-impression"]
    register_date = request.form["input-register-date"]
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