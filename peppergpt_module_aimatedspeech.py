# -*- coding: utf-8 -*-

###########################################################
# This module receives results from the speechrecognition module and prints to console
#
# Syntax:
#    python scriptname --pip <ip> --pport <port>
#
#    --pip <ip>: specify the ip of your robot (without specification it will use the NAO_IP defined below
#
# Author: Johannes Bramauer, Vienna University of Technology
# Created: May 30, 2018
# License: MIT
###########################################################

# NAO_PORT = 65445 # Virtual Machine
NAO_PORT = 9559 # Robot


# NAO_IP = "127.0.0.1" # Virtual Machine
NAO_IP = "nao.local" # Pepper default

import os
from optparse import OptionParser
import naoqi
import time
import sys
from naoqi import ALProxy

from chatgpt import Conversation


class BaseSpeechReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName )
            self.BIND_PYTHON( self.getName(),"callback" )
            self.strNaoIp = strNaoIp

        except BaseException, err:
            print( "ERR: ReceiverModule: loading error: %s" % str(err) )

    # __init__ - end
    def __del__( self ):
        print( "INF: ReceiverModule.__del__: cleaning everything" )
        self.stop()

    def start( self ):

        #Test
        #self.testMotionProxy = ALProxy("ALAnimationPlayer", self.strNaoIp, NAO_PORT)

        #set speech to text mode
        self.sttProxy = ALProxy("SpeechRecognition")
        self.sttProxy.start()
        self.sttProxy.setHoldTime(2.5)
        self.sttProxy.setIdleReleaseTime(1.0)
        self.sttProxy.setMaxRecordingDuration(10)
        self.sttProxy.setLookaheadDuration(0.5)
        self.sttProxy.setLanguage("de-de")
        self.sttProxy.calibrate()
        self.sttProxy.setAutoDetectionThreshold(5)
        self.sttProxy.enableAutoDetection()

        # set the speech mode 
        speak_move_service = ALProxy("ALSpeakingMovement", self.strNaoIp, NAO_PORT)
        speak_move_service.setMode("contextual")

        # set the listening mode
        listen_move_service = ALProxy("ALListeningMovement", self.strNaoIp, NAO_PORT)
        listen_move_service.setEnabled(False)

        # Disable AL speech recognition function
        #listen_service = ALProxy("ALSpeechRecognition", self.strNaoIp, NAO_PORT)
        #listen_service.pause(True)
        #listen_service.removeAllContext()
        #listen_service = ALProxy("ALDialog", self.strNaoIp, NAO_PORT)
        #listen_service.setConfidenceThreshold('BNF', 1, "English")
        
        memory = naoqi.ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        memory.subscribeToEvent("SpeechRecognition", self.getName(), "speechRecognized")
        memory.subscribeToEvent("ALAnimatedSpeech/EndOfAnimatedSpeech", self.getName(), "sayFinished")
        self.converstion = Conversation(os.getenv("CHATGPT_API"), "gpt-3.5-turbo", "Du bist jetzt ein autonomer sozialer Roboter names Pepper "
                                        "und antwortest bei allen Fragen als solcher und bleibst deiner Rolle treu. Fasse deine Antworten möglichst kurz und verwende nie mehr als 50 Wörter. "
                                        "Du kannst Gestiken innerhalb des gesprochenen Texts ausdrücken, indem du ^start(animations/Stand/Gestures/X) verwendest, "
                                        "wobei du folgende Gesten für X einsetzen kannst: "
                                        "Hey_3, Hey_4, Yes_1, Yes_2, Yes_3, No_1, No_2, No_3, Explain_1, Explain_2, Explain_3, Thinking_1, Thinking_3, Thinking_4, "
                                        "Please_1, CalmDown_1, CalmDown_5, Choice_1, Desperate_1, Desperate_2, Desperate_4, Enthusiastic_4, Enthusiastic_5, Excited_1, IDontKnow_1, IDontKnow_2, "
                                        "Me_1, Me_2, Me_4, ShowFloor_1, ShowFloor_3, ShowSky_1, ShowSky_2, YouKnowWhat_1, YouKnowWhat_2, You_1, You_4, Give_3, Give_4 "
                                        "Hysterical_1, Peaceful_1, BowShort_1, But_1, Bored_1, Far_1, Far_2, Nothing_2. "
                                        "^start darf nie am Schluss nach dem gesprochenen Text der Nachricht verwendet werden, "
                                        "falls eine Animation am Schluss kommt, verwende ^run statt ^start. "
                                        "Gib am Ende der Nachricht ^wait(animations/Stand/Gestures/X) ein, aber nur wenn du vorher ^start(animations/Stand/Gestures/X) verwendet hast. "
                                        "Achtung: X muss immer gleich sein für ^start und ^wait! "
                                        "mit ^start startest du eine Animation, mit ^wait am Schluss des Satzes bringst du sie zu Ende. "
                                        "Benutze 1) allgemein möglichst viele verschiedenen Gestiken. "
                                        "Beispiel1: ^start(animations/Stand/Gestures/Hey_1) Ich bin Pepper, mir geht es gut, und dir? ^wait(animations/Stand/Gestures/Hey_1) "
                                        "Beispiel2: ^start(animations/Stand/Gestures/Thinking_1) Hmm, ich bin mir ehrlich gesagt nicht sicher. ^wait(animations/Stand/Gestures/Thinking_1")
        self.ttsProxy = naoqi.ALProxy("ALAnimatedSpeech", self.strNaoIp, NAO_PORT)
        print( "INF: ReceiverModule: started!" )


    def stop( self ):
        print( "INF: ReceiverModule: stopping..." )
        memory = naoqi.ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        memory.unsubscribe(self.getName())

        print( "INF: ReceiverModule: stopped!" )

    def version( self ):
        return "1.1"

    def sayFinished(self, signalName, finished, id):
        if finished:
            self.sttProxy.enableAutoDetection()
    
    def speechRecognized(self, signalName, message):
        print("STT: %s" % message)
        response = self.converstion.send(message)
        print("ChatGPT: %s" % response)
        self.sttProxy.disableAutoDetection()
        self.ttsProxy.say(response.encode("utf-8"), "contextual")

        #Test 
        #self.testMotionProxy.run("animations/Stand/Gestures/ShowSky_1")
        #self.ttsProxy.say("Hallo, ^start(animations/Stand/Gestures/ShowSky_1) Mein Name ist Pepper, wie geht es dir? ^wait(animations/Stand/Gestures/Me_1)")

def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=NAO_PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    try:
        p = ALProxy("BaseSpeechReceiverModule")
        p.exit()  # kill previous instance
    except:
        pass
    # Reinstantiate module

    # Warning: ReceiverModule must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global BaseSpeechReceiverModule
    BaseSpeechReceiverModule = BaseSpeechReceiverModule("BaseSpeechReceiverModule", pip)
    BaseSpeechReceiverModule.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()