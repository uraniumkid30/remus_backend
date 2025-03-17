from conf.core.enums import CustomEnum


class UserRoles(CustomEnum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MERCHANT = "merchant"
    CHEF = "chef"
    WAITER = "waiter"

    @classmethod
    def choices(cls):
        return (
            (cls.CUSTOMER, "CUSTOMER"),
            (cls.ADMIN, "ADMIN"),
            (cls.MERCHANT, "MERCHANT"),
            (cls.CHEF, "CHEF"),
            (cls.WAITER, "WAITER")
        )

    @classmethod
    def default(cls):
        return cls.CUSTOMER
