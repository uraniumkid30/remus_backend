from conf.core.enums import CustomEnum


class UserRoles(CustomEnum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MERCHANT = "merchant"

    @classmethod
    def choices(cls):
        return (
            (cls.CUSTOMER, "CUSTOMER"),
            (cls.ADMIN, "ADMIN"),
            (cls.MERCHANT, "MERCHANT"),
        )

    @classmethod
    def default(cls):
        return cls.CUSTOMER


class VerificationStatus(CustomEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    FAILED = "failed"

    @classmethod
    def choices(cls):
        return (
            (cls.UNVERIFIED, "UNVERIFIED"),
            (cls.PENDING, "PENDING"),
            (cls.FAILED, "FAILED"),
            (cls.VERIFIED, "VERIFIED"),
        )

    @classmethod
    def default(cls):
        return cls.UNVERIFIED


class DocumentCategories(CustomEnum):
    UTILITY_BILL = "utility_bill"
    ID = "id"

    @classmethod
    def choices(cls):
        return (
            (cls.ID, "ID"),
            (cls.UTILITY_BILL, "UTILITY_BILL"),
        )

    @classmethod
    def default(cls):
        return cls.ID


class DocumentTypes(CustomEnum):
    NIN = "nin"
    DRIVERS_LICENSE = "drivers_licence"
    ELECTRICITY_BILL = "electricity_bill"
    WASTE_BILL = "waste_bill"

    @classmethod
    def choices(cls):
        return {
            DocumentCategories.ID: {
                cls.NIN: "NIN",
                cls.DRIVERS_LICENSE: "DRIVERS_LICENSE",
            },
            DocumentCategories.UTILITY_BILL: {
                cls.ELECTRICITY_BILL: "ELECTRICITY_BILL",
                cls.WASTE_BILL: "WASTE_BILL",
            }
        }

    @classmethod
    def default(cls):
        return cls.NIN
