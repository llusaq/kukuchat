from django.core import signing

from channels.db import database_sync_to_async


async def autolog(user, providers):
    for provider in providers:
        name, prov_obj = provider
        credentials = signing.loads(user.credentials)
        try:
            credentials = credentials[name]
        except KeyError:
            continue
        await prov_obj.login(credentials)


async def store_creds(user, prov_inst, data):
    new_creds = {prov_inst.name: {name: data[name] for name in prov_inst._required_credentials}}
    user_creds = {} if not user.credentials else signing.loads(user.credentials)
    user_creds.update(new_creds)
    user.credentials = signing.dumps(user_creds)
    user.save()
