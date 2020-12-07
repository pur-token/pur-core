# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import contextlib
from unittest import TestCase
from mock import Mock, MagicMock, patch

from pyqryptonight.pyqryptonight import StringToUInt256

from tests.misc.helper import get_alice_purss, get_random_purss
from pur.core import config
from pur.core.misc import logger
from pur.core.OptimizedAddressState import OptimizedAddressState
from pur.core.ESyncState import ESyncState
from pur.core.GenesisBlock import GenesisBlock
from pur.core.node import POW

from tests.misc.helper import replacement_getTime

logger.initialize_default()


@contextlib.contextmanager
def set_mining_enabled(new_value):
    old_value = config.user.mining_enabled
    try:
        config.user.mining_enabled = new_value
        yield
    finally:
        config.user.mining_enabled = old_value


@patch('pur.core.misc.ntp.getTime', new=replacement_getTime)
class TestNode(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNode, self).__init__(*args, **kwargs)

    def test_create(self):
        chain_manager = Mock()
        p2p_factory = Mock()
        sync_state = Mock()
        time_provider = Mock()

        node = POW(chain_manager=chain_manager,
                   p2p_factory=p2p_factory,
                   sync_state=sync_state,
                   time_provider=time_provider,
                   mining_address=get_random_purss().address,
                   mining_thread_count=0)

        self.assertIsNotNone(node)

    def test_sync_state_change_unsynced(self):
        chain_manager = Mock()
        p2p_factory = Mock()
        sync_state = Mock()
        time_provider = Mock()

        node = POW(chain_manager=chain_manager,
                   p2p_factory=p2p_factory,
                   sync_state=sync_state,
                   time_provider=time_provider,
                   mining_address=get_random_purss().address,
                   mining_thread_count=0)

        self.assertIsNotNone(node)
        node.update_node_state(ESyncState.unsynced)
        # FIpurE: Add more asserts

    def test_sync_state_change_syncing(self):
        chain_manager = Mock()
        p2p_factory = Mock()
        sync_state = Mock()
        time_provider = Mock()

        node = POW(chain_manager=chain_manager,
                   p2p_factory=p2p_factory,
                   sync_state=sync_state,
                   time_provider=time_provider,
                   mining_address=get_random_purss().address,
                   mining_thread_count=0)

        self.assertIsNotNone(node)
        node.update_node_state(ESyncState.syncing)
        # FIpurE: Add more asserts

    def test_sync_state_change_synced(self):
        chain_manager = Mock()
        chain_manager.height = 0
        chain_manager.get_block = MagicMock(return_value=GenesisBlock())
        chain_manager.last_block = GenesisBlock()
        chain_manager.tx_pool = Mock()
        chain_manager.tx_pool.transaction_pool = []
        chain_manager.tx_pool.transactions = chain_manager.tx_pool.transaction_pool

        get_block_metadata_response = Mock()
        get_block_metadata_response.block_difficulty = StringToUInt256('2')
        chain_manager.get_block_metadata = MagicMock(return_value=get_block_metadata_response)

        alice_purss = get_alice_purss()
        chain_manager._state.get_address_state = MagicMock(
            return_value=OptimizedAddressState.get_default(alice_purss.address))
        chain_manager._state.get_measurement = MagicMock(return_value=60)

        p2p_factory = Mock()
        sync_state = Mock()
        time_provider = Mock()
        # Setting mining enabled False, when update_note_state set to synced,
        # starts miner which is not exited properly by unit test
        with set_mining_enabled(False):
            node = POW(chain_manager=chain_manager,
                       p2p_factory=p2p_factory,
                       sync_state=sync_state,
                       time_provider=time_provider,
                       mining_address=get_random_purss().address,
                       mining_thread_count=0)

            self.assertIsNotNone(node)
            node.update_node_state(ESyncState.synced)
        # FIpurE: Add more asserts

    def test_sync_state_change_forked(self):
        chain_manager = Mock()
        p2p_factory = Mock()
        sync_state = Mock()
        time_provider = Mock()

        node = POW(chain_manager=chain_manager,
                   p2p_factory=p2p_factory,
                   sync_state=sync_state,
                   time_provider=time_provider,
                   mining_address=get_random_purss().address,
                   mining_thread_count=0)

        self.assertIsNotNone(node)
        node.update_node_state(ESyncState.forked)
        # FIpurE: Add more asserts
