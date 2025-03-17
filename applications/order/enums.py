from conf.core.enums import CustomEnum


class OrderStatus(CustomEnum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING, "PENDING"),
            (cls.PREPARING, "PREPARING"),
            (cls.READY, "READY"),
            (cls.SERVED, "SERVED"),
            (cls.CANCELLED, "CANCELLED"),
        )

    @classmethod
    def default(cls):
        return cls.PENDING


class OrderMethod(CustomEnum):
    TAKE_OUT = "take_out"
    DINE_IN = "dine_in"
    DELIVERY = "delivery"

    @classmethod
    def choices(cls):
        return (
            (cls.TAKE_OUT, cls.TAKE_OUT.upper()),
            (cls.DINE_IN, cls.DINE_IN.upper()),
            (cls.DELIVERY, cls.DELIVERY.upper()),
        )

    @classmethod
    def default(cls):
        return cls.DINE_IN
