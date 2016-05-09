import os
import logging

LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 8888
WS_LISTEN_ADDR = '0.0.0.0'
WS_LISTEN_PORT = 8889
VIEWER_ADDR = '0.0.0.0'
VIEWER_PORT = 8890

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
MESHES_DIR = os.path.join(PROJECT_DIR, '..', 'meshes')

LOG_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s\t[%(name)s]'
LOG_LEVEL = logging.INFO
