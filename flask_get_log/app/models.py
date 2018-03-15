from app import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.REAL(), index=True)
    event = db.Column(db.String())

    def __repr__(self):
        return '<Log {}>'.format(self.dt)


class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    gender = db.Column(db.String())

    def __repr__(self):
        return 'People {0} {1}'.format(self.first_name, self.last_name)
