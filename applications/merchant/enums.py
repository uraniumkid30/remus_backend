from conf.core.enums import CustomEnum


class PosProvider(CustomEnum):
    MONNIFY = "monnify"
    PAYSTACK = "paystack"

    @classmethod
    def choices(cls):
        return (
            (cls.MONNIFY, "MONNIFY"),
            (cls.PAYSTACK, "PAYSATCK"),
        )

    @classmethod
    def default(cls):
        return cls.MONNIFY


class SubscriptionStatus(CustomEnum):
    LIVE = "live"
    DEMO = "demo"
    TEST = "test"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return (
            (cls.LIVE, "Live"),
            (cls.DEMO, "Demo"),
            (cls.TEST, "Test"),
            (cls.CANCELLED, "Cancelled"),
        )

    @classmethod
    def default(cls):
        return cls.DEMO


class BillingCycle(CustomEnum):
    ONETIME = "onetime"
    YEARLY = "yearly"
    MONTHLY = "monthly"

    @classmethod
    def choices(cls):
        return (
            (cls.YEARLY, "Yearly"),
            (cls.MONTHLY, "Monthly"),
            (cls.ONETIME, "Onetime"),
        )

    @classmethod
    def default(cls):
        return cls.ONETIME


class SubscriptionType(CustomEnum):
    REMUS_PAYSTACK = "paystack"
    REMUS_MONNIFY = "monnify"

    @classmethod
    def choices(cls):
        return (
            (cls.REMUS_PAYSTACK, cls.REMUS_PAYSTACK.capitalize()),
            (cls.REMUS_MONNIFY, cls.REMUS_MONNIFY.capitalize()),
        )

    @classmethod
    def default(cls):
        return cls.REMUS_MONNIFY


class CategoryType(CustomEnum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    @classmethod
    def choices(cls):
        return (
            (cls.BASIC, "Basic"),
            (cls.STANDARD, "Standard"),
            (cls.PREMIUM, "Premium"),
        )

    @classmethod
    def default(cls):
        return cls.BASIC


class CategoryPrice(CustomEnum):
    ONETIME_BASIC = 1000000
    ONETIME_STANDARD = 2000000
    ONETIME_PREMIUM = 3000000
    YEARLY_BASIC = 120000
    YEARLY_STANDARD = 240000
    YEARLY_PREMIUM = 360000
    MONTHLY_BASIC = 10000
    MONTHLY_STANDARD = 20000
    MONTHLY_PREMIUM = 30000

    @classmethod
    def choices(cls):
        return cls.type_to_price()

    @classmethod
    def type_to_price(cls):
        return {
            BillingCycle.ONETIME: {
                cls.ONETIME_BASIC: f"BASIC #{cls.ONETIME_BASIC}",
                cls.ONETIME_STANDARD: f"STANDARD #{cls.ONETIME_STANDARD}",
                cls.ONETIME_PREMIUM: f"PREMIUM #{cls.ONETIME_PREMIUM}",
            },
            BillingCycle.YEARLY: {
                cls.YEARLY_BASIC: f"BASIC #{cls.YEARLY_BASIC}",
                cls.YEARLY_STANDARD: f"STANDARD #{cls.YEARLY_STANDARD}",
                cls.YEARLY_PREMIUM: f"PREMIUM #{cls.YEARLY_PREMIUM}",
            },
            BillingCycle.MONTHLY: {
                cls.MONTHLY_BASIC: f"BASIC #{cls.MONTHLY_BASIC}",
                cls.MONTHLY_STANDARD: f"STANDARD #{cls.MONTHLY_STANDARD}",
                cls.MONTHLY_PREMIUM: f"PREMIUM #{cls.MONTHLY_PREMIUM}",
            }
        }

    @classmethod
    def default(cls):
        return cls.ONETIME_BASIC


class CategoryMeta(CustomEnum):
    BASIC = [

    ]
    STANDARD = [

    ]
    PREMIUM = [

    ]

    @classmethod
    def choices(cls):
        return (
            (cls.BASIC, "Basic"),
            (cls.STANDARD, "Standard"),
            (cls.PREMIUM, "Premium"),
        )

    @classmethod
    def type_to_price(cls):
        return {
            CategoryType.BASIC: cls.BASIC,
            CategoryType.STANDARD: cls.STANDARD,
            CategoryType.PREMIUM: cls.PREMIUM,
        }

    @classmethod
    def default(cls):
        return cls.BASIC


class QRScanResult(CustomEnum):
    INIT_PAYMENT = "init_payment"
    CUSTOM_ROUTE = "custom_route"

    @classmethod
    def choices(cls):
        return (
            (cls.INIT_PAYMENT, "INIT_PAYMENT"),
            (cls.CUSTOM_ROUTE, "CUSTOM_ROUTE"),
        )

    @classmethod
    def default(cls):
        return cls.INIT_PAYMENT
