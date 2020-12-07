# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import contextlib
import os
import shutil
import tempfile
import time
from copy import deepcopy

import simplejson as json
from mock import mock
from pypurlib.pypurlib import purssFast
from pypurlib.pypurlib import bin2hstr, hstr2bin
from pyqryptonight.pyqryptonight import StringToUInt256

from pur.core import config
from pur.core.Block import Block
from pur.core.BlockMetadata import BlockMetadata
from pur.core.ChainManager import ChainManager
from pur.core.OptimizedAddressState import OptimizedAddressState
from pur.core.GenesisBlock import GenesisBlock
from pur.core.txs.Transaction import Transaction
from pur.core.txs.SlaveTransaction import SlaveTransaction
from pur.core.txs.TokenTransaction import TokenTransaction
from pur.crypto.purss import purSS
from pur.generated import pur_pb2


def replacement_getTime():
    return int(time.time())


@contextlib.contextmanager
def set_default_balance_size(new_value=100 * int(config.dev.shor_per_quanta)):
    old_value = config.dev.default_account_balance
    try:
        config.dev.default_account_balance = new_value
        yield
    finally:
        config.dev.default_account_balance = old_value


@contextlib.contextmanager
def set_hard_fork_block_number(hard_fork_index=0, new_value=1):
    old_value = config.dev.hard_fork_heights[hard_fork_index]
    try:
        config.dev.hard_fork_heights[hard_fork_index] = new_value
        yield
    finally:
        config.dev.hard_fork_heights[hard_fork_index] = old_value


@contextlib.contextmanager
def set_wallet_dir(wallet_name):
    dst_dir = tempfile.mkdtemp()
    prev_val = config.user.wallet_dir
    try:
        test_path = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(test_path, "..", "data", wallet_name)
        shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        config.user.wallet_dir = dst_dir
        yield dst_dir
    finally:
        shutil.rmtree(dst_dir)
        config.user.wallet_dir = prev_val


@contextlib.contextmanager
def set_pur_dir(data_name):
    dst_dir = tempfile.mkdtemp()
    prev_val = config.user.pur_dir
    try:
        test_path = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(test_path, "..", "data")
        src_dir = os.path.join(data_dir, data_name)
        shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        shutil.copy(os.path.join(data_dir, 'core', 'genesis.yml'), dst_dir)
        shutil.copy(os.path.join(data_dir, 'core', 'config.yml'), dst_dir)
        config.user.pur_dir = dst_dir
        yield dst_dir
    finally:
        shutil.rmtree(dst_dir)
        config.user.pur_dir = prev_val


def get_genesis_with_only_coin_base_txn(coin_base_reward_addr, dev_config):
    g = GenesisBlock()

    coin_base_tx = Transaction.from_pbdata(g.transactions[0])
    coin_base_tx.update_mining_address(coin_base_reward_addr)

    # Remove all other transaction except CoinBase txn
    del g.transactions[:]

    g.pbdata.transactions.extend([coin_base_tx.pbdata])
    g.blockheader.generate_headerhash(dev_config)

    return g


def read_data_file(filename):
    test_path = os.path.dirname(os.path.abspath(__file__))
    src_file = os.path.join(test_path, "..", "data", filename)
    with open(src_file, 'r') as f:
        return f.read()


@contextlib.contextmanager
def mocked_genesis():
    custom_genesis_block = deepcopy(GenesisBlock())
    with mock.patch('pur.core.GenesisBlock.GenesisBlock.instance'):
        GenesisBlock.instance = custom_genesis_block
        yield custom_genesis_block


@contextlib.contextmanager
def clean_genesis():
    data_name = "no_data"
    dst_dir = tempfile.mkdtemp()
    prev_val = config.user.pur_dir
    try:
        GenesisBlock.instance = None
        test_path = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(test_path, "..", "data", data_name)
        shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)
        config.user.pur_dir = dst_dir
        _ = GenesisBlock()  # noqa
        config.user.pur_dir = prev_val
        config.user = config.UserConfig(True)
        yield
    finally:
        shutil.rmtree(dst_dir)
        GenesisBlock.instance = None
        config.user.pur_dir = prev_val


def get_some_address(idx=0) -> bytes:
    seed = bytearray([i for i in range(48)])
    seed[0] = idx
    purss = purSS(purssFast(seed, 4))
    return purss.address


def get_alice_purss(purss_height=6) -> purSS:
    seed = bytes([i for i in range(48)])
    return purSS(purssFast(seed, purss_height))


