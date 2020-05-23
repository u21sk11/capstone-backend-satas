from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def set_up(app):
    d = "postgres"
    user = "przorgkwvdvzvs"
    password = "6ec48f0258d245a8a6302f7b7bd923d25f1ef086ca1944594474b7850d13860f"
    host = "ec2-54-217-204-34.eu-west-1.compute.amazonaws.com"
    port = "5432"
    lib = "d3s52rgbce333f"
    app.config["SQLALCHEMY_DATABASE_URI"] = "{}://{}:{}@{}:{}/{}".format(d, user, password, host, port, lib)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def patch(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def patch(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
