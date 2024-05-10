from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from vendor.models import VendorModel
import json
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST', 'GET'])
def create_or_list_all_vendors(request):
    data = {}

    if request.method == 'POST':
        try:
            # Load JSON data from the request
            vendor_data = json.loads(request.body)
            
            # Create a new vendor instance dynamically
            new_vendor = VendorModel()
            fields = {f.name: f for f in VendorModel._meta.fields}
            
            for field_name in fields:
                if field_name in vendor_data:
                    setattr(new_vendor, field_name, vendor_data[field_name])
            
            new_vendor.save()
            data['message'] = 'Vendor created successfully!'
            data['vendor'] = model_to_dict(new_vendor)  # Convert the vendor model instance to a dictionary
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        vendors = VendorModel.objects.all()
        vendors_list = [model_to_dict(vendor) for vendor in vendors]
        data['vendors'] = vendors_list

    return JsonResponse(data)


@api_view(['GET', 'PUT', 'DELETE'])
def get_or_edit_vendors(request):
    vendor_id = request.GET.get('vendor_id', None)

    if vendor_id is None:
        return JsonResponse({'error': 'Missing vendor_id'}, status=400)

    try:
        vendor = VendorModel.objects.get(vendor_code=vendor_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'GET':
        # Use Django's model_to_dict to automatically convert the model instance to a dictionary
        vendor_data = model_to_dict(vendor)
        return JsonResponse(vendor_data)

    elif request.method == 'PUT':
        # Update the vendor details
        try:
            updated_data = json.loads(request.body)
            for key, value in updated_data.items():
                if hasattr(vendor, key):  # Check if the attribute exists on the model before setting it
                    setattr(vendor, key, value)
            vendor.save()
            return JsonResponse({'message': 'Vendor updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        # Delete the vendor
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

    