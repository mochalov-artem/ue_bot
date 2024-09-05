from mega import crypto
from Crypto.Util import Counter
from Crypto.Cipher import AES
import aiohttp
import json


async def _api_request(self, data):
    params = {'id': self.sequence_num}
    self.sequence_num += 1

    if self.sid:
        params.update({'sid': self.sid})

    if not isinstance(data, list):
        data = [data]

    url = f'{self.schema}://g.api.{self.domain}/cs'

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, data=json.dumps(data), timeout=10) as resp:
            json_resp = await resp.json()

    return json_resp[0]


async def mega_func_2(f_id, file_key, m):
    file_data = m._api_request({'a': 'g', 'g': 1, 'n': f'{f_id}'})

    k = (file_key[0] ^ file_key[4], file_key[1] ^ file_key[5],
         file_key[2] ^ file_key[6], file_key[3] ^ file_key[7])
    iv = file_key[4:6] + (0, 0)
    file_url = file_data['g']

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            content = await response.read()

    k_str = crypto.a32_to_str(k)
    counter = Counter.new(128, initial_value=((iv[0] << 32) + iv[1]) << 64)
    aes = AES.new(k_str, AES.MODE_CTR, counter=counter)

    chunk = aes.decrypt(content)
    return chunk
