#!/usr/bin/fish

set DIR (cd (dirname (status -f)); and pwd)

set -gx PYTHONPATH $DIR/ $PYTHONPATH
