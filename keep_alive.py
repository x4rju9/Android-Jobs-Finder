from threading import Thread
from flask import Flask
import os
import time

PORT = os.environ.get("PORT")
start_time = time.time()
bot = Flask(__name__)

@bot.route("/")
def home():
    end_time = time.time()
    uptime_seconds = end_time - start_time
    uptime_minutes = uptime_seconds / 60
    return f"Bot uptime: {uptime_minutes:.2f} minutes"

@bot.route("/livetv/update")
def liveUpdate():
    json = """
    {
        "latestVersion": "1.1",
        "latestVersionCode": 2,
        "url": "https://index.4rju9.workers.dev/0:/liveTv/app-release.apk",
        "releaseNotes": [
            "- Fixed some major bugs.",
            "- Added Subtitle Feature: now you can enjoy both subbed and dubbed content.",
            "- Kindly update the app to the latest to enjoy it to the fullest."
        ]
    }
    """
    return json.strip()

@bot.route("/livetv/fetch")
def liveFetch():
  json = f"""
  {{
        "sports": {getLiveSports()},
        "entertainment": {getLiveEntertainment()},
        "movies": {getLiveMovies()},
        "music": {getLiveMusic()},
        "news": {getLiveNews()},
  }}
  """
  return json.strip()

def getLiveSports():
    json = """
    [
        {
            "title": "Willow HD",
            "quality": "Multi",
            "language": "English",
            "mediaType": "Mpd",
            "hasContent": "false",
            "hasDrm": "true",
            "logo": "https://github.com/4rju9/live/assets/63835760/c246051b-d0d2-4280-b2ae-1542d709ac35",
            "url": "https://cip4-2048b75120.linear-novi.stvacdn.spectrum.com/LIVE/1131/dash/cenc/WLLOHD_10364/manifest.mpd",
            "keyId": "ZlPAXkL8T6yPSdfL+ZSY/g",
            "key": "O4jyz/Ov/vILJlyEC6/AzA"
        },
        {
            "title": "Sports 18",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://v3img.voot.com/resizeMedium,w_1090,h_613/v3Storage/assets/sports18_khel_tray-1693931658589.jpg",
            "url": "https://prod-sports-hin-fa.jiocinema.com/bpk-tv/Sports18_1_HD_voot_MOB/Fallback/index.m3u8"
        },
        {
            "title": "Star Sports 1 HD",
            "quality": "Multi",
            "language": "Hindi",
            "mediaType": "Mpd",
            "hasContent": "false",
            "hasDrm": "true",
            "logo": "https://github.com/4rju9/live/assets/63835760/de58dbb4-3391-4d6c-8710-68fa4e9ce721",
            "url": "https://bpprod5linear.akamaized.net/bpk-tv/irdeto_com_Channel_252/output/manifest.mpd",
            "keyId": "ap5CBPP4V36/bnmzsYVz+A",
            "key": "eMog1vi+kE7sYcDprKPFEQ"
        },
        {
            "title": "Star Sports 2 HD",
            "quality": "Multi",
            "language": "English",
            "mediaType": "Mpd",
            "hasContent": "false",
            "hasDrm": "true",
            "logo": "https://github.com/4rju9/live/assets/63835760/905a981b-5216-4c98-b8d3-8d45b62eaaca",
            "url": "https://bpprod5linear.akamaized.net/bpk-tv/irdeto_com_Channel_251/output/manifest.mpd",
            "keyId": "vF6pUmmFU9qrqFeHAB1gkw",
            "key": "UofZ+COiRv2w7P7jjwCpKg"
        }
    ]
    """
    return json.strip()

