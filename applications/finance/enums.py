from conf.core.enums import CustomEnum


class Source(CustomEnum):
    BANK = "bank"
    PAYSTACK = "paystack"
    MONNIFY = "monnify"

    @classmethod
    def choices(cls):
        return (
            (cls.BANK, "BANK"),
            (cls.PAYSTACK, "PAYSTACK"),
            (cls.MONNIFY, "MONNIFY"),
        )

    @classmethod
    def default(cls):
        return cls.BANK


class AccountType(CustomEnum):
    BANK = "bank"
    VIRTUAL = "virtual"

    @classmethod
    def choices(cls):
        return (
            (cls.BANK, "BANK"),
            (cls.VIRTUAL, "VIRTUAL"),
        )

    @classmethod
    def default(cls):
        return cls.BANK
