from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events

# Credentials.
api_id = ''
api_hash = ''
ss = ''
apis = []

try:
    apiss = open('api.txt', 'r')
    apis = apiss.readlines()
    apiss.close()
except:
    apiss = open('api.txt', 'w')
    apiss.close()
    apiss = open('api.txt', 'r')
    apis = apiss.readlines()
    apiss.close()


if apis == []:
    print("Note: These Credentials will be saved for later use!")
    print("You can delete 'api.txt' to login from different account.")
    api_id = int(input("API ID: "))
    api_hash = input("API HASH: ")

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        ss = client.session.save()
    api_id = int(str(api_id).replace(" ", ""))
    api_hash = api_hash.replace(" ", "")
    apiss = open('api.txt', 'w')
    apiss.write(str(api_id)+"\n")
    apiss.write(api_hash+'\n'+ss)
    apiss.close()
    system('cls')

elif len(apis) == 2:
    api_id = int(apis[0])
    api_hash = apis[1]

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        ss = client.session.save()
    apiss = open('api.txt', 'a')
    apiss.write(f'\n{ss}')
    apiss.close()
    system('cls')

elif len(apis) == 3:
    api_id = int(apis[0])
    api_hash = apis[1]
    ss = apis[2]



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

fuel = [
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
    'x4rju9'
]

with TelegramClient(StringSession(ss), api_id, api_hash) as client:

    @client.on(events.NewMessage(chats = fuel))
    async def handler(event):
        job = event.raw_text
        result = isAndroidJob(job.lower())

        if result:
            await client.send_message('x4rju9', job, link_preview=False)

    
    client.start()
    client.run_until_disconnected()