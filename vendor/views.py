from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['POST', 'GET'])
def create_or_list_all_vendors(request):
    data = {}
    if request.method == 'POST':
        pass
    
    elif request.method == 'GET':
        pass
    
    return JsonResponse(data=data)


@api_view(['PUT', 'GET', 'DELETE'])
def get_or_edit_vendors(request):
    vendor_id = request.GET.get('vendor_id', None)
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    return JsonResponse(data={'message':vendor_id})
    