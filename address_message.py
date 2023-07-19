"""curl -X  POST \
'https://graph.facebook.com/v15.0/FROM_PHONE_NUMBER_ID/messages' \
-H 'Authorization: Bearer ACCESS_TOKEN' \
-H 'Content-Type: application/json' \
-d
'{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "91xxxxxxxxxx",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": {
          "country": "IN",
          "saved_addresses": [
             {
                 "id": "address1",
                 "value": {
                    "name": "CUSTOMER_NAME",
                    "phone_number": "+91xxxxxxxxxx",
                    "in_pin_code": "400063",
                    "floor_number": "8",
                    "building_name": "",
                    "address": "Wing A, Cello Triumph,IB Patel Rd",
                    "landmark_area": "Goregaon",
                    "city": "Mumbai"
                 }
             }
          ]
       }
    }
  }
}'"""

import asyncio
import aiohttp


class Address:
    id: str
    name: str
    phone_number: str
    in_pin_code: str
    floor_number: str
    building_name: str
    address: str
    landmark_area: str
    city: str

    def __init__(self, id, name, phone_number="", in_pin_code="", floor_number="0", building_name="", address="", landmark_area="", city=""):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.in_pin_code = in_pin_code
        self.floor_number = floor_number
        self.building_name = building_name
        self.address = address
        self.landmark_area = landmark_area
        self.city = city

    def to_dict(self):
        return {
            "id": self.id,
            "value": {
                "name": self.name,
                "phone_number": self.phone_number,
                "in_pin_code": self.in_pin_code,
                "floor_number": self.floor_number,
                "building_name": self.building_name,
                "address": self.address,
                "landmark_area": self.landmark_area,
                "city": self.city
            }
        }


async def send_whatsapp_address_message(number, message, address1, address2, address3, access_token,
                                        from_phone_number_id):
    url = f'https://graph.facebook.com/v15.0/{from_phone_number_id}/messages'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "address_message",
            "body": {
                "text": message
            },
            "action": {
                "name": "address_message",
                "parameters": {
                    "country": "IN",
                    "saved_addresses": [
                        address1.to_dict(), address2.to_dict(), address3.to_dict()
                    ]
                }
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
