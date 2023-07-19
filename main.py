import json
import aiohttp
from aiohttp import web
from cloudflared.cloudflare import CloudflareTunnels
import asyncio
import aiosqlite
import sqlalchemy as sa
import aiohttp_sqlalchemy as ahsa
from sqlalchemy import orm
from list_message import send_list_message, Section, Row
from Praser import WhatsappMessage
from send_message import send_whatsapp_message
from reply_button import send_whatsapp_reply_button
from address_message import send_whatsapp_address_message, Address


class Data:
    block: str | None
    car: str | None
    color: str | None
    vehicle_number: str | None

    def __init__(self):
        self.block = None
        self.car = None
        self.color = None
        self.vehicle_number = None

    def set_block(self, block):
        self.block = block

    def set_car(self, car):
        self.car = car

    def get_block(self):
        return self.block

    def get_car(self):
        return self.car

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_vehicle_number(self, vehicle_number):
        self.vehicle_number = vehicle_number

    def get_vehicle_number(self):
        return self.vehicle_number


dict_a = {}

access_token = "EAAwIubFdeA8BAGWkQA43000k1ZAubZA2JWfhrJyXl2U8uQYBYrNb45ftJg4VV9yejlOcniUSZAu9Nq5ZBHlRNkiZAslo8WUjrXfUEqIzV0BJafKqAJDewEccl261k7YxXnWmlYlzCXcQmPt9RYtIyLsApCnIoRYUrfX1xDCruCbflDfEhPgCIvSj3iTo5Ht5KDyVsDIH7LdC9h5oihM1B"
from_phone_number_id = "101395609536249"

app_cloudflare = CloudflareTunnels()
app_cloudflare.create_tunnel("whatsapp")
app_cloudflare.add_dns('whatsapp', 'whatsapp.sigireddybalasai.tech')
routes = web.RouteTableDef()
loopa = asyncio.new_event_loop()


@routes.get('/webhook')
async def wa_callback(request: web.Request):
    print("hello")
    print(request)
    print(request.rel_url)
    if request.method == 'GET':
        try:
            if request.rel_url.query['hub.mode'] and request.rel_url.query['hub.challenge'] and request.rel_url.query[
                'hub.verify_token']:
                hub_mode = request.rel_url.query['hub.mode']
                hub_challenge = request.rel_url.query['hub.challenge']
                hub_verify_token = request.rel_url.query['hub.verify_token']
                print(hub_mode, hub_mode == 'subscribe', hub_challenge, hub_verify_token, hub_verify_token == 'happy')
                if hub_mode == 'subscribe' and hub_verify_token == 'happy':
                    print("Validating webhook")
                    return web.Response(text=hub_challenge, status=200)
                else:
                    return web.Response(text='Failed validation. Make sure the validation tokens match.', status=403)
            else:
                return web.Response(text='Failed validation. Make sure the validation tokens match.', status=403)
        except Exception as e:
            print(e)
            return web.Response(text='Failed validation. Make sure the validation tokens match.', status=403)


@routes.post('/webhook')
async def wa_callback(request: web.Request):
    ok = await request.json()
    print(ok)
    message = WhatsappMessage(ok)
    print(message.message_text, message.user, message.message_type, message.button_title)
    if message.message_text == 'hi':
        dict_a[message.user] = Data()
        await send_whatsapp_message(message.user,
                                    "Hi it appears if you don't have account with us how about we introduce ourself first",
                                    access_token, from_phone_number_id)
        await send_whatsapp_reply_button(message.user,
                                         "We are TCWC by 68 detailers. We provide subscription based car washing to selected condominiums and residence in Singapore. For as low as $5 per wash, 8 limes a week at the convenience of your residential carpark",
                                         "learn more", 'signup', access_token, from_phone_number_id)
    elif message.button_title == 'signup' and message.message_type == 'interactive':
        address1 = Row("1", "1", "Maysprings Condominium -2 Peter Road")
        address2 = Row("2", "2", "B Riversuites")
        address3 = Row("3", "3", "CityView Residents")
        address4 = Row("4", "4", "My Condominium is not listed in the above.Please get in touch with me")
        section1 = Section("Select any one option", [address1, address2, address3, address4])
        await send_list_message(from_phone_number_id, "Please select any one option", 'Please enter your location',
                                access_token, message.user,
                                section1)
    elif message.message_type == 'interactive' and message.interactive_type == 'list_reply':
        if message.list_reply_id != '4':
            await send_whatsapp_message(message.user, "Thats great lets move on to next details", access_token,
                                        from_phone_number_id)
            await send_whatsapp_message(message.user, "Please enter your block number", access_token,
                                        from_phone_number_id)
        else:
            await send_whatsapp_message(message.user, "We will contact you soon", access_token, from_phone_number_id)
    elif message.message_type == 'text':
        if dict_a[message.user].get_block() is None:
            dict_a[message.user].set_block(message.message_text)
            await send_whatsapp_message(message.user, "That's great lets move to your car details", access_token,
                                        from_phone_number_id)
            await send_whatsapp_message(message.user, "Brand name of car", access_token, from_phone_number_id)
        elif dict_a[message.user].get_car() is None:
            dict_a[message.user].set_car(message.message_text)
            await send_whatsapp_message(message.user, "Colour name of car", access_token, from_phone_number_id)
        elif dict_a[message.user].get_color() is None:
            dict_a[message.user].set_color(message.message_text)
            await send_whatsapp_message(message.user, "Vehicle number", access_token, from_phone_number_id)
        elif dict_a[message.user].get_vehicle_number() is None:
            dict_a[message.user].set_vehicle_number(message.message_text)
            await send_whatsapp_reply_button(message.user,
                                             "How would you like to move forward",
                                             "Add another vehicle", 'move to packages', access_token, from_phone_number_id)
    elif message.message_type == 'interactive' and message.interactive_type == 'reply_button':
        if(message.message_text == 'move to packages'):
            await send_whatsapp_reply_button(message.user,"Please choose the package Package A monday and thursdays only at $ 55 per month or 6.85 per wash 50 slots left"
                                                          "Package B monday and thursdays only at $155 per month or 6.80 for wash ask any questions",'Package A','Package B',access_token,from_phone_number_id)
        elif(message.message_text == 'Package A'):
            address1 = Row("1", "1", "Weekly tyre shine $5 per month")
            address2 = Row("2", "2", "Monthly interior cleaning $10 per month appintment required")
            address3 = Row("3", "3", "Northing else")
            section1 = Section("Select any one option", [address1, address2, address3])
            await send_list_message(from_phone_number_id, "Please select any one option", 'Please enter any additions',access_token,message.user,section1)
        elif(message.message_text == 'Package B'):
            address1 = Row("1", "1", "Weekly tyre shine $5 per month")
            address2 = Row("2", "2", "Monthly interior cleaning $10 per month appintment required")
            address3 = Row("3", "3", "Northing else")
            section1 = Section("Select any one option", [address1, address2, address3])
            await send_list_message(from_phone_number_id, "Please select any one option", 'Please enter any additions',access_token,message.user,section1)
        elif(message.interactive_type == 'list_reply'):
            await send_whatsapp_message(message.user, "Thats great lets proceed to payment you will not be charged ",
                                        access_token, from_phone_number_id)

    return web.Response(text='ok', status=200)


@routes.get('/hello')
async def hello(request):
    print("helo")
    return web.Response(text="Hello, world")


app = web.Application()
app.router.add_routes(routes)
app_cloudflare.run('whatsapp', "localhost:8080")
web.run_app(app, port=8080)
