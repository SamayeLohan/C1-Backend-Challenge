import requests
import json

# create user
created_user = requests.post("http://localhost:5000/user/create_session",json={"email": "a@b.com", "first_name": "a", "last_name": "b"})


assert(created_user.status_code == 200)

# get users UUID
created_user = json.loads(created_user.content)["UUID"]

print("created USER = " + created_user)

questionIds = []
print("GETTING QUESTIONS")
while(True):
    # get questions while there are questions
    questionObj = requests.get(
        "http://localhost:5000/assessment/" + created_user)
    assert(questionObj.status_code == 200)
    question = json.loads(questionObj.content)
    if (question["status"] == "NO QUESTIONS LEFT" or question["status"] == "NO TIME LEFT"):
        break
    questionIds.append(question["question_id"])
    print("-----------------QUESTION------------------")
    print(question)
    print("--------------------END--------------------")

print("SUBMITTING ANSWERS")
# submit answers for all questions in questionIds
for questionId in questionIds:
    success = requests.post("http://localhost:5000/assessment/" + created_user,
                            # the answer to the universe
                            json={"question_id": questionId, "answer": "42"})

    assert(success.status_code == 200)
    success = json.loads(success.content)
    assert(success["status"] == "SUBMITTED")

    print("SUBMITTED ANSWER = " + str(42) +
          " FOR question_id" + str(questionId))

print("GETTING LIST OF ALL QUESTIONS WITH SUBMITTED ANSWERS")
questionsWithAnswers = requests.get(
    "http://localhost:5000/answers/" + created_user)

assert(questionsWithAnswers.status_code == 200)
questionsWithAnswers = json.loads(questionsWithAnswers.content)

assert(questionsWithAnswers["status"] == 'QUESTIONS')
questionsWithAnswers = questionsWithAnswers["data"]

userAnswers = {}
for questionWithAnswer in questionsWithAnswers:
    print("-----------------QUESTION------------------")
    for i in questionWithAnswer:
        print(i + " : ", questionWithAnswer[i])
    print("--------------------END--------------------")

# modify answers of even numbered questions
resubmit = []
for i in range(len(questionIds)):
    question = {"question_id": questionIds[i]}
    if (i % 2 == 0):
        question["updated_user_answer"] = 1234
        resubmit.append(question)

print("MODIFYING ANSWERS FOR: ")
data = {"data":resubmit}
print(data)

success = requests.post("http://localhost:5000/answers/" + created_user, json=data)
assert(success.status_code == 200)
success = json.loads(success.content)
assert(success["status"] == "SUBMITTED")
