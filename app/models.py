from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
badges = db.Table('badges',
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    badges = db.relationship('Badge', secondary=badges, lazy='subquery', backref=db.backref('users', lazy=True))
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    user = db.relationship('User', backref=db.backref('question-user', lazy = True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    def __repr__(self):
        return '<Category %r>' % self.name

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
    question = db.relationship('Question', backref=db.backref('question', lazy = True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    user = db.relationship('User', backref=db.backref('user', lazy = True))
