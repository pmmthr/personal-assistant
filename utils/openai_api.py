import json

import aiohttp
import asyncio


async def req_async_openai(messages, _key):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'X-OpenAI-Client-User-Agent': '{"bindings_version": "0.25.0", "httplib": "requests", "lang": "python", "lang_version": "3.9.6", "platform": "macOS-10.16-x86_64-i386-64bit", "publisher": "openai", "uname": "Darwin 21.2.0 Darwin Kernel Version 21.2.0: Sun Nov 28 20:29:10 PST 2021; root:xnu-8019.61.5~1/RELEASE_ARM64_T8101 x86_64"}',
               'User-Agent': 'OpenAI/v1 PythonBindings/0.25.0',
               'Authorization': f'Bearer {_key}', 'Content-Type': 'application/json'}
    data = {"model": "gpt-3.5-turbo", "messages": messages}

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as resp:
            return await resp.json()


async def req_nalog_api(message):
    url = f'https://api-fns.ru/api/search?key=key&q={message}'
    # headers = {'X-OpenAI-Client-User-Agent': '{"bindings_version": "0.25.0", "httplib": "requests", "lang": "python", "lang_version": "3.9.6", "platform": "macOS-10.16-x86_64-i386-64bit", "publisher": "openai", "uname": "Darwin 21.2.0 Darwin Kernel Version 21.2.0: Sun Nov 28 20:29:10 PST 2021; root:xnu-8019.61.5~1/RELEASE_ARM64_T8101 x86_64"}',
    #            'User-Agent': 'OpenAI/v1 PythonBindings/0.25.0',
    #            'Authorization': f'Bearer {_key}', 'Content-Type': 'application/json'}
    data = {"key": 'key', "q": message}

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as resp:
            # print(await resp.text())
            # print( await resp.json())
            return await resp.json()

# asyncio.run(req_nalog_api(message='ООО «МИЦ «Известия»'))
