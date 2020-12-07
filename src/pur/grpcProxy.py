# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import argparse
import os
import simplejson as json
import grpc
from google.protobuf.json_format import MessageToJson
from pur.core import config
from pur.core.AddressState import AddressState
from pur.crypto.purss import purSS
from pur.core.txs.Transaction import Transaction
from pur.core.txs.TransferTransaction import TransferTransaction
from pypurlib.pypurlib import hstr2bin, bin2hstr

from pur.generated import pur_pb2_grpc, pur_pb2, purmining_pb2, purmining_pb2_grpc
from flask import Flask, Response, request
from jsonrpc.backend.flask import api

app = Flask(__name__)


def read_slaves(slaves_filename):
    with open(slaves_filename, 'r') as f:
        slave_data = json.load(f)
        slave_data[0] = bytes(hstr2bin(slave_data[0]))
        return slave_data


def get_addr_state(addr: bytes) -> AddressState:
    stub = get_public_stub()
    response = stub.GetAddressState(request=pur_pb2.GetAddressStateReq(address=addr))
    return AddressState(response.state)


def set_unused_ots_key(purss, addr_state, start=0):
    for i in range(start, 2 ** purss.height):
        if not addr_state.ots_key_reuse(i):
            purss.set_ots_index(i)
            return True
    return False


def valid_payment_permission(public_stub, master_address_state, payment_purss, json_slave_txn):
    access_type = master_address_state.get_slave_permission(payment_purss.pk)

    if access_type == -1:
        tx = Transaction.from_json(json_slave_txn)
        public_stub.PushTransaction(request=pur_pb2.PushTransactionReq(transaction_signed=tx.pbdata))
        return None

    if access_type == 0:
        return True

    return False


def get_unused_payment_purss(public_stub):
    global payment_slaves
    global payment_purss

    master_address = payment_slaves[0]
    master_address_state = get_addr_state(master_address)

    if payment_purss:
        addr_state = get_addr_state(payment_purss.address)
        if set_unused_ots_key(payment_purss, addr_state, payment_purss.ots_index):
            if valid_payment_permission(public_stub, master_address_state, payment_purss, payment_slaves[2]):
                return payment_purss
        else:
            payment_purss = None

    if not payment_purss:
        unused_ots_found = False
        for slave_seed in payment_slaves[1]:
            purss = purSS.from_extended_seed(slave_seed)
            addr_state = get_addr_state(purss.address)
            if set_unused_ots_key(purss, addr_state):  # Unused ots_key_found
                payment_purss = purss
                unused_ots_found = True
                break

        if not unused_ots_found:  # Unused ots_key_found
            return None

    if not valid_payment_permission(public_stub, master_address_state, payment_purss, payment_slaves[2]):
        return None

    return payment_purss


@app.route('/api/<api_method_name>')
def api_proxy(api_method_name):
    """
    Proxy JSON RPC requests to the gRPC server as well as converts back gRPC response
    to JSON.
    :param api_method_name:
    :return:
    """
    stub = pur_pb2_grpc.PublicAPIStub(grpc.insecure_channel('{}:{}'.format(config.user.public_api_host,
                                                                           config.user.public_api_port),
                                                            options=[('grpc.max_receive_message_length', 10485760)]))
    public_api = pur_pb2.DESCRIPTOR.services_by_name['PublicAPI']
    api_method = public_api.FindMethodByName(api_method_name)
    api_request = getattr(pur_pb2, api_method.input_type.name)()

    for arg in request.args:
        if arg not in api_method.input_type.fields_by_name:
            raise Exception('Invalid args %s', arg)
        data_type = type(getattr(api_request, arg))
        if data_type == bool and request.args[arg].lower() == 'false':
            continue
        value = data_type(request.args.get(arg, type=data_type))
        setattr(api_request, arg, value)

    resp = getattr(stub, api_method_name)(api_request, timeout=10)
    return Response(response=MessageToJson(resp, sort_keys=True), status=200, mimetype='application/json')


def get_mining_stub():
    global mining_stub
    return mining_stub


def get_public_stub():
    global public_stub
    return public_stub


@api.dispatcher.add_method
def getlastblockheader(height=0):
    stub = get_mining_stub()
    request = purmining_pb2.GetLastBlockHeaderReq(height=height)
    grpc_response = stub.GetLastBlockHeader(request=request, timeout=10)

    block_header = {
        'difficulty': grpc_response.difficulty,
        'height': grpc_response.height,
        'timestamp': grpc_response.timestamp,
        'reward': grpc_response.reward,
        'hash': grpc_response.hash,
        'depth': grpc_response.depth
    }

    resp = {
        "block_header": block_header,
        "status": "OK"
    }
    return resp


@api.dispatcher.add_method
def getblockheaderbyheight(height):
    return getlastblockheader(height)


