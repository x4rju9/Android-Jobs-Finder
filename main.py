from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
import os
from keep_alive import keep_alive

# Credentials.
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
ss = os.environ.get('STRING_SESSION')

# Main

def getJobRole(job):
    if "android" in job:
        return "android"
    elif "mobile" in job:
        return "android"
    elif "application" in job:
        return "android"
    elif "mobile app" in job:
        return "android"
    elif "android app" in job:
        return "android"
    elif "android developer" in job:
        return "android"
    elif "mobile developer" in job:
        return "android"
    elif "application developer" in job:
        return "android"
    elif "software application" in job:
        return "android"
    elif "full stack" in job:
        return "full_stack"
    elif "fullstack" in job:
        return "full_stack"
    else:
        return "null"
    
    return "null"

def isApprovedCreditCard(cc):
    if "approved" in cc:
        return True
    else:
        return False
    return False

# Filter Jobs Channels
fuel_jobs = []
jobs = os.environ.get('JOBS').split(",")
for job in jobs:
	job = job.strip()
	if '-' in job:
		fuel_jobs.append(int(job))
	else:
		fuel_jobs.append(job)

# Filter CC Channels
fuel_credit_card = []
cc = os.environ.get('CC').split(",")
for c in cc:
	c = c.strip()
	if '-' in c:
		fuel_credit_card.append(int(c))
	else:
		fuel_credit_card.append(c)

# Filter Credit Cards From Each Message.
def filter_pattern(message):
    import re
    pattern1 = re.compile(r'(\b\d{16}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)', re.DOTALL)
    pattern2 = re.compile(r'(\b\d{16}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)', re.DOTALL)
    pattern3 = re.compile(r'(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)', re.DOTALL)
    pattern4 = re.compile(r'(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b).(\b\d{4}\b)[a-zA-Z\W]*?(\b\d{3,4}\b)[a-zA-Z\W]*?(\b\d{2}\b)[a-zA-Z\W]*?(\b\d{2,4}\b)', re.DOTALL)
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
    return result,pattern

def filter_cc(cc):
    matches, pattern = filter_pattern(cc)
    cc, mm, yy, cvv = "","","",""
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
            cc = ''.join(match[0:4])
            mm = match[4]
            yy = match[5]
            cvv = match[6]
        elif pattern == 4:
            cc = ''.join(match[0:4])
            mm = match[5]
            yy = match[6]
            cvv = match[4]
        if len(yy) < 4:
            yy = '20' + yy
    return f"{cc}|{mm}|{yy}|{cvv}"

def create_response(message):
    status = ""

    if "ccn" in message.lower():
        status = " CCN"
    elif "cvv" in message.lower():
        status = " CVV"

    text_1 = f"""
    [✯] Spytube Checker  
    ━━━━━━━━━━━━━━━━
    [✯] CC ↯  {filter_cc(message)}
    [✯] Status ↯  APPROVED{status} ✅
    ━━━━━━━━━━━━━━━━
    [✯] Proxy  ↯  LIVE 🟩
    [✯] Leeched by ↯  @xCatBurglar [Premium]
    [✯] Bot by ↯  @x4rju9"""

    return text_1

def main():
    with TelegramClient(StringSession(ss), api_id, api_hash) as client:

        @client.on(events.NewMessage(chats = fuel_jobs))
        async def find_jobs(event):
            job = event.raw_text
            result = getJobRole(job.lower())
    
            if "android" in result:
                await client.send_message('x4rju9', job, link_preview=False)
            elif "full_stack" in result:
                await client.send_message(-1002236063557, job, link_preview=False)

        @client.on(events.NewMessage(chats = fuel_credit_card))
        async def cc_leecher(event):
            cc = event.raw_text
            result = isApprovedCreditCard(cc.lower())
    
            if result:
                splited = create_response(cc).split("\n")
                cc = ""
                for each in splited:
                    cc += each.strip() + "\n"
                await client.send_message(-1001769821742, cc, link_preview=False)
        
        @client.on(events.MessageEdited(chats = fuel_credit_card))
        async def cc_leecher_edited(event):
            cc = event.raw_text
            result = isApprovedCreditCard(cc.lower())
    
            if result:
                splited = create_response(cc).split("\n")
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
