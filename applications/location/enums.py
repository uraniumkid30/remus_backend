from conf.core.enums import CustomEnum


class States(CustomEnum):
    LAGOS = "Lagos"

    @classmethod
    def choices(cls):
        return (
            (cls.LAGOS, cls.LAGOS),
        )

    @classmethod
    def default(cls):
        return cls.LAGOS


class Countries(CustomEnum):
    NIGERIA = "Nigeria"

    @classmethod
    def choices(cls):
        return (
            (cls.NIGERIA, cls.NIGERIA.upper()),
        )

    @classmethod
    def default(cls):
        return cls.NIGERIA


class CountryCode(CustomEnum):
    NIGERIA = "NIG"

    @classmethod
    def choices(cls):
        return (
            (cls.NIGERIA, cls.NIGERIA),
        )

    @classmethod
    def default(cls):
        return cls.NIGERIA
