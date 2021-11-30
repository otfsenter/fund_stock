import json
import requests
from fund_img import data2buffer

url_upload = 'https://sm.ms/api/v2/upload'


def is_success(resp):
    if resp.status_code == 200:
        origin_resp = resp.json()
        result = origin_resp.get('success')
        if result:
            return True, 'success'
        else:
            code = origin_resp.get('code')
            if code and code == 'image_repeated':
                return False, 'mage_repeated'
            else:
                reason = origin_resp.get('message')
                return False, str(reason)
    else:
        try:
            origin_resp = resp.json()
        except:
            pass
        return False, 'upload failed'


def get_token():
    a = open('smms_token.txt').read()
    return a.strip()


def upload_img():
    """
    :return: png url
    """
    secret_token = get_token()
    headers = {'Authorization': f'{secret_token}'}
    files = {
        'smfile': data2buffer(),
    }
    resp = requests.post(
        url=url_upload,
        headers=headers,
        files=files,
    )

    flag_success, msg = is_success(resp)
    if flag_success:
        a = json.loads(resp.text)
        png_url = a.get('data', {}).get('url', '')
        return png_url
    else:
        return msg


def main():
    url = upload_img()
    print(url)


if __name__ == '__main__':
    main()