def getLiveEntertainment():
    json = """
    [
        {
            "title": "Discovery HD",
            "quality": "Multi",
            "language": "Multi",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://github.com/4rju9/live/assets/63835760/67f30deb-b5ff-472e-a915-bcf1e9d90271",
            "url": "https://raw.githubusercontent.com/Maxmentor/Max-LiveTv-Web/main/api-discovery/Discovery_Channel.m3u8"
        },
        {
            "title": "Animal Planet",
            "quality": "Multi",
            "language": "Multi",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://github.com/4rju9/live/assets/63835760/ce19f9a3-2f1d-4dde-8206-4d0c26990bb9",
            "url": "https://raw.githubusercontent.com/Maxmentor/Max-LiveTv-Web/main/api-discovery/Animal_Planet.m3u8"
        },
        {
            "title": "Yamato Animations",
            "quality": "Multi",
            "language": "Multi",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://github.com/4rju9/live/assets/63835760/fe952534-91ba-4aad-b82c-ef8e73976fcb",
            "url": "https://yamatovideo-yamatoanimation-1-it.samsung.wurl.tv/playlist.m3u8"
        },
        {
            "title": "Sonic Tv",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://images.squarespace-cdn.com/content/v1/63becd303aee236fcf26d494/1673448832400-1HDU45UGPPEXX6T8YLJQ/Sonic_Dynamite_Poster.jpg?format=1500w",
            "url": "https://epg.provider.plex.tv/library/parts/5e20b730f2f8d5003d739db7-62ba4aaff663580a7238f327.m3u8?includeAllStreams=0&X-Plex-Product=Plex+Mediaverse&X-Plex-Token=siYANTQxuHwtbsjy1aXV"
        },
        {
            "title": "TG Juniors",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTt5jot95950X8iMkYfJB5RcewmXgE1Bw4VwruEbJy7kiBNbbwQiFc0rjRga_wPxNLm_v4&usqp=CAU",
            "url": "https://epg.provider.plex.tv/library/parts/5e20b730f2f8d5003d739db7-5f123330eca6a20040b328e8.m3u8?includeAllStreams=0&X-Plex-Product=Plex+Mediaverse&X-Plex-Token=ppyNxvvixxd_kBkPx8rZ"
        },
        {
            "title": "Cartoon Classics",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://m.media-amazon.com/images/S/pv-target-images/f0bdd60bec861b5473270cc0b72e58b72e313f738554402853dca990ea616d5f._UR1920,1080_CLs%7C1920,1080%7C/G/bundle/BottomRightCardGradient16x9.png,/G/01/digital/video/merch/subs/benefit-id/a-f/freewithads/logos/channels-logo-white.png%7C0,0,1920,1080+0,0,1920,1080+1466,847,375,117_.jpg",
            "url": "https://streams2.sofast.tv/ptnr-yupptv/title-CARTOON-TV-CLASSICS-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/d5543c06-5122-49a7-9662-32187f48aa2c/manifest.m3u8?ads.channel=6591&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728552204~exp=1728573804~acl=!*/ptnr-yupptv/title-CARTOON-TV-CLASSICS-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/d5543c06-5122-49a7-9662-32187f48aa2c/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_48_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_48_-1~hmac=1213dd2e6708a082de7c5d719e3fe599d9c478d584d1d3d0bdbe4c1558079b27&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=ENTERTAINMENT&ads.channel_name=CartoonTVClassics&ads.language=ENG&ads.user=0"
        },
        {
            "title": "Kidoodle Tv",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSq8QZBjve4NO06NwuUgrJG6aTGjKdujf6qQ&s",
            "url": "https://epg.provider.plex.tv/library/parts/5e20b730f2f8d5003d739db7-5eea605574085f0040ddc794.m3u8?includeAllStreams=0&X-Plex-Product=Plex+Mediaverse&X-Plex-Token=wdMD9Bz7wMsHghYQKAHU"
        },
        {
            "title": "Kiddo TV",
            "quality": "Multi",
            "language": "English",
            "mediaType": "m3u8",
            "hasContent": "false",
            "hasDrm": "false",
            "logo": "https://github.com/4rju9/live/assets/63835760/0eeb1582-0aa6-4688-b761-9ad09a27175f",
            "url": "https://streams2.sofast.tv/ptnr-yupptv/title-KIDDO-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/5bcf9d24-04f2-401d-a93f-7af54f29461a/manifest.m3u8?ads.channel=6471&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728552022~exp=1728573622~acl=!*/ptnr-yupptv/title-KIDDO-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/5bcf9d24-04f2-401d-a93f-7af54f29461a/*!..."
        }
    ]
    """
    return json

