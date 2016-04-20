#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/proto
protoc holoscanner.proto --python_out=../holoscanner-server/proto/
cd -
