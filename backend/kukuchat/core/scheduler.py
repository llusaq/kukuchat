class Scheduler:

    def __init__(self, consumer):
        self.consumer = consumer

    async def _get_messages(self, provider, data):
        for c_id in data['chat_ids']:
            msgs = await self.consumer.get_messages({'chat_ids': [c_id]})
            await self.consumer.send_json(msgs)

    async def add_task(self, data):
        method = f'_{data["method"]}'
        method = getattr(self, method)
        provider = getattr(self.consumer, data['provider'])
        await method(provider, data)
