# Protocol Documentation
<a name="top"/>

## Table of Contents

- [pur.proto](#pur.proto)
    - [AddressList](#pur.AddressList)
    - [AddressState](#pur.AddressState)
    - [Block](#pur.Block)
    - [BlockExtended](#pur.BlockExtended)
    - [BlockHeader](#pur.BlockHeader)
    - [BlockHeaderExtended](#pur.BlockHeaderExtended)
    - [BlockMetaData](#pur.BlockMetaData)
    - [BlockMetaDataList](#pur.BlockMetaDataList)
    - [EphemeralMessage](#pur.EphemeralMessage)
    - [GenesisBalance](#pur.GenesisBalance)
    - [GetAddressStateReq](#pur.GetAddressStateReq)
    - [GetAddressStateResp](#pur.GetAddressStateResp)
    - [GetBlockReq](#pur.GetBlockReq)
    - [GetBlockResp](#pur.GetBlockResp)
    - [GetKnownPeersReq](#pur.GetKnownPeersReq)
    - [GetKnownPeersResp](#pur.GetKnownPeersResp)
    - [GetLatestDataReq](#pur.GetLatestDataReq)
    - [GetLatestDataResp](#pur.GetLatestDataResp)
    - [GetLocalAddressesReq](#pur.GetLocalAddressesReq)
    - [GetLocalAddressesResp](#pur.GetLocalAddressesResp)
    - [GetNodeStateReq](#pur.GetNodeStateReq)
    - [GetNodeStateResp](#pur.GetNodeStateResp)
    - [GetObjectReq](#pur.GetObjectReq)
    - [GetObjectResp](#pur.GetObjectResp)
    - [GetStakersReq](#pur.GetStakersReq)
    - [GetStakersResp](#pur.GetStakersResp)
    - [GetStatsReq](#pur.GetStatsReq)
    - [GetStatsResp](#pur.GetStatsResp)
    - [GetWalletReq](#pur.GetWalletReq)
    - [GetWalletResp](#pur.GetWalletResp)
    - [LatticePublicKeyTxnReq](#pur.LatticePublicKeyTxnReq)
    - [MR](#pur.MR)
    - [MsgObject](#pur.MsgObject)
    - [NodeInfo](#pur.NodeInfo)
    - [Peer](#pur.Peer)
    - [PingReq](#pur.PingReq)
    - [PongResp](#pur.PongResp)
    - [PushTransactionReq](#pur.PushTransactionReq)
    - [PushTransactionResp](#pur.PushTransactionResp)
    - [StakeValidator](#pur.StakeValidator)
    - [StakeValidatorsList](#pur.StakeValidatorsList)
    - [StakeValidatorsTracker](#pur.StakeValidatorsTracker)
    - [StakeValidatorsTracker.ExpiryEntry](#pur.StakeValidatorsTracker.ExpiryEntry)
    - [StakeValidatorsTracker.FutureStakeAddressesEntry](#pur.StakeValidatorsTracker.FutureStakeAddressesEntry)
    - [StakeValidatorsTracker.FutureSvDictEntry](#pur.StakeValidatorsTracker.FutureSvDictEntry)
    - [StakeValidatorsTracker.SvDictEntry](#pur.StakeValidatorsTracker.SvDictEntry)
    - [StakerData](#pur.StakerData)
    - [StoredPeers](#pur.StoredPeers)
    - [Timestamp](#pur.Timestamp)
    - [Transaction](#pur.Transaction)
    - [Transaction.CoinBase](#pur.Transaction.CoinBase)
    - [Transaction.Destake](#pur.Transaction.Destake)
    - [Transaction.Duplicate](#pur.Transaction.Duplicate)
    - [Transaction.LatticePublicKey](#pur.Transaction.LatticePublicKey)
    - [Transaction.Stake](#pur.Transaction.Stake)
    - [Transaction.Transfer](#pur.Transaction.Transfer)
    - [Transaction.Vote](#pur.Transaction.Vote)
    - [TransactionCount](#pur.TransactionCount)
    - [TransactionCount.CountEntry](#pur.TransactionCount.CountEntry)
    - [TransactionExtended](#pur.TransactionExtended)
    - [TransferCoinsReq](#pur.TransferCoinsReq)
    - [TransferCoinsResp](#pur.TransferCoinsResp)
    - [Wallet](#pur.Wallet)
    - [WalletStore](#pur.WalletStore)

    - [GetLatestDataReq.Filter](#pur.GetLatestDataReq.Filter)
    - [GetStakersReq.Filter](#pur.GetStakersReq.Filter)
    - [NodeInfo.State](#pur.NodeInfo.State)
    - [Transaction.Type](#pur.Transaction.Type)


    - [AdminAPI](#pur.AdminAPI)
    - [P2PAPI](#pur.P2PAPI)
    - [PublicAPI](#pur.PublicAPI)


- [purbase.proto](#purbase.proto)
    - [GetNodeInfoReq](#pur.GetNodeInfoReq)
    - [GetNodeInfoResp](#pur.GetNodeInfoResp)



    - [Base](#pur.Base)


- [purlegacy.proto](#purlegacy.proto)
    - [BKData](#pur.BKData)
    - [FBData](#pur.FBData)
    - [LegacyMessage](#pur.LegacyMessage)
    - [MRData](#pur.MRData)
    - [NoData](#pur.NoData)
    - [PBData](#pur.PBData)
    - [PLData](#pur.PLData)
    - [PONGData](#pur.PONGData)
    - [SYNCData](#pur.SYNCData)
    - [VEData](#pur.VEData)

    - [LegacyMessage.FuncName](#pur.LegacyMessage.FuncName)




- [Scalar Value Types](#scalar-value-types)



<a name="pur.proto"/>
<p align="right"><a href="#top">Top</a></p>

## pur.proto



<a name="pur.AddressList"/>

### AddressList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addresses | [bytes](#bytes) | repeated |  |






<a name="pur.AddressState"/>

### AddressState



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |
| balance | [uint64](#uint64) |  |  |
| nonce | [uint64](#uint64) |  | FIpurE: Discuss. 32 or 64 bits? |
| pubhashes | [bytes](#bytes) | repeated |  |
| transaction_hashes | [bytes](#bytes) | repeated |  |






<a name="pur.Block"/>

### Block



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#pur.BlockHeader) |  |  |
| transactions | [Transaction](#pur.Transaction) | repeated |  |
| dup_transactions | [Transaction](#pur.Transaction) | repeated | TODO: Review this |
| vote | [Transaction](#pur.Transaction) | repeated |  |
| genesis_balance | [GenesisBalance](#pur.GenesisBalance) | repeated | This is only applicable to genesis blocks |






<a name="pur.BlockExtended"/>

### BlockExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block | [Block](#pur.Block) |  |  |
| voted_weight | [uint64](#uint64) |  |  |
| total_stake_weight | [uint64](#uint64) |  |  |






<a name="pur.BlockHeader"/>

### BlockHeader



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  | Header |
| epoch | [uint64](#uint64) |  |  |
| timestamp | [Timestamp](#pur.Timestamp) |  | FIpurE: Temporary |
| hash_header | [bytes](#bytes) |  |  |
| hash_header_prev | [bytes](#bytes) |  |  |
| reward_block | [uint64](#uint64) |  |  |
| reward_fee | [uint64](#uint64) |  |  |
| merkle_root | [bytes](#bytes) |  |  |
| hash_reveal | [bytes](#bytes) |  |  |
| stake_selector | [bytes](#bytes) |  |  |






<a name="pur.BlockHeaderExtended"/>

### BlockHeaderExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#pur.BlockHeader) |  |  |
| transaction_count | [TransactionCount](#pur.TransactionCount) |  |  |
| voted_weight | [uint64](#uint64) |  |  |
| total_stake_weight | [uint64](#uint64) |  |  |






<a name="pur.BlockMetaData"/>

### BlockMetaData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| hash_header | [bytes](#bytes) |  |  |






<a name="pur.BlockMetaDataList"/>

### BlockMetaDataList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number_hashes | [BlockMetaData](#pur.BlockMetaData) | repeated |  |






<a name="pur.EphemeralMessage"/>

### EphemeralMessage



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [bytes](#bytes) |  |  |
| ttl | [uint64](#uint64) |  |  |
| data | [bytes](#bytes) |  | Encrypted String containing aes256_symkey, prf512_seed, purss_address, signature |






<a name="pur.EphemeralMessage.Data"/>

### EphemeralMessage.Data



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| aes256_symkey | [bytes](#bytes) |  |  |
| prf512_seed | [bytes](#bytes) |  |  |
| purss_address | [bytes](#bytes) |  |  |
| purss_signature | [bytes](#bytes) |  |  |






<a name="pur.GenesisBalance"/>

### GenesisBalance



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [string](#string) |  | Address is string only here to increase visibility |
| balance | [uint64](#uint64) |  |  |






<a name="pur.GetAddressStateReq"/>

### GetAddressStateReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |






<a name="pur.GetAddressStateResp"/>

### GetAddressStateResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| state | [AddressState](#pur.AddressState) |  |  |






<a name="pur.GetBlockReq"/>

### GetBlockReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  | Indicates the index number in mainchain |
| after_hash | [bytes](#bytes) |  | request the node that comes after hash |






<a name="pur.GetBlockResp"/>

### GetBlockResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#pur.NodeInfo) |  |  |
| block | [Block](#pur.Block) |  |  |






<a name="pur.GetKnownPeersReq"/>

### GetKnownPeersReq







<a name="pur.GetKnownPeersResp"/>

### GetKnownPeersResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#pur.NodeInfo) |  |  |
| known_peers | [Peer](#pur.Peer) | repeated |  |






<a name="pur.GetLatestDataReq"/>

### GetLatestDataReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| filter | [GetLatestDataReq.Filter](#pur.GetLatestDataReq.Filter) |  |  |
| offset | [uint32](#uint32) |  | Offset in the result list (works backwards in this case) |
| quantity | [uint32](#uint32) |  | Number of items to retrive. Capped at 100 |






<a name="pur.GetLatestDataResp"/>

### GetLatestDataResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| blockheaders | [BlockHeaderExtended](#pur.BlockHeaderExtended) | repeated |  |
| transactions | [TransactionExtended](#pur.TransactionExtended) | repeated |  |
| transactions_unconfirmed | [TransactionExtended](#pur.TransactionExtended) | repeated |  |






<a name="pur.GetLocalAddressesReq"/>

### GetLocalAddressesReq







<a name="pur.GetLocalAddressesResp"/>

### GetLocalAddressesResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addresses | [bytes](#bytes) | repeated |  |






<a name="pur.GetNodeStateReq"/>

### GetNodeStateReq







<a name="pur.GetNodeStateResp"/>

### GetNodeStateResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| info | [NodeInfo](#pur.NodeInfo) |  |  |






<a name="pur.GetObjectReq"/>

### GetObjectReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| query | [bytes](#bytes) |  |  |






<a name="pur.GetObjectResp"/>

### GetObjectResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| found | [bool](#bool) |  |  |
| address_state | [AddressState](#pur.AddressState) |  |  |
| transaction | [TransactionExtended](#pur.TransactionExtended) |  |  |
| block | [Block](#pur.Block) |  |  |






<a name="pur.GetStakersReq"/>

### GetStakersReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| filter | [GetStakersReq.Filter](#pur.GetStakersReq.Filter) |  | Indicates which group of stakers (current / next) |
| offset | [uint32](#uint32) |  | Offset in the staker list |
| quantity | [uint32](#uint32) |  | Number of stakers to retrive. Capped at 100 |






<a name="pur.GetStakersResp"/>

### GetStakersResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stakers | [StakerData](#pur.StakerData) | repeated |  |






<a name="pur.GetStatsReq"/>

### GetStatsReq







<a name="pur.GetStatsResp"/>

### GetStatsResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| node_info | [NodeInfo](#pur.NodeInfo) |  |  |
| epoch | [uint64](#uint64) |  | Current epoch |
| uptime_network | [uint64](#uint64) |  | Indicates uptime in seconds |
| stakers_count | [uint64](#uint64) |  | Number of active stakers |
| block_last_reward | [uint64](#uint64) |  |  |
| block_time_mean | [uint64](#uint64) |  |  |
| block_time_sd | [uint64](#uint64) |  |  |
| coins_total_supply | [uint64](#uint64) |  |  |
| coins_emitted | [uint64](#uint64) |  |  |
| coins_atstake | [uint64](#uint64) |  |  |






<a name="pur.GetWalletReq"/>

### GetWalletReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |






<a name="pur.GetWalletResp"/>

### GetWalletResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| wallet | [Wallet](#pur.Wallet) |  | FIpurE: Encrypt |






<a name="pur.LatticePublicKeyTxnReq"/>

### LatticePublicKeyTxnReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_from | [bytes](#bytes) |  |  |
| kyber_pk | [bytes](#bytes) |  |  |
| dilithium_pk | [bytes](#bytes) |  |  |
| purss_pk | [bytes](#bytes) |  |  |
| purss_ots_index | [uint64](#uint64) |  |  |






<a name="pur.MR"/>

### MR
FIpurE: This is legacy. Plan removal


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hash | [bytes](#bytes) |  | FIpurE: rename this to block_headerhash |
| type | [string](#string) |  | FIpurE: type/string what is this |
| stake_selector | [bytes](#bytes) |  |  |
| block_number | [uint64](#uint64) |  |  |
| prev_headerhash | [bytes](#bytes) |  |  |
| reveal_hash | [bytes](#bytes) |  |  |






<a name="pur.MsgObject"/>

### MsgObject



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| ephemeral | [EphemeralMessage](#pur.EphemeralMessage) |  | Overlapping - objects used for 2-way exchanges P2PRequest request = 1; P2PResponse response = 2; |






<a name="pur.NodeInfo"/>

### NodeInfo



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| state | [NodeInfo.State](#pur.NodeInfo.State) |  |  |
| num_connections | [uint32](#uint32) |  |  |
| num_known_peers | [uint32](#uint32) |  |  |
| uptime | [uint64](#uint64) |  | Uptime in seconds |
| block_height | [uint64](#uint64) |  |  |
| block_last_hash | [bytes](#bytes) |  |  |
| stake_enabled | [bool](#bool) |  |  |
| network_id | [string](#string) |  |  |






<a name="pur.Peer"/>

### Peer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| ip | [string](#string) |  |  |






<a name="pur.PingReq"/>

### PingReq







<a name="pur.PongResp"/>

### PongResp







<a name="pur.PushTransactionReq"/>

### PushTransactionReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| transaction_signed | [Transaction](#pur.Transaction) |  |  |






<a name="pur.PushTransactionResp"/>

### PushTransactionResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| some_response | [string](#string) |  |  |






<a name="pur.StakeValidator"/>

### StakeValidator



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [bytes](#bytes) |  |  |
| slave_public_key | [bytes](#bytes) |  |  |
| terminator_hash | [bytes](#bytes) |  |  |
| balance | [uint64](#uint64) |  |  |
| activation_blocknumber | [uint64](#uint64) |  |  |
| nonce | [uint64](#uint64) |  |  |
| is_banned | [bool](#bool) |  |  |
| is_active | [bool](#bool) |  |  |






<a name="pur.StakeValidatorsList"/>

### StakeValidatorsList



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stake_validators | [StakeValidator](#pur.StakeValidator) | repeated |  |






<a name="pur.StakeValidatorsTracker"/>

### StakeValidatorsTracker



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sv_dict | [StakeValidatorsTracker.SvDictEntry](#pur.StakeValidatorsTracker.SvDictEntry) | repeated |  |
| future_stake_addresses | [StakeValidatorsTracker.FutureStakeAddressesEntry](#pur.StakeValidatorsTracker.FutureStakeAddressesEntry) | repeated |  |
| expiry | [StakeValidatorsTracker.ExpiryEntry](#pur.StakeValidatorsTracker.ExpiryEntry) | repeated |  |
| future_sv_dict | [StakeValidatorsTracker.FutureSvDictEntry](#pur.StakeValidatorsTracker.FutureSvDictEntry) | repeated |  |
| total_stake_amount | [uint64](#uint64) |  |  |






<a name="pur.StakeValidatorsTracker.ExpiryEntry"/>

### StakeValidatorsTracker.ExpiryEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint64](#uint64) |  |  |
| value | [AddressList](#pur.AddressList) |  |  |






<a name="pur.StakeValidatorsTracker.FutureStakeAddressesEntry"/>

### StakeValidatorsTracker.FutureStakeAddressesEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [StakeValidator](#pur.StakeValidator) |  |  |






<a name="pur.StakeValidatorsTracker.FutureSvDictEntry"/>

### StakeValidatorsTracker.FutureSvDictEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint64](#uint64) |  |  |
| value | [StakeValidatorsList](#pur.StakeValidatorsList) |  |  |






<a name="pur.StakeValidatorsTracker.SvDictEntry"/>

### StakeValidatorsTracker.SvDictEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [StakeValidator](#pur.StakeValidator) |  |  |






<a name="pur.StakerData"/>

### StakerData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_state | [AddressState](#pur.AddressState) |  |  |
| terminator_hash | [bytes](#bytes) |  |  |






<a name="pur.StoredPeers"/>

### StoredPeers



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| peers | [Peer](#pur.Peer) | repeated |  |






<a name="pur.Timestamp"/>

### Timestamp
TODO: Avoid using timestamp until the github issue is fixed
import &#34;google/protobuf/timestamp.proto&#34;;


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| seconds | [int64](#int64) |  |  |
| nanos | [int32](#int32) |  |  |






<a name="pur.Transaction"/>

### Transaction



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [Transaction.Type](#pur.Transaction.Type) |  |  |
| nonce | [uint64](#uint64) |  |  |
| addr_from | [bytes](#bytes) |  |  |
| public_key | [bytes](#bytes) |  |  |
| transaction_hash | [bytes](#bytes) |  |  |
| ots_key | [uint32](#uint32) |  |  |
| signature | [bytes](#bytes) |  |  |
| transfer | [Transaction.Transfer](#pur.Transaction.Transfer) |  |  |
| stake | [Transaction.Stake](#pur.Transaction.Stake) |  |  |
| coinbase | [Transaction.CoinBase](#pur.Transaction.CoinBase) |  |  |
| latticePK | [Transaction.LatticePublicKey](#pur.Transaction.LatticePublicKey) |  |  |
| duplicate | [Transaction.Duplicate](#pur.Transaction.Duplicate) |  |  |
| vote | [Transaction.Vote](#pur.Transaction.Vote) |  |  |






<a name="pur.Transaction.CoinBase"/>

### Transaction.CoinBase



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addr_to | [bytes](#bytes) |  |  |
| amount | [uint64](#uint64) |  |  |






<a name="pur.Transaction.Destake"/>

### Transaction.Destake







<a name="pur.Transaction.Duplicate"/>

### Transaction.Duplicate



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| prev_header_hash | [uint64](#uint64) |  |  |
| coinbase1_hhash | [bytes](#bytes) |  |  |
| coinbase2_hhash | [bytes](#bytes) |  |  |
| coinbase1 | [Transaction](#pur.Transaction) |  |  |
| coinbase2 | [Transaction](#pur.Transaction) |  |  |






<a name="pur.Transaction.LatticePublicKey"/>

### Transaction.LatticePublicKey



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| kyber_pk | [bytes](#bytes) |  |  |
| dilithium_pk | [bytes](#bytes) |  |  |






<a name="pur.Transaction.Stake"/>

### Transaction.Stake



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| activation_blocknumber | [uint64](#uint64) |  |  |
| slavePK | [bytes](#bytes) |  |  |
| hash | [bytes](#bytes) |  |  |






<a name="pur.Transaction.Transfer"/>

### Transaction.Transfer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| addr_to | [bytes](#bytes) |  |  |
| amount | [uint64](#uint64) |  |  |
| fee | [uint64](#uint64) |  |  |






<a name="pur.Transaction.Vote"/>

### Transaction.Vote



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| block_number | [uint64](#uint64) |  |  |
| hash_header | [bytes](#bytes) |  |  |






<a name="pur.TransactionCount"/>

### TransactionCount



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| count | [TransactionCount.CountEntry](#pur.TransactionCount.CountEntry) | repeated |  |






<a name="pur.TransactionCount.CountEntry"/>

### TransactionCount.CountEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [uint32](#uint32) |  |  |
| value | [uint32](#uint32) |  |  |






<a name="pur.TransactionExtended"/>

### TransactionExtended



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| header | [BlockHeader](#pur.BlockHeader) |  |  |
| tx | [Transaction](#pur.Transaction) |  |  |






<a name="pur.TransferCoinsReq"/>

### TransferCoinsReq



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address_from | [bytes](#bytes) |  | Transaction source address |
| address_to | [bytes](#bytes) |  | Transaction destination address |
| amount | [uint64](#uint64) |  | Amount. It should be expressed in Shor |
| fee | [uint64](#uint64) |  | Fee. It should be expressed in Shor |
| purss_pk | [bytes](#bytes) |  | purSS Public key |
| purss_ots_index | [uint64](#uint64) |  | purSS One time signature index |






<a name="pur.TransferCoinsResp"/>

### TransferCoinsResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| transaction_unsigned | [Transaction](#pur.Transaction) |  |  |






<a name="pur.Wallet"/>

### Wallet



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| address | [string](#string) |  | FIpurE move to bytes |
| mnemonic | [string](#string) |  |  |
| purss_index | [int32](#int32) |  |  |






<a name="pur.WalletStore"/>

### WalletStore



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| wallets | [Wallet](#pur.Wallet) | repeated |  |








<a name="pur.GetLatestDataReq.Filter"/>

### GetLatestDataReq.Filter


| Name | Number | Description |
| ---- | ------ | ----------- |
| ALL | 0 |  |
| BLOCKHEADERS | 1 |  |
| TRANSACTIONS | 2 |  |
| TRANSACTIONS_UNCONFIRMED | 3 |  |



<a name="pur.GetStakersReq.Filter"/>

### GetStakersReq.Filter


| Name | Number | Description |
| ---- | ------ | ----------- |
| CURRENT | 0 |  |
| NEXT | 1 |  |



<a name="pur.NodeInfo.State"/>

### NodeInfo.State


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| UNSYNCED | 1 |  |
| SYNCING | 2 |  |
| SYNCED | 3 |  |
| FORKED | 4 |  |



<a name="pur.Transaction.Type"/>

### Transaction.Type


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| TRANSFER | 1 |  |
| STAKE | 2 |  |
| DESTAKE | 3 |  |
| COINBASE | 4 |  |
| LATTICE | 5 |  |
| DUPLICATE | 6 |  |
| VOTE | 7 |  |







<a name="pur.AdminAPI"/>

### AdminAPI
This is a place holder for testing/instrumentation APIs

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetLocalAddresses | [GetLocalAddressesReq](#pur.GetLocalAddressesReq) | [GetLocalAddressesResp](#pur.GetLocalAddressesReq) | FIpurE: Use TLS and some signature scheme to validate the cli? At the moment, it will run locally |


<a name="pur.P2PAPI"/>

### P2PAPI
This service describes the P2P API

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeState | [GetNodeStateReq](#pur.GetNodeStateReq) | [GetNodeStateResp](#pur.GetNodeStateReq) |  |
| GetKnownPeers | [GetKnownPeersReq](#pur.GetKnownPeersReq) | [GetKnownPeersResp](#pur.GetKnownPeersReq) |  |
| GetBlock | [GetBlockReq](#pur.GetBlockReq) | [GetBlockResp](#pur.GetBlockReq) | rpc PublishBlock(PublishBlockReq) returns (PublishBlockResp); |
| ObjectExchange | [MsgObject](#pur.MsgObject) | [MsgObject](#pur.MsgObject) | A bidirectional streaming channel is used to avoid any firewalling/NAT issues. |


<a name="pur.PublicAPI"/>

### PublicAPI
This service describes the Public API used by clients (wallet/cli/etc)

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeState | [GetNodeStateReq](#pur.GetNodeStateReq) | [GetNodeStateResp](#pur.GetNodeStateReq) |  |
| GetKnownPeers | [GetKnownPeersReq](#pur.GetKnownPeersReq) | [GetKnownPeersResp](#pur.GetKnownPeersReq) |  |
| GetStats | [GetStatsReq](#pur.GetStatsReq) | [GetStatsResp](#pur.GetStatsReq) |  |
| GetAddressState | [GetAddressStateReq](#pur.GetAddressStateReq) | [GetAddressStateResp](#pur.GetAddressStateReq) |  |
| GetObject | [GetObjectReq](#pur.GetObjectReq) | [GetObjectResp](#pur.GetObjectReq) |  |
| GetLatestData | [GetLatestDataReq](#pur.GetLatestDataReq) | [GetLatestDataResp](#pur.GetLatestDataReq) |  |
| GetStakers | [GetStakersReq](#pur.GetStakersReq) | [GetStakersResp](#pur.GetStakersReq) |  |
| TransferCoins | [TransferCoinsReq](#pur.TransferCoinsReq) | [TransferCoinsResp](#pur.TransferCoinsReq) |  |
| PushTransaction | [PushTransactionReq](#pur.PushTransactionReq) | [PushTransactionResp](#pur.PushTransactionReq) |  |
| GetLatticePublicKeyTxn | [LatticePublicKeyTxnReq](#pur.LatticePublicKeyTxnReq) | [TransferCoinsResp](#pur.LatticePublicKeyTxnReq) |  |





<a name="purbase.proto"/>
<p align="right"><a href="#top">Top</a></p>

## purbase.proto



<a name="pur.GetNodeInfoReq"/>

### GetNodeInfoReq







<a name="pur.GetNodeInfoResp"/>

### GetNodeInfoResp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| grpcProto | [string](#string) |  |  |












<a name="pur.Base"/>

### Base


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetNodeInfo | [GetNodeInfoReq](#pur.GetNodeInfoReq) | [GetNodeInfoResp](#pur.GetNodeInfoReq) |  |





<a name="purlegacy.proto"/>
<p align="right"><a href="#top">Top</a></p>

## purlegacy.proto



<a name="pur.BKData"/>

### BKData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| mrData | [MRData](#pur.MRData) |  |  |
| block | [Block](#pur.Block) |  |  |






<a name="pur.FBData"/>

### FBData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  |  |






<a name="pur.LegacyMessage"/>

### LegacyMessage
Adding old code to refactor while keeping things working


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| func_name | [LegacyMessage.FuncName](#pur.LegacyMessage.FuncName) |  |  |
| noData | [NoData](#pur.NoData) |  |  |
| veData | [VEData](#pur.VEData) |  |  |
| pongData | [PONGData](#pur.PONGData) |  |  |
| mrData | [MRData](#pur.MRData) |  |  |
| sfmData | [MRData](#pur.MRData) |  |  |
| bkData | [BKData](#pur.BKData) |  |  |
| fbData | [FBData](#pur.FBData) |  |  |
| pbData | [PBData](#pur.PBData) |  |  |
| pbbData | [PBData](#pur.PBData) |  |  |
| syncData | [SYNCData](#pur.SYNCData) |  |  |






<a name="pur.MRData"/>

### MRData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| hash | [bytes](#bytes) |  | FIpurE: rename this to block_headerhash |
| type | [LegacyMessage.FuncName](#pur.LegacyMessage.FuncName) |  | FIpurE: type/string what is this |
| stake_selector | [bytes](#bytes) |  |  |
| block_number | [uint64](#uint64) |  |  |
| prev_headerhash | [bytes](#bytes) |  |  |
| reveal_hash | [bytes](#bytes) |  |  |






<a name="pur.NoData"/>

### NoData







<a name="pur.PBData"/>

### PBData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| index | [uint64](#uint64) |  |  |
| block | [Block](#pur.Block) |  |  |






<a name="pur.PLData"/>

### PLData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| peer_ips | [string](#string) | repeated |  |






<a name="pur.PONGData"/>

### PONGData







<a name="pur.SYNCData"/>

### SYNCData







<a name="pur.VEData"/>

### VEData



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |
| genesis_prev_hash | [bytes](#bytes) |  |  |








<a name="pur.LegacyMessage.FuncName"/>

### LegacyMessage.FuncName


| Name | Number | Description |
| ---- | ------ | ----------- |
| VE | 0 | Version |
| PL | 1 | Peers List |
| PONG | 2 | Pong |
| MR | 3 | Message received |
| SFM | 4 | Send Full Message |
| BK | 5 | Block |
| FB | 6 | Fetch request for block |
| PB | 7 | Push Block |
| PBB | 8 | Push Block Buffer |
| ST | 9 | Stake Transaction |
| DST | 10 | Destake Transaction |
| DT | 11 | Duplicate Transaction |
| TX | 12 | Transfer Transaction |
| VT | 13 | Vote |
| SYNC | 14 | Add into synced list, if the node replies |










## Scalar Value Types

| .proto Type | Notes | C++ Type | Java Type | Python Type |
| ----------- | ----- | -------- | --------- | ----------- |
| <a name="double" /> double |  | double | double | float |
| <a name="float" /> float |  | float | float | float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long |
| <a name="bool" /> bool |  | bool | boolean | boolean |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str |

