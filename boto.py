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
        "weather": ["weather", "cold", "hot", "warm", "chilly", "freezing"],
        "age": ["age", "old", "how old are you?"],
        "gestures": ["how are you?", "how you doing?", "hows it going?", "how's it going?", "how is it going?"],
        "names": ["daniel", "ben", "lauren", "omer", "josh", "rifat", "yan", "tanya", "lorine", "sylvie", "deborah", "lior", "nathaniel", "tomer"],
        "reactions": ["good", "bad", "great", "sad", "mad", "upset", "happy", "excited",
                      "i am good", "i am bad", "not so well", "not so great", "amazing",
                      "could be better", "super", "great", "fantastic"],
        "locations": ["usa", "us", "united states", "america", "new york", "miami", "las vegas", "boston,"
                      "france", "tel aviv", "israel", "india", "switzerland", "seattle", "london", "england"],
        "curses": ["shit", "bitch", "fuck", "asshole", "crap", "bullshit"]
    },

    "responses": {
        "greetings": ["Hey there!", "Hey man!", "Hey bro!", "My man!"],
        "weather": ["The weather today is cold", "The weather today is hot", "The weather today is nice"],
        "age": ["I am infinity years old", "My age is none of your business!", "That's a secret!"],
        "gestures": ["I'm doing great, thanks for asking, and yourself?", "I have no feelings, how about you?",
                     "Fantastic, thanks! How about you?"],
        "names": ["Hey there, {} , whats up? ", "Sup {}, how are you?", "Nice to meet you {}, how's it going?",
                  "I've been waiting for you {}, how are you?", "I know who you are, {}, how are you feeling?"],
        "reactions": ["Good to hear about your day, would you like to know about the weather?(Hint: type 'weather')",
                     "I understand, a joke can always help regardless of your mood, type 'joke'",
                      "I hear you, perhaps you can try some activities like "
                      "sports, reading, shopping, or programming in your local area",
                      "Good to hear about your status, where are you from?"],
        "locations": ["Cool, I have a cousin that lives there", "No way! What an awesome place",
                      "Wow! I hope to travel there one day!" , "You are a very lucky person, that's an amazing place"],
        "curses": ["Sorry but cursing of any form is not tolerated, please try again"],
        "jokes": ["Q: Why couldn't the blonde add 10 and seven on a calculator?/n A: She couldn't find the 10 key.",
                  "How is a computer like an air conditioner? When you open Windows it won't work!",
                  "Guy 1: Hey! Why do you smoke cigarettes even"
                  "though there is a warning on the pack that says it's bad for your health?" 
                  "Guy 2: I am a software professional.  I don't bother about warnings -- I am concerned only about the Alerts. ",
                  "Q: What's the difference between a woman and a computer?"
                  "A: Woman doesn't accept 3 1/2 inch floppies."],
        "weather": ["It's a really nice day out! Go have fun!", "The weather today is pretty warm",
                    "It's really cold today, stay inside and talk with me", "It is extremely hot outside, you should hit the beach",
                    "It's like a desert out there, don't forget to drink water!"]

    },

    "animations":  {
        "greetings": ["inlove", "ok", "dancing", "excited"],
        "weather": ["ok", "excited", "crying"],
        "age": [],
        "gestures": ["afraid", "bored", "confused", "excited", "inlove", "heartbroke"],
        "names": ["excited", "dancing", "takeoff"],
        "reactions": ["excited", "money", "dancing", "dog", "giggling", "waiting"],
        "locations": ["takeoff", "excited", "money", "dancing"],
        "curses": ["afraid", "no", "crying"],
        "jokes": ["laughing", "giggling", "excited", "dancing"],
        "weather": ["dancing", "excited",]
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

def check_if_curse(user_message):
    user_message_curses = communication["message"]["curses"]
    robot_response_curses = communication["responses"]["curses"]
    robot_response_animation = communication["animations"]["curses"]

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_curses:
            robot_response = robot_response_curses[randint(0, (len(robot_response_curses) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response}

    else:
        return None

def check_if_joke(user_message):
    if "joke" in user_message:
        robot_response_jokes = communication["responses"]["jokes"]
        robot_response_animation = communication["animations"]["jokes"]
        robot_response = robot_response_jokes[randint(0, (len(robot_response_jokes) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

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

def check_if_reaction(user_message):
    user_message_reactions = communication["message"]["reactions"]
    robot_response_reactions = communication["responses"]["reactions"]
    robot_response_animation = communication["animations"]["reactions"]
    if user_message in user_message_reactions:
        robot_response = robot_response_reactions[randint(0, (len(robot_response_reactions) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_reactions:
            robot_response = robot_response_reactions[randint(0, (len(robot_response_reactions) - 1))]
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
        return {"animation": robot_animation, "msg": robot_response.format(user_message)}

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_names:
            robot_response = robot_response_names[randint(0, (len(robot_response_names) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response.format(word)}

def check_if_location(user_message):
    user_message_locations = communication["message"]["locations"]
    robot_response_locations = communication["responses"]["locations"]
    robot_response_animation = communication["animations"]["locations"]
    if user_message in user_message_locations:
        robot_response = robot_response_locations[randint(0, (len(robot_response_locations) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_locations:
            robot_response = robot_response_locations[randint(0, (len(robot_response_locations) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response.format(word)}

def check_if_weather(user_message):
    user_message_weather = communication["message"]["weather"]
    robot_response_weather = communication["responses"]["weather"]
    robot_response_animation = communication["animations"]["reactions"]
    if user_message in user_message_weather:
        robot_response = robot_response_weather[randint(0, (len(robot_response_weather) - 1))]
        robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
        return {"animation": robot_animation, "msg": robot_response}

    user_message_list = user_message.split()
    for word in user_message_list:
        if word in user_message_weather:
            robot_response = robot_response_weather[randint(0, (len(robot_response_weather) - 1))]
            robot_animation = robot_response_animation[randint(0, (len(robot_response_animation) - 1))]
            return {"animation": robot_animation, "msg": robot_response}

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    new_object = {}
    robot_response = "I'm sorry, I don't understand!, Try asking about me, the weather, or a joke"
    user_message = request.POST.get('msg')
    user_message = user_message.lower()

    new_object = check_if_curse(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

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

    new_object = check_if_reaction(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    new_object = check_if_location(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    new_object = check_if_joke(user_message)
    if new_object is not None:
        robot_response = new_object["msg"]
        robot_animation = new_object["animation"]
        return json.dumps({"animation": robot_animation, "msg": robot_response})

    new_object = check_if_weather(user_message)
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
