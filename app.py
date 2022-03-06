from flask import Flask
from flask_restful import Api, Resource

from contest_search import ContestSearch

# Init the server
app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello():
    return "Hello"


# Init the scrapping bot
bot_search = ContestSearch()


class HelloWorld(Resource):
    def get(self, contest):

        # return competitive programming contest
        if contest == "cp":
            bot_search.get_cp_contests()
            return {"data": bot_search.cp_data}

        # return machine learning contest
        if contest == "ml":
            bot_search.get_ml_contests()
            return {"data": bot_search.ml_data}

        # return hackathon contest
        if contest == "hackathon":
            bot_search.get_hackathon_contests()
            return {"data": bot_search.hackathon_data}
        return {"data": []}


api.add_resource(HelloWorld, "/get/<string:contest>")

if __name__ == '__main__':
    app.run(debug=True)