from enum import StrEnum


class LanguageEnum(StrEnum):
    EN = "en"
    UZ = "uz"
    RU = "ru"
    UNKNOWN = "unknown"

    @classmethod
    def langs(cls):
        return {lang.value: lang for lang in cls}