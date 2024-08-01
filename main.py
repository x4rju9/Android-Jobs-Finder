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
    'placify_Fam',
    'x4rju9'
]

def main():
    with TelegramClient(StringSession(ss), api_id, api_hash) as client:
    
        @client.on(events.NewMessage(chats = fuel))
        async def handler(event):
            job = event.raw_text
            result = isAndroidJob(job.lower())
    
            if result:
                await client.send_message('x4rju9', job, link_preview=False)
    
        
        client.start()
        client.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()
    main()