def getLiveMovies():
    json = """
    [
		{
			"title": "Shemaroo Bollywood",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://mms.businesswire.com/media/20220816005528/en/1545398/22/shemaroo.jpg",
			"url": "https://epg.provider.plex.tv/library/parts/5e20b730f2f8d5003d739db7-62d1a58e520656fda09e609d.m3u8?includeAllStreams=0&X-Plex-Product=Plex+Mediaverse&X-Plex-Token=Zd7PNPDpB5728txQy_ZC"
		},
		{
			"title": "Bhojpuri Cinema",
			"quality": "360p",
			"language": "Bhojpuri",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "data:image/png;base64,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",
			"url": "https://live-bhojpuri.akamaized.net/liveabr/pub-iobhojpuqbu6yj/live_360p/chunks.m3u8"
		},
        {
			"title": "Bollywood 4u",
			"quality": "Multi",
			"language": "Bangali",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://exchange4media.gumlet.io/news-photo/123954-big8.jpg",
			"url": "https://streams2.sofast.tv/ptnr-yupptv/title-BOLLYWOOD-4U-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/22d13e33-8705-40e8-9809-4e80aa795f15/manifest.m3u8?ads.channel=6604&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728551450~exp=1728573050~acl=!*/ptnr-yupptv/title-BOLLYWOOD-4U-ENG_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/22d13e33-8705-40e8-9809-4e80aa795f15/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_47_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_47_-1~hmac=0896a14a0af5abf9cc1410f8840f2b3be6f32a3329ca3d3fc954b5909b0d397e&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=ENTERTAINMENT&ads.channel_name=Bollywood4U&ads.language=HIN&ads.user=0"
		},
		{
			"title": "Enter 10 Bangla",
			"quality": "360p",
			"language": "Bangali",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "data:image/jpeg;base64,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",
			"url": "https://live-bangla.akamaized.net/liveabr/pub-iobanglakp3sff/live_360p/chunks.m3u8"
		}
	]
    """
    return json.strip()

def getLiveMusic():
    json = """
    [
		{
			"title": "9XM",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://github.com/4rju9/live/assets/63835760/72750f73-c58a-4aa8-a2e3-7dba218b5b45",
			"url": "https://d2q8p4pe5spbak.cloudfront.net/bpk-tv/9XM/9XM.isml/index.m3u8"
		},
		{
			"title": "9X Jhakaas",
			"quality": "Multi",
			"language": "Punjabi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://github.com/4rju9/live/assets/63835760/b9812e1d-f6e0-49ff-b93e-4f43b16be361",
			"url": "https://amg01281-9xmediapvtltd-9xjhakaas-samsungin-ci2cs.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjhakaas-samsungin/playlist.m3u8"
		},
		{
			"title": "9X Tashan",
			"quality": "Multi",
			"language": "Punjabi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://github.com/4rju9/live/assets/63835760/9bc3a63e-dc39-4f38-8d7e-8d19481977a9",
			"url": "https://amg01281-9xmediapvtltd-9xtashan-samsungin-xz1sd.amagi.tv/playlist/amg01281-9xmediapvtltd-9xtashan-samsungin/playlist.m3u8"
		},
		{
			"title": "9X Jalwa",
			"quality": "Multi",
			"language": "Punjabi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://github.com/4rju9/live/assets/63835760/bc4d37a4-b884-47aa-a0b2-d3a7ce4b8fcd",
			"url": "https://amg01281-9xmediapvtltd-9xjalwa-samsungin-goszf.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjalwa-samsungin/playlist.m3u8"
		},
		{
			"title": "Haryanvi Hits",
			"quality": "Multi",
			"language": "Haryanvi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://scontent.fbek1-4.fna.fbcdn.net/v/t39.30808-6/326921491_888183515731407_2309849597301984856_n.jpg?stp=dst-jpg_s960x960&_nc_cat=101&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=21b8pdeSTOsQ7kNvgHxMbVJ&_nc_ht=scontent.fbek1-4.fna&_nc_gid=AL_pIg3CpXGZMrzOxB7LwPy&oh=00_AYAKzNMogQSwzqugkJUaESF6MguOkX_wRz3z0eLAztDARQ&oe=670D6E35",
			"url": "https://yuppnimresmum.akamaized.net/28072023/smil:haryanvihits.smil/playlist.m3u8?ads.channel=6374&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728551745~exp=1728573345~acl=!*/28072023/smil:haryanvihits.smil/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_192_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_192_-1~hmac=51c1eed2841c90defc49b20c63390ffbbba5dc0ba5fc02d23c9b146a330956c3&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=MUSIC&ads.channel_name=HaryanviHits&ads.language=HIN&ads.user=0"
		},
		{
			"title": "Mastiii",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/dac9fa101578521.5f21d577e0ed7.jpg",
			"url": "https://sabliveyupp.akamaized.net/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/sablive_https/mastii/playlist.m3u8?ads.channel=5229&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728551586~exp=1728573186~acl=!*/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/sablive_https/mastii/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_23_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_23_-1~hmac=a5613ade63e7f369d0adc8c9096c7df233fc8dd3004cbf4b8f7a3811407e519c&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=MUSIC&ads.channel_name=Mastiii&ads.language=HIN&ads.user=0"
		},
		{
			"title": "ShowBox",
			"quality": "Multi",
			"language": "Multi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://i.ytimg.com/vi/gG_wUS6IIOc/maxresdefault.jpg",
			"url": "https://epiconvh.s.llnwi.net/live/showbox/master.m3u8?s=1728553857&e=1729849857&h=410c257468eb2d112f5280259f26964e&hls_force_no_caption_tag=true&filter=(type!=%22audio%22||systemBitrate%3E128000)"
		},
		{
			"title": "Zoom",
			"quality": "Multi",
			"language": "Multi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://blog.distro.tv/wp-content/uploads/2022/08/Blog-Covers-5.png",
			"url": "https://d1g66oqspoyxao.cloudfront.net/master.m3u8"
		}
	]
    """
    return json.strip()

