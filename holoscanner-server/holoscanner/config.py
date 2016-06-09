import os
import logging

SERVER_DEVICE_ID = '__server__'

GAME_LISTEN_ADDR = '0.0.0.0'
GAME_LISTEN_PORT = 8888
RELAY_LISTEN_ADDR = '0.0.0.0'
RELAY_LISTEN_PORT = 8889
DASHBOARD_ADDR = '0.0.0.0'
DASHBOARD_PORT = 8890
REPLAYVIEWER_ADDR = '0.0.0.0'
REPLAYVIEWER_PORT = 8891

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
MESHES_DIR = os.path.join(PROJECT_DIR, '..', 'meshes')
MESHES_SAVE_DIR = os.path.join(PROJECT_DIR, '..', 'client_meshes')
IMAGE_SAVE_DIR = '/home/kpar/www/'

LOG_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s\t[%(name)s]'
LOG_LEVEL = logging.INFO

MESH_PLANE_FINDING_BINS = 100
NUM_TARGETS_GEN = 50
HULL_SCALE = 30

DEVICE_COLOR_MAP = {
    'hs-red': 'Red',
    'hs-yellow': 'Yellow',
    'hs-blue': 'Blue',
    'hs-green': 'Green',
    'hs-purple': 'Purple',
    'hs-orange': 'Orange',
    'localhost': 'White'
}
DEFAULT_COLOR = 'Black'
