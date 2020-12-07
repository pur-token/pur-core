# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

# FIpurE: This is odd...
import sys

import os
from grpc._cython.cygrpc import StatusCode

from pur.core.purnode import purNode
from pur.generated.purbase_pb2 import GetNodeInfoReq, GetNodeInfoResp
from pur.generated.purbase_pb2_grpc import BaseServicer


class BaseService(BaseServicer):
    def __init__(self, purnode: purNode):
        self.purnode = purnode

    def GetNodeInfo(self, request: GetNodeInfoReq, context) -> GetNodeInfoResp:
        try:
            resp = GetNodeInfoResp()
            resp.version = self.purnode.version

            pkgdir = os.path.dirname(sys.modules['pur'].__file__)
            grpcprotopath = os.path.join(pkgdir, "protos", "pur.proto")
            with open(grpcprotopath, 'r') as infile:
                resp.grpcProto = infile.read()

            return resp
        except Exception as e:
            context.set_code(StatusCode.unknown)
            context.set_details(e)
            return GetNodeInfoResp()
