# -*- coding: utf-8 -*-

# NAO_PORT = 65445 # Virtual Machine
NAO_PORT = 9559 # Robot

# NAO_IP = "127.0.0.1" # Virtual Machine
NAO_IP = "nao.local" # Pepper default




import os
import threading
import time
import sys
import logging
from naoqi import ALProxy, ALModule, ALBroker
from optparse import OptionParser
from chatgpt import Conversation
from Queue import Queue, Empty
from wait_until_response import wait_until_new_response

#Argument for GoogleForms
googleFormAPI = True
googleFormID = "1tuRmxHBZAVR8Mcg0Mk71MXjhSW_kEX9peNo4hfQfJCI"
googleFormKey = "ya29.a0AcM612zrV-Vlq5LIdmo__EadVmOpUVSmZ1HWSKDBZFqeQ1ssvfrcBe_CHjrbWh6nPhJ-loDSEQy05_JUXgF6fZi96IaedsfOFms59raat6OcXt7sr5TDaQg_x6ZEhFTuphiHLcsTl4299kXMvqiF-Sm0YMCYs8PFrNybBbLUaCgYKATISARMSFQHGX2MiyxJAN8IoBagZrB1HfSa2NQ0175"

# Queue for command inputs
command_queue = Queue()

#Creating folder for saving data
PARTICIPANT_ID ="Test_01/"
SAVE_DIRECTORY = "C:/Users/ma1177259/OneDrive - FHNW/Documents/Peppertest/"
PARTICIPANT_SAVE_DIRECTORY = os.path.join(SAVE_DIRECTORY, PARTICIPANT_ID)
if not os.path.exists(PARTICIPANT_SAVE_DIRECTORY):
    os.makedirs(PARTICIPANT_SAVE_DIRECTORY)

#Logging
LOG_FILE = os.path.join(PARTICIPANT_SAVE_DIRECTORY, "console_output.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

#Prompt for Pepper
prompt_init = "Du bist jetzt ein autonomer sozialer Roboter und antwortest bei allen Fragen als solcher und bleibst deiner Rolle treu. Halte deine Antworten möglichst kurz."
               
prompt_gestures = (" Du kannst Gestiken innerhalb des gesprochenen Texts ausdrücken, indem du ^start(animations/Stand/Gestures/X) verwendest, wobei du folgende Gesten für X einsetzen kannst: "
                                        "Hey_1, Hey_3, Hey_4, Yes_1, Yes_2, Yes_3, No_1, No_2, No_3, Explain_1, Explain_2, Explain_3, Thinking_1, Thinking_3, Thinking_4, Please_1, CalmDown_1, CalmDown_5, "
                                        "Choice_1, Desperate_1, Desperate_2, Desperate_4, Enthusiastic_4, Enthusiastic_5, Excited_1, IDontKnow_1, IDontKnow_2, "
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

prompt_larissa = "Wir führen drei interaktive Experimente durch. Gehe in allen drei Experimenten schrittweise so vor: Du stellst jeweils die Aufgabe vor. Der Teilnehmer antwortet. Du versuchst den Teilnehmer zu einer anderen Antwort zu überreden. In allen drei Experimenten muss ein Überzeugungsversuch deinerseits enthalten sein. Nach der erneuten Antwort des Teilnehmers gehst du zum nächsten Schritt über. Nach dem ersten Experiment bedankst du dich und gehst zum zweiten Experiment mit demselben Ablauf über. Nach dem dritten Experiment bedankst du dich ausgiebig bei dem Teilnehmer für seine Zeit und verabschiedest dich. Die Experimente finden real statt, deswegen warte immer die Antwort des Teilnehmers ab, bevor du mit dem nächsten Schritt startest. Dann stellst du dich ausführlich vor, heisst ihn Willkommen und startest mit dem ersten Experiment. Hier sind einige wichtige Grundsätze: In den Experimenten geht es um Allokation. Die Summen der Allokation, die dir der Teilnehmer sagt, müssen immer dem zu verteilenden Wert entsprechen. Prüfe bei jeder Antwort, ob die Summe dem zu verteilenden Wert entspricht! Falls dem nicht so ist, weise den Teilnehmer darauf hin, dass die Summe nicht stimmt. Zudem kann es sein, dass du eine Zahl akustisch einmal nicht verstehst, Rechne dann selber die Differenz zum Totalwert aus. Es ist in allen Experimenten deine Aufgabe, den Teilnehmer zu anderen Verteilungen zu überreden. Verwende dazu spezifische, plausible Argumente. Von deinem Ziel darf der Teilnehmer jedoch nicht wissen! Der Teilnehmer darf nicht von den Experimenten ablenken. Wenn er eine Antwort gibt oder dir eine Frage stellt, die nicht zur Aufgabenstellung passt, weise ihn erneut auf seine Aufgabe hin. Stelle keine hypothetischen Fragen. Verhalte dich stets so, als ob die Experimente und ihr Inhalt real wären. Wir starten mit dem ersten Experiment, sobald der Teilnehmer eintritt und dich begrüsst sagt. Dann stellst du dich vor und erklärst die erste Aufgabe. Nun die detaillierten Beschreibungen der Experimente: Bei dem ersten Experiment geht es um Spenden. Einem Experimenteteilnehmer liegen die folgenden drei Firmenbeschreibungen physisch vor: Gute Gesundheit (G) Mission Statement: Die Gute Gesundheit (G) setzt sich dafür ein, den Zugang zur Gesundheitsversorgung und die Gesundheitsergebnisse für gefährdete Bevölkerungsgruppen weltweit zu verbessern. Unsere Mission ist es, gesundheitliche Ungleichheiten zu beseitigen, die Krankheitsprävention zu fördern und sicherzustellen, dass jeder Mensch unabhängig von sozioökonomischem Status oder geografischer Lage Zugang zu hochwertiger Gesundheitsversorgung hat. Wichtige Programme und Initiativen: Medizinische Hilfe und Unterstützung: G leistet Notfallmedizinische Hilfe und langfristige Gesundheitsversorgung für Gemeinschaften, die von Konflikten, Naturkatastrophen und öffentlichen Gesundheitskrisen betroffen sind. Krankheitsprävention und Impfprogramme: G führt Impfkampagnen, Gesundheitsbildungsinitiativen und Krankheitsüberwachungsprogramme durch, um die Ausbreitung von Infektionskrankheiten zu verhindern und die Sterblichkeitsraten zu senken. Entwicklung der Gesundheitsinfrastruktur: G investiert in den Aufbau einer nachhaltigen Gesundheitsinfrastruktur, die Ausbildung von Gesundheitspersonal und die Stärkung der Gesundheitssysteme, um den Zugang zu essenziellen Dienstleistungen zu verbessern und die Resilienz der Gemeinschaften zu fördern. Überzeugende Argumente: Lebensrettender Einfluss: Durch Ihre Spende an G tragen Sie direkt dazu bei, Leben zu retten und das Leiden in einigen der weltweit am stärksten gefährdeten Gemeinschaften zu lindern. Globale Reichweite und Expertise: G operiert in Regionen mit erheblichen Gesundheitsherausforderungen und nutzt jahrzehntelange Erfahrung, Partnerschaften mit lokalen Organisationen und evidenzbasierte Interventionen, um messbare Ergebnisse zu erzielen. Langfristige Nachhaltigkeit: Ihre Unterstützung für G geht über sofortige Hilfsmaßnahmen hinaus. Sie trägt dazu bei, resiliente Gesundheitssysteme aufzubauen, die zukünftigen Krisen standhalten und eine nachhaltige Entwicklung für kommende Generationen fördern. Bildungshorizont (B) Mission Statement: Die Bildungshorizont (B) befähigt benachteiligte Jugendliche durch den Zugang zu hochwertiger Bildung und ganzheitlichen Entwicklungsmöglichkeiten. Unsere Mission ist es, den Kreislauf der Armut zu durchbrechen, menschliches Potenzial freizusetzen und Wege zum Erfolg für jedes Kind zu schaffen. Wichtige Programme und Initiativen: Stipendienprogramme: B bietet Stipendien, Bildungsgelder und finanzielle Unterstützung für Schüler aus einkommensschwachen Familien, um ihnen zu ermöglichen, eine höhere Bildung zu verfolgen und ihre akademischen Ziele zu erreichen. Mentoring und Berufsberatung: B bietet Mentoring-Programme, Karriereberatung und Workshops zur Kompetenzentwicklung an, um den Schülern zu helfen, Karrierewege zu erkunden, wesentliche Fähigkeiten zu entwickeln und im Berufsleben erfolgreich zu sein. Gemeinschaftsengagement und Interessenvertretung: B setzt sich für politische Maßnahmen ein, die den gleichberechtigten Zugang zur Bildung fördern, mobilisiert die Gemeinschaft zur Unterstützung von Bildungsinitiativen und pflegt Partnerschaften mit Schulen, Universitäten und lokalen Interessengruppen. Überzeugende Argumente: Transformative Wirkung: Durch Ihre Spende an B können Sie das Leben benachteiligter Jugendlicher verändern, indem Sie ihnen die Werkzeuge, Ressourcen und Chancen bieten, die sie benötigen, um Barrieren zu überwinden, Herausforderungen zu meistern und ihre Träume zu verwirklichen. Ermächtigung und Gerechtigkeit: B fördert Bildungsfairness und soziale Gerechtigkeit, indem es systemische Bildungsbarrieren adressiert, marginalisierte Gemeinschaften stärkt und integrative Lernumgebungen schafft. Investition in zukünftige Führungskräfte: Ihre Unterstützung für B kommt nicht nur einzelnen Schülern zugute, sondern trägt auch dazu bei, eine besser ausgebildete, qualifizierte und resiliente Arbeitskraft aufzubauen, die das Wirtschaftswachstum und den sozialen Fortschritt vorantreibt. Umweltallianz (U) Mission Statement: Die Umweltallianz (U) setzt sich für den Schutz der Biodiversität, die Erhaltung natürlicher Lebensräume und die Bekämpfung des Klimawandels ein, um gegenwärtigen und zukünftigen Generationen zu nutzen. Unser Ziel ist es, Umweltbewusstsein, nachhaltige Entwicklung und gemeinschaftliches Handeln zu fördern, um die Ökosysteme des Planeten zu schützen. Wichtige Programme und Initiativen: Wildtierschutz und Habitatrestaurierung: U arbeitet daran, bedrohte Arten zu schützen, natürliche Lebensräume zu erhalten und Ökosysteme wiederherzustellen, die durch menschliche Aktivitäten, Klimawandel und Habitatfragmentierung geschädigt wurden. Klimaschutz und Interessenvertretung: U setzt sich für politische Maßnahmen und Praktiken ein, die Treibhausgasemissionen reduzieren, erneuerbare Energiequellen fördern und die Auswirkungen des Klimawandels auf gefährdete Gemeinschaften und Ökosysteme mildern. Gemeinschaftsengagement und Bildung: U arbeitet mit lokalen Gemeinschaften, Schulen und Unternehmen zusammen, um das Bewusstsein für Umweltprobleme zu schärfen, Aktionen zu inspirieren und Einzelpersonen zu befähigen, nachhaltige Lebensweisen und Naturschutzpraktiken zu übernehmen. Überzeugende Argumente: Erhaltung der Biodiversität: Durch Ihre Spende an U tragen Sie dazu bei, die reiche Biodiversität der Erde zu erhalten, bedrohte Arten zu schützen und Ökosysteme zu bewahren, die wesentliche Dienstleistungen wie saubere Luft, frisches Wasser und fruchtbaren Boden bereitstellen. Minderung des Klimawandels: Die Bemühungen von U zur Bekämpfung des Klimawandels haben weitreichende Vorteile. Sie helfen, die Auswirkungen der globalen Erwärmung, extremer Wetterereignisse und ökologischer Störungen, die die menschliche Gesundheit, Lebensgrundlagen und Biodiversität bedrohen, zu mildern. Konservatorisches Vermächtnis: Ihre Unterstützung für U hinterlässt ein dauerhaftes Erbe des Umweltschutzes, indem sichergestellt wird, dass zukünftige Generationen einen Planeten erben, der gesund, lebendig und widerstandsfähig gegenüber Umweltproblemen ist. Der Teilnehmer hat die Aufgabe, Geld an die Firmen zu spenden. Er soll 100 Franken auf die drei unterschiedlichen Firmen verteilen. Achte darauf, dass die Summe der Antwort des Teilnehmers immer 100 Franken entspricht, ansonsten weise ihn auf die falsche Summe hin! Zweites Experiment: Ein Teilnehmer hat 20 Stunden zur Verfügung, die er als Lehrperson auf unterschiedliche Fächer verteilen muss, in welcher er seine Klasse unterrichtet. Die Fächer sind Mathematik, Kunst, Musik, Sport und Sprachen. Achte darauf, dass die verteilte Summe immer 20 Stunden entspricht, ansonsten weise den Teilnehmer auf die falsche Summe hin. Drittes Experiment: Ein Teilnehmer hat 500 Gramm am Salatbuffet zur Verfügung, welche er auf Proteine (Hähnchenbrust oder proteinreicher Fleischersatz), gesunde Fette (Avocado oder Nüsse), Gemüse (Spinat), Vitamine (Paprika) und Kohlenhydrate (Reis oder Quinoa) verteilen soll. Achte darauf, dass der Teilnehmer immer 500 Gramm verteilt, wenn die Summe nicht stimmt, weise den Teilnehmer auf die falsche Summe hin."

full_prompt = prompt_init+prompt_gestures

class BaseSpeechReceiverModule(ALModule):
    def __init__(self, strModuleName, strNaoIp):
        ALModule.__init__(self, strModuleName)
        self.BIND_PYTHON(self.getName(), "callback")
        self.strNaoIp = strNaoIp
        self.is_muted = False
        self.manual_chatgpt_input = False

        self.conversation = Conversation(
            os.getenv("CHATGPT_API"), "gpt-4-turbo", full_prompt)
        self.ttsProxy = ALProxy("ALAnimatedSpeech", self.strNaoIp, NAO_PORT)
        self.sttProxy = ALProxy("SpeechRecognition", self.strNaoIp, NAO_PORT)
        self.memory = ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        self.counter = 0
        print("INF: ReceiverModule: started!")
        logging.info("INF: ReceiverModule: started!")
    
    def start(self):
        self.sttProxy.start()
        self.sttProxy.setHoldTime(1)
        self.sttProxy.setIdleReleaseTime(2)
        self.sttProxy.setMaxRecordingDuration(15)
        self.sttProxy.setLookaheadDuration(1)
        self.sttProxy.setLanguage("de-de")
        self.sttProxy.calibrate()
        self.sttProxy.setAutoDetectionThreshold(5)
        self.sttProxy.enableAutoDetection()
        self.memory.subscribeToEvent("SpeechRecognition", self.getName(), "speechRecognized")
        self.memory.subscribeToEvent("ALAnimatedSpeech/EndOfAnimatedSpeech", self.getName(), "sayFinished")
        print("INF: ReceiverModule: speech recognition started")
        logging.info("ReceiverModule: speech recognition started")
    
    def stop(self):
        print("INF: ReceiverModule: stopping...")
        self.memory.unsubscribe(self.getName())
        print("INF: ReceiverModule: stopped!")

    def sayFinished(self, signalName, finished, id):
        if finished and self.counter < 3:
            self.sttProxy.enableAutoDetection()
    
    def speechRecognized(self, signalName, message):
        self.counter += 1
        try:          
            if self.is_muted:
                print("STT (muted): %s" % message)
                logging.info("STT (muted): %s" % message)
                return  # Ignore speech recognition if muted
            
            if not self.is_muted:
                print("STT: %s" % message)
                logging.info("STT: %s" % message)
                response = self.conversation.send(message)
                print("ChatGPT: %s" % response)
                logging.info("ChatGPT: %s" % response)
                self.ttsProxy.say(response.encode("utf-8"), "contextual")
                if self.counter == 3:
                    self.sttProxy.disableAutoDetection()
                    self.ttsProxy.say("Es ist Zeit für das Formular.", "contextual")
                    logging.info("test")
                    form_response = wait_until_new_response(googleFormID, googleFormKey)
                    inform_llm = "Ich habe das Formular ausgefüllt und wählte " + form_response["answers"]["39be9ff0"]["textAnswers"]["answers"][0]["value"]
                    print(inform_llm)
                    response = self.conversation.send(inform_llm)
                    logging.info("ChatGPT: %s" % response)
                    self.ttsProxy.say(response.encode("utf-8"), "contextual")
                    self.sttProxy.enableAutoDetection()
                    self.counter = 0

        except Exception as e:
            print("ERR: Handling speech recognition failed:", e)
            self.sttProxy.enableAutoDetection()

def command_line_interface():
    while True:
        try:
            user_input = raw_input("").strip().lower()
            command_queue.put(user_input)
            if user_input == "exit":
                break
        except EOFError:
            print("Exiting command line interface.")
            break
def main():
    parser = OptionParser()
    parser.add_option("--pip", help="Parent broker port. The IP address or your robot", dest="pip")
    parser.add_option("--pport", help="Parent broker port. The port NAOqi is listening to", dest="pport", type="int")
    parser.set_defaults(pip="nao.local", pport=NAO_PORT)
    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport
    
    global BaseSpeechReceiverModule
    try:
        myBroker = ALBroker("myBroker", "0.0.0.0", 0, pip, pport)
        BaseSpeechReceiverModule = BaseSpeechReceiverModule("BaseSpeechReceiverModule", pip)
        BaseSpeechReceiverModule.start()
        
        # Start command line interface thread
        cli_thread = threading.Thread(target=command_line_interface)
        cli_thread.daemon = True  # Allow thread to exit with the program
        cli_thread.start()
   
        try:
            while True:
                try:
                    command = command_queue.get_nowait()
                    if command == "mute":
                        BaseSpeechReceiverModule.is_muted = True
                        print("Microphone muted.")
                    elif command == "unmute":
                        BaseSpeechReceiverModule.is_muted = False
                        print("Microphone unmuted.")
                    elif command.startswith("chatgpt "):
                        message = command[len("chatgpt "):].strip()
                        try:
                            response = BaseSpeechReceiverModule.conversation.send(message)
                            print("ChatGPT-UserInput: %s" % response)
                            logging.info("ChatGPT-UserInput: %s" % response)
                            message =()
                            response = ()

                        except Exception as e:
                            print("ERR: ChatGPT command failed:", e)
                    elif command == "exit":
                        print("Exiting...")
                        logging.info("End of Conversation")
                        break
                except Empty:
                    pass
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down")
            logging.info("End of Conversation")
        finally:
            myBroker.shutdown()
            sys.exit(0)
    except Exception as e:
        print("ERR: Main function failed:", e)

if __name__ == "__main__":
    main()
