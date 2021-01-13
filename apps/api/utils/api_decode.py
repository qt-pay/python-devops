import hashlib
import time
from django.conf import settings
from Crypto.Cipher import AES
import base64
import json
TOKEN_HISTORY = {}
def decrypt_get(http_token,):
    try:
        server_time = time.time()
        client_md5, client_time = http_token.split('|')
        client_time = float(client_time)
        if server_time - float(client_time) > 10:
            return {'code': 10200, 'data': '访问超时', 'message': '访问时间超时'}

        # 应该放到redis 设置过期时间
        if client_md5 in TOKEN_HISTORY:
            return {'code':10200, 'data':'key不可重复使用','message':'key不可重复使用'}

        tmp = f'{settings.CMDB_API_GET_KEY}|{client_time}'
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        serve_md5 = m.hexdigest()
        if client_md5 != serve_md5:
            return {'code': 10200, 'data': '验证未通过', 'message': '验证未通过'}
        return {'code': 2000, 'data': '验证通过', 'message': '验证通过'}
    except Exception as e:
        return {'code': 10200, 'data': str(e), 'message': 'error'}

def decrypt_post(message):
    try:
        text = message.encode(encoding='utf-8')  # 需要解密的文本
        ecrypted_base64 = base64.decodebytes(text)  # base64解码成字节流
        key = bytes(settings.CMDB_API_POST_KEY, encoding='utf-8')
        cipher = AES.new(key, AES.MODE_CBC, key)
        result = cipher.decrypt(ecrypted_base64)
        bytes_data = result[0:-result[-1]]
        str_data = str(bytes_data, encoding='utf-8')
        dic_data = json.loads(str_data)
        if isinstance(dic_data,dict) or isinstance(dic_data,list):
            return dic_data
    except Exception as e:
        return False