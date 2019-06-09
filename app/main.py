from flask import Flask, request
from config import Config
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from extensions import db
import resources
import models
import json

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

    # create single assessment
    assessment = models.assessments(
        id=Config.ASSESSMENT_ID, number_of_questions=Config.NUMBER_OF_QUESTIONS)
    db.session.add(assessment)
    db.session.commit()

    # load test assessment questions into db
    with open("test_questions.json", "r") as datafile:
        questions = json.load(datafile)["data"]
        for question in questions:
            questionObj = models.questions(question_type=question["question_type"],
                                           body=question["body"],
                                           answers=json.dumps(
                                               question["answers"]),
                                           correct_answer=question["correct_answer"],
                                           assessment_id=int(question["assessment_id"])                                           )
            db.session.add(questionObj)
    db.session.commit()

api.add_resource(resources.User, '/user/create_session')
api.add_resource(resources.Question, '/assessment/<string:session_id>')
api.add_resource(resources.Answers, '/answers/<string:session_id>')

if __name__ == '__main__':
    app.run(debug=True)
