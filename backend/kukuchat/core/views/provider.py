import json

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.providers import facebook, telegram


provider_mapping = {
    'telegram': telegram.TelegramProvider,
    'facebook': facebook.FacebookProvider,
}


@api_view(['GET'])
def get_avaliable_providers(request):
    providers_dirpath = f'{settings.BASE_DIR}/core/providers'
    providers = [
        {'name': k, 'credentials': v.get_required_credentials()}
        for k, v in provider_mapping.items()
    ]
    return Response({'providers': providers})


@api_view(['POST'])
def provider_interact(request, provider_name, provider_func_name):
    data = json.loads(request.body)
    provider = provider_mapping[provider_name]
    func = getattr(provider, provider_func_name)
    ret = func(**data)
    return Response(ret)
