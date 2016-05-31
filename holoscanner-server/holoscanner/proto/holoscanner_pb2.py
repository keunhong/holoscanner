# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: holoscanner.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='holoscanner.proto',
  package='Holoscanner.Proto',
  syntax='proto3',
  serialized_pb=_b('\n\x11holoscanner.proto\x12\x11Holoscanner.Proto\"(\n\x05Vec3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"3\n\x05Vec4D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\t\n\x01w\x18\x04 \x01(\x02\"N\n\x06\x43lient\x12\x11\n\tdevice_id\x18\x01 \x01(\t\x12\r\n\x05score\x18\n \x01(\r\x12\x10\n\x08is_ready\x18\x14 \x01(\x08\x12\x10\n\x08nickname\x18\x1e \x01(\t\"h\n\x0e\x43lientPosition\x12*\n\x08position\x18\x64 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12*\n\x08rotation\x18\x65 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec4D\"\xee\x01\n\x04Mesh\x12\x0f\n\x07mesh_id\x18\x02 \x01(\r\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x0f\n\x07is_last\x18\x04 \x01(\x08\x12\x10\n\x08is_first\x18\x05 \x01(\x08\x12.\n\x0c\x63\x61m_position\x18\x64 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12.\n\x0c\x63\x61m_rotation\x18\x65 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec4D\x12+\n\x08vertices\x18\xc8\x01 \x03(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12\x12\n\ttriangles\x18\xc9\x01 \x03(\x05\"G\n\x06Target\x12\x11\n\ttarget_id\x18\x01 \x01(\r\x12*\n\x08position\x18\x02 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\"\x87\x01\n\tGameState\x12\x0f\n\x07\x66loor_y\x18\x01 \x01(\x02\x12\x11\n\tceiling_y\x18\x02 \x01(\x02\x12*\n\x07targets\x18\n \x03(\x0b\x32\x19.Holoscanner.Proto.Target\x12*\n\x07\x63lients\x18\x14 \x03(\x0b\x32\x19.Holoscanner.Proto.Client\"\xee\x03\n\x07Message\x12-\n\x04type\x18\x01 \x01(\x0e\x32\x1f.Holoscanner.Proto.Message.Type\x12\x11\n\tdevice_id\x18\x02 \x01(\t\x12%\n\x04mesh\x18\x64 \x01(\x0b\x32\x17.Holoscanner.Proto.Mesh\x12:\n\x0f\x63lient_position\x18\x65 \x01(\x0b\x32!.Holoscanner.Proto.ClientPosition\x12\x31\n\ngame_state\x18\xf4\x03 \x01(\x0b\x32\x1c.Holoscanner.Proto.GameState\x12\x12\n\ttarget_id\x18\xd8\x04 \x01(\r\"\xf6\x01\n\x04Type\x12\x07\n\x03\x41\x43K\x10\x00\x12\x07\n\x03\x46IN\x10\x01\x12\x08\n\x04MESH\x10\n\x12\x0e\n\nGAME_STATE\x10\r\x12\x16\n\x12GAME_STATE_REQUEST\x10\x0e\x12\x10\n\x0cTARGET_FOUND\x10\x14\x12\x0e\n\nSTART_GAME\x10\x15\x12\x0c\n\x08\x45ND_GAME\x10\x16\x12\x13\n\x0f\x43LIENT_POSITION\x10(\x12\x10\n\x0c\x43LIENT_READY\x10)\x12\x17\n\x13\x43LIENT_SET_NICKNAME\x10*\x12\x10\n\x0c\x43LEAR_MESHES\x10\x64\x12\x14\n\x10\x43LEAR_GAME_STATE\x10\x65\x12\x12\n\x0eUPDATE_TARGETS\x10\x66\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_MESSAGE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='Holoscanner.Proto.Message.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ACK', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESH', index=2, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAME_STATE', index=3, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAME_STATE_REQUEST', index=4, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TARGET_FOUND', index=5, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='START_GAME', index=6, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='END_GAME', index=7, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT_POSITION', index=8, number=40,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT_READY', index=9, number=41,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLIENT_SET_NICKNAME', index=10, number=42,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLEAR_MESHES', index=11, number=100,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLEAR_GAME_STATE', index=12, number=101,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE_TARGETS', index=13, number=102,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1022,
  serialized_end=1268,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_TYPE)


_VEC3D = _descriptor.Descriptor(
  name='Vec3D',
  full_name='Holoscanner.Proto.Vec3D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Holoscanner.Proto.Vec3D.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='Holoscanner.Proto.Vec3D.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='Holoscanner.Proto.Vec3D.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=80,
)


_VEC4D = _descriptor.Descriptor(
  name='Vec4D',
  full_name='Holoscanner.Proto.Vec4D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Holoscanner.Proto.Vec4D.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='Holoscanner.Proto.Vec4D.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='Holoscanner.Proto.Vec4D.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='w', full_name='Holoscanner.Proto.Vec4D.w', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=133,
)


_CLIENT = _descriptor.Descriptor(
  name='Client',
  full_name='Holoscanner.Proto.Client',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='Holoscanner.Proto.Client.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='Holoscanner.Proto.Client.score', index=1,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_ready', full_name='Holoscanner.Proto.Client.is_ready', index=2,
      number=20, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='Holoscanner.Proto.Client.nickname', index=3,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=213,
)


_CLIENTPOSITION = _descriptor.Descriptor(
  name='ClientPosition',
  full_name='Holoscanner.Proto.ClientPosition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='Holoscanner.Proto.ClientPosition.position', index=0,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='Holoscanner.Proto.ClientPosition.rotation', index=1,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=215,
  serialized_end=319,
)


