from django.urls import path, include

from purchase_order.views import create_or_list_all_purchase_orders, get_or_edit_purchase_orders


urlpatterns = [
    path('purchase_orders', create_or_list_all_purchase_orders),
    path('purchase_orders/<str:po_id>', get_or_edit_purchase_orders)
]


"""
● POST /api/purchase_orders/: Create a purchase order.
● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.
● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
● PUT /api/purchase_orders/{po_id}/: Update a purchase order.
● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
"""