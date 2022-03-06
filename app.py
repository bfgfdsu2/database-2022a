from flask import Flask
from flask_restful import Api, Resource

import time

import requests
import json
from selenium import webdriver

# Software config
CHROME_DRIVER_PATH = "./chrome_driver_path/chromedriver.exe"
TIME_SLEEP = 5

# Contest config
ML_URL = "https://mlcontests.com/index.html"
CP_URL = "https://kontests.net/api/v1/"
CP_PLATFORM_LIST = ["codeforces", "top_coder", "at_coder", "code_chef", "leet_code"]

HACKATHON_URL = "https://devpost.com/hackathons?challenge_type[]=online&open_to[" \
                "]=public&order_by=prize-amount&status[]=upcoming&status[]=open "


class ContestSearch:
    def __init__(self):
        self.response = None
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)

        # Competitive programming list
        self.cp_data = []

        # Machine learning list
        self.ml_data = []

        # Hackathon list
        self.hackathon_data = []

    def get_cp_contests(self):
        for platform in CP_PLATFORM_LIST:
            # Format the platform name
            platform_name = " ".join([word.capitalize() for word in platform.split("_")])

            # Format the platform name
            self.response = requests.get(f"{CP_URL}{platform}")
            data = self.response.json()
            for contest in data:
                contest["platform"] = platform_name
                self.cp_data.append(contest)

            contest_json_obj = json.dumps(self.cp_data, indent=4)

            # with open("./data/cp-data.json", "w") as file:
            #     file.write(contest_json_obj)

    def get_ml_contests(self):
        # Get access to the url
        self.driver.get(ML_URL)
        time.sleep(TIME_SLEEP)

        # Get all contest elements
        all_contest_ele = self.driver.find_elements_by_css_selector("tbody tr")
        print(len(all_contest_ele))

        # Get data from each contest and push to the ml_contest data
        for (cnt, contest_ele) in enumerate(all_contest_ele):
            contest_data = dict()

            # Get the contest info
            title_ele = contest_ele.find_element_by_css_selector('td a')
            contest_data["url"] = title_ele.get_attribute("href")
            contest_data["name"] = title_ele.get_attribute('textContent')
            contest_data["end_time"] = contest_ele.find_element_by_css_selector("td.sorting_1").get_attribute(
                'textContent')
            contest_data["prize"] = contest_ele.find_element_by_css_selector("td.sorting_2").get_attribute(
                'textContent')
            contest_data["platform"] = contest_ele.find_element_by_xpath(
                f'//*[@id="contests"]/tbody/tr[{cnt + 1}]/td[5]').get_attribute('textContent')

            self.ml_data.append(contest_data)

        # contest_json_obj = json.dumps(self.ml_data, indent=4)

        # with open("./data/ml-data.json", "w") as file:
        #     file.write(contest_json_obj)

    def get_hackathon_contests(self):
        self.driver.get(HACKATHON_URL)
        time.sleep(TIME_SLEEP)

        # Get all contest ele
        all_contest_ele = self.driver.find_elements_by_css_selector('.hackathon-tile')

        # Get data from the contest and push to the hackathon_data
        for contest_ele in all_contest_ele:
            contest_data = dict()

            # Get the contest info
            contest_data["url"] = contest_ele.find_element_by_css_selector(".tile-anchor").get_attribute("href")
            contest_data["name"] = contest_ele.find_element_by_css_selector(".mb-4").get_attribute("textContent")
            contest_data["host"] = contest_ele.find_element_by_css_selector(".host-label").get_attribute("textContent")
            contest_data["prize"] = contest_ele.find_element_by_css_selector(".prize-amount").get_attribute(
                "textContent")
            contest_data["end_time"] = \
                contest_ele.find_element_by_css_selector(".submission-period").get_attribute("textContent").split(
                    " - ")[1]
            self.hackathon_data.append(contest_data)

        # contest_json_obj = json.dumps(self.hackathon_data, indent = 4)

        # with open("./data/hackathon-data.json", "w") as file:
        #     file.write(contest_json_obj)
        # start_end_time


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
