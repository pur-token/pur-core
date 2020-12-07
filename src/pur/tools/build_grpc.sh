#!/usr/bin/env bash
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )
cd ..

python -m grpc_tools.protoc -I=pur/protos --python_out=pur/generated --grpc_python_out=pur/generated pur/protos/pur.proto
python -m grpc_tools.protoc -I=pur/protos/pur.proto -I=pur/protos --python_out=pur/generated --grpc_python_out=pur/generated pur/protos/purlegacy.proto
python -m grpc_tools.protoc -I=pur/protos --python_out=pur/generated --grpc_python_out=pur/generated pur/protos/purbase.proto
python -m grpc_tools.protoc -I=pur/protos --python_out=pur/generated --grpc_python_out=pur/generated pur/protos/purmining.proto

# Patch import problem in generated code
sed -i 's|import pur_pb2 as pur__pb2|import pur.generated.pur_pb2 as pur__pb2|g' pur/generated/pur_pb2_grpc.py
sed -i 's|import pur_pb2 as pur__pb2|import pur.generated.pur_pb2 as pur__pb2|g' pur/generated/purlegacy_pb2.py
sed -i 's|import pur_pb2 as pur__pb2|import pur.generated.pur_pb2 as pur__pb2|g' pur/generated/purmining_pb2.py

sed -i 's|import purlegacy_pb2 as purlegacy__pb2|import pur.generated.purlegacy_pb2 as purlegacy__pb2|g' pur/generated/purlegacy_pb2_grpc.py
sed -i 's|import purbase_pb2 as purbase__pb2|import pur.generated.purbase_pb2 as purbase__pb2|g' pur/generated/purbase_pb2_grpc.py
sed -i 's|import purmining_pb2 as purmining__pb2|import pur.generated.purmining_pb2 as purmining__pb2|g' pur/generated/purmining_pb2_grpc.py

find pur/generated -name '*.py'|grep -v migrations|xargs autoflake --in-place

#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/pur/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=markdown,proto.md
#
#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/pur/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=html,index.html

popd > /dev/null
