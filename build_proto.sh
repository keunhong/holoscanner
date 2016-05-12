#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROTOC_VERSION="$(protoc --version)"

SERVER_PROTO_DIR="$DIR/holoscanner-server/holoscanner/proto/"
CLIENT_PROTO_DIR="$DIR/holoscanner-client/Assets/Proto/"
JS_PROTO_DIR="$DIR/holoscanner-server/holoscanner/viewer/static/"

if [[ "$PROTOC_VERSION" != "libprotoc 3."* ]]; then
  echo "Protobuf version >=3.0.0 required."
  echo "Download at https://github.com/google/protobuf/releases"
  exit 1
fi

CURRENT_DIR="$(pwd)"

cd $DIR/proto
protoc holoscanner.proto --python_out=$SERVER_PROTO_DIR
echo "Saved to $SERVER_PROTO_DIR"
protoc holoscanner.proto --csharp_out=$CLIENT_PROTO_DIR
echo "Saved to $CLIENT_PROTO_DIR"
cp holoscanner.proto $JS_PROTO_DIR
cd $CURRENT_DIR;
