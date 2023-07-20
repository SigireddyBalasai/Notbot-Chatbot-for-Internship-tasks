"""curl -X  POST \
 'https://graph.facebook.com/v17.0/FROM_PHONE_NUMBER_ID/messages' \
 -H 'Authorization: Bearer ACCESS_TOKEN' \
 -H 'Content-Type: application/json' \
 -d '{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "PHONE_NUMBER",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {
      "text": "BUTTON_TEXT"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
            "id": name1,
            "title": "BUTTON_TITLE_1"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "UNIQUE_BUTTON_ID_2",
            "title": "BUTTON_TITLE_2"
          }
        }
      ]
    }
  }
}'"""
import asyncio
import aiohttp


async def send_whatsapp_reply_button(number, message, name1, name2, access_token, from_phone_number_id):
    url = f'https://graph.facebook.com/v17.0/{from_phone_number_id}/messages'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": message
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": name1,
                            "title": name1
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": name2,
                            "title": name2
                        }
                    }
                ]
            }
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Message sent successfully.")
            else:
                print(f"Failed to send message. Status code: {response.status}")
                print(await response.text(), headers, data)
