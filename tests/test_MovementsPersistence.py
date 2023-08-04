
import unittest
from domain.business_core.adapters.MovementsPersistence import MovementsPersistence
from domain.business_core.models.Movements import Movements


class TestMovementsPersistence(unittest.IsolatedAsyncioTestCase):
    movements = MovementsPersistence()

    async def test_update_field(self):
        await self.movements.update_field('ea72e616-ea5d-41b1-b3c2-9d99595b8915', 'status', 'P')

    async def test_save(self):
        movement = Movements(
            id='ea72e616-ea5d-41b1-b3c2-9d99595b8915',
            account_id='ea72e616-ea5d-41b1-b3c2-9d99595b8915',
            amount=10.0,
            concept='test',
            date='2021-09-01',
            movement_type='test',
            origin_contract='test',
            status='P',
            timestamp=1630454400000,
            transaction_id='ea72e616-ea5d-41b1-b3c2-9d99595b8915',
            type=201
        )
        
        await self.movements.save(movement)
        
        self.assertEqual(movement.id, 'ea72e616-ea5d-41b1-b3c2-9d99595b8915')
