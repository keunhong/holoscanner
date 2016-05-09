import os
import logging

LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 8888

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
MESHES_DIR = os.path.join(PROJECT_DIR, '..', 'meshes')

LOG_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s\t[%(name)s]'
LOG_LEVEL = logging.INFO