def getLiveNews():
    json = """
    [
		{
			"title": "Aaj Tak Live",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSj8md-6ECp04gQUAvjEteic0nEEZcvVzEegg&usqp=CAU",
			"url": "https://feeds.intoday.in/aajtak/api/aajtakhd/master.m3u8"
		},
		{
			"title": "ABP News Live",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3GWCSyY3hyoNfKh7xdDWcVAU_c6J_bogaQA&usqp=CAU",
			"url": "https://abplivetv.akamaized.net/hls/live/2043010/hindi/master.m3u8"
		},
		{
			"title": "NDTV India Live",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://cdn.ndtv.com/common/images/ogndtv.png",
			"url": "https://ndtvindiaelemarchana.akamaized.net//hls//live//2003679//ndtvindia//ndtvindiamaster.m3u8"
		},
		{
			"title": "Republic Bharat",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://i0.wp.com/www.opindia.com/wp-content/uploads/2022/03/r_logo_1024x1024.png?w=1920&ssl=1",
			"url": "https://vg-republictvyupp.akamaized.net/ptnr-yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/vglive-sk-561573/main.m3u8?ads.channel=4923&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728552378~exp=1728573978~acl=!*/ptnr-yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/vglive-sk-561573/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_20_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_20_-1~hmac=26e9c99e094861340fa5e4663378f4c4955996a9e5837e7da11e0e46340b99e9&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=RepublicBharat&ads.language=HIN&ads.user=0"
		},
		{
			"title": "TV9 Bharatvarsh",
			"quality": "Multi",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://cdn.myportfolio.com/822c501a1f7e2b70f9df29f21633dffc/037cb243-64df-4639-bd24-e69e01cd3d55_rw_1920.jpg?h=147d0b24e40d329d24312deb7c1c62f2",
			"url": "https://vg-tv9yupp.akamaized.net/ptnr-yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/vglive-sk-234604/main.m3u8?ads.channel=6377&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728552474~exp=1728574074~acl=!*/ptnr-yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/vglive-sk-234604/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_34_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_34_-1~hmac=931e692a386ace6eb34df296812dab12839801788e3759fbbff543c696de4956&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=TV9Bharatvarsh&ads.language=HIN&ads.user=0"
		},
		{
			"title": "Hindi Khabar",
			"quality": 360p",
			"language": "Hindi",
			"mediaType": "m3u8",
			"hasContent": "false",
			"hasDrm": "false",
			"logo": "https://samachar4media.gumlet.io/60445-Hindi.jpg",
			"url": "https://yuppftalive.akamaized.net/080823/hindikhabar/playlist.m3u8?ads.channel=6425&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1728552535~exp=1728574135~acl=!*/080823/hindikhabar/*!/payload/yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_160_-1/*~data=yupptvott_5_-1_b403087ecd3e48e0_IN_110.226.197.87_yuppfast_2_channel_160_-1~hmac=5dac8bac513aff8f553b74188b8320366696a61eb522fb2f61cdc7299d09cedd&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=HindiKhabar&ads.language=HIN&ads.user=0"
		}
	]
    """
    return json.strip()

def run():
    bot.run(host="0.0.0.0", port=PORT)

def keep_alive():
    t = Thread(target=run)
    t.start()
