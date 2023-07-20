import aiohttp
import asyncio
import mimetypes

async def upload_media(access_token,phone_number_id,filename):
    url = f'https://graph.facebook.com/v17.0/{phone_number_id}/media'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    content_type, _ = mimetypes.guess_type(filename)

    data = aiohttp.FormData()
    data.add_field('file', open(filename, 'rb'), filename=filename)
    data.add_field('type', content_type)
    data.add_field('messaging_product', 'whatsapp')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                print("Media uploaded successfully.")
                return await response.text()
            else:
                print(f"Failed to upload media. Status code: {response.status}")
                print(await response.text())


async def download_url(access_token,media_id):
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    url = f'https://graph.facebook.com/v17.0/{media_id}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as response:
            return await response.text()
