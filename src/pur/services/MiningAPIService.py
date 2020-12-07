# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from grpc import StatusCode

from pypurlib.pypurlib import bin2hstr

from pur.core import config
from pur.core.purnode import purNode
from pur.crypto.Qryptonight import Qryptonight
from pur.generated import purmining_pb2
from pur.generated.purmining_pb2_grpc import MiningAPIServicer
from pur.services.grpcHelper import GrpcExceptionWrapper


class MiningAPIService(MiningAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, purnode: purNode):
        self.purnode = purnode
        self._qn = Qryptonight()

    @GrpcExceptionWrapper(purmining_pb2.GetBlockMiningCompatibleResp, StatusCode.UNKNOWN)
    def GetBlockMiningCompatible(self,
                                 request: purmining_pb2.GetBlockMiningCompatibleReq,
                                 context) -> purmining_pb2.GetBlockMiningCompatibleResp:

        blockheader, block_metadata = self.purnode.get_blockheader_and_metadata(request.height)

        response = purmining_pb2.GetBlockMiningCompatibleResp()
        if blockheader is not None and block_metadata is not None:
            response = purmining_pb2.GetBlockMiningCompatibleResp(
                blockheader=blockheader.pbdata,
                blockmetadata=block_metadata.pbdata)

        return response

    @GrpcExceptionWrapper(purmining_pb2.GetLastBlockHeaderResp, StatusCode.UNKNOWN)
    def GetLastBlockHeader(self,
                           request: purmining_pb2.GetLastBlockHeaderReq,
                           context) -> purmining_pb2.GetLastBlockHeaderResp:
        response = purmining_pb2.GetLastBlockHeaderResp()

        blockheader, block_metadata = self.purnode.get_blockheader_and_metadata(request.height)

        response.difficulty = int(bin2hstr(block_metadata.block_difficulty), 16)
        response.height = blockheader.block_number
        response.timestamp = blockheader.timestamp
        response.reward = blockheader.block_reward + blockheader.fee_reward
        response.hash = bin2hstr(blockheader.headerhash)
        response.depth = self.purnode.block_height - blockheader.block_number

        return response

    @GrpcExceptionWrapper(purmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def GetBlockToMine(self,
                       request: purmining_pb2.GetBlockToMineReq,
                       context) -> purmining_pb2.GetBlockToMineResp:

        response = purmining_pb2.GetBlockToMineResp()

        blocktemplate_blob_and_difficulty = self.purnode.get_block_to_mine(request.wallet_address)

        if blocktemplate_blob_and_difficulty:
            response.blocktemplate_blob = blocktemplate_blob_and_difficulty[0]
            response.difficulty = blocktemplate_blob_and_difficulty[1]
            response.height = self.purnode.block_height + 1
            response.reserved_offset = config.dev.extra_nonce_offset
            seed_block_number = self._qn.get_seed_height(response.height)
            response.seed_hash = bin2hstr(self.purnode.get_block_header_hash_by_number(seed_block_number))

        return response

    @GrpcExceptionWrapper(purmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def SubmitMinedBlock(self,
                         request: purmining_pb2.SubmitMinedBlockReq,
                         context) -> purmining_pb2.SubmitMinedBlockResp:
        response = purmining_pb2.SubmitMinedBlockResp()

        response.error = not self.purnode.submit_mined_block(request.blob)

        return response
