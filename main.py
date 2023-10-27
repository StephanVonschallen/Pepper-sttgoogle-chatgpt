import os, sys, time

import ConfigParser

_stdin_encoding = sys.stdin.encoding or 'utf-8'

required_settings = ["CHATGPT_API", "PYTHONPATH"]
config = ConfigParser.ConfigParser()

if os.path.isfile("config.cfg"):
    config.read('config.cfg')

for setting in required_settings:
    if not os.getenv(setting):
        if config.get("ENV", setting):
            os.environ[setting] = config.get("ENV", setting)
        else:
            os.environ[setting] = raw_input("%s: " % setting).decode(_stdin_encoding)

python_path = os.path.join(os.getcwd(), os.getenv("PYTHONPATH"))
if python_path not in sys.path:
    sys.path.append(python_path)

import naoqi
import qi

import chatgpt

IP = "localhost"
PORT = 59694

logger = qi.logging.Logger("main")

if __name__ == "__main__":
    ttsProxy = naoqi.ALProxy("ALTextToSpeech", IP, PORT)
    conversation = chatgpt.Conversation(os.getenv("CHATGPT_API"), "gpt-3.5-turbo", "You are a helpful real robot named Pepper.")
    try: 
        while True:
            try:
                message = raw_input("User: ").decode(_stdin_encoding)
            except EOFError as e:
                break
            except KeyboardInterrupt:
                break
            response = conversation.send(message)
            print("Pepper: %s" % response.encode(_stdin_encoding))
            ttsProxy.say(response.encode("utf-8"))
    except KeyboardInterrupt:
        print("^C")
    sys.exit(0)