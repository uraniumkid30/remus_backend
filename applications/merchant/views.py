from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from applications.merchant import models as merchant_models
from applications.merchant.services.qr_routing import QRScanRouter


def request_menu(request, qrtag_id):
    qr_tag = get_object_or_404(
        merchant_models.QRTag.objects.select_related(
            "table", "table__restaurant", "table__restaurant__merchant"
        ),
        id=qrtag_id,
    )
    action_router = QRScanRouter(qr_tag)
    calculated_url = action_router.route()
    return redirect(calculated_url)
