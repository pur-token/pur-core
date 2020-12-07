# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase
from mock import MagicMock

from pur.core.LastTransactions import LastTransactions
from pur.core.misc import logger, db
from pur.core.State import State
from pur.core.txs.TransferTransaction import TransferTransaction
from pur.core.Block import Block

from tests.misc.helper import set_pur_dir, get_alice_purss, get_some_address

logger.initialize_default()


class TestLastTransactions(TestCase):
    def setUp(self):
        with set_pur_dir('no_data'):
            self.state = State()
        self.m_db = MagicMock(name='mock DB', autospec=db.DB)

    def test_update_last_tx(self):
        alice_purss = get_alice_purss()
        # Test Case: When there is no last txns
        self.assertEqual(LastTransactions.get_last_txs(self.state), [])

        block = Block()
        tx1 = TransferTransaction.create(addrs_to=[get_some_address(1), get_some_address(2)],
                                         amounts=[1, 2],
                                         message_data=None,
                                         fee=0,
                                         purss_pk=alice_purss.pk)
        block._data.transactions.extend([tx1.pbdata])
        LastTransactions._update_last_tx(self.state, block, None)
        last_txns = LastTransactions.get_last_txs(self.state)

        # Test Case: When there is only 1 last txns
        self.assertEqual(len(last_txns), 1)
        self.assertEqual(last_txns[0].to_json(), tx1.to_json())

        block = Block()
        tx2 = TransferTransaction.create(addrs_to=[get_some_address(2), get_some_address(3)],
                                         amounts=[1, 2],
                                         message_data=None,
                                         fee=0,
                                         purss_pk=alice_purss.pk)

        tx3 = TransferTransaction.create(addrs_to=[get_some_address(4), get_some_address(5)],
                                         amounts=[1, 2],
                                         message_data=None,
                                         fee=0,
                                         purss_pk=alice_purss.pk)
        block._data.transactions.extend([tx2.pbdata, tx3.pbdata])
        LastTransactions._update_last_tx(self.state, block, None)
        last_txns = LastTransactions.get_last_txs(self.state)

        # Test Case: When there are 3 last txns
        self.assertEqual(len(last_txns), 3)
        self.assertEqual(last_txns[0].to_json(),
                         tx3.to_json())
        self.assertEqual(last_txns[1].to_json(),
                         tx2.to_json())
        self.assertEqual(last_txns[2].to_json(),
                         tx1.to_json())

    def test_get_last_txs(self):
        self.assertEqual(LastTransactions.get_last_txs(self.state), [])

        alice_purss = get_alice_purss()
        block = Block()
        tx1 = TransferTransaction.create(addrs_to=[get_some_address(0), get_some_address(1)],
                                         amounts=[1, 2],
                                         message_data=None,
                                         fee=0,
                                         purss_pk=alice_purss.pk)
        block._data.transactions.extend([tx1.pbdata])
        LastTransactions._update_last_tx(self.state, block, None)
        last_txns = LastTransactions.get_last_txs(self.state)

        # Test Case: When there is only 1 last txns
        self.assertEqual(len(last_txns), 1)
        self.assertEqual(last_txns[0].to_json(), tx1.to_json())

    def test_remove_last_tx(self):
        # Test Case: When there is no last txns
        self.assertEqual(LastTransactions.get_last_txs(self.state), [])

        alice_purss = get_alice_purss()

        block = Block()
        tx1 = TransferTransaction.create(addrs_to=[get_some_address(1), get_some_address(2)],
                                         amounts=[1, 2],
                                         message_data=None,
                                         fee=0,
                                         purss_pk=alice_purss.pk)
        block._data.transactions.extend([tx1.pbdata])
        LastTransactions._update_last_tx(self.state, block, None)
        last_txns = LastTransactions.get_last_txs(self.state)

        self.assertEqual(last_txns[0].to_json(), tx1.to_json())

        LastTransactions._remove_last_tx(self.state, block, None)
        last_txns = LastTransactions.get_last_txs(self.state)
        self.assertEqual(last_txns, [])