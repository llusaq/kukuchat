from django.core import signing

from channels.db import database_sync_to_async

from core.models import Contact, Chat


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


async def get_chat_for_provider_contact(prov_name, uid, name):
    try:
        contact = await database_sync_to_async(Contact.objects.get)(
            provider=prov_name,
            uid=uid,
        )
    except Contact.DoesNotExist:
        chat = await database_sync_to_async(Chat.objects.create)(
            name=name,
        )
        await database_sync_to_async(Contact.objects.create)(
            provider=prov_name,
            uid=uid,
            chat=chat,
        )
    else:
        chat = contact.chat
    return chat


async def turn_provider_contacts_into_chats(contact, uid_func, name_func, prov_name):
    ret = []
    for c in contact:
        uid = uid_func(c)
        name = name_func(c)

        def tmp():
            try:
                contact = Contact.objects.get(
                    provider=prov_name,
                    uid=uid,
                )
            except Contact.DoesNotExist:
                chat = Chat.objects.create(
                    name=name,
                )
                Contact.objects.create(
                    provider=prov_name,
                    uid=uid,
                    chat=chat,
                )
            else:
                chat = contact.chat
            return chat

        ret.append(await database_sync_to_async(tmp)())
    return ret