def get_bob_purss(purss_height=6) -> purSS:
    seed = bytes([i + 5 for i in range(48)])
    return purSS(purssFast(seed, purss_height))


def get_slave_purss() -> purSS:
    purss_height = 6
    seed = bytes([i + 10 for i in range(48)])
    return purSS(purssFast(seed, purss_height))


def get_random_purss(purss_height=6) -> purSS:
    return purSS.from_height(purss_height)


def get_token_transaction(purss1, purss2, amount1=400000000, amount2=200000000, fee=1) -> TokenTransaction:
    initial_balances = list()
    initial_balances.append(pur_pb2.AddressAmount(address=purss1.address,
                                                  amount=amount1))
    initial_balances.append(pur_pb2.AddressAmount(address=purss2.address,
                                                  amount=amount2))

    return TokenTransaction.create(symbol=b'pur',
                                   name=b'Quantum Resistant Ledger',
                                   owner=purss1.address,
                                   decimals=4,
                                   initial_balances=initial_balances,
                                   fee=fee,
                                   purss_pk=purss1.pk)


def destroy_state():
    try:
        db_path = os.path.join(config.user.data_dir, config.dev.db_name)
        shutil.rmtree(db_path)
    except FileNotFoundError:
        pass


def get_slaves(alice_ots_index, txn_nonce):
    # [master_address: bytes, slave_seeds: list, slave_txn: json]

    slave_purss = get_slave_purss()
    alice_purss = get_alice_purss()

    alice_purss.set_ots_index(alice_ots_index)
    slave_txn = SlaveTransaction.create([slave_purss.pk],
                                        [1],
                                        0,
                                        alice_purss.pk)
    slave_txn._data.nonce = txn_nonce
    slave_txn.sign(alice_purss)

    slave_data = json.loads(json.dumps([bin2hstr(alice_purss.address), [slave_purss.extended_seed], slave_txn.to_json()]))
    slave_data[0] = bytes(hstr2bin(slave_data[0]))
    return slave_data


def get_random_master():
    random_master = get_random_purss(config.dev.purss_tree_height)
    slave_data = json.loads(json.dumps([bin2hstr(random_master.address), [random_master.extended_seed], None]))
    slave_data[0] = bytes(hstr2bin(slave_data[0]))
    return slave_data


def gen_blocks(block_count, state, miner_address):
    blocks = []
    block = None
    with mock.patch('pur.core.misc.ntp.getTime') as time_mock:
        time_mock.return_value = 1615270948
        addresses_state = dict()
        for i in range(0, block_count):
            if i == 0:
                block = GenesisBlock()
                for genesis_balance in GenesisBlock().genesis_balance:
                    bytes_addr = genesis_balance.address
                    addresses_state[bytes_addr] = OptimizedAddressState.get_default(bytes_addr)
                    addresses_state[bytes_addr]._data.balance = genesis_balance.balance
            else:
                block = Block.create(dev_config=config.dev,
                                     block_number=i,
                                     prev_headerhash=block.headerhash,
                                     prev_timestamp=block.timestamp,
                                     transactions=[],
                                     miner_address=miner_address,
                                     seed_height=None,
                                     seed_hash=None)
                addresses_set = ChainManager.set_affected_address(block)
                coin_base_tx = Transaction.from_pbdata(block.transactions[0])
                coin_base_tx.set_affected_address(addresses_set)

                chain_manager = ChainManager(state)
                state_container = chain_manager.new_state_container(addresses_set,
                                                                    block.block_number,
                                                                    False,
                                                                    None)
                coin_base_tx.apply(state, state_container)

                for tx_idx in range(1, len(block.transactions)):
                    tx = Transaction.from_pbdata(block.transactions[tx_idx])
                    if not chain_manager.update_state_container(tx, state_container):
                        return False
                    tx.apply(state, state_container)

                block.set_nonces(dev_config=config.dev, mining_nonce=10, extra_nonce=0)
            blocks.append(block)

            metadata = BlockMetadata()
            metadata.set_block_difficulty(StringToUInt256('256'))
            BlockMetadata.put_block_metadata(state, block.headerhash, metadata, None)

            Block.put_block(state, block, None)
            bm = pur_pb2.BlockNumberMapping(headerhash=block.headerhash,
                                            prev_headerhash=block.prev_headerhash)

            Block.put_block_number_mapping(state, block.block_number, bm, None)
            state.update_mainchain_height(block.block_number, None)
            OptimizedAddressState.put_optimized_addresses_state(state, addresses_state)

    return blocks
