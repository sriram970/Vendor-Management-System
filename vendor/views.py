from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST', 'GET'])
def create_or_list_all_vendors():
    pass


@api_view(['PUT', 'GET', 'DELETE'])
def get_or_edit_vendors():
    pass