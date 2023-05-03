from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "GM.db"
)
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String, nullable=False)

    def __init__(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name

    reviews = db.relationship("Review", backref="reviews", cascade="delete")

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
        }


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"))
    game_name = db.Column(db.String)
    play_status = db.Column(db.Integer)
    evaluation = db.Column(db.Integer)
    category = db.Column(db.String)
    impression = db.Column(db.String)
    register_date = db.Column(db.Date)

    def __init__(
        self,
        game_id,
        play_status,
        evaluation,
        category,
        impression,
        register_date,
    ):
        self.game_id = game_id
        self.play_status = play_status
        self.evaluation = evaluation
        self.category = category
        self.impression = impression
        self.register_date = register_date


with app.app_context():
    db.create_all()
