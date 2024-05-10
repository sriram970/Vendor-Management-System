from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST', 'GET'])
def create_or_list_all_purchase_orders():
    """
    This function used for creating and list all purchase orders
    """
    pass


@api_view(['PUT', 'GET', 'DELETE'])
def get_or_edit_purchase_orders():
    """
    This function used for get or edit or delete purchase orders.
    """
    pass
