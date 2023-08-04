
import asyncio
import unittest
from domain.store.adapters.StoreGoogleService import StoreGoogleService


class TestStoreGoogleService(unittest.TestCase):
    def test_retrieve_details_purchase(self):
        service = StoreGoogleService()
        asyncio.run(service.retrieve_details_purchase("test"))
