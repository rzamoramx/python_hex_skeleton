
class SubscriptionVersionChangedException(Exception):
    def __init__(self):
        super().__init__("Subscription version changed")


class InvalidStoreIdException(Exception):
    def __init__(self, store_id):
        super().__init__(f"Invalid store id: {store_id}")
