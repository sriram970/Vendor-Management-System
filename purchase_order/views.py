from django.forms import ValidationError, model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from purchase_order.models import PurchaseOrder
from vendor.models import VendorModel
import json
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST', 'GET'])
def create_or_list_all_purchase_orders(request):
    """
    Handles creating a new PurchaseOrder with a POST request or
    listing all PurchaseOrders with a GET request. Fields are handled dynamically.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vendor = VendorModel.objects.get(pk=data.pop('vendor', None))
            purchase_order = PurchaseOrder(vendor=vendor)  # Initialize with vendor first as it's a required ForeignKey

            # Set attributes dynamically based on what's provided in the request
            for field in PurchaseOrder._meta.fields:
                if field.name in data and field.name != 'vendor':
                    setattr(purchase_order, field.name, data[field.name])

            purchase_order.save()
            return JsonResponse({'message': 'Purchase Order created successfully', 'id': purchase_order.po_number}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        orders_data = [model_to_dict(order) for order in purchase_orders]
        return JsonResponse(orders_data, safe=False)  # `safe=False` is necessary to allow serializing arrays.

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@api_view(['GET', 'PUT', 'DELETE'])
def get_or_edit_purchase_orders(request):
    """
    Fetch, update, or delete a specific purchase order based on the po_number provided.
    Handles requests dynamically to adapt to changes in the model structure.
    """
    po_number = request.GET.get('po_number', None)
    if po_number is None:
        return JsonResponse({'error': 'Missing po_number'}, status=400)

    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Purchase order not found'}, status=404)

    if request.method == 'GET':
        # Dynamically return the details of the purchase order
        po_data = model_to_dict(purchase_order)
        return JsonResponse(po_data)

    elif request.method == 'PUT':
        # Update the purchase order details dynamically
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(purchase_order, key):  # Ensure the attribute exists before setting
                    setattr(purchase_order, key, value)
            purchase_order.save()
            return JsonResponse({'message': 'Purchase order updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e.messages)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        # Delete the purchase order
        purchase_order.delete()
        return JsonResponse({'message': 'Purchase order deleted successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

