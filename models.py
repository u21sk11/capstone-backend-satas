from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def set_up(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://przorgkwvdvzvs:6ec48f0258d245a8a6302f7b7bd923d25f1ef086ca1944594474b7850d13860f@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d3s52rgbce333f"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def insert(self):
        db.session.add(self)
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