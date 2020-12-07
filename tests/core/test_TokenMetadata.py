# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from mock import MagicMock
from unittest import TestCase
from pypurlib.pypurlib import sha2_256

from tests.misc.helper import get_slave_purss
from pur.core.misc import logger
from pur.core.State import State
from pur.core.txs.TransferTokenTransaction import TransferTokenTransaction
from pur.core.TokenMetadata import TokenMetadata

from tests.misc.helper import set_pur_dir, get_alice_purss, get_bob_purss, get_token_transaction

logger.initialize_default()

alice = get_alice_purss()
slave = get_slave_purss()


class TestTokenMetadata(TestCase):
    def setUp(self):
        with set_pur_dir('no_data'):
            self.state = State()

    def test_create_token_metadata(self):
        alice_purss = get_alice_purss()
        bob_purss = get_bob_purss()

        token_transaction = get_token_transaction(alice_purss, bob_purss)
        TokenMetadata.create_token_metadata(self.state, token_transaction, None)

        token_metadata = TokenMetadata.get_token_metadata(self.state, token_transaction.txhash)
        self.assertEqual(token_metadata.token_txhash, token_transaction.txhash)
        self.assertEqual(token_metadata.transfer_token_tx_hashes[0], token_transaction.txhash)

    def test_update_token_metadata(self):
        alice_purss = get_alice_purss()
        bob_purss = get_bob_purss()

        token_transaction = get_token_transaction(alice_purss, bob_purss)
        TokenMetadata.create_token_metadata(self.state, token_transaction, None)

        transfer_token_transaction = TransferTokenTransaction.create(token_txhash=token_transaction.txhash,
                                                                     addrs_to=[alice_purss.address],
                                                                     amounts=[100000000],
                                                                     fee=1,
                                                                     purss_pk=bob_purss.pk)

        TokenMetadata.update_token_metadata(self.state, transfer_token_transaction, None)

        token_metadata = TokenMetadata.get_token_metadata(self.state, token_transaction.txhash)
        self.assertEqual(len(token_metadata.transfer_token_tx_hashes), 2)
        self.assertEqual(token_metadata.transfer_token_tx_hashes[0], token_transaction.txhash)
        self.assertEqual(token_metadata.transfer_token_tx_hashes[1], transfer_token_transaction.txhash)

    def test_get_token_metadata(self):
        token_txhash = bytes(sha2_256(b'alpha'))
        token_metadata = TokenMetadata.create(token_txhash,
                                              [bytes(sha2_256(b'delta')),
                                               bytes(sha2_256(b'gamma'))])
        self.state._db.get_raw = MagicMock(return_value=token_metadata.serialize())
        self.assertEqual(TokenMetadata.get_token_metadata(self.state, token_txhash).to_json(),
                         token_metadata.to_json())

    def test_remove_transfer_token_metadata(self):
        alice_purss = get_alice_purss()
        bob_purss = get_bob_purss()

        token_transaction = get_token_transaction(alice_purss, bob_purss)
        TokenMetadata.create_token_metadata(self.state, token_transaction, None)

        transfer_token = TransferTokenTransaction.create(token_txhash=token_transaction.txhash,
                                                         addrs_to=[alice_purss.address],
                                                         amounts=[100000000],
                                                         fee=1,
                                                         purss_pk=bob_purss.pk)
        transfer_token.sign(alice_purss)

        TokenMetadata.update_token_metadata(self.state, transfer_token, None)
        token_metadata = TokenMetadata.get_token_metadata(self.state, transfer_token.token_txhash)
        self.assertIn(transfer_token.txhash,
                      token_metadata.transfer_token_tx_hashes)

        TokenMetadata.remove_transfer_token_metadata(self.state, transfer_token, None)
        token_metadata = TokenMetadata.get_token_metadata(self.state, transfer_token.token_txhash)
        self.assertNotIn(transfer_token.txhash,
                         token_metadata.transfer_token_tx_hashes)

    def test_remove_token_metadata(self):
        alice_purss = get_alice_purss()
        bob_purss = get_bob_purss()

        token_tx = get_token_transaction(alice_purss, bob_purss)
        TokenMetadata.create_token_metadata(self.state, token_tx, None)

        token_metadata = TokenMetadata.get_token_metadata(self.state, token_tx.txhash)
        self.assertEqual(token_metadata.token_txhash, token_tx.txhash)
        TokenMetadata.remove_token_metadata(self.state, token_tx, None)
        self.assertIsNone(TokenMetadata.get_token_metadata(self.state, token_tx.txhash))
