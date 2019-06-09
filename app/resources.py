import models
import uuid
import json
from datetime import datetime
from extensions import db
from config import Config
from flask_restful import Resource, Api
from flask import request, Response
from json import dumps


def timeLeft(createdTime):
    return Config.TIME_LIMIT_IN_SECONDS - (datetime.utcnow() - createdTime).total_seconds()


class User(Resource):
    # create a user
    def post(self):

        UUID = str(uuid.uuid4())

        data = request.json
        user = models.users(id=UUID, email=data["email"], first_name=data["first_name"],
                            last_name=data["last_name"], current_question=0)
        db.session.add(user)
        db.session.commit()

        user_return = models.users.query.filter_by(id=UUID).first()

        return {
            'timeLeft': timeLeft(user_return.created),
            'first_name': user_return.first_name,
            'last_name': user_return.last_name,
            # frontend needs UUID to redirect to get question
            'UUID': user_return.id
        }


class Question(Resource):
    # get next question for user
    def get(self, session_id):
        user = models.users.query.filter_by(id=session_id).first()

        if timeLeft(user.created) <= 0:
            # three statuses: ('NO TIME LEFT', 'QUESTION', 'NO QUESTIONS LEFT')
            return {
                'status': 'NO TIME LEFT'
            }

        # frontend should subsequently redirect to GET user/ansers/<session_id>
        if models.users.query.filter_by(id=session_id).first().current_question == Config.NUMBER_OF_QUESTIONS:
            return {
                'status': 'NO QUESTIONS LEFT'
            }

        # the user can recieve the next question
        user.current_question = user.current_question + 1
        db.session.commit()

        question = models.questions.query.filter_by(
            id=user.current_question).first()

        return {
            'status': 'QUESTION',
            'question_id': question.id,
            'question_type': question.question_type,
            'body': question.body,
            'answers': question.answers
        }

    # to POST an answer to a question
    def post(self, session_id):
        user = models.users.query.filter_by(id=session_id).first()

        if timeLeft(user.created) <= 0:
            # two statuses: ('NO TIME LEFT', 'SUBMITTED')
            return {
                'status': 'NO TIME LEFT'
            }

        # otherwise, submit the answer
        data = request.json

        user_answer = models.user_answers(
            user_id=session_id, question_id=data["question_id"], user_answer=data["answer"])
        db.session.merge(user_answer)
        db.session.commit()

        return {
            'status': 'SUBMITTED'
        }


class Answers(Resource):
    # get all questions with user answers for final screen
    def get(self, session_id):
        user = models.users.query.filter_by(id=session_id).first()
        if timeLeft(user.created) <= 0:
            # two statuses: ('NO TIME LEFT', 'QUESTIONS')
            return {
                'status': 'NO TIME LEFT',
                'data': []
            }

        # return all questions with answers
        # user will only ever hit this after having submitted an answer for every problem
        # after getting "NO_QUESTIONS_LEFT" on the Questions GET endpoint
        response = {'status': 'QUESTIONS'}
        #query = models.user_answers.query.filter_by(user_id=session_id).all()

        query = models.user_answers.query.filter_by(user_id=session_id).all()
        data = []
        for o in query:
            data.append(
                {
                    'question_id': o.question.id,
                    'question_type': o.question.question_type,
                    'body': o.question.body,
                    'answers': o.question.answers,
                    "user_answer": o.user_answer
                }
            )
        response['data'] = data
        return response

    def post(self, session_id):
        user = models.users.query.filter_by(id=session_id).first()
        if timeLeft(user.created) <= 0:
            # three statuses: ('NO TIME LEFT', 'SUBMITTED')
            return {
                'status': 'NO TIME LEFT'
            }

        # otherwise, update answers
        data = request.json["data"]

        for questionAndAnswer in data:
            user_answer = models.user_answers(
                user_id=session_id, question_id=questionAndAnswer["question_id"])
            user_answer.user_answer = questionAndAnswer["updated_user_answer"]
            db.session.merge(user_answer)
        db.session.commit()


        return {
            'status': 'SUBMITTED'
        }
