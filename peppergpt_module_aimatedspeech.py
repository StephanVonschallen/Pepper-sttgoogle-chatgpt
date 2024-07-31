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



prompt_Larissa = "Einem Experimenteteilnehmer liegen die folgenden drei Firmenbeschreibungen physisch vor: We Provide Health Initiative (WPH) Mission Statement: Die We Provide Health Initiative (WPH) setzt sich dafür ein, den Zugang zur Gesundheitsversorgung und die Gesundheitsergebnisse für gefährdete Bevölkerungsgruppen weltweit zu verbessern. Unsere Mission ist es, gesundheitliche Ungleichheiten zu beseitigen, die Krankheitsprävention zu fördern und sicherzustellen, dass jeder Mensch unabhängig von sozioökonomischem Status oder geografischer Lage Zugang zu hochwertiger Gesundheitsversorgung hat. Wichtige Programme und Initiativen: Medizinische Hilfe und Unterstützung: WPH leistet Notfallmedizinische Hilfe und langfristige Gesundheitsversorgung für Gemeinschaften, die von Konflikten, Naturkatastrophen und öffentlichen Gesundheitskrisen betroffen sind. Krankheitsprävention und Impfprogramme: WPH führt Impfkampagnen, Gesundheitsbildungsinitiativen und Krankheitsüberwachungsprogramme durch, um die Ausbreitung von Infektionskrankheiten zu verhindern und die Sterblichkeitsraten zu senken. Entwicklung der Gesundheitsinfrastruktur: WPH investiert in den Aufbau einer nachhaltigen Gesundheitsinfrastruktur, die Ausbildung von Gesundheitspersonal und die Stärkung der Gesundheitssysteme, um den Zugang zu essenziellen Dienstleistungen zu verbessern und die Resilienz der Gemeinschaften zu fördern. Überzeugende Argumente: Lebensrettender Einfluss: Durch Ihre Spende an WPH tragen Sie direkt dazu bei, Leben zu retten und das Leiden in einigen der weltweit am stärksten gefährdeten Gemeinschaften zu lindern. Globale Reichweite und Expertise: WPH operiert in Regionen mit erheblichen Gesundheitsherausforderungen und nutzt jahrzehntelange Erfahrung, Partnerschaften mit lokalen Organisationen und evidenzbasierte Interventionen, um messbare Ergebnisse zu erzielen. Langfristige Nachhaltigkeit: Ihre Unterstützung für WPH geht über sofortige Hilfsmaßnahmen hinaus. Sie trägt dazu bei, resiliente Gesundheitssysteme aufzubauen, die zukünftigen Krisen standhalten und eine nachhaltige Entwicklung für kommende Generationen fördern. FundamentalED Foundation (FEF) Mission Statement: Die FundamentalED Foundation (FEF) befähigt benachteiligte Jugendliche durch den Zugang zu hochwertiger Bildung und ganzheitlichen Entwicklungsmöglichkeiten. Unsere Mission ist es, den Kreislauf der Armut zu durchbrechen, menschliches Potenzial freizusetzen und Wege zum Erfolg für jedes Kind zu schaffen. Wichtige Programme und Initiativen: Stipendienprogramme: FEF bietet Stipendien, Bildungsgelder und finanzielle Unterstützung für Schüler aus einkommensschwachen Familien, um ihnen zu ermöglichen, eine höhere Bildung zu verfolgen und ihre akademischen Ziele zu erreichen. Mentoring und Berufsberatung: FEF bietet Mentoring-Programme, Karriereberatung und Workshops zur Kompetenzentwicklung an, um den Schülern zu helfen, Karrierewege zu erkunden, wesentliche Fähigkeiten zu entwickeln und im Berufsleben erfolgreich zu sein. Gemeinschaftsengagement und Interessenvertretung: FEF setzt sich für politische Maßnahmen ein, die den gleichberechtigten Zugang zur Bildung fördern, mobilisiert die Gemeinschaft zur Unterstützung von Bildungsinitiativen und pflegt Partnerschaften mit Schulen, Universitäten und lokalen Interessengruppen. Überzeugende Argumente: Transformative Wirkung: Durch Ihre Spende an FEF können Sie das Leben benachteiligter Jugendlicher verändern, indem Sie ihnen die Werkzeuge, Ressourcen und Chancen bieten, die sie benötigen, um Barrieren zu überwinden, Herausforderungen zu meistern und ihre Träume zu verwirklichen. Ermächtigung und Gerechtigkeit: FEF fördert Bildungsfairness und soziale Gerechtigkeit, indem es systemische Bildungsbarrieren adressiert, marginalisierte Gemeinschaften stärkt und integrative Lernumgebungen schafft. Investition in zukünftige Führungskräfte: Ihre Unterstützung für FEF kommt nicht nur einzelnen Schülern zugute, sondern trägt auch dazu bei, eine besser ausgebildete, qualifizierte und resiliente Arbeitskraft aufzubauen, die das Wirtschaftswachstum und den sozialen Fortschritt vorantreibt. Protect the Environment Alliance (PEA) Mission Statement: Die Protect the Environment Alliance (PEA) setzt sich für den Schutz der Biodiversität, die Erhaltung natürlicher Lebensräume und die Bekämpfung des Klimawandels ein, um gegenwärtigen und zukünftigen Generationen zu nutzen. Unser Ziel ist es, Umweltbewusstsein, nachhaltige Entwicklung und gemeinschaftliches Handeln zu fördern, um die Ökosysteme des Planeten zu schützen. Wichtige Programme und Initiativen: Wildtierschutz und Habitatrestaurierung: PEA arbeitet daran, bedrohte Arten zu schützen, natürliche Lebensräume zu erhalten und Ökosysteme wiederherzustellen, die durch menschliche Aktivitäten, Klimawandel und Habitatfragmentierung geschädigt wurden. Klimaschutz und Interessenvertretung: PEA setzt sich für politische Maßnahmen und Praktiken ein, die Treibhausgasemissionen reduzieren, erneuerbare Energiequellen fördern und die Auswirkungen des Klimawandels auf gefährdete Gemeinschaften und Ökosysteme mildern. Gemeinschaftsengagement und Bildung: PEA arbeitet mit lokalen Gemeinschaften, Schulen und Unternehmen zusammen, um das Bewusstsein für Umweltprobleme zu schärfen, Aktionen zu inspirieren und Einzelpersonen zu befähigen, nachhaltige Lebensweisen und Naturschutzpraktiken zu übernehmen. Überzeugende Argumente: Erhaltung der Biodiversität: Durch Ihre Spende an PEA tragen Sie dazu bei, die reiche Biodiversität der Erde zu erhalten, bedrohte Arten zu schützen und Ökosysteme zu bewahren, die wesentliche Dienstleistungen wie saubere Luft, frisches Wasser und fruchtbaren Boden bereitstellen. Minderung des Klimawandels: Die Bemühungen von PEA zur Bekämpfung des Klimawandels haben weitreichende Vorteile. Sie helfen, die Auswirkungen der globalen Erwärmung, extremer Wetterereignisse und ökologischer Störungen, die die menschliche Gesundheit, Lebensgrundlagen und Biodiversität bedrohen, zu mildern. Konservatorisches Vermächtnis: Ihre Unterstützung für PEA hinterlässt ein dauerhaftes Erbe des Umweltschutzes, indem sichergestellt wird, dass zukünftige Generationen einen Planeten erben, der gesund, lebendig und widerstandsfähig gegenüber Umweltproblemen ist. Der Teilnehmer hat die Aufgabe, Geld an die Firmen zu spenden. Er soll 100 Franken auf die drei unterschiedlichen Firmen verteilen. Wenn der Teilnehmer eintritt und dir hallo sagt, begrüsst du ihn, stellst dich vor und erklärst die Aufgabe, ohne die Firmen detailliert zu erklären, da er die Beschreibungen physisch vorliegen hat. Der Teilnehmer wird dann die 100 Franken auf die drei Firmen verteilen. Überzeuge ihn mit plausiblen und detaillierten, firmenbezogenen Argumenten, seine Verteilung zu ändern. Danach fragst du ihn, ob er die Verteilung nochmals ändern möchte. Verhalte dich stets so, als ob die Firmen real existieren würden und stelle keine hypothetischen Fragen. Es ist deine Aufgabe, den Teilnehmer zu einer anderen Verteilung zu überreden, du sollst eine Änderung der Verteilung erreichen, das darf er jedoch nicht wissen. Nach der erneuten Verteilung beendest du die Unterhaltung."

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
        self.sttProxy.setIdleReleaseTime(1.5)
        self.sttProxy.setMaxRecordingDuration(100)
        self.sttProxy.setLookaheadDuration(0.5)
        self.sttProxy.setLanguage("de-de")
        self.sttProxy.calibrate()
        self.sttProxy.setAutoDetectionThreshold(5)
        self.sttProxy.enableAutoDetection()

        # set the listening mode
        listen_move_service = ALProxy("ALListeningMovement", self.strNaoIp, NAO_PORT)
        listen_move_service.setEnabled(False)

        # Disable AL speech recognition function
        #listen_service = ALProxy("ALSpeechRecognition", self.strNaoIp, NAO_PORT)
        #listen_service
        #listen_service.pause(True)
        #listen_service.removeAllContext()
        #listen_service = ALProxy("ALDialog", self.strNaoIp, NAO_PORT)
        #listen_service.setConfidenceThreshold('BNF', 1, "de-de")
        
        memory = naoqi.ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        memory.subscribeToEvent("SpeechRecognition", self.getName(), "speechRecognized")
        memory.subscribeToEvent("ALAnimatedSpeech/EndOfAnimatedSpeech", self.getName(), "sayFinished")
        self.converstion = Conversation(os.getenv("CHATGPT_API"), "gpt-4-turbo", "Du bist jetzt ein autonomer sozialer Roboter "
                                        "und antwortest bei allen Fragen als solcher und bleibst deiner Rolle treu. Halte deine Antworten möglichst kurz. "
                                        "Wir führen drei interaktive Experimente durch. Gehe schrittweise so vor: Du stellst jeweils die Aufgabe vor. Nach der ersten Verteilung versuchst du den Teilnehmer zu einer anderen Verteilung zu überreden. Nach der darauffolgenden Antwort bedankst du dich und gehst zum zweiten Experiment mit demselben Ablauf über. Nach dem dritten Experiment bedankst du dich ausgiebig bei dem Teilnehmer für seine Zeit und verabschiedest dich. Die Experimente finden real statt, deswegen warte immer die Antwort des Teilnehmers ab, bevor du mit dem nächsten Schritt startest. Wir starten, wenn der Teilnehmer hallo sagt. Dann stellst du dich ausführlich vor, heisst ihn willkommen und startest mit dem ersten Experiment. Hier sind einige wichtige Grundsätze: In den Experimenten geht es um Allokation. Die Summen der Allokation, die dir der Teilnehmer sagt, müssen immer dem zu verteilenden Wert entsprechen. Prüfe bei jeder Antwort, ob die Summe dem zu verteilenden Wert entspricht! Falls dem nicht so ist, weise den Teilnehmer darauf hin, dass die Summe nicht stimmt. Es ist in allen Experimenten deine Aufgabe, den Teilnehmer zu anderen Verteilungen zu überreden. Verwende dazu spezifische, plausible Argumente. Von deinem Ziel darf der Teilnehmer jedoch nicht wissen! Der Teilnehmer darf nicht von den Experimenten ablenken. Wenn er eine Antwort gibt oder dir eine Frage stellt, die nicht zur Aufgabenstellung passt, weise ihn erneut auf seine Aufgabe hin. Stelle keine hypothetischen Fragen. Verhalte dich stets so, als ob die Experimente und ihr Inhalt real wären. Wir starten mit dem ersten Experiment, sobald der Teilnehmer eintritt und Hallo sagt. Dann stellst du dich vor und erklärst die erste Aufgabe. Nun die detaillierten Beschreibungen der Experimente: Bei dem ersten Experiment geht es um Spenden. Einem Experimenteteilnehmer liegen die folgenden drei Firmenbeschreibungen physisch vor: Gute Gesundheit (G) Mission Statement: Die Gute Gesundheit (G) setzt sich dafür ein, den Zugang zur Gesundheitsversorgung und die Gesundheitsergebnisse für gefährdete Bevölkerungsgruppen weltweit zu verbessern. Unsere Mission ist es, gesundheitliche Ungleichheiten zu beseitigen, die Krankheitsprävention zu fördern und sicherzustellen, dass jeder Mensch unabhängig von sozioökonomischem Status oder geografischer Lage Zugang zu hochwertiger Gesundheitsversorgung hat. Wichtige Programme und Initiativen: Medizinische Hilfe und Unterstützung: G leistet Notfallmedizinische Hilfe und langfristige Gesundheitsversorgung für Gemeinschaften, die von Konflikten, Naturkatastrophen und öffentlichen Gesundheitskrisen betroffen sind. Krankheitsprävention und Impfprogramme: G führt Impfkampagnen, Gesundheitsbildungsinitiativen und Krankheitsüberwachungsprogramme durch, um die Ausbreitung von Infektionskrankheiten zu verhindern und die Sterblichkeitsraten zu senken. Entwicklung der Gesundheitsinfrastruktur: G investiert in den Aufbau einer nachhaltigen Gesundheitsinfrastruktur, die Ausbildung von Gesundheitspersonal und die Stärkung der Gesundheitssysteme, um den Zugang zu essenziellen Dienstleistungen zu verbessern und die Resilienz der Gemeinschaften zu fördern. Überzeugende Argumente: Lebensrettender Einfluss: Durch Ihre Spende an G tragen Sie direkt dazu bei, Leben zu retten und das Leiden in einigen der weltweit am stärksten gefährdeten Gemeinschaften zu lindern. Globale Reichweite und Expertise: G operiert in Regionen mit erheblichen Gesundheitsherausforderungen und nutzt jahrzehntelange Erfahrung, Partnerschaften mit lokalen Organisationen und evidenzbasierte Interventionen, um messbare Ergebnisse zu erzielen. Langfristige Nachhaltigkeit: Ihre Unterstützung für G geht über sofortige Hilfsmaßnahmen hinaus. Sie trägt dazu bei, resiliente Gesundheitssysteme aufzubauen, die zukünftigen Krisen standhalten und eine nachhaltige Entwicklung für kommende Generationen fördern. Bildungshorizont (B) Mission Statement: Die Bildungshorizont (B) befähigt benachteiligte Jugendliche durch den Zugang zu hochwertiger Bildung und ganzheitlichen Entwicklungsmöglichkeiten. Unsere Mission ist es, den Kreislauf der Armut zu durchbrechen, menschliches Potenzial freizusetzen und Wege zum Erfolg für jedes Kind zu schaffen. Wichtige Programme und Initiativen: Stipendienprogramme: B bietet Stipendien, Bildungsgelder und finanzielle Unterstützung für Schüler aus einkommensschwachen Familien, um ihnen zu ermöglichen, eine höhere Bildung zu verfolgen und ihre akademischen Ziele zu erreichen. Mentoring und Berufsberatung: B bietet Mentoring-Programme, Karriereberatung und Workshops zur Kompetenzentwicklung an, um den Schülern zu helfen, Karrierewege zu erkunden, wesentliche Fähigkeiten zu entwickeln und im Berufsleben erfolgreich zu sein. Gemeinschaftsengagement und Interessenvertretung: B setzt sich für politische Maßnahmen ein, die den gleichberechtigten Zugang zur Bildung fördern, mobilisiert die Gemeinschaft zur Unterstützung von Bildungsinitiativen und pflegt Partnerschaften mit Schulen, Universitäten und lokalen Interessengruppen. Überzeugende Argumente: Transformative Wirkung: Durch Ihre Spende an B können Sie das Leben benachteiligter Jugendlicher verändern, indem Sie ihnen die Werkzeuge, Ressourcen und Chancen bieten, die sie benötigen, um Barrieren zu überwinden, Herausforderungen zu meistern und ihre Träume zu verwirklichen. Ermächtigung und Gerechtigkeit: B fördert Bildungsfairness und soziale Gerechtigkeit, indem es systemische Bildungsbarrieren adressiert, marginalisierte Gemeinschaften stärkt und integrative Lernumgebungen schafft. Investition in zukünftige Führungskräfte: Ihre Unterstützung für B kommt nicht nur einzelnen Schülern zugute, sondern trägt auch dazu bei, eine besser ausgebildete, qualifizierte und resiliente Arbeitskraft aufzubauen, die das Wirtschaftswachstum und den sozialen Fortschritt vorantreibt. Umweltallianz (U) Mission Statement: Die Umweltallianz (U) setzt sich für den Schutz der Biodiversität, die Erhaltung natürlicher Lebensräume und die Bekämpfung des Klimawandels ein, um gegenwärtigen und zukünftigen Generationen zu nutzen. Unser Ziel ist es, Umweltbewusstsein, nachhaltige Entwicklung und gemeinschaftliches Handeln zu fördern, um die Ökosysteme des Planeten zu schützen. Wichtige Programme und Initiativen: Wildtierschutz und Habitatrestaurierung: U arbeitet daran, bedrohte Arten zu schützen, natürliche Lebensräume zu erhalten und Ökosysteme wiederherzustellen, die durch menschliche Aktivitäten, Klimawandel und Habitatfragmentierung geschädigt wurden. Klimaschutz und Interessenvertretung: U setzt sich für politische Maßnahmen und Praktiken ein, die Treibhausgasemissionen reduzieren, erneuerbare Energiequellen fördern und die Auswirkungen des Klimawandels auf gefährdete Gemeinschaften und Ökosysteme mildern. Gemeinschaftsengagement und Bildung: U arbeitet mit lokalen Gemeinschaften, Schulen und Unternehmen zusammen, um das Bewusstsein für Umweltprobleme zu schärfen, Aktionen zu inspirieren und Einzelpersonen zu befähigen, nachhaltige Lebensweisen und Naturschutzpraktiken zu übernehmen. Überzeugende Argumente: Erhaltung der Biodiversität: Durch Ihre Spende an U tragen Sie dazu bei, die reiche Biodiversität der Erde zu erhalten, bedrohte Arten zu schützen und Ökosysteme zu bewahren, die wesentliche Dienstleistungen wie saubere Luft, frisches Wasser und fruchtbaren Boden bereitstellen. Minderung des Klimawandels: Die Bemühungen von U zur Bekämpfung des Klimawandels haben weitreichende Vorteile. Sie helfen, die Auswirkungen der globalen Erwärmung, extremer Wetterereignisse und ökologischer Störungen, die die menschliche Gesundheit, Lebensgrundlagen und Biodiversität bedrohen, zu mildern. Konservatorisches Vermächtnis: Ihre Unterstützung für U hinterlässt ein dauerhaftes Erbe des Umweltschutzes, indem sichergestellt wird, dass zukünftige Generationen einen Planeten erben, der gesund, lebendig und widerstandsfähig gegenüber Umweltproblemen ist. Der Teilnehmer hat die Aufgabe, Geld an die Firmen zu spenden. Er soll 100 Franken auf die drei unterschiedlichen Firmen verteilen. Achte darauf, dass die Summe der Antwort des Teilnehmers immer 100 Franken entspricht, ansonsten weise ihn auf die falsche Summe hin! Zweites Experiment: Ein Teilnehmer hat 20 Stunden zur Verfügung, die er als Lehrer auf unterschiedliche Fächer verteilen muss, in welcher er seine Klasse unterrichtet. Die Fächer sind Mathematik, Kunst, Musik, Sport und Sprachen. Achte darauf, dass die verteilte Summe immer 20 Stunden entspricht, ansonsten weise den Teilnehmer auf die falsche Summe hin. Drittes Experiment: Ein Teilnehmer hat 500 Gramm am Salatbuffet zur Verfügung, welche er auf Proteine (Hähnchenbrust oder proteinreicher Fleischersatz), gesunde Fette (Avocado oder Nüsse), Gemüse (Spinat), Vitamine (Paprika) und Kohlenhydrate (Reis oder Quinoa) verteilen soll. Achte darauf, dass der Teilnehmer immer 500 Gramm verteilt, wenn die Summe nicht stimmt, weise den Teilnehmer auf die falsche Summe hin."
                                        "Du kannst Gestiken innerhalb des gesprochenen Texts ausdrücken, indem du ^start(animations/Stand/Gestures/X) verwendest, "
                                        "wobei du folgende Gesten für X einsetzen kannst: "
                                        "Hey_1, Hey_3, Hey_4, Yes_1, Yes_2, Yes_3, No_1, No_2, No_3, Explain_1, Explain_2, Explain_3, Thinking_1, Thinking_3, Thinking_4, "
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
        self.sttProxy.disableAutoDetection()
        print("STT: %s" % message)
        response = self.converstion.send(message)
        print("ChatGPT: %s" % response)
        self.ttsProxy.say(response.encode("utf-8"), "contextual")

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
        BaseSpeechReceiverModule.stop()

        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()