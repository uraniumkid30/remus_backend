import os
from datetime import timedelta, datetime
from abc import ABC, abstractmethod
from pytz import timezone as pytz_timezone

from applications.order.models import TableSession
from applications.merchant.enums import QRScanResult
from applications.merchant.models import QRScan
from applications.merchant.utils.subscriptions import (
    is_subscription_active,
)


class QRRoutingAction(ABC):
    def __init__(self, qr):
        self.qr = qr
        self.restaurant = qr.table.restaurant
        self.merchant = self.restaurant.merchant

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

    def _get_front_end_website(self):
        res = self.restaurant.platform_setting.website
        return res or self.restaurant.platform_setting.custom_link

    def perform_action(self):
        result = self._get_result()
        print(f"EVENT:QR scanned at {self.qr} - RESULT: {result}")
        QRScan.objects.create(
            qr=self.qr,
            result=result,
        )
        return self._get_redirect_url()


class QRRouteToInactiveSubscription(QRRoutingAction):

    def _get_result(self):
        return QRScanResult.INACTIVE_SUBSCRIPTION

    def _load_receipt(self):
        return None

    def _get_redirect_url(self):
        query_params = "?session=inactive_subscription"
        url = os.path.join(self._get_front_end_website(), query_params)
        return url

    def trigger_condition(self):
        restaurant = self.qr.table.restaurant
        return is_subscription_active({"restaurant": restaurant})


class QRRouteToMenu(QRRoutingAction):

    def _get_result(self):
        return QRScanResult.MENU_ROUTE

    def _load_receipt(self):
        return None

    def _get_redirect_url(self):
        session = TableSession.objects.create(table=self.qr.table)
        query_params = f"?session={session.id}"
        url = os.path.join(self._get_front_end_website(), query_params)
        return url

    def trigger_condition(self):
        previous_sessions = TableSession.objects.filter(table=self.qr.table)
        if previous_sessions.exists():
            previous_sess = previous_sessions.last()
            tz = pytz_timezone("Africa/Lagos")
            now = tz.localize(datetime.now())
            scan_difference = now - previous_sess.created_at
            return scan_difference > timedelta(seconds=8)
        return True


class QRScanRouter:
    def __init__(self, qr):
        self.qr = qr
        self.merchant = qr.table.restaurant.merchant
        self.routers = [
            QRRouteToInactiveSubscription(self.qr),
            QRRouteToMenu(self.qr),
        ]

    def route(self):
        try:
            for router in self.routers:
                if router.trigger_condition():
                    return router.perform_action()
        except Exception as err:
            print(err)
            print("Error in QR Scan router")
