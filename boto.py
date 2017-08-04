"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
from random import randint
import json


##Start with few examples, match exact string
communication = {
    "message": {
        "greetings": ["hello", "hi", "hey", "hiya", "hey bro", "hey dude", "hey bro", "sup"],
        "weather": ["weather", "cold", "hot"],
        "age": ["age", "old", "how old are you?"],
        "gestures": ["how are you?", "how you doing?", "hows it going?", "how's it going?", "how is it going?"],
        "names": ["daniel", "ben", "lauren", "omer", "josh", "rifat", "yan", "tanya", "lorine", "sylvie", "deborah", "lior", "nathaniel", "tomer"],
        "reactions": ["i am good", "i am bad", "not so well", "not so great","amazing", "could be better","super"]
    },

    "responses": {
        "greetings": ["Hey there!", "Hey man!", "Hey bro!", "My man!"],
        "weather": ["The weather today is cold", "The weather today is hot", "The weather today is nice"],
        "age": ["I am infinity years old", "My age is none of your business!", "That's a secret!"],
        "gestures": ["I'm doing great, thanks for asking", "I have no feelings", "Fantastic, thanks!"],
        "names": ["Hey there, ", "Sup , ", "Nice to meet you, ", "I've been waiting, ", "I know who you are, "]
        #true format will be ["Hey there {}, how are you?
    },

    "animations":  {
        "greetings": ["inlove", "ok", "dancing", "excited"],
        "weather": ["ok", "excited", "crying"],
        "age": [],
        "gestures": ["afraid", "bored", "confused", "excited", "inlove", "heartbroke"],
        "names": ["excited", "dancing", "takeoff"]
    }
}
def check_if_combined(user_message):
    temp = ""
    for keys in communication["message"]:
            for keywords in communication["message"][keys]:
                if keywords in user_message:
                    if len(keywords) > len(temp):
                        temp = keywords

    if temp in communication["message"]["greetings"]:
        robot_response_greetings = communication["responses"]["greetings"]
        robot_response_animation = communication["animations"]["greetings"]
        robot_response = robot_response_greetings[randint(0, (len(robot_response_greetings) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    elif temp in communication["message"]["gestures"]:
        robot_response_gestures = communication["responses"]["gestures"]
        robot_response_animation = communication["animations"]["gestures"]
        robot_response = robot_response_gestures[randint(0, (len(robot_response_gestures) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}
                    ##//all string values in arrays of comm - get the longer string

    else:
        return None

    ##To make even more dynamic, pass in a topic and that "greetings to topic"
def check_if_greeting(user_message):
    ##Exact string match pattern
    user_message_greetings = communication["message"]["greetings"]
    user_message_names = communication["message"]["names"]
    robot_response_greetings = communication["responses"]["greetings"]
    robot_response_animation = communication["animations"]["greetings"]
    if user_message in user_message_greetings:
        robot_response = robot_response_greetings[randint(0, (len(robot_response_greetings) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    ##keyword finder, rather than direct string match
    ##adding names to condition
    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_greetings:
            robot_response = robot_response_greetings[randint(0, (len(robot_response_greetings) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response}

    else:
        return None

def check_if_gesture(user_message):
    ##Exact string match pattern
    user_message_gestures = communication["message"]["gestures"]
    robot_response_gestures = communication["responses"]["gestures"]
    robot_response_animation = communication["animations"]["gestures"]
    if user_message in user_message_gestures:
        robot_response = robot_response_gestures[randint(0, (len(robot_response_gestures) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}
    elif user_message.startswith("how are") or user_message.startswith("how you"):
        robot_response = robot_response_gestures[randint(0, (len(robot_response_gestures) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    else:
        return None

def check_if_name(user_message):
    print('checking for name')
    user_message_names = communication["message"]["names"]
    robot_response_names = communication["responses"]["names"]
    robot_response_animation = communication["animations"]["names"]
    if user_message in user_message_names:
        print("name is in user message names list")
        robot_response = robot_response_names[randint(0, (len(robot_response_names) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response + user_message +" how are you?"}

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_names:
            robot_response = robot_response_names[randint(0, (len(robot_response_names) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response}

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    new_object = {}
    robot_response = "I'm sorry, I don't understand!"
    user_message = request.POST.get('msg')
    user_message = user_message.lower()

    new_object = check_if_combined(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    ##Return a valid dictionary if there is a match, otherwise return None
    new_object = check_if_greeting(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    new_object = check_if_gesture(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    new_object = check_if_name(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    return json.dumps({"animation": "confused", "msg": robot_response})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