@api.dispatcher.add_method
def getblocktemplate(reserve_size, wallet_address):
    stub = get_mining_stub()
    request = purmining_pb2.GetBlockToMineReq(wallet_address=wallet_address.encode())
    grpc_response = stub.GetBlockToMine(request=request, timeout=10)
    resp = {
        'blocktemplate_blob': grpc_response.blocktemplate_blob,
        'difficulty': grpc_response.difficulty,
        'height': grpc_response.height,
        'reserved_offset': grpc_response.reserved_offset,
        'seed_hash': grpc_response.seed_hash,
        'status': 'OK'
    }

    return resp


@api.dispatcher.add_method
def getbalance():
    stub = get_public_stub()
    grpc_response = stub.GetOptimizedAddressState(request=pur_pb2.GetAddressStateReq(address=payment_slaves[0]))
    return grpc_response.state.balance


@api.dispatcher.add_method
def getheight():
    stub = get_public_stub()
    grpc_response = stub.GetHeight(request=pur_pb2.GetHeightReq())

    resp = {'height': grpc_response.height}
    return resp


@api.dispatcher.add_method
def submitblock(blob):
    stub = get_mining_stub()
    request = purmining_pb2.SubmitMinedBlockReq(blob=bytes(hstr2bin(blob)))
    response = stub.SubmitMinedBlock(request=request, timeout=10)
    if response.error:
        raise Exception  # Mining pool expected exception when block submission fails
    return {'status': 'OK', 'error': 0}


@api.dispatcher.add_method
def getblockmininpurompatible(height):
    stub = get_mining_stub()
    request = purmining_pb2.GetBlockMiningCompatibleReq(height=height)
    response = stub.GetBlockMiningCompatible(request=request, timeout=10)
    return MessageToJson(response, sort_keys=True)


@api.dispatcher.add_method
def transfer(destinations, fee, mixin, unlock_time):
    if len(destinations) > config.dev.transaction_multi_output_limit:
        raise Exception('Payment Failed: Amount exceeds the allowed limit')

    addrs_to = []
    amounts = []

    for tx in destinations:
        addrs_to.append(bytes(hstr2bin(tx['address'][1:])))  # Skipping 'Q'
        amounts.append(tx['amount'])

    stub = get_public_stub()

    purss = get_unused_payment_purss(stub)
    if not purss:
        raise Exception('Payment Failed: No Unused Payment purSS found')

    tx = TransferTransaction.create(addrs_to=addrs_to,
                                    amounts=amounts,
                                    message_data=None,
                                    fee=fee,
                                    purss_pk=purss.pk,
                                    master_addr=payment_slaves[0])

    tx.sign(purss)

    response = stub.PushTransaction(request=pur_pb2.PushTransactionReq(transaction_signed=tx.pbdata))

    if response.error_code != 3:
        raise Exception('Transaction Submission Failed, Response Code: %s', response.error_code)

    response = {'tx_hash': bin2hstr(tx.txhash)}

    return response


app.add_url_rule('/json_rpc', 'api', api.as_view(), methods=['POST'])


def parse_arguments():
    parser = argparse.ArgumentParser(description='pur node')
    parser.add_argument('--purdir', '-d', dest='pur_dir', default=config.user.pur_dir,
                        help="Use a different directory for node data/configuration")
    parser.add_argument('--network-type', dest='network_type', choices=['mainnet', 'testnet'],
                        default='mainnet', required=False, help="Runs pur Testnet Node")
    return parser.parse_args()


def main():
    args = parse_arguments()

    pur_dir_post_fix = ''
    copy_files = []
    if args.network_type == 'testnet':
        pur_dir_post_fix = '-testnet'
        package_directory = os.path.dirname(os.path.abspath(__file__))
        copy_files.append(os.path.join(package_directory, 'network/testnet/genesis.yml'))
        copy_files.append(os.path.join(package_directory, 'network/testnet/config.yml'))

    config.user.pur_dir = os.path.expanduser(os.path.normpath(args.pur_dir) + pur_dir_post_fix)
    config.create_path(config.user.pur_dir, copy_files)
    config.user.load_yaml(config.user.config_path)

    global payment_slaves, payment_purss
    global mining_stub, public_stub
    mining_stub = purmining_pb2_grpc.MiningAPIStub(grpc.insecure_channel('{0}:{1}'.format(config.user.mining_api_host,
                                                                                          config.user.mining_api_port)))
    public_stub = pur_pb2_grpc.PublicAPIStub(grpc.insecure_channel('{0}:{1}'.format(config.user.public_api_host,
                                                                                    config.user.public_api_port),
                                                                   options=[('grpc.max_receive_message_length',
                                                                             10485760)]))
    payment_purss = None
    payment_slaves = read_slaves(config.user.mining_pool_payment_wallet_path)
    app.run(host=config.user.grpc_proxy_host, port=config.user.grpc_proxy_port, threaded=False)


if __name__ == '__main__':
    main()
