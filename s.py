import requests
import json
import re
import os
import time
from timeit import default_timer as timer
import base64
import requests
import sys
import xmltodict
#import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
import subprocess

##### COLOR SETTINGS #####
os.system('')
GREEN = '\033[32m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
RED = '\033[31m'
CYAN = '\033[36m'
CYAN_BRIGHT = '\033[1;36m'
RESET = '\033[0m'
########################
print(f'''\n
  #####     ####  
 ##   ##   ##  ## 
 ##       ##      
  #####   ##      
      ##  ##  ### 
 ##   ##   ##  ## 
  #####     ##### 
                  

    -- SG Downloader --
       Contact Sam
    ''')

# Read the URLs from show_urls.tx

#url = pyperclip.paste()
url = input('Url:')
serialname = url
# Define the API endpoint URL
api_url = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

# Define common JSON data and headers
data = {
    'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDI0LTA4LTI1VDA3OjQ4OjU0LjQ5OVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTcyNDU3MjEzNH0.VXKJUa_PgJ1IWDznK5nYnYmAxrrTv_xRHMfLPj2SD7k',
    'Authorization': 'bearer eyJraWQiOiJkZjViZjBjOC02YTAxLTQ0MWEtOGY2MS0yMDllMjE2MGU4MTUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI4RTcxRTQ2Qy1EQUU0LTQ0RjEtQkZERS0xMEQyOEMwMjVEMDciLCJkZXZpY2VfaWQiOiJmMjJmYjUwMS00ZDM0LTQ2OTEtODkzMC1hNmJiY2I1NTlkNjYiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJpc3MiOiJodHRwczovL3VzZXJhcGkuemVlNS5jb20iLCJ2ZXJzaW9uIjo4LCJjbGllbnRfaWQiOiJyZWZyZXNoX3Rva2VuX2NsaWVudCIsImF1ZCI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwicHJvZmlsZWFwaSIsImdhbWUtcGxheSJdLCJ1c2VyX3R5cGUiOiJSZWdpc3RlcmVkIiwibmJmIjoxNzI0NTYxNTAyLCJ1c2VyX2lkIjoiOGU3MWU0NmMtZGFlNC00NGYxLWJmZGUtMTBkMjhjMDI1ZDA3Iiwic2NvcGUiOlsidXNlcmFwaSIsInN1YnNjcmlwdGlvbmFwaSIsInByb2ZpbGVhcGkiXSwic2Vzc2lvbl90eXBlIjoiR0VORVJBTCIsImV4cCI6MTcyNjI4OTUwMiwiaWF0IjoxNzI0NTYxNTAyLCJqdGkiOiI1YmZkZWI3YS0yZWE3LTRhZGMtYTdlNS1iYTQ3OTI2NmNmODIifQ.fzKjc-XONKo7VW2ACC1PlW7YzNs8n5mP7uZ2s5rfjwjxDbP4f4bvYBRuNmnpBmgWQbMVXKHEHLOyLKuKwUBm2ShMpuVm2UC-CEOnk_g5ZTEBrE-7j3sCn2f99kZ0i9Hkcp01o5o-n7bts4BJ6ARq6w1KFfTi_6mziJwMrzl9bac-iR9GN59F52IvwLVsZeXXIdTIevFmQZ6ytVDm9AcAAaIToe7tGesx7UAt8CNG5A8ldN8lwgNRWdf-psyJZ0Ed4GK8PcOdxnfG-Mw1von_ZcQUN6EY_bhwjZoFLzgjaHWv4gQe_u9QS7l-zKXuDv55NGkqEVCSQou_fU2Sa7AwnQ',
    'x-dd-token': 'eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ==',
}

m3u8DL_RE = './N_m3u8DL-RE'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Referer': 'https://www.zee5.com/',
    'Origin': 'https://www.zee5.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

# Loop through the URLs and make requests for each one
    # Remove leading/trailing whitespaces and newline characters
