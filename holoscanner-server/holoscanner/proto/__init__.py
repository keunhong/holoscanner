from holoscanner.proto import holoscanner_pb2 as pb


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
