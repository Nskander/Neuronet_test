import sys

import handlers
from neuronet_script import INTENTS


class Handler:
    def __init__(self, client_name, company_name):
        self.state = None
        self.context = {'client_name': client_name, 'company_name': company_name}

    def run(self):
        if self.state is not None:
            self.continue_scenario()
        else:
            self.start_scenario()

    def start_scenario(self):
        self.state = 'hello'
        self.talk_to(INTENTS[self.state]['prompt_text'])

    def continue_scenario(self):
        state = INTENTS[self.state]
        answer = self.listen_from()
        handler = getattr(handlers, state['handler'])
        if handler(text=answer, state=self.state, context=self.context):

            self.state = INTENTS[self.state]['scenario'][self.context[self.state]]
            self.talk_to(INTENTS[self.state]['prompt_text'])

            if INTENTS[self.state]['scenario'] == "hangup_action":
                sys.exit()

    def talk_to(self, text):
        print(text.format(**self.context))

    def listen_from(self):
        answer = input('Ответ: ')
        return answer


if __name__ == '__main__':
    handler = Handler('Борис', 'Гагава')
    handler.run()
    while True:
        handler.run()
