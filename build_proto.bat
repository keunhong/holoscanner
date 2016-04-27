SET SERVER_PROTO_DIR="..\holoscanner-server\holoscanner\proto"
SET CLIENT_PROTO_DIR="..\holoscanner-client\Assets\Proto"
cd proto
protoc.exe holoscanner.proto --csharp_out=%CLIENT_PROTO_DIR%
protoc.exe holoscanner.proto --python_out=%SERVER_PROTO_DIR%
cd ..
