from abc import ABC, abstractmethod

from django.shortcuts import redirect
from django.urls import reverse

from merchant.enums import QRScanResult
from merchant.models import QRTag as QRScan


class QRRoutingAction(ABC):
    def __init__(self, qr):
        self.qr = qr
        self.merchant = qr.point_of_sale.store.merchant

    @abstractmethod
    def trigger_condition(self):
        pass

    @abstractmethod
    def _get_result(self):
        pass

    @abstractmethod
    def _load_receipt(self):
        pass

    @abstractmethod
    def _get_redirect_url(self):
        pass

    def perform_action(self):
        result = self._get_result()
        print(f'EVENT:QR scanned at {self.qr} - RESULT: {result}')
        QRScan.objects.create(
            qr=self.qr,
            result=result,
        )
        redirect_to = self._get_redirect_url()
        return redirect(redirect_to)


class QRRouteToCustomRoute(QRRoutingAction):

    def _get_result(self):
        return QRScanResult.CUSTOM_ROUTE

    def _load_receipt(self):
        return None

    def _get_redirect_url(self):
        # return reverse(
        #     'merchant:custom_route',
        # )
        redirect(self.merchant.custom_link)

    def trigger_condition(self):
        return True


class QRScanRouter:
    def __init__(self, qr):
        self.qr = qr
        self.merchant = qr.point_of_sale.store.merchant
        self.routers = [
            QRRouteToCustomRoute(self.qr),
        ]

    def route(self):
        try:
            for router in self.routers:
                if router.trigger_condition():
                    return router.perform_action()
        except Exception:
            print('Error in QR Scan router')
