from conf.core.enums import CustomEnum


class ProductStatus(CustomEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

    @classmethod
    def choices(cls):
        return (
            (cls.UNAVAILABLE, 'UNAVAILABLE'),
            (cls.AVAILABLE, 'AVAILABLE'),
        )

    @classmethod
    def default(cls):
        return cls.UNAVAILABLE
