from unittest import TestCase

from mock import patch, Mock

from pur.core import config
from pur.core.Indexer import Indexer
from pur.core.misc import logger
from pur.core.State import State
from pur.core.StateContainer import StateContainer
from pur.core.OptimizedAddressState import OptimizedAddressState
from pur.core.txs.MessageTransaction import MessageTransaction
from tests.misc.helper import get_alice_purss, get_bob_purss, set_pur_dir

logger.initialize_default()


@patch('pur.core.txs.Transaction.logger')
class TestTransactionValidateSlave(TestCase):
    def setUp(self):
        with set_pur_dir('no_data'):
            self.state = State()

        self.alice = get_alice_purss()
        self.params = {
            "message_hash": b'Test Message',
            "addr_to": None,
            "fee": 1,
            "purss_pk": self.alice.pk
        }
        self.m_addr_state = Mock(autospec=OptimizedAddressState, name='addr_state', balance=200)
        self.m_addr_from_pk_state = Mock(autospec=OptimizedAddressState, name='addr_from_pk_state')

    def test_validate_slave_valid(self, m_logger):
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)
        result = tx.validate_slave(0)
        self.assertTrue(result)

    def test_validate_slave_master_addr_same_as_signing_addr(self, m_logger):
        self.params["master_addr"] = self.alice.address
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)
        result = tx.validate_slave(None)
        self.assertFalse(result)

    def test_validate_slave_signing_purss_state_has_no_slave_permissions_in_state(self, m_logger):
        bob = get_bob_purss()
        # Let's say Alice is Bob's master.
        self.params["master_addr"] = self.alice.address
        self.params["purss_pk"] = bob.pk

        # We need to add extra data to the mock AddressState.
        tx = MessageTransaction.create(**self.params)
        tx.sign(self.alice)
        state_container = StateContainer(addresses_state=dict(),
                                         tokens=Indexer(b'token', None),
                                         slaves=Indexer(b'slave', None),
                                         lattice_pk=Indexer(b'lattice_pk', None),
                                         multi_sig_spend_txs=dict(),
                                         votes_stats=dict(),
                                         block_number=1,
                                         total_coin_supply=1000,
                                         current_dev_config=config.dev,
                                         write_access=True,
                                         my_db=self.state._db,
                                         batch=None)
        result = tx.validate_slave(state_container)
        self.assertFalse(result)
