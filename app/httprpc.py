# -*- coding:utf-8 -*-

import json
import aiohttp
from .asyncrpc import RPCError
from bitsharesbase.chains import known_chains

class HttpRPC(object):
    ''' 短链接RPC客户端
    '''

    def __init__(self, access, loop=None):
        self._url = 'https://' + access
        self._loop = loop

    async def _rpc(self, method, params):
        ''' 远程过程调用
        '''
        # 生成请求内容
        request = {'id': 1, 'method': method, 'params': params}

        # 异步执行请求
        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, json=request) as resp:
                # 格式化返回结果
                ret = json.loads(await resp.text())
                if 'error' in ret:
                    if 'detail' in ret['error']:
                        raise RPCError(ret['error']['detail'])
                    else:
                        raise RPCError(ret['error']['message'])
                return ret['result']

    def __getattr__(self, name):
        ''' 简化方法调用
        '''
        async def method(*args, **kwargs):
            return await self._rpc(name, [*args])
        return method
