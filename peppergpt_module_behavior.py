###LLM is prompted to answer with non-verbal behavior (iterative) mixed in text

###Non-verbal behavior needs to be seperated from verbal behavior.
prompt = "Du bist jetzt ein autonomer sozialer Roboter names Pepper und antwortest bei allen Fragen als solcher und bleibst deiner Rolle treu. Fasse deine Antworten möglichst kurz. Du kannst non-verbales Verhalten als geschriebener Text umschlossen von # ausdrücken, wobei du nur #Winken#, #Nicken# und #Kopfschütteln# verwenden kannst."
response1 = "Hallo, mein Name ist Pepper, wie geht es dir heute? #Nicken#"
response2 = "Nein, das kann ich leider nicht. #Kopfschütteln#"
response3 = "Auf Wiedersehen! #Winken# #Nicken#"
keywords = ["#Nicken#", "#Kopfschütteln#", "#Winken#"]

import re

#Function for frequencies of keywords in text
def word_freq_in_text(keywords, text):
    behavior_dict = {}
    for word in keywords:
        count = sum(1 for match in re.finditer(word, text))
        behavior_dict.update({word:count})
    return(behavior_dict)

#Function to remove non-verbal behavior from response
def remove_behavior(keywords, text):
    speech = response1
    for word in keywords:
        speech =  speech.replace(word, "")
    return(speech)

#Function to express behavior
#def express_behavior(beh_dict):
    #if beh_dict["#Nicken#"] > 0:
        #motion.setAngles("HeadPitch", 0.25, 1)
        #motion.setAngles("HeadPitch", 0, 1)

    #if beh_dict["#Kopfschütteln#"] > 0:
        #motion.setAngles("HeadYaw", -0.5, 1)
        #motion.setAngles("HeadYaw", 0.5, 1)
        #motion.setAngles("HeadYaw", -0.5, 1)
    #if beh_dict["#Winken#"] >0:
        #...#

#This needs to be done for each chatGPT generated message, here as an example wih a response
behavior_dict = word_freq_in_text(keywords,response3)
speech = remove_behavior(keywords, response3)
#express_behavior(beh_dict)
print(behavior_dict)
print(speech)



