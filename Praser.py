class WhatsappMessage:
    def __init__(self, message_object):
        self.message_test = None
        self.interactive_type = None
        self.object = None
        self.entry_id = None
        self.messaging_product = None
        self.display_phone_number = None
        self.phone_number_id = None
        self.contact_name = None
        self.contact_wa_id = None
        self.user = None
        self.message_id = None
        self.message_timestamp = None
        self.message_type = None
        self.button_id = None
        self.button_title = None
        self.list_reply_id = None
        self.list_reply_title = None
        self.list_reply_description = None
        self.message_text = None

        try:
            self.object = message_object['object']
            self.entry_id = message_object['entry'][0]['id']

            value = message_object['entry'][0]['changes'][0]['value']
            self.messaging_product = value['messaging_product']
            self.display_phone_number = value['metadata']['display_phone_number']
            self.phone_number_id = value['metadata']['phone_number_id']
            self.contact_name = value['contacts'][0]['profile']['name']
            self.contact_wa_id = value['contacts'][0]['wa_id']

            message = value['messages'][0]
            self.user = message['from']
            self.message_id = message['id']
            self.message_timestamp = message['timestamp']
            self.message_type = message['type']

            if self.message_type == 'text':
                self.message_text = message['text']['body']
            elif self.message_type == 'interactive':
                interactive = message['interactive']

                self.process_interactive_message(interactive)
        except (KeyError, IndexError):
            pass

    def process_interactive_message(self, interactive):
        interactive_type = interactive['type']
        self.interactive_type = interactive_type
        if interactive_type == 'button_reply':
            self.button_id = interactive['button_reply']['id']
            self.button_title = interactive['button_reply']['title']
        elif interactive_type == 'list_reply':
            self.list_reply_id = interactive['list_reply']['id']
            self.list_reply_title = interactive['list_reply']['title']
            self.list_reply_description = interactive['list_reply']['description']