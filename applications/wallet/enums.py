from conf.core.enums import CustomEnum


class MerchantWalletType(CustomEnum):
    PRE_PAID = "pre-paid"
    POST_PAID = "post-paid"

    @classmethod
    def choices(cls):
        return (
            (cls.PRE_PAID, "PRE-PAID"),
            (cls.POST_PAID, "POST-PAID"),
        )

    @classmethod
    def default(cls):
        return cls.PRE_PAID


class WalletStatus(CustomEnum):
    ACTIVE = "active"
    DORMANT = "dormant"
    DEACTIVATED = "deactivated"
    DELETED = "deleted"

    @classmethod
    def choices(cls):
        return (
            (cls.ACTIVE, "ACTIVE"),
            (cls.DORMANT, "DORMANT"),
            (cls.DELETED, "DELETED"),
            (cls.DEACTIVATED, "DEACTIVATED"),
        )

    @classmethod
    def default(cls):
        return cls.ACTIVE


class TransactionDirection(CustomEnum):
    DEBIT = "debit"
    CREDIT = "credit"

    @classmethod
    def choices(cls):
        return (
            (cls.DEBIT, "DEBIT"),
            (cls.CREDIT, "CREDIT"),
        )

    @classmethod
    def default(cls):
        return cls.DEBIT


class TransactionStatus(CustomEnum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REVERSED = "reversed"

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING, "PENDING"),
            (cls.SUCCESSFUL, "SUCCESSFUL"),
            (cls.FAILED, "FAILED"),
            (cls.REVERSED, "REVERSED"),
        )

    @classmethod
    def default(cls):
        return cls.PENDING


class DepositStatus(TransactionStatus):
    pass


class CategoryType(CustomEnum):
    WALLET_DEPOSIT = "wallet_deposit"
    WALLET_WITHDRAWAL = "wallet_withdrawal"
    BANK_DEPOSIT = "bank_deposit"
    BANK_WITHDRAWAL = "bank_withdrawal"
    BONUS = "bonus"
    REFERRAL = "referral"

    @classmethod
    def choices(cls):
        return (
            (cls.WALLET_DEPOSIT, "WALLET DEPOSIT"),
            (cls.WALLET_WITHDRAWAL, "WALLET WITHDRAWAL"),
            (cls.BANK_DEPOSIT, "BANK DEPOSIT"),
            (cls.BANK_WITHDRAWAL, "BANK WITHDRAWAL"),
            (cls.BONUS, "BONUS"),
            (cls.REFERRAL, "REFERRAL"),
        )

    @classmethod
    def default(cls):
        return cls.WALLET_DEPOSIT


class TransactionCategory(CustomEnum):
    CUSTOMER_ORDER = "customer_order"
    CLIENT_ORDER_PAYMENT = "client_order_payment"
    SERVICE_ORDER_PAYMENT = "service_order_payment"
    SUBSCRIPTION = "subscription"
    WALLET_TOPUP = "wallet_topup"

    @classmethod
    def choices(cls):
        return (
            (cls.CUSTOMER_ORDER, cls.CUSTOMER_ORDER.upper()),
            (cls.SUBSCRIPTION, cls.SUBSCRIPTION.upper()),
            (cls.CLIENT_ORDER_PAYMENT, cls.CLIENT_ORDER_PAYMENT.upper()),
            (cls.SERVICE_ORDER_PAYMENT, cls.SERVICE_ORDER_PAYMENT.upper()),
            (cls.WALLET_TOPUP, cls.WALLET_TOPUP.upper()),
        )

    @classmethod
    def default(cls):
        return cls.CUSTOMER_ORDER
