import json
import aiohttp
from aiohttp import web
import openvpn_api
import asyncio

routes = web.RouteTableDef()
loopa = asyncio.new_event_loop()


async def get_port():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://pywhatkit-team.is-a-good.dev/get_remote_port') as resp:
            text = await resp.text()
            return text.split(",")


async def send_message(number, access_token):
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'
               }
    data = json.dumps({"messaging_product": "whatsapp",
                       "to": number, "type": "template",
                       "template": {"name": "hello_world", "language": {"code": "en_US"}}})
    async with aiohttp.ClientSession() as session:
        async with session.post('https://graph.facebook.com/v15.0/101395609536249/messages', headers=headers,
                                data=data) as resp:
            print(resp.status)
            print(await resp.text())
            print(resp.__dict__)


@routes.get('/wa_callback/<customer_id>')
async def wa_callback(request, customer_id):
    if request.method == 'GET':
        if 'hub.mode' in request.args and 'hub.challenge' in request.args and 'hub.verify_token' in request.args:
            hub_mode = request.args.get('hub.mode')
            hub_challenge = request.args.get('hub.challenge')
            hub_verify_token = request.args.get('hub.verify_token')
            if hub_mode == 'subscribe' and hub_verify_token == 'happy':
                return hub_challenge
            else:
                return 'Failed validation. Make sure the validation tokens match.'
        else:
            return 'Failed validation. Make sure the validation tokens match.'
    elif request.method == 'POST':
        print(request.json)
        print(request.data)
        print(request.form)
        print(request.args)
        return 'ok'


@routes.get('/')
async def hello(request):
    await send_message("919398993400",
                       'EAAwIubFdeA8BAIZANZCKpgdP1HZCZA77mcNTLhEibuk32aatpi2PZAAeX8eWV5MmdznHCDj90uGGBZCIWqyZALv1fZCfpQybu8V5GzJ8j3Yal1hC9GwXZC0D2jm6tRFMHpKi0GTTeSjyKJGgN19AZB7gJEviENsa6kmAA2pNLJO2gmUtDP8qqgsCOeZAfg1AGxHJdtTUkXOYKEAiKErMwMoX5KS')
    return web.Response(text="Hello, world")


app = web.Application()
app.router.add_routes(routes)



web.run_app(app)