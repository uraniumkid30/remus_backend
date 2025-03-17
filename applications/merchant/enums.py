from conf.core.enums import CustomEnum


class PaymentProvider(CustomEnum):
    # MONNIFY = "monnify"
    PAYSTACK = "paystack"

    @classmethod
    def choices(cls):
        return (
            # (cls.MONNIFY, "MONNIFY"),
            (cls.PAYSTACK, "PAYSATCK"),
        )

    @classmethod
    def default(cls):
        return cls.PAYSTACK


class SubscriptionStatus(CustomEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    @classmethod
    def choices(cls):
        return (
            (cls.ACTIVE, "Active"),
            (cls.PAUSED, "Paused"),
            (cls.CANCELLED, "Cancelled"),
            (cls.EXPIRED, "Expired"),
        )

    @classmethod
    def default(cls):
        return cls.PAUSED


class BillingCycle(CustomEnum):
    YEARLY = "yearly"
    MONTHLY = "monthly"
    ONE_TIME = "one_time"

    @classmethod
    def choices(cls):
        return (
            (cls.YEARLY, "Yearly"),
            (cls.MONTHLY, "Monthly"),
            (cls.ONE_TIME, "One_Time"),
        )

    @classmethod
    def default(cls):
        return cls.ONE_TIME


class SubscriptionPlan(CustomEnum):
    FREE = "free"
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    @classmethod
    def choices(cls):
        return (
            (cls.FREE, "Free"),
            (cls.BASIC, "Basic"),
            (cls.STANDARD, "Standard"),
            (cls.PREMIUM, "Premium"),
        )

    @classmethod
    def default(cls):
        return cls.FREE


class OrderVolume(CustomEnum):
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"
    TIER_3 = "TIER_3"
    TIER_4 = "TIER_4"
    TIER_5 = "TIER_5"

    @classmethod
    def choices(cls):
        return (
            (cls.TIER_1, "0 - 10,000"),
            (cls.TIER_2, "10,001 - 100,000"),
            (cls.TIER_3, "100,001 - 1,000,000"),
            (cls.TIER_4, "1,000,0001 - 5,000,000"),
            (cls.TIER_5, "5,000,001 - 1,000,000,000"),
        )

    @classmethod
    def default(cls):
        return cls.TIER_1


class QRScanResult(CustomEnum):
    INIT_PAYMENT = "init_payment"
    MENU_ROUTE = "menu_route"
    INACTIVE_SUBSCRIPTION = "inactive_subscription"

    @classmethod
    def choices(cls):
        return (
            (cls.INIT_PAYMENT, "INIT_PAYMENT"),
            (cls.MENU_ROUTE, "MENU_ROUTE"),
            (cls.INACTIVE_SUBSCRIPTION, "INACTIVE_SUBSCRIPTION"),
        )

    @classmethod
    def default(cls):
        return cls.MENU_ROUTE


class QRType(CustomEnum):
    DEFAULT_QR = "default_qr"
    ANIMATED_QR = "animated_qr"

    @classmethod
    def choices(cls):
        return (
            (cls.DEFAULT_QR, cls.DEFAULT_QR.upper()),
            (cls.ANIMATED_QR, cls.ANIMATED_QR.upper()),
        )

    @classmethod
    def default(cls):
        return cls.DEFAULT_QR


class DaysOfTheWeek(CustomEnum):
    SUNDAY = "sunday"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"

    @classmethod
    def choices(cls):
        return (
            (cls.SUNDAY, cls.SUNDAY.upper()),
            (cls.MONDAY, cls.MONDAY.upper()),
            (cls.TUESDAY, cls.TUESDAY.upper()),
            (cls.WEDNESDAY, cls.WEDNESDAY.upper()),
            (cls.THURSDAY, cls.THURSDAY.upper()),
            (cls.FRIDAY, cls.FRIDAY.upper()),
            (cls.SATURDAY, cls.SATURDAY.upper()),
        )

    @classmethod
    def default(cls):
        return cls.MONDAY
