from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "GM.db"
)
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_name = db.Column(db.String, nullable=False)

    reviews = db.relationship(
        "Review", backref="game", lazy=True, cascade="delete"
    )

    def __init__(self, game_name):
        self.game_name = game_name

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "game_name": self.game_name,
        }


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(
        db.Integer, db.ForeignKey("games.game_id"), nullable=False
    )
    play_status = db.Column(db.Integer, nullable=False)
    evaluation = db.Column(db.Integer)
    category = db.Column(db.String)
    impression = db.Column(db.String)
    register_date = db.Column(db.Date, nullable=False)

    def __init__(
        self,
        play_status,
        evaluation,
        category,
        impression,
        register_date,
        game_id=None,
        review_id=None,
    ):
        self.play_status = play_status
        self.evaluation = evaluation
        self.category = category
        self.impression = impression
        self.register_date = register_date
        self.game_id = game_id
        self.review_id = review_id
        self.register_date = parse_date(register_date)

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "play_status": self.play_status,
            "evaluation": self.evaluation,
            "category": self.category,
            "impression": self.impression,
            "register_date": self.register_date.strftime("%Y-%m-%d"),
        }


def parse_date(date_str):
    """Parse ISO datetime string to datetime object."""
    try:
        date_str = str(date_str)
        date = datetime.fromisoformat(date_str)
        return date.date()
    except ValueError:
        return None


with app.app_context():
    db.create_all()
