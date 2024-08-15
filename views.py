import pytesseract
import base64, urllib.parse, time
import requests, re, random, string, json
from requests_toolbelt import MultipartEncoder

c = 0
s = requests.session()
url = "https://zefoy.com"
COOKIES = {"Cookie": None}
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def DECRYPTION_BASE64(base64_code):
    return base64.b64decode(urllib.parse.unquote(base64_code[::-1])).decode()


def BYPASS_IKLAN_GOOGLE():
    with requests.Session() as r:
        r.headers.update(
            {
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': COOKIES["Cookie"],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Host': 'zefoy.com',
                'Sec-Fetch-Site': 'none',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            }
        )
        params = {
            'domain': 'zefoy.com',
            'callback': '_gfp_s_',
            'client': 'ca-pub-3192305768699763',
        }
        response = r.get('https://partner.googleadservices.com/gampad/cookie.js', params=params).text
        if '_gfp_s_' in str(response):
            json_cookies = json.loads(re.search('_gfp_s_\\((.*?)\\);', str(response)).group(1))
            return (f"_gads={json_cookies['_cookies_'][0]['_value_']}; __gpi={json_cookies['_cookies_'][1]['_value_']}")
        else:
            return ('_gads=; __gpi=;')
    
s.headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Host': 'zefoy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document'
}

r = s.get(url).text

captcha_image = re.search('src="(.*?)" onerror="imgOnError\\(\\)"', r).group(1).replace('amp;', '')
form = re.search('type="text" name="(.*?)"', str(r)).group(1)

s.headers.update(
    {
        'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in s.cookies.get_dict().items()]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
)

r2 = s.get('{}{}'.format(url, captcha_image))

with open('CAPTCHA.png', 'wb') as f:
    f.write(r2.content)

BYPASS_CAPTCHA = pytesseract.image_to_string("CAPTCHA.png")
BYPASS_CAPTCHA = BYPASS_CAPTCHA.replace('\n', '')

data = {
    form: BYPASS_CAPTCHA,
}

r3 = s.post('https://zefoy.com/', data = data).text


def lol():
    global c

    if 'placeholder="Enter Video URL"' in str(r3):
        video_form = re.search('name="(.*?)" placeholder="Enter Video URL"', str(r3)).group(1)
        post_action = re.findall('action="(.*?)">', str(r3))[3]

        COOKIES.update(
            {
                "Cookie": "; ".join([str(x)+"="+str(y) for x,y in s.cookies.get_dict().items()])
            }
        )

        boundary = '----WebKitFormBoundary' \
            + ''.join(random.sample(string.ascii_letters + string.digits, 16))

        s.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Cookie': f'{COOKIES["Cookie"]}; {BYPASS_IKLAN_GOOGLE()}; window_size=1280x601; user_agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36;',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Connection': 'keep-alive',
                'Origin': 'https://zefoy.com',
                'Sec-Fetch-Dest': 'empty',
                'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
                'Accept': '*/*'
            }
        )
        
        data = MultipartEncoder(
            {
                video_form: (None, video_url)
            }, boundary=boundary
        )
        

        response = s.post('https://zefoy.com/{}'.format(post_action), data = data).text
        base64_string = DECRYPTION_BASE64(response)


        if 'type="submit"' in str(base64_string):

            boundary = '----WebKitFormBoundary' \
                + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            s.headers.update(
                {
                    'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
                }
            )

            find_form_videoid = re.search('type="hidden" name="(.*?)" value="(\d+)"', str(base64_string))
            form_videoid, videoid = find_form_videoid.group(1), find_form_videoid.group(2)
            next_post_action = re.search('action="(.*?)"', str(base64_string)).group(1)

            data = MultipartEncoder(
                {
                    form_videoid: (None, videoid)
                }, boundary=boundary
            )
            

            response2 = s.post('https://zefoy.com/{}'.format(next_post_action), data = data).text
            base64_string2 = DECRYPTION_BASE64(response2)

            if 'Successfully 1000 views sent.' in str(base64_string2):
                c+=1
                print(f'Successfully 1000 views sent. - {c}', end = "\r")
            else:
                pass

        else:
            pass

    else:
        pass



if __name__ == '__main__':
    video_url = input("Link: ")
    tttt = 120

    while True:
        lol()
        time.sleep(tttt)
