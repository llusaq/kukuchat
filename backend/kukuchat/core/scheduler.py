import asyncio


class Scheduler:

    def __init__(self, consumer):
        self.consumer = consumer

    async def _get_messages_impl(self, chat_id):
        msgs = await self.consumer.get_messages({'chat_ids': [chat_id]})
        await self.consumer.send_json(msgs)

    async def _get_messages(self, provider, data):
        for c_id in data['chat_ids']:
            asyncio.create_task(self._get_messages_impl(c_id))

    async def add_task(self, data):
        method = f'_{data["method"]}'
        method = getattr(self, method)
        provider = getattr(self.consumer, data['provider'])
        await method(provider, data)