url = url.strip()

    # Split the URL by '/' and get the relevant parts
url_parts = url.split('/')

    # Extract the content_id and show_id from the URL
content_id = url_parts[-1]  # Last part of the URL
show_id = url_parts[-3]     # Second-to-last part of the URL

    # Define the payload data for this URL
payload = {
        "content_id": content_id,
        "show_id": show_id,
        "device_id": "cf06446c-3f2a-41d6-adfc-41985fdb9f86",
        "platform_name": "desktop_web",
        "translation": "en",
        "user_language": "en,hi,mr",
        "country": "IN",
        "state": "UT",
        "app_version": "4.0.3",
        "user_type": "premium",
        "check_parental_control": "false",
        "gender": "Male",
        'uid': 'c8d3cd8e-0e6f-40dd-be1d-f058025b9e74',
    	'ppid': 'cf06446c-3f2a-41d6-adfc-41985fdb9f86',
        "version": "12"
    }

    # Convert the JSON data dictionary to JSON format
json_data = json.dumps(data)

    # Make the POST request with JSON data, payload, and headers for this URL
response = requests.post(api_url, data=json_data, headers=headers, params=payload)

    # Check the response for this URL
if response.status_code == 200:
        # Request was successful
    try:
            # Parse the JSON response
            response_data = response.json()
            key_os_details = response_data.get("keyOsDetails", {})
            nl_data = key_os_details.get("nl")
            sdrm_data = key_os_details.get("sdrm")

            print(f"{nl_data}")
            print(f"{sdrm_data}")
    except json.JSONDecodeError:
            print(f"Failed to parse JSON response for URL '{url}'")
            
# Split the URL by '/' and get the relevant parts
url_parts = url.split('/')

# Extract the content_id and show_id from the URL
content_id = url_parts[-1]
url = "https://gwapi.zee5.com/content/details/" + content_id + "?translation=en&country=IN"
headers = {
    'authority': 'gwapi.zee5.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.zee5.com',
    'referer': 'https://www.zee5.com/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Opera";v="101", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
    'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDI0LTA4LTI1VDA3OjQ4OjU0LjQ5OVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTcyNDU3MjEzNH0.VXKJUa_PgJ1IWDznK5nYnYmAxrrTv_xRHMfLPj2SD7k',
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the response status code is not 200 (OK)
    
    data = response.json()  # Parse the JSON response

    # Check if the "video_details" field is present in the JSON data
    if "video_details" in data:
        video_details = data["video_details"]
        
        # Check if the "url" field is present in the video_details
        if "url" in video_details:
            url = video_details["url"]
            
            # Prepend the URL with the specified prefix
            mediacloudfront_url = "https://mediacloudfront.zee5.com" + url
            print("Media Cloudfront URL:", mediacloudfront_url)

            # Download the MPD manifest
            mpd_response = requests.get(mediacloudfront_url)
            mpd_response.raise_for_status()

            # Search for PSSH within <cenc:pssh> tags using regex
            pssh_matches = re.findall(r'<cenc:pssh>(.*?)</cenc:pssh>', mpd_response.text, re.DOTALL)
            
            if pssh_matches:
                shortest_pssh = min(pssh_matches, key=len)
                print("Shortest PSSH found in the MPD:")
                print(shortest_pssh)
            else:
                print("PSSH not found in the MPD.")
        else:
            print("The 'url' field is not present in the video_details.")
    else:
        print("The 'video_details' field is not present in the JSON response.")

except requests.exceptions.RequestException as e:
    print("Error making the GET request:", e)

except ValueError as e:
    print("Error parsing JSON response:", e)
    
# Define your headers here
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/octet-stream',
    'Referer': 'https://www.zee5.com/',
    'nl': nl_data,
    'customdata': sdrm_data,
    'Origin': 'https://www.zee5.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

pssh = shortest_pssh
lic_url = 'https://spapi.zee5.com/widevine/getLicense'
def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
    widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers)
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt

