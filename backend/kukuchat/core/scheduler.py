import functools

import asyncio


class Scheduler:

    def __init__(self, consumer):
        self.consumer = consumer

    async def _try_few_times(self, func, n=10):
        i = 0
        while True:
            try:
                res = await func()
            except Exception as e:
                print(e)
                i += 1
                if i < n:
                    return {}
                await asyncio.sleep(0.3)
            else:
                return res

    async def _get_messages_impl(self, chat_id, count):
        func = functools.partial(self.consumer.get_messages, {'chat_ids': [chat_id], 'count': count})
        msgs = await self._try_few_times(func)

        await self.consumer.send_json({'action': 'new_message', **msgs})

    async def _get_messages(self, provider, data):
        for c_id in data['chat_ids']:
            asyncio.create_task(self._get_messages_impl(c_id, data.get('count', 20)))

    async def add_task(self, data):
        method = f'_{data["method"]}'
        method = getattr(self, method)
        provider = getattr(self.consumer, data['provider'])
        await method(provider, data)
