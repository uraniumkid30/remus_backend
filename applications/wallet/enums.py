from conf.core.enums import CustomEnum

POS_PROVIDER = []


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
            (cls.ACTIVE, 'ACTIVE'),
            (cls.DORMANT, 'DORMANT'),
            (cls.DELETED, 'DELETED'),
            (cls.DEACTIVATED, 'DEACTIVATED'),
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


class WithdrawalStatusType(CustomEnum):
    APPROVED = "approved"
    DECLINED = "declined"
    DISBURSED = "disbursed"
    REQUESTED = "requested"

    @classmethod
    def choices(cls):
        return (
            (cls.APPROVED, 'APPROVED'),
            (cls.DECLINED, 'DECLINED'),
            (cls.DISBURSED, 'DISBURSED'),
            (cls.REQUESTED, 'REQUESTED'),
        )

    @classmethod
    def default(cls):
        return cls.REQUESTED


class TransactionStatus(CustomEnum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REVERSED = "reversed"

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING, 'PENDING'),
            (cls.SUCCESSFUL, 'SUCCESSFUL'),
            (cls.FAILED, 'FAILED'),
            (cls.REVERSED, 'REVERSED'),
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
