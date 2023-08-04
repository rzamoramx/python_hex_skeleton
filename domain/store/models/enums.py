
class EnumAppleStatuses:
    ACTIVE = 1
    EXPIRED = 2
    RETRY_PERIOD = 3
    GRACE_PERIOD = 4
    CANCELED = 5


class EnumGoogleStatuses:
    PAYMENT_PENDING = 0
    PAYMENT_OK = 1
    FREE_TRIAL = 2
    PENDING_UPDATE_OR_DOWNGRADE = 3


class EnumLocalStatuses:
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    CANCELED = 'CANCELED'

    @staticmethod
    def from_apple(apple_status: int) -> str:
        mapping = {
            EnumAppleStatuses.ACTIVE: EnumLocalStatuses.ACTIVE,
            EnumAppleStatuses.EXPIRED: EnumLocalStatuses.EXPIRED,
            EnumAppleStatuses.RETRY_PERIOD: EnumLocalStatuses.ACTIVE,
            EnumAppleStatuses.GRACE_PERIOD: EnumLocalStatuses.ACTIVE,
            EnumAppleStatuses.CANCELED: EnumLocalStatuses.CANCELED,
        }
        return mapping.get(apple_status, None)

    @staticmethod
    def from_google(google_status: int) -> str:
        mapping = {
            EnumGoogleStatuses.PAYMENT_PENDING: EnumLocalStatuses.ACTIVE,
            EnumGoogleStatuses.PAYMENT_OK: EnumLocalStatuses.ACTIVE,
            EnumGoogleStatuses.FREE_TRIAL: EnumLocalStatuses.ACTIVE,
            EnumGoogleStatuses.PENDING_UPDATE_OR_DOWNGRADE: EnumLocalStatuses.ACTIVE,
        }

        return mapping.get(google_status, None)
