# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from unittest import TestCase

from tests.misc.helper import get_slave_purss
from pur.core.misc import logger
from pur.core.BlockMetadata import BlockMetadata
from pur.core.State import State

from tests.misc.helper import set_pur_dir, get_alice_purss

logger.initialize_default()

alice = get_alice_purss()
slave = get_slave_purss()


class TestTokenMetadata(TestCase):
    def setUp(self):
        with set_pur_dir('no_data'):
            self.state = State()

    def test_put_block_metadata(self):
        block_metadata = BlockMetadata.create()
        block_metadata.update_last_headerhashes([b'test1', b'test2'], b'test3')

        BlockMetadata.put_block_metadata(self.state, b'block_headerhash', block_metadata, None)
        BlockMetadata.put_block_metadata(self.state, b'block_headerhash2', BlockMetadata.create(), None)

        self.assertEqual(BlockMetadata.get_block_metadata(self.state, b'block_headerhash').to_json(),
                         block_metadata.to_json())

        expected_json = b'{\n  "blockDifficulty": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",\n  ' \
                        b'"cumulativeDifficulty": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="\n}'

        self.assertEqual(BlockMetadata.get_block_metadata(self.state, b'block_headerhash2').to_json(),
                         expected_json)

    def test_get_block_metadata(self):
        self.assertIsNone(BlockMetadata.get_block_metadata(self.state, b'test1'))
        BlockMetadata.put_block_metadata(self.state, b'block_headerhash2', BlockMetadata.create(), None)

        tmp_json = BlockMetadata.get_block_metadata(self.state, b'block_headerhash2').to_json()

        expected_json = b'{\n  "blockDifficulty": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",\n  ' \
                        b'"cumulativeDifficulty": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="\n}'

        self.assertEqual(tmp_json, expected_json)
