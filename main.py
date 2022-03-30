import random
import time
import json

from image_url import IMAGE_URL_LIST

WORD_LIST = ["Fly", "Sky", "Blue", "Green", "Sun", "Moon", "X", "Launch"]
STATUS_LIST = ["success", "fail"]



def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y/%m/%d', prop)

data = []
sql_cmd = "INSERT ALL\n"

for i in range(50):
    name = f"{random.choice(WORD_LIST)} {random.choice(WORD_LIST)} {random.randint(1, 10)}"
    date = str(random_date("2000/04/14", "2020/05/17", random.random()))
    status = random.choice(STATUS_LIST)
    image_url = random.choice(IMAGE_URL_LIST)
    obj = {"NAME": name, "DATE": date, "STATUS": status, "IMAGE_URL": image_url}
    data.append(obj)

for obj in data:
    name = obj["NAME"]
    date = obj["DATE"]
    status = obj["STATUS"]
    image_url = obj["IMAGE_URL"]
    cmd = f"\tINTO LAUNCH(NAME, STATUS, LAUNCH_DATE, IMAGE_URL) VALUES ('{name}', '{status}', TO_DATE('{date}', 'YYYY/MM/DD'), '{image_url}')\n"
    sql_cmd += cmd

sql_cmd += "SELECT * FROM dual;"

with open("./sql_script.txt", "w") as file:
    file.write(sql_cmd)