correct, keys = WV_Function(pssh, lic_url)

if keys:
                    for key in keys:
                        print("")
                        print(f"{GREEN}[+] OBTAINED KEYS: ")
                        print(f'{YELLOW}--key {key}')
                        print("")

for key in keys:
    ke_ys = ' '.join([f'--key {key}' for key in keys]).split()
    #print('--key ' + key)

# Use the pyperclip library to copy the key_string to the clipboard
#pyperclip.copy(key_string)


cd = os.getcwd()
name = "upload"

# Use the pyperclip library to copy the key_string to the clipboard
#pyperclip.copy(key_string)

try:
    os.remove("./video.mp4")
    os.remove("./video.mr.m4a")
except FileNotFoundError:
    pass

subprocess.run([m3u8DL_RE,
                '-M', 'format=mkv:muxer=mkvmerge',
                '-sv', 'res="1080*"', '-sa', 'best', '--concurrent-download',
                '--log-level', 'INFO',
                '--save-name', 'video', '--use-shaka-packager',
                mpd_response.url,  # Separate mpd_response.url from the previous options
                *ke_ys  
                ])
             
             
print("")
print(f"{RED}[+] Muxing Version 2 {RESET}")

subprocess.run([
            'ffmpeg',
            '-y', '-i', 'video.mp4',
            '-i', 'video.mr.m4a', 
            '-c', 'copy', 'upload.mp4'])

try:
    os.remove("./video.mp4")
    os.remove("./video.mr.m4a")
except FileNotFoundError:
    pass
print(f"{GREEN}[+] All Done :){RESET}")

time.sleep(1)

print(serialname)

if "jai" in serialname:
    title = "जय भीम"
    print(title)
    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
            'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
            #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
            'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
        }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "appi" in serialname :
    title = "अप्पी आमची"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "sara" in serialname :
    title = "सार काही"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "paaru" in serialname :
    title = "पारु"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "hitlerla" in serialname :
    title = "नवरी मिळे"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "shiva" in serialname :
    title = "शिवा"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "lakhat" in serialname :
    title = "आमचा दादा"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }
    
    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "shikvin" in serialname :
    title = "तुला शिकवीन"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }

    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")

elif "kartavya" in serialname :
    title = "पुन्हा कर्तव्य"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }
    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")
    
elif "saatvi" in serialname :
    title = "सात मुली"
    print(title)

    access = "EAAUrFf5aO5cBO5SUBf271vfWPHFti0bhlkQxPAI73v6w8nohdagYx4JYCsnOZC3fNX8jHmJalNasuZASYaZAjw4h2hNbLbv1ERWejgxm5JnLpg7CKQ14CyBDePIG2vLsoKt6KSKrcSgzvMUVoSivSPVNZC1uQQ4VjO7p5Ntb3ZBtDt6fMCZCxgAhTN9WzoZBbgIKMH9ZCvG30Eqw3IIZD"
    url='https://graph-video.facebook.com/109443242107502/videos?access_token='+str(access)
    #path="/home/abc.mp4"
    path="./upload.mp4"
    files={'file':open(path,'rb')}
    params = {
        'title': f'{title} नवा भाग पुढील भागसाठी follow करा',
        #'description' : f'{title} नवा भाग पुढील भागसाठी follow करा',
        'targeting': '{\n  "geo_locations": {\n    "regions": [\n      {\n        "key": "1735"\n      }\n    ]\n  }\n}'
    }
    start = timer()
    print(params)
    flag=requests.post(url, params=params, files=files)
    end = timer()
    print(flag.json)
    vidid = flag.json()["id"]
    print(vidid)
    colurl = f'https://graph.facebook.com/v20.0/{vidid}/collaborators'
    colabpara = {
      "access_token": access,
      "target_id": "111670005328457"
    }
    invite = requests.post(colurl, params=colabpara)
    print(invite.json)
    print(end - start) # Time in seconds, e.g. 5.38091952400282
    print(f"Upload Complete")