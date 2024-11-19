from django.shortcuts import get_object_or_404
from applications.merchant import models as merchant_models
from applications.merchant.services.qr_routing import (
    QRScanRouter,
    #check_pos_provider_and_trigger
)


def request_receipt(request, qrtag_id):
    qr_tag = get_object_or_404(
        merchant_models.QRTag.objects.select_related(
            "point_of_sale",
            "point_of_sale__store",
            "point_of_sale__store__merchant"
        ),
        id=qrtag_id
    )
    # integration_triggered = check_pos_provider_and_trigger(qr_tag)
    # if integration_triggered:
    #     qr_tag.refresh_from_db()
    action_router = QRScanRouter(
        qr_tag
    )
    return action_router.route()


def custom_route(request):
    return 
