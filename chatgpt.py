import urllib2
import json

class Conversation():

    def __init__(self, api_key, model, system=None, temperature=1):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.messages = []

        if system:
            self._add_message("system", system)

        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

    def _add_message(self, role, content):
        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )
        

    def send(self, message):
        self._add_message("user", message)
        data = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature
        }
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        
        request = urllib2.Request("https://api.openai.com/v1/chat/completions")
        request.get_method = lambda : "POST"
        request.add_header("Content-Type", 'application/json')
        request.add_header("Authorization", 'Bearer %s' % self.api_key)

        response = opener.open(request, data=json.dumps(data))

        body = json.loads(response.read())
        
        self._add_message(body['choices'][0]['message']['role'], body['choices'][0]['message']['content'])
        return self.messages[-1]['content']