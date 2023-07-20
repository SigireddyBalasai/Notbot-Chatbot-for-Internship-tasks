import aiohttp
import aiohttp
import asyncio


async def send_whatsapp_message(number, message, access_token, from_phone_number_id):
    url = f'https://graph.facebook.com/v17.0/{from_phone_number_id}/messages'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "text": {"body": message}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Message sent successfully.")
            else:
                print(f"Failed to send message. Status code: {response.status}")
                print(await response.text(),headers,data)

