# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from mock import PropertyMock, patch
from unittest import TestCase
from math import ceil

from pur.core import config
from pur.core.misc import logger
from pur.core.State import State
from pur.core.OptimizedAddressState import OptimizedAddressState
from pur.core.PaginatedBitfield import PaginatedBitfield
from pur.core.AddressState import AddressState
from tests.misc.helper import get_alice_purss, get_slave_purss, set_pur_dir

logger.initialize_default()

alice = get_alice_purss()
slave = get_slave_purss()


class TestOptimizedAddressState(TestCase):
    def setUp(self):
        with set_pur_dir('no_data'):
            self.state = State()

    # TODO: Move this test to Optimized Address State
    def test_get_optimized_address_state(self):
        alice_purss = get_alice_purss()

        alice_address = alice_purss.address
        address_state = OptimizedAddressState.get_optimized_address_state(self.state, alice_address)
        self.assertTrue(isinstance(address_state.address, bytes))

        alice_address = bytearray(alice_purss.address)
        with self.assertRaises(TypeError):
            OptimizedAddressState.get_optimized_address_state(self.state, alice_address)

        alice_address = alice_purss.address
        address_state = OptimizedAddressState.get_optimized_address_state(self.state, alice_address)
        addresses_state = {
            alice_address: address_state
        }
        self.assertTrue(isinstance(address_state.address, bytes))
        AddressState.put_addresses_state(self.state, addresses_state)

        address_state = OptimizedAddressState.get_optimized_address_state(self.state, alice_address)
        self.assertTrue(isinstance(address_state.address, bytes))

    def test_get_optimized_address_state2(self):
        alice_purss = get_alice_purss()

        alice_address = alice_purss.address
        address_state = OptimizedAddressState.get_optimized_address_state(self.state, alice_address)
        addresses_state = {
            alice_address: address_state
        }
        self.assertTrue(isinstance(address_state.address, bytes))
        OptimizedAddressState.put_optimized_addresses_state(self.state, addresses_state)
        address_state = OptimizedAddressState.get_optimized_address_state(self.state, alice_address)
        self.assertTrue(isinstance(address_state.address, bytes))

    def test_update_used_page_in_address_state(self):
        alice_purss = get_alice_purss(4)
        address = alice_purss.address
        address_state = OptimizedAddressState.get_default(address)
        addresses_state = {address: address_state}
        paginated_bitfield = PaginatedBitfield(True, self.state._db)
        key = paginated_bitfield.generate_bitfield_key(address, 1)
        paginated_bitfield.update_used_page_in_address_state(address, addresses_state, 1)
        self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(0, 16):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            if i != 15:
                self.assertEqual(address_state.ots_bitfield_used_page, 0)
            else:
                self.assertEqual(address_state.ots_bitfield_used_page, 1)

        for i in range(0, 16):
            ots_bitfield = paginated_bitfield.key_value[key]
            ots_key_index = i % config.dev.ots_tracking_per_page
            offset = ots_key_index >> 3
            relative = ots_key_index % 8
            bitfield = bytearray(ots_bitfield[offset])
            self.assertEqual(bytes([bitfield[0] >> relative & 1]), b'\x01')

        self.assertEqual(address_state.ots_bitfield_used_page, 1)

    @patch('pur.core.config.DevConfig.ots_tracking_per_page', new_callable=PropertyMock, return_value=1024)
    @patch('pur.core.config.DevConfig.ots_bitfield_size', new_callable=PropertyMock)
    def test_update_used_page_in_address_state2(self, mock_ots_bitfield_size, mock_ots_tracking_per_page):
        mock_ots_bitfield_size.return_value = ceil(config.dev.ots_tracking_per_page / 8)

        alice_purss = get_alice_purss(12)
        address = alice_purss.address
        address_state = OptimizedAddressState.get_default(address)
        addresses_state = {address: address_state}
        paginated_bitfield = PaginatedBitfield(True, self.state._db)
        paginated_bitfield.update_used_page_in_address_state(address, addresses_state, 1)
        self.assertEqual(address_state.ots_bitfield_used_page, 0)

        factor = min(config.dev.ots_tracking_per_page, 2 ** alice_purss.height)
        for i in range(0, 2 ** alice_purss.height):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, (i + 1) // factor)

        self.assertEqual(address_state.ots_bitfield_used_page, 4)

    @patch('pur.core.config.DevConfig.ots_tracking_per_page', new_callable=PropertyMock, return_value=1024)
    @patch('pur.core.config.DevConfig.ots_bitfield_size', new_callable=PropertyMock)
    def test_update_used_page_in_address_state3(self, mock_ots_bitfield_size, mock_ots_tracking_per_page):
        mock_ots_bitfield_size.return_value = ceil(config.dev.ots_tracking_per_page / 8)

        alice_purss = get_alice_purss(12)
        address = alice_purss.address
        address_state = OptimizedAddressState.get_default(address)
        addresses_state = {address: address_state}
        paginated_bitfield = PaginatedBitfield(True, self.state._db)
        paginated_bitfield.update_used_page_in_address_state(address, addresses_state, 1)
        self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(3072, 2 ** alice_purss.height):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(2048, 3072):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(1024, 2048):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(0, 1024):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            if i + 1 == 1024:
                self.assertEqual(address_state.ots_bitfield_used_page, 4)

        self.assertEqual(address_state.ots_bitfield_used_page, 4)

    @patch('pur.core.config.DevConfig.ots_tracking_per_page', new_callable=PropertyMock, return_value=1024)
    @patch('pur.core.config.DevConfig.ots_bitfield_size', new_callable=PropertyMock)
    def test_update_used_page_in_address_state4(self, mock_ots_bitfield_size, mock_ots_tracking_per_page):
        mock_ots_bitfield_size.return_value = ceil(config.dev.ots_tracking_per_page / 8)

        alice_purss = get_alice_purss(12)
        address = alice_purss.address
        address_state = OptimizedAddressState.get_default(address)
        addresses_state = {address: address_state}
        paginated_bitfield = PaginatedBitfield(True, self.state._db)
        paginated_bitfield.update_used_page_in_address_state(address, addresses_state, 1)
        self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(2048, 3072):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(1024, 2048):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            self.assertEqual(address_state.ots_bitfield_used_page, 0)

        for i in range(0, 1024):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            if i + 1 == 1024:
                self.assertEqual(address_state.ots_bitfield_used_page, 3)

        for i in range(3072, 2 ** alice_purss.height):
            paginated_bitfield.set_ots_key(addresses_state, address, i)
            if i + 1 == 2 ** alice_purss.height:
                self.assertEqual(address_state.ots_bitfield_used_page, 4)
            else:
                self.assertEqual(address_state.ots_bitfield_used_page, 3)

        self.assertEqual(address_state.ots_bitfield_used_page, 4)
