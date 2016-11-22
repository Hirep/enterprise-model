from application import db
from datetime import datetime


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name_first = db.Column(db.String(64))
#     name_second = db.Column(db.String(64))
#     department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
#     position_id = db.Column(db.Integer,  db.ForeignKey('departments.id'))
#     email = db.Column(db.String(64), unique=True)
#     tel = db.Column(db.String(15))
#     birth_date = db.Column(db.Date(), default=datetime.utcnow)

#     def __repr__(self):
#         return "Name: {} {}\nEmail: {}\nTel: {}".format(self.name_first,
#                             self.name_second,
#                             self.email,
#                             self.tel)

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(64), unique=True)
    parental_department_id = db.Column(db.Integer)
    head_id = db.Column(db.Integer, unique=True)
    about = db.Column(db.Text())


class Position(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(64), unique=True)
    about = db.Column(db.Text())

    



    