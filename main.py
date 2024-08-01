from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from dotenv import load_dotenv
from os import getenv

# Credentials.
api_id = int(getenv('API_ID'))
api_hash = getenv('API_HASH')
ss = getenv('STRING_SESSION')

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
