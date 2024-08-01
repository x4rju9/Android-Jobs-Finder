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

def isAndroidJob(job):
    if "android" in job:
        return True
    elif "mobile" in job:
        return True
    elif "application" in job:
        return True
    elif "mobile app" in job:
        return True
    elif "android app" in job:
        return True
    elif "android developer" in job:
        return True
    elif "mobile developer" in job:
        return True
    elif "application developer" in job:
        return True
    elif "software application" in job:
        return True
    else:
        return False
    
    return False

def isApprovedCreditCard(cc):
    if "approved" in cc:
        return True
    elif "ccn" in cc:
        return True
    else:
        return False
    return False

fuel_android = [
    'TechUprise_Updates',
    'placify100',
    'internfreak',
    'JobPostingsIT',
    'gocareers',
    'JobSupportAndCodingDiscussions',
    'jobsinternshipswale',
    'jobs_and_internships_updates',
    'off_campus_jobs_and_internships',
    'the_placement_cafe',
    'opportunitycellofficial',
    'freshershunt',
    'placementkit',
    'oflatestblog',
    'engineerjobsindia',
    'hirelisting',
    'seekeraswfh',
    'Walkininterview_seekeras',
    'allcoding1_official',
    'goyalarsh',
    'offcampus_phodenge',
    'placify_Fam',
    'x4rju9'
]

fuel_credit_card = [
    -1001636378189,
    -1001910288205,
    -1001296359075,
    -1001118293322,
    -1001185460808,
    -1001542531535,
    -1001718470703,
    'x4rju9'
]

def main():
    with TelegramClient(StringSession(ss), api_id, api_hash) as client:

        @client.on(events.NewMessage(chats = fuel_android))
        async def android_jobs(event):
            job = event.raw_text
            result = isAndroidJob(job.lower())
    
            if result:
                await client.send_message('x4rju9', job, link_preview=False)

        @client.on(events.NewMessage(chats = fuel_android))
        async def full_stack_jobs(event):
            job = event.raw_text

            if "full stack" in job.lower():
                await client.send_message(-1002236063557, job, link_preview=False)

        @client.on(events.NewMessage(chats = fuel_credit_card))
        async def cc_leecher(event):
            cc = event.raw_text
            print(cc)
            result = isApprovedCreditCard(cc.lower())
    
            if result:
                await client.send_message(-1001242921653, cc, link_preview=False)
                await client.send_message(-1001769821742, cc, link_preview=False)
        
        @client.on(events.MessageEdited(chats = fuel_credit_card))
        async def cc_leecher_edited(event):
            cc = event.raw_text
            print(cc)
            result = isApprovedCreditCard(cc.lower())
    
            if result:
                await client.send_message(-1001242921653, cc, link_preview=False)
                await client.send_message(-1001769821742, cc, link_preview=False)

        # start bot
        client.start()
        client.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()
    main()
