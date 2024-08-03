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

def fetchKeyword(keyword, source):
    return len(findall(fr"\b{keyword}\b", source)) >= 1

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
    status = "APPROVED"
    mes = message.lower()

    if "ccn" in mes:
        status += " CCN"
    elif len(findall(r"(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b).(\b\d{1,2}\b)", mes)) >= 1:
        status = "CHARGED CC"
    elif len(findall(r"(\bcharged\b).(\b\d{1,2}\b)", mes)) >= 1:
        status = "CHARGED CC"
    elif len(findall(r"(\b\d{1,2}\b).(\b𝗖𝗵𝗮𝗿𝗴𝗲𝗱\b)", mes)) >= 1:
        status = "CHARGED CC"
    elif len(findall(r"(\b\d{1,2}\b).(\bcharged\b)", mes)) >= 1:
        status = "CHARGED CC"
    elif "incorrect cvc" in mes:
        status += " CCN"
    elif "invalid postal code" in mes:
        status += " INCORRECT POSTAL"
    elif "declined cvv" in mes:
        status += " DECLINED CVV"
    elif "insufficient fund" in mes or "not enough balance" in mes:
        status += " CVV LOW-FUNDS"
    elif "cvv" in message.lower():
        status += " CVV"

    credit_card = filter_cc(message)
    if len(credit_card) <= 3:
        return "null"

    text_1 = f"""
    [✯] Spytube Checker  
    ━━━━━━━━━━━━━━━━
    [✯] CC ↯  {credit_card}
    [✯] Status ↯  {status} ✅
    ━━━━━━━━━━━━━━━━
    [✯] Proxy  ↯  LIVE 🟩
    [✯] Leeched by ↯  @xCatBurglar [Premium]
    [✯] Bot by ↯  @x4rju9"""

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
                splited = response.split("\n")
                cc = ""
                for each in splited:
                    cc += each.strip() + "\n"
                await client.send_message(-1001769821742, cc, link_preview=False)

        # start bot
        client.start()
        client.run_until_disconnected()


if __name__ == "__main__":
    keep_alive()
    main()
