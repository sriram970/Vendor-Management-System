from django.urls import path, include

from vendor.views import create_or_list_all_vendors, get_or_edit_vendors


urlpatterns = [
    path('vendors/', create_or_list_all_vendors),
    path('vendors/<str:vendor_id>', get_or_edit_vendors),
]

"""
● POST / api/vendors /: Create a new vendor.
● GET / api/vendors /: List all vendors.
● GET / api/vendors/{vendor_id} /: Retrieve a specific vendor's details.
● PUT / api/vendors/{vendor_id} /: Update a vendor's details.
● DELETE / api/vendors/{vendor_id}/: Delete a vendor.
"""