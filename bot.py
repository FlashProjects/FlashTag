import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**Ben Mention Tag Bot**, Grup veya kanaldaki hemen hemen tüm üyelerden bahsedebilirim. 👻\nTık **/help** daha fazla bilgi için__\n\n Follow [@Mahoaga](https://t.me/Mahoaga) telegram",
                    buttons=(
                      [Button.url('📣 Channel', 'https://t.me/sohbetdestek'),
                      Button.url('📦 Source', 'https://t.me/Mahoaga')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**MentionAllBot Yardım Menüsü**\n\nCommand: /mentionall\n__Bu komutu, başkalarına bahsetmek istediğiniz metinle kullanabilirsiniz.__\n`Example: /Herkese Günaydın!`\n__Bu komutu herhangi bir iletiye yanıt olarak. Bot, kullanıcıları yanıtlanan karışıklıkla etiketleyecek__.\n\nFollow [@SohbetDestek](https://t.me/Sohbetdestek) on Channel"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('📣 Channel', 'https://t.me/Sohbetdestek'),
                      Button.url('📦 Source', 'https://t.me/Mahoaga')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__Bu komut gruplar ve kanallar halinde kullanılabilir!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca yöneticiler tüm!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Benim eski iletiler için üyelerden bahsedilemiyor! (gruba eklemeden önce gönderilen iletiler)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver.!__")
  else:
    return await event.respond("__Bir iletiyi yanıtlama veya diğerlerinden bahsetmem için bana bazı metinler verme!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
