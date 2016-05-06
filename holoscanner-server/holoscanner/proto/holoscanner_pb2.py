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
  serialized_pb=_b('\n\x11holoscanner.proto\x12\x11Holoscanner.Proto\"(\n\x05Vec3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"3\n\x05Vec4D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\t\n\x01w\x18\x04 \x01(\x02\"*\n\x04\x46\x61\x63\x65\x12\n\n\x02v1\x18\x01 \x01(\r\x12\n\n\x02v2\x18\x02 \x01(\r\x12\n\n\x02v3\x18\x03 \x01(\r\"\xe0\x01\n\x04Mesh\x12\x0f\n\x07mesh_id\x18\x02 \x01(\r\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12.\n\x0c\x63\x61m_position\x18\x64 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12.\n\x0c\x63\x61m_rotation\x18\x65 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec4D\x12+\n\x08vertices\x18\xc8\x01 \x03(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12\'\n\x05\x66\x61\x63\x65s\x18\xc9\x01 \x03(\x0b\x32\x17.Holoscanner.Proto.Face\"\x11\n\x0fLocationRequest\"m\n\x10LocationResponse\x12*\n\x08location\x18\x01 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\x12-\n\x0borientation\x18\x02 \x01(\x0b\x32\x18.Holoscanner.Proto.Vec3D\"\xba\x02\n\x07Message\x12-\n\x04type\x18\x01 \x01(\x0e\x32\x1f.Holoscanner.Proto.Message.Type\x12\x11\n\tdevice_id\x18\x02 \x01(\r\x12%\n\x04mesh\x18\x64 \x01(\x0b\x32\x17.Holoscanner.Proto.Mesh\x12=\n\x10location_request\x18\xac\x02 \x01(\x0b\x32\".Holoscanner.Proto.LocationRequest\x12?\n\x11location_response\x18\x90\x03 \x01(\x0b\x32#.Holoscanner.Proto.LocationResponse\"F\n\x04Type\x12\x07\n\x03\x41\x43K\x10\x00\x12\x08\n\x04MESH\x10\n\x12\x14\n\x10LOCATION_REQUEST\x10\x0b\x12\x15\n\x11LOCATION_RESPONSE\x10\x0c\x62\x06proto3')
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
      name='MESH', index=1, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCATION_REQUEST', index=2, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCATION_RESPONSE', index=3, number=12,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=781,
  serialized_end=851,
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


_FACE = _descriptor.Descriptor(
  name='Face',
  full_name='Holoscanner.Proto.Face',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='v1', full_name='Holoscanner.Proto.Face.v1', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='v2', full_name='Holoscanner.Proto.Face.v2', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='v3', full_name='Holoscanner.Proto.Face.v3', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=135,
  serialized_end=177,
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
      name='cam_position', full_name='Holoscanner.Proto.Mesh.cam_position', index=2,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cam_rotation', full_name='Holoscanner.Proto.Mesh.cam_rotation', index=3,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vertices', full_name='Holoscanner.Proto.Mesh.vertices', index=4,
      number=200, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='faces', full_name='Holoscanner.Proto.Mesh.faces', index=5,
      number=201, type=11, cpp_type=10, label=3,
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
  serialized_start=180,
  serialized_end=404,
)


_LOCATIONREQUEST = _descriptor.Descriptor(
  name='LocationRequest',
  full_name='Holoscanner.Proto.LocationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=406,
  serialized_end=423,
)


_LOCATIONRESPONSE = _descriptor.Descriptor(
  name='LocationResponse',
  full_name='Holoscanner.Proto.LocationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='Holoscanner.Proto.LocationResponse.location', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='orientation', full_name='Holoscanner.Proto.LocationResponse.orientation', index=1,
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
  serialized_start=425,
  serialized_end=534,
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
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
      name='location_request', full_name='Holoscanner.Proto.Message.location_request', index=3,
      number=300, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='location_response', full_name='Holoscanner.Proto.Message.location_response', index=4,
      number=400, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=537,
  serialized_end=851,
)

_MESH.fields_by_name['cam_position'].message_type = _VEC3D
_MESH.fields_by_name['cam_rotation'].message_type = _VEC4D
_MESH.fields_by_name['vertices'].message_type = _VEC3D
_MESH.fields_by_name['faces'].message_type = _FACE
_LOCATIONRESPONSE.fields_by_name['location'].message_type = _VEC3D
_LOCATIONRESPONSE.fields_by_name['orientation'].message_type = _VEC3D
_MESSAGE.fields_by_name['type'].enum_type = _MESSAGE_TYPE
_MESSAGE.fields_by_name['mesh'].message_type = _MESH
_MESSAGE.fields_by_name['location_request'].message_type = _LOCATIONREQUEST
_MESSAGE.fields_by_name['location_response'].message_type = _LOCATIONRESPONSE
_MESSAGE_TYPE.containing_type = _MESSAGE
DESCRIPTOR.message_types_by_name['Vec3D'] = _VEC3D
DESCRIPTOR.message_types_by_name['Vec4D'] = _VEC4D
DESCRIPTOR.message_types_by_name['Face'] = _FACE
DESCRIPTOR.message_types_by_name['Mesh'] = _MESH
DESCRIPTOR.message_types_by_name['LocationRequest'] = _LOCATIONREQUEST
DESCRIPTOR.message_types_by_name['LocationResponse'] = _LOCATIONRESPONSE
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

Face = _reflection.GeneratedProtocolMessageType('Face', (_message.Message,), dict(
  DESCRIPTOR = _FACE,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Face)
  ))
_sym_db.RegisterMessage(Face)

Mesh = _reflection.GeneratedProtocolMessageType('Mesh', (_message.Message,), dict(
  DESCRIPTOR = _MESH,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Mesh)
  ))
_sym_db.RegisterMessage(Mesh)

LocationRequest = _reflection.GeneratedProtocolMessageType('LocationRequest', (_message.Message,), dict(
  DESCRIPTOR = _LOCATIONREQUEST,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.LocationRequest)
  ))
_sym_db.RegisterMessage(LocationRequest)

LocationResponse = _reflection.GeneratedProtocolMessageType('LocationResponse', (_message.Message,), dict(
  DESCRIPTOR = _LOCATIONRESPONSE,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.LocationResponse)
  ))
_sym_db.RegisterMessage(LocationResponse)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'holoscanner_pb2'
  # @@protoc_insertion_point(class_scope:Holoscanner.Proto.Message)
  ))
_sym_db.RegisterMessage(Message)


# @@protoc_insertion_point(module_scope)
