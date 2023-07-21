import json
import aiohttp
from aiohttp import web
import asyncio
from sqlalchemy import create_engine
from list_message import send_list_message, Row, Section
from send_message import send_whatsapp_message
from address_message import send_whatsapp_address_message
from reply_button import send_whatsapp_reply_button
from Praser import WhatsappMessage
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class User2(Base):
    __tablename__ = 'user2'
    name = Column(String)
    email_id = Column(String)
    Experience = Column(String)
    id = Column(Integer, primary_key=True)

    def __init__(self, name, email_id, Experience):
        self.name = name
        self.email_id = email_id
        self.Experience = Experience


Base.metadata.create_all(engine)


class User:
    name: str
    email_id: str
    Experience: str

    def __init__(self):
        self.name = ""
        self.email_id = ""
        self.Experience = ""

    def set_name(self, name: str):
        if (name.isdigit()):
            return False
        self.name = name
        return True

    def set_email_id(self, email_id: str):
        if email_id.isdigit() or '@' not in email_id:
            return False
        self.email_id = email_id
        return True

    def check_name(self):
        if self.name == "":
            return False
        return True

    def check_email_id(self):
        if self.email_id == "":
            return False
        return True


dict_a = {}

access_token = "EAAwIubFdeA8BAMft2mCY3WFZCD6ZC795zxYBjGwvwOegboCSJm1rSMnsA3ZAV2T0SZAD6jdb1NJMMbs8mZAqutIAZB2VGpumnG6pxzR2upfQgbDqtfiQck88vsbjZBGT4JACgRrh20k2QVuHjfSA44HTo2ZBHUHSx7qLucnyOwjGfSBjrKq3sv3FSgbwKgrpuGFMbHboHWbU9ZCKQSlvKlys4"
from_phone_number_id = "101395609536249"
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
    if message.message_text == 'Hi!':
        await send_whatsapp_reply_button(message.user, "Hi are you here to apply for internship?", "Yes", "No",
                                         access_token, from_phone_number_id)
        dict_a[message.user] = User()
    elif message.button_title == 'Yes' and message.message_type == 'interactive':
        await send_whatsapp_message(message.user, "Please enter your name", access_token, from_phone_number_id)
    elif message.button_title == 'No' and message.message_type == 'interactive':
        await send_whatsapp_message(message.user, "Please enter your name", access_token, from_phone_number_id)
    elif message.message_type == 'text' and dict_a[message.user].check_name() == False:
        ok = dict_a[message.user].set_name(message.message_text)
        if ok and dict_a[message.user].check_email_id() == False:
            await send_whatsapp_message(message.user, "Please enter your email id", access_token, from_phone_number_id)
        else:
            await send_whatsapp_message(message.user, "Please enter a valid name", access_token, from_phone_number_id)
    elif message.message_type == 'text' and dict_a[message.user].check_email_id() == False:
        ok = dict_a[message.user].set_email_id(message.message_text)
        if ok and dict_a[message.user].check_name():
            Row1 = Row('1', '1 year', '1 year')
            Row2 = Row('2', '2 year', '2 year')
            Row3 = Row('3', '3 year', '3 year')
            Row4 = Row('4', '4 year', '4 year')
            Row5 = Row('5', '5 year', '5 year')
            section = Section('Experience', [Row1, Row2, Row3, Row4, Row5])
            await send_list_message(from_phone_number_id, 'Please select one',
                                    "Please select how many years of experience you have with Python/JS/ Automation Development",
                                    access_token,
                                    message.user, section)
        else:
            await send_whatsapp_message(message.user, "Please enter a valid email id", access_token,
                                        from_phone_number_id)
    if message.message_type == 'interactive':
        print(message.list_reply_id, message.list_reply_title)
        if message.list_reply_title == '1 year' or message.list_reply_title == '2 year' or message.list_reply_title == '3 year' or message.list_reply_title == '4 year' or message.list_reply_title == '5 year':
            print(hello)
            user = User2(dict_a[message.user].name, dict_a[message.user].email_id, message.list_reply_title)
            print(user)
            session.add(user)
            session.commit()
            await send_whatsapp_message(message.user, "Thank you for contacting us we will reach you soon",
                                        access_token,
                                        from_phone_number_id)
    return web.Response(text="ok", status=200)


@routes.get('/hello')
async def hello(request):
    print("helo")
    return web.Response(text="Hello, world")

@routes.get('/send')
async def send(request):
    await send_whatsapp_message('919398993400',"working",access_token,from_phone_number_id)
    return web.Response(text="Sent")


app = web.Application()
app.router.add_routes(routes)
print(os.environ)
