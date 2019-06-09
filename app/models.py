from extensions import db
from datetime import datetime
from sqlalchemy import ForeignKey


class users(db.Model):
    id = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    current_question = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.email


class questions(db.Model):
    # automatically increments, default
    id = db.Column(db.Integer, primary_key=True)
    # question_type = "multiple_choice" || "text_answer"
    question_type = db.Column(db.String())
    body = db.Column(db.String())
    answers = db.Column(db.String())
    correct_answer = db.Column(db.String())
    assessment_id = db.Column(db.Integer)
    users_answers = db.relationship("user_answers", backref="question")


class user_answers(db.Model):
    user_id = db.Column(db.String(), ForeignKey(users.id), primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey(
        questions.id), primary_key=True)
    user_answer = db.Column(db.String())


class assessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_questions = db.Column(db.Integer)
