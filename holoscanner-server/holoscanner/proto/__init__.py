from holoscanner.proto import holoscanner_pb2 as pb
from holoscanner import config


def create_mesh_message(client_id, mesh_pb):
    msg = pb.Message()
    msg.device_id = client_id
    msg.type = pb.Message.MESH
    msg.mesh.MergeFrom(mesh_pb)
    return msg


def create_ack():
    msg = pb.Message()
    msg.type = pb.Message.ACK
    return msg


def create_game_started_message():
    msg = pb.Message()
    msg.type = pb.Message.START_GAME
    msg.device_id = config.SERVER_DEVICE_ID
    return msg