_MESH = _descriptor.Descriptor(
  name='Mesh',
  full_name='Holoscanner.Proto.Mesh',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mesh_id', full_name='Holoscanner.Proto.Mesh.mesh_id', index=0,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Holoscanner.Proto.Mesh.timestamp', index=1,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_last', full_name='Holoscanner.Proto.Mesh.is_last', index=2,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_first', full_name='Holoscanner.Proto.Mesh.is_first', index=3,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cam_position', full_name='Holoscanner.Proto.Mesh.cam_position', index=4,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cam_rotation', full_name='Holoscanner.Proto.Mesh.cam_rotation', index=5,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vertices', full_name='Holoscanner.Proto.Mesh.vertices', index=6,
      number=200, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='triangles', full_name='Holoscanner.Proto.Mesh.triangles', index=7,
      number=201, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=322,
  serialized_end=560,
)


_TARGET = _descriptor.Descriptor(
  name='Target',
  full_name='Holoscanner.Proto.Target',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='target_id', full_name='Holoscanner.Proto.Target.target_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='position', full_name='Holoscanner.Proto.Target.position', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=562,
  serialized_end=633,
)


_GAMESTATE = _descriptor.Descriptor(
  name='GameState',
  full_name='Holoscanner.Proto.GameState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='floor_y', full_name='Holoscanner.Proto.GameState.floor_y', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ceiling_y', full_name='Holoscanner.Proto.GameState.ceiling_y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='targets', full_name='Holoscanner.Proto.GameState.targets', index=2,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clients', full_name='Holoscanner.Proto.GameState.clients', index=3,
      number=20, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=636,
  serialized_end=771,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='Holoscanner.Proto.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Holoscanner.Proto.Message.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='Holoscanner.Proto.Message.device_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mesh', full_name='Holoscanner.Proto.Message.mesh', index=2,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_position', full_name='Holoscanner.Proto.Message.client_position', index=3,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_state', full_name='Holoscanner.Proto.Message.game_state', index=4,
      number=500, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_id', full_name='Holoscanner.Proto.Message.target_id', index=5,
      number=600, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGE_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=774,
  serialized_end=1268,
)

_CLIENTPOSITION.fields_by_name['position'].message_type = _VEC3D
_CLIENTPOSITION.fields_by_name['rotation'].message_type = _VEC4D
_MESH.fields_by_name['cam_position'].message_type = _VEC3D
_MESH.fields_by_name['cam_rotation'].message_type = _VEC4D
_MESH.fields_by_name['vertices'].message_type = _VEC3D
_TARGET.fields_by_name['position'].message_type = _VEC3D
_GAMESTATE.fields_by_name['targets'].message_type = _TARGET
_GAMESTATE.fields_by_name['clients'].message_type = _CLIENT
_MESSAGE.fields_by_name['type'].enum_type = _MESSAGE_TYPE
_MESSAGE.fields_by_name['mesh'].message_type = _MESH
_MESSAGE.fields_by_name['client_position'].message_type = _CLIENTPOSITION
_MESSAGE.fields_by_name['game_state'].message_type = _GAMESTATE
_MESSAGE_TYPE.containing_type = _MESSAGE
DESCRIPTOR.message_types_by_name['Vec3D'] = _VEC3D
DESCRIPTOR.message_types_by_name['Vec4D'] = _VEC4D
DESCRIPTOR.message_types_by_name['Client'] = _CLIENT
DESCRIPTOR.message_types_by_name['ClientPosition'] = _CLIENTPOSITION
DESCRIPTOR.message_types_by_name['Mesh'] = _MESH
DESCRIPTOR.message_types_by_name['Target'] = _TARGET
DESCRIPTOR.message_types_by_name['GameState'] = _GAMESTATE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE

Vec3D = _reflection.GeneratedProtocolMessageType('Vec3D', (_message.Message,), dict(
  DESCRIPTOR = _VEC3D,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Vec3D)
  ))
_sym_db.RegisterMessage(Vec3D)

Vec4D = _reflection.GeneratedProtocolMessageType('Vec4D', (_message.Message,), dict(
  DESCRIPTOR = _VEC4D,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Vec4D)
  ))
_sym_db.RegisterMessage(Vec4D)

Client = _reflection.GeneratedProtocolMessageType('Client', (_message.Message,), dict(
  DESCRIPTOR = _CLIENT,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Client)
  ))
_sym_db.RegisterMessage(Client)

ClientPosition = _reflection.GeneratedProtocolMessageType('ClientPosition', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTPOSITION,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.ClientPosition)
  ))
_sym_db.RegisterMessage(ClientPosition)

Mesh = _reflection.GeneratedProtocolMessageType('Mesh', (_message.Message,), dict(
  DESCRIPTOR = _MESH,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Mesh)
  ))
_sym_db.RegisterMessage(Mesh)

Target = _reflection.GeneratedProtocolMessageType('Target', (_message.Message,), dict(
  DESCRIPTOR = _TARGET,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Target)
  ))
_sym_db.RegisterMessage(Target)

GameState = _reflection.GeneratedProtocolMessageType('GameState', (_message.Message,), dict(
  DESCRIPTOR = _GAMESTATE,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.GameState)
  ))
_sym_db.RegisterMessage(GameState)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Message)
  ))
_sym_db.RegisterMessage(Message)


# @@protoc_insertion_point(module_scope)
