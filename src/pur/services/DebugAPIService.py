# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from pur.core import config
from pur.core.purnode import purNode
from pur.generated import purdebug_pb2
from pur.generated.purdebug_pb2_grpc import DebugAPIServicer
from pur.services.grpcHelper import GrpcExceptionWrapper


class DebugAPIService(DebugAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, purnode: purNode):
        self.purnode = purnode

    @GrpcExceptionWrapper(purdebug_pb2.GetFullStateResp)
    def GetFullState(self, request: purdebug_pb2.GetFullStateReq, context) -> purdebug_pb2.GetFullStateResp:
        return purdebug_pb2.GetFullStateResp(
            coinbase_state=self.purnode.get_address_state(config.dev.coinbase_address).pbdata,
            addresses_state=self.purnode.get_all_address_state()
        )
