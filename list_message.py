'''curl -X  POST \
 'https://graph.facebook.com/v17.0/FROM_PHONE_NUMBER_ID/messages' \
 -H 'Authorization: Bearer ACCESS_TOKEN' \
 -H 'Content-Type: application/json' \
 -d '{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "PHONE_NUMBER",
  "type": "interactive",
  "interactive": {
    "type": "list"
    "sections": [
        {
          "title": "SECTION_1_TITLE",
          "rows": [
            {
              "id": "SECTION_1_ROW_1_ID",
              "title": "SECTION_1_ROW_1_TITLE",
              "description": "SECTION_1_ROW_1_DESCRIPTION"
            },
            {
              "id": "SECTION_1_ROW_2_ID",
              "title": "SECTION_1_ROW_2_TITLE",
              "description": "SECTION_1_ROW_2_DESCRIPTION"
            }
          ]
        },
        {
          "title": "SECTION_2_TITLE",
          "rows": [
            {
              "id": "SECTION_2_ROW_1_ID",
              "title": "SECTION_2_ROW_1_TITLE",
              "description": "SECTION_2_ROW_1_DESCRIPTION"
            },
            {
              "id": "SECTION_2_ROW_2_ID",
              "title": "SECTION_2_ROW_2_TITLE",
              "description": "SECTION_2_ROW_2_DESCRIPTION"
            }
          ]
        }
      ]
    },'''

import asyncio
import aiohttp


class Row:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }


class Section:
    def __init__(self, title, rows):
        self.title = title
        self.rows = rows

    def to_json(self):
        return {
            'title': self.title,
            'rows': [row.to_json() for row in self.rows]
        }


async def send_list_message(phone_number_id,header,body, access_token, phone_number, section1):
    url = 'https://graph.facebook.com/v17.0/' + phone_number_id + '/messages'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': phone_number,
        'type': 'interactive',
        'interactive': {
            'type': 'list',
            'header': {
                'type': 'text',
                'text': header
            },
            'body': {
                'text': body
            },
            'action': {
                'button': "Select one",
            'sections': [
                section1.to_json()
            ]
            }
        },
    }
    print(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            print(await response.text())
