// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: holoscanner.proto
#pragma warning disable 1591, 0612, 3021
#region Designer generated code

using pb = global::Google.Protobuf;
using pbc = global::Google.Protobuf.Collections;
using pbr = global::Google.Protobuf.Reflection;
using scg = global::System.Collections.Generic;
namespace Holoscanner.Proto {

  /// <summary>Holder for reflection information generated from holoscanner.proto</summary>
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public static partial class HoloscannerReflection {

    #region Descriptor
    /// <summary>File descriptor for holoscanner.proto</summary>
    public static pbr::FileDescriptor Descriptor {
      get { return descriptor; }
    }
    private static pbr::FileDescriptor descriptor;

    static HoloscannerReflection() {
      byte[] descriptorData = global::System.Convert.FromBase64String(
          string.Concat(
            "ChFob2xvc2Nhbm5lci5wcm90bxIRSG9sb3NjYW5uZXIuUHJvdG8iKAoFVmVj",
            "M0QSCQoBeBgBIAEoAhIJCgF5GAIgASgCEgkKAXoYAyABKAIiMwoFVmVjNEQS",
            "CQoBeBgBIAEoAhIJCgF5GAIgASgCEgkKAXoYAyABKAISCQoBdxgEIAEoAiIq",
            "CgRGYWNlEgoKAnYxGAEgASgNEgoKAnYyGAIgASgNEgoKAnYzGAMgASgNIuAB",
            "CgRNZXNoEg8KB21lc2hfaWQYAiABKA0SEQoJdGltZXN0YW1wGAMgASgEEi4K",
            "DGNhbV9wb3NpdGlvbhhkIAEoCzIYLkhvbG9zY2FubmVyLlByb3RvLlZlYzNE",
            "Ei4KDGNhbV9yb3RhdGlvbhhlIAEoCzIYLkhvbG9zY2FubmVyLlByb3RvLlZl",
            "YzREEisKCHZlcnRpY2VzGMgBIAMoCzIYLkhvbG9zY2FubmVyLlByb3RvLlZl",
            "YzNEEicKBWZhY2VzGMkBIAMoCzIXLkhvbG9zY2FubmVyLlByb3RvLkZhY2Ui",
            "EQoPTG9jYXRpb25SZXF1ZXN0Im0KEExvY2F0aW9uUmVzcG9uc2USKgoIbG9j",
            "YXRpb24YASABKAsyGC5Ib2xvc2Nhbm5lci5Qcm90by5WZWMzRBItCgtvcmll",
            "bnRhdGlvbhgCIAEoCzIYLkhvbG9zY2FubmVyLlByb3RvLlZlYzNEIroCCgdN",
            "ZXNzYWdlEi0KBHR5cGUYASABKA4yHy5Ib2xvc2Nhbm5lci5Qcm90by5NZXNz",
            "YWdlLlR5cGUSEQoJZGV2aWNlX2lkGAIgASgNEiUKBG1lc2gYZCABKAsyFy5I",
            "b2xvc2Nhbm5lci5Qcm90by5NZXNoEj0KEGxvY2F0aW9uX3JlcXVlc3QYrAIg",
            "ASgLMiIuSG9sb3NjYW5uZXIuUHJvdG8uTG9jYXRpb25SZXF1ZXN0Ej8KEWxv",
            "Y2F0aW9uX3Jlc3BvbnNlGJADIAEoCzIjLkhvbG9zY2FubmVyLlByb3RvLkxv",
            "Y2F0aW9uUmVzcG9uc2UiRgoEVHlwZRIHCgNBQ0sQABIICgRNRVNIEAoSFAoQ",
            "TE9DQVRJT05fUkVRVUVTVBALEhUKEUxPQ0FUSU9OX1JFU1BPTlNFEAxiBnBy",
            "b3RvMw=="));
      descriptor = pbr::FileDescriptor.FromGeneratedCode(descriptorData,
          new pbr::FileDescriptor[] { },
          new pbr::GeneratedCodeInfo(null, new pbr::GeneratedCodeInfo[] {
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.Vec3D), global::Holoscanner.Proto.Vec3D.Parser, new[]{ "X", "Y", "Z" }, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.Vec4D), global::Holoscanner.Proto.Vec4D.Parser, new[]{ "X", "Y", "Z", "W" }, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.Face), global::Holoscanner.Proto.Face.Parser, new[]{ "V1", "V2", "V3" }, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.Mesh), global::Holoscanner.Proto.Mesh.Parser, new[]{ "MeshId", "Timestamp", "CamPosition", "CamRotation", "Vertices", "Faces" }, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.LocationRequest), global::Holoscanner.Proto.LocationRequest.Parser, null, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.LocationResponse), global::Holoscanner.Proto.LocationResponse.Parser, new[]{ "Location", "Orientation" }, null, null, null),
            new pbr::GeneratedCodeInfo(typeof(global::Holoscanner.Proto.Message), global::Holoscanner.Proto.Message.Parser, new[]{ "Type", "DeviceId", "Mesh", "LocationRequest", "LocationResponse" }, null, new[]{ typeof(global::Holoscanner.Proto.Message.Types.Type) }, null)
          }));
    }
    #endregion

  }
  #region Messages
  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class Vec3D : pb::IMessage<Vec3D> {
    private static readonly pb::MessageParser<Vec3D> _parser = new pb::MessageParser<Vec3D>(() => new Vec3D());
    public static pb::MessageParser<Vec3D> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[0]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public Vec3D() {
      OnConstruction();
    }

    partial void OnConstruction();

    public Vec3D(Vec3D other) : this() {
      x_ = other.x_;
      y_ = other.y_;
      z_ = other.z_;
    }

    public Vec3D Clone() {
      return new Vec3D(this);
    }

    /// <summary>Field number for the "x" field.</summary>
    public const int XFieldNumber = 1;
    private float x_;
    public float X {
      get { return x_; }
      set {
        x_ = value;
      }
    }

    /// <summary>Field number for the "y" field.</summary>
    public const int YFieldNumber = 2;
    private float y_;
    public float Y {
      get { return y_; }
      set {
        y_ = value;
      }
    }

    /// <summary>Field number for the "z" field.</summary>
    public const int ZFieldNumber = 3;
    private float z_;
    public float Z {
      get { return z_; }
      set {
        z_ = value;
      }
    }

    public override bool Equals(object other) {
      return Equals(other as Vec3D);
    }

    public bool Equals(Vec3D other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (X != other.X) return false;
      if (Y != other.Y) return false;
      if (Z != other.Z) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (X != 0F) hash ^= X.GetHashCode();
      if (Y != 0F) hash ^= Y.GetHashCode();
      if (Z != 0F) hash ^= Z.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (X != 0F) {
        output.WriteRawTag(13);
        output.WriteFloat(X);
      }
      if (Y != 0F) {
        output.WriteRawTag(21);
        output.WriteFloat(Y);
      }
      if (Z != 0F) {
        output.WriteRawTag(29);
        output.WriteFloat(Z);
      }
    }

    public int CalculateSize() {
      int size = 0;
      if (X != 0F) {
        size += 1 + 4;
      }
      if (Y != 0F) {
        size += 1 + 4;
      }
      if (Z != 0F) {
        size += 1 + 4;
      }
      return size;
    }

    public void MergeFrom(Vec3D other) {
      if (other == null) {
        return;
      }
      if (other.X != 0F) {
        X = other.X;
      }
      if (other.Y != 0F) {
        Y = other.Y;
      }
      if (other.Z != 0F) {
        Z = other.Z;
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 13: {
            X = input.ReadFloat();
            break;
          }
          case 21: {
            Y = input.ReadFloat();
            break;
          }
          case 29: {
            Z = input.ReadFloat();
            break;
          }
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class Vec4D : pb::IMessage<Vec4D> {
    private static readonly pb::MessageParser<Vec4D> _parser = new pb::MessageParser<Vec4D>(() => new Vec4D());
    public static pb::MessageParser<Vec4D> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[1]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public Vec4D() {
      OnConstruction();
    }

    partial void OnConstruction();

    public Vec4D(Vec4D other) : this() {
      x_ = other.x_;
      y_ = other.y_;
      z_ = other.z_;
      w_ = other.w_;
    }

    public Vec4D Clone() {
      return new Vec4D(this);
    }

    /// <summary>Field number for the "x" field.</summary>
    public const int XFieldNumber = 1;
    private float x_;
    public float X {
      get { return x_; }
      set {
        x_ = value;
      }
    }

    /// <summary>Field number for the "y" field.</summary>
    public const int YFieldNumber = 2;
    private float y_;
    public float Y {
      get { return y_; }
      set {
        y_ = value;
      }
    }

    /// <summary>Field number for the "z" field.</summary>
    public const int ZFieldNumber = 3;
    private float z_;
    public float Z {
      get { return z_; }
      set {
        z_ = value;
      }
    }

    /// <summary>Field number for the "w" field.</summary>
    public const int WFieldNumber = 4;
    private float w_;
    public float W {
      get { return w_; }
      set {
        w_ = value;
      }
    }

    public override bool Equals(object other) {
      return Equals(other as Vec4D);
    }

    public bool Equals(Vec4D other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (X != other.X) return false;
      if (Y != other.Y) return false;
      if (Z != other.Z) return false;
      if (W != other.W) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (X != 0F) hash ^= X.GetHashCode();
      if (Y != 0F) hash ^= Y.GetHashCode();
      if (Z != 0F) hash ^= Z.GetHashCode();
      if (W != 0F) hash ^= W.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (X != 0F) {
        output.WriteRawTag(13);
        output.WriteFloat(X);
      }
      if (Y != 0F) {
        output.WriteRawTag(21);
        output.WriteFloat(Y);
      }
      if (Z != 0F) {
        output.WriteRawTag(29);
        output.WriteFloat(Z);
      }
      if (W != 0F) {
        output.WriteRawTag(37);
        output.WriteFloat(W);
      }
    }

    public int CalculateSize() {
      int size = 0;
      if (X != 0F) {
        size += 1 + 4;
      }
      if (Y != 0F) {
        size += 1 + 4;
      }
      if (Z != 0F) {
        size += 1 + 4;
      }
      if (W != 0F) {
        size += 1 + 4;
      }
      return size;
    }

    public void MergeFrom(Vec4D other) {
      if (other == null) {
        return;
      }
      if (other.X != 0F) {
        X = other.X;
      }
      if (other.Y != 0F) {
        Y = other.Y;
      }
      if (other.Z != 0F) {
        Z = other.Z;
      }
      if (other.W != 0F) {
        W = other.W;
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 13: {
            X = input.ReadFloat();
            break;
          }
          case 21: {
            Y = input.ReadFloat();
            break;
          }
          case 29: {
            Z = input.ReadFloat();
            break;
          }
          case 37: {
            W = input.ReadFloat();
            break;
          }
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class Face : pb::IMessage<Face> {
    private static readonly pb::MessageParser<Face> _parser = new pb::MessageParser<Face>(() => new Face());
    public static pb::MessageParser<Face> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[2]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public Face() {
      OnConstruction();
    }

    partial void OnConstruction();

    public Face(Face other) : this() {
      v1_ = other.v1_;
      v2_ = other.v2_;
      v3_ = other.v3_;
    }

    public Face Clone() {
      return new Face(this);
    }

    /// <summary>Field number for the "v1" field.</summary>
    public const int V1FieldNumber = 1;
    private uint v1_;
    public uint V1 {
      get { return v1_; }
      set {
        v1_ = value;
      }
    }

    /// <summary>Field number for the "v2" field.</summary>
    public const int V2FieldNumber = 2;
    private uint v2_;
    public uint V2 {
      get { return v2_; }
      set {
        v2_ = value;
      }
    }

    /// <summary>Field number for the "v3" field.</summary>
    public const int V3FieldNumber = 3;
    private uint v3_;
    public uint V3 {
      get { return v3_; }
      set {
        v3_ = value;
      }
    }

    public override bool Equals(object other) {
      return Equals(other as Face);
    }

    public bool Equals(Face other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (V1 != other.V1) return false;
      if (V2 != other.V2) return false;
      if (V3 != other.V3) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (V1 != 0) hash ^= V1.GetHashCode();
      if (V2 != 0) hash ^= V2.GetHashCode();
      if (V3 != 0) hash ^= V3.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (V1 != 0) {
        output.WriteRawTag(8);
        output.WriteUInt32(V1);
      }
      if (V2 != 0) {
        output.WriteRawTag(16);
        output.WriteUInt32(V2);
      }
      if (V3 != 0) {
        output.WriteRawTag(24);
        output.WriteUInt32(V3);
      }
    }

    public int CalculateSize() {
      int size = 0;
      if (V1 != 0) {
        size += 1 + pb::CodedOutputStream.ComputeUInt32Size(V1);
      }
      if (V2 != 0) {
        size += 1 + pb::CodedOutputStream.ComputeUInt32Size(V2);
      }
      if (V3 != 0) {
        size += 1 + pb::CodedOutputStream.ComputeUInt32Size(V3);
      }
      return size;
    }

    public void MergeFrom(Face other) {
      if (other == null) {
        return;
      }
      if (other.V1 != 0) {
        V1 = other.V1;
      }
      if (other.V2 != 0) {
        V2 = other.V2;
      }
      if (other.V3 != 0) {
        V3 = other.V3;
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 8: {
            V1 = input.ReadUInt32();
            break;
          }
          case 16: {
            V2 = input.ReadUInt32();
            break;
          }
          case 24: {
            V3 = input.ReadUInt32();
            break;
          }
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class Mesh : pb::IMessage<Mesh> {
    private static readonly pb::MessageParser<Mesh> _parser = new pb::MessageParser<Mesh>(() => new Mesh());
    public static pb::MessageParser<Mesh> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[3]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public Mesh() {
      OnConstruction();
    }

    partial void OnConstruction();

    public Mesh(Mesh other) : this() {
      meshId_ = other.meshId_;
      timestamp_ = other.timestamp_;
      CamPosition = other.camPosition_ != null ? other.CamPosition.Clone() : null;
      CamRotation = other.camRotation_ != null ? other.CamRotation.Clone() : null;
      vertices_ = other.vertices_.Clone();
      faces_ = other.faces_.Clone();
    }

    public Mesh Clone() {
      return new Mesh(this);
    }

    /// <summary>Field number for the "mesh_id" field.</summary>
    public const int MeshIdFieldNumber = 2;
    private uint meshId_;
    public uint MeshId {
      get { return meshId_; }
      set {
        meshId_ = value;
      }
    }

    /// <summary>Field number for the "timestamp" field.</summary>
    public const int TimestampFieldNumber = 3;
    private ulong timestamp_;
    public ulong Timestamp {
      get { return timestamp_; }
      set {
        timestamp_ = value;
      }
    }

    /// <summary>Field number for the "cam_position" field.</summary>
    public const int CamPositionFieldNumber = 100;
    private global::Holoscanner.Proto.Vec3D camPosition_;
    /// <summary>
    ///  We need the camera position in case we want to do space carving.
    /// </summary>
    public global::Holoscanner.Proto.Vec3D CamPosition {
      get { return camPosition_; }
      set {
        camPosition_ = value;
      }
    }

    /// <summary>Field number for the "cam_rotation" field.</summary>
    public const int CamRotationFieldNumber = 101;
    private global::Holoscanner.Proto.Vec4D camRotation_;
    public global::Holoscanner.Proto.Vec4D CamRotation {
      get { return camRotation_; }
      set {
        camRotation_ = value;
      }
    }

    /// <summary>Field number for the "vertices" field.</summary>
    public const int VerticesFieldNumber = 200;
    private static readonly pb::FieldCodec<global::Holoscanner.Proto.Vec3D> _repeated_vertices_codec
        = pb::FieldCodec.ForMessage(1602, global::Holoscanner.Proto.Vec3D.Parser);
    private readonly pbc::RepeatedField<global::Holoscanner.Proto.Vec3D> vertices_ = new pbc::RepeatedField<global::Holoscanner.Proto.Vec3D>();
    public pbc::RepeatedField<global::Holoscanner.Proto.Vec3D> Vertices {
      get { return vertices_; }
    }

    /// <summary>Field number for the "faces" field.</summary>
    public const int FacesFieldNumber = 201;
    private static readonly pb::FieldCodec<global::Holoscanner.Proto.Face> _repeated_faces_codec
        = pb::FieldCodec.ForMessage(1610, global::Holoscanner.Proto.Face.Parser);
    private readonly pbc::RepeatedField<global::Holoscanner.Proto.Face> faces_ = new pbc::RepeatedField<global::Holoscanner.Proto.Face>();
    public pbc::RepeatedField<global::Holoscanner.Proto.Face> Faces {
      get { return faces_; }
    }

    public override bool Equals(object other) {
      return Equals(other as Mesh);
    }

    public bool Equals(Mesh other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (MeshId != other.MeshId) return false;
      if (Timestamp != other.Timestamp) return false;
      if (!object.Equals(CamPosition, other.CamPosition)) return false;
      if (!object.Equals(CamRotation, other.CamRotation)) return false;
      if(!vertices_.Equals(other.vertices_)) return false;
      if(!faces_.Equals(other.faces_)) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (MeshId != 0) hash ^= MeshId.GetHashCode();
      if (Timestamp != 0UL) hash ^= Timestamp.GetHashCode();
      if (camPosition_ != null) hash ^= CamPosition.GetHashCode();
      if (camRotation_ != null) hash ^= CamRotation.GetHashCode();
      hash ^= vertices_.GetHashCode();
      hash ^= faces_.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (MeshId != 0) {
        output.WriteRawTag(16);
        output.WriteUInt32(MeshId);
      }
      if (Timestamp != 0UL) {
        output.WriteRawTag(24);
        output.WriteUInt64(Timestamp);
      }
      if (camPosition_ != null) {
        output.WriteRawTag(162, 6);
        output.WriteMessage(CamPosition);
      }
      if (camRotation_ != null) {
        output.WriteRawTag(170, 6);
        output.WriteMessage(CamRotation);
      }
      vertices_.WriteTo(output, _repeated_vertices_codec);
      faces_.WriteTo(output, _repeated_faces_codec);
    }

    public int CalculateSize() {
      int size = 0;
      if (MeshId != 0) {
        size += 1 + pb::CodedOutputStream.ComputeUInt32Size(MeshId);
      }
      if (Timestamp != 0UL) {
        size += 1 + pb::CodedOutputStream.ComputeUInt64Size(Timestamp);
      }
      if (camPosition_ != null) {
        size += 2 + pb::CodedOutputStream.ComputeMessageSize(CamPosition);
      }
      if (camRotation_ != null) {
        size += 2 + pb::CodedOutputStream.ComputeMessageSize(CamRotation);
      }
      size += vertices_.CalculateSize(_repeated_vertices_codec);
      size += faces_.CalculateSize(_repeated_faces_codec);
      return size;
    }

    public void MergeFrom(Mesh other) {
      if (other == null) {
        return;
      }
      if (other.MeshId != 0) {
        MeshId = other.MeshId;
      }
      if (other.Timestamp != 0UL) {
        Timestamp = other.Timestamp;
      }
      if (other.camPosition_ != null) {
        if (camPosition_ == null) {
          camPosition_ = new global::Holoscanner.Proto.Vec3D();
        }
        CamPosition.MergeFrom(other.CamPosition);
      }
      if (other.camRotation_ != null) {
        if (camRotation_ == null) {
          camRotation_ = new global::Holoscanner.Proto.Vec4D();
        }
        CamRotation.MergeFrom(other.CamRotation);
      }
      vertices_.Add(other.vertices_);
      faces_.Add(other.faces_);
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 16: {
            MeshId = input.ReadUInt32();
            break;
          }
          case 24: {
            Timestamp = input.ReadUInt64();
            break;
          }
          case 802: {
            if (camPosition_ == null) {
              camPosition_ = new global::Holoscanner.Proto.Vec3D();
            }
            input.ReadMessage(camPosition_);
            break;
          }
          case 810: {
            if (camRotation_ == null) {
              camRotation_ = new global::Holoscanner.Proto.Vec4D();
            }
            input.ReadMessage(camRotation_);
            break;
          }
          case 1602: {
            vertices_.AddEntriesFrom(input, _repeated_vertices_codec);
            break;
          }
          case 1610: {
            faces_.AddEntriesFrom(input, _repeated_faces_codec);
            break;
          }
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class LocationRequest : pb::IMessage<LocationRequest> {
    private static readonly pb::MessageParser<LocationRequest> _parser = new pb::MessageParser<LocationRequest>(() => new LocationRequest());
    public static pb::MessageParser<LocationRequest> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[4]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public LocationRequest() {
      OnConstruction();
    }

    partial void OnConstruction();

    public LocationRequest(LocationRequest other) : this() {
    }

    public LocationRequest Clone() {
      return new LocationRequest(this);
    }

    public override bool Equals(object other) {
      return Equals(other as LocationRequest);
    }

    public bool Equals(LocationRequest other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
    }

    public int CalculateSize() {
      int size = 0;
      return size;
    }

    public void MergeFrom(LocationRequest other) {
      if (other == null) {
        return;
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class LocationResponse : pb::IMessage<LocationResponse> {
    private static readonly pb::MessageParser<LocationResponse> _parser = new pb::MessageParser<LocationResponse>(() => new LocationResponse());
    public static pb::MessageParser<LocationResponse> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[5]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public LocationResponse() {
      OnConstruction();
    }

    partial void OnConstruction();

    public LocationResponse(LocationResponse other) : this() {
      Location = other.location_ != null ? other.Location.Clone() : null;
      Orientation = other.orientation_ != null ? other.Orientation.Clone() : null;
    }

    public LocationResponse Clone() {
      return new LocationResponse(this);
    }

    /// <summary>Field number for the "location" field.</summary>
    public const int LocationFieldNumber = 1;
    private global::Holoscanner.Proto.Vec3D location_;
    public global::Holoscanner.Proto.Vec3D Location {
      get { return location_; }
      set {
        location_ = value;
      }
    }

    /// <summary>Field number for the "orientation" field.</summary>
    public const int OrientationFieldNumber = 2;
    private global::Holoscanner.Proto.Vec3D orientation_;
    public global::Holoscanner.Proto.Vec3D Orientation {
      get { return orientation_; }
      set {
        orientation_ = value;
      }
    }

    public override bool Equals(object other) {
      return Equals(other as LocationResponse);
    }

    public bool Equals(LocationResponse other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (!object.Equals(Location, other.Location)) return false;
      if (!object.Equals(Orientation, other.Orientation)) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (location_ != null) hash ^= Location.GetHashCode();
      if (orientation_ != null) hash ^= Orientation.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (location_ != null) {
        output.WriteRawTag(10);
        output.WriteMessage(Location);
      }
      if (orientation_ != null) {
        output.WriteRawTag(18);
        output.WriteMessage(Orientation);
      }
    }

    public int CalculateSize() {
      int size = 0;
      if (location_ != null) {
        size += 1 + pb::CodedOutputStream.ComputeMessageSize(Location);
      }
      if (orientation_ != null) {
        size += 1 + pb::CodedOutputStream.ComputeMessageSize(Orientation);
      }
      return size;
    }

    public void MergeFrom(LocationResponse other) {
      if (other == null) {
        return;
      }
      if (other.location_ != null) {
        if (location_ == null) {
          location_ = new global::Holoscanner.Proto.Vec3D();
        }
        Location.MergeFrom(other.Location);
      }
      if (other.orientation_ != null) {
        if (orientation_ == null) {
          orientation_ = new global::Holoscanner.Proto.Vec3D();
        }
        Orientation.MergeFrom(other.Orientation);
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 10: {
            if (location_ == null) {
              location_ = new global::Holoscanner.Proto.Vec3D();
            }
            input.ReadMessage(location_);
            break;
          }
          case 18: {
            if (orientation_ == null) {
              orientation_ = new global::Holoscanner.Proto.Vec3D();
            }
            input.ReadMessage(orientation_);
            break;
          }
        }
      }
    }

  }

  [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
  public sealed partial class Message : pb::IMessage<Message> {
    private static readonly pb::MessageParser<Message> _parser = new pb::MessageParser<Message>(() => new Message());
    public static pb::MessageParser<Message> Parser { get { return _parser; } }

    public static pbr::MessageDescriptor Descriptor {
      get { return global::Holoscanner.Proto.HoloscannerReflection.Descriptor.MessageTypes[6]; }
    }

    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    public Message() {
      OnConstruction();
    }

    partial void OnConstruction();

    public Message(Message other) : this() {
      type_ = other.type_;
      deviceId_ = other.deviceId_;
      Mesh = other.mesh_ != null ? other.Mesh.Clone() : null;
      LocationRequest = other.locationRequest_ != null ? other.LocationRequest.Clone() : null;
      LocationResponse = other.locationResponse_ != null ? other.LocationResponse.Clone() : null;
    }

    public Message Clone() {
      return new Message(this);
    }

    /// <summary>Field number for the "type" field.</summary>
    public const int TypeFieldNumber = 1;
    private global::Holoscanner.Proto.Message.Types.Type type_ = global::Holoscanner.Proto.Message.Types.Type.ACK;
    public global::Holoscanner.Proto.Message.Types.Type Type {
      get { return type_; }
      set {
        type_ = value;
      }
    }

    /// <summary>Field number for the "device_id" field.</summary>
    public const int DeviceIdFieldNumber = 2;
    private uint deviceId_;
    public uint DeviceId {
      get { return deviceId_; }
      set {
        deviceId_ = value;
      }
    }

    /// <summary>Field number for the "mesh" field.</summary>
    public const int MeshFieldNumber = 100;
    private global::Holoscanner.Proto.Mesh mesh_;
    /// <summary>
    ///  One or less of the following will be filled in.
    /// </summary>
    public global::Holoscanner.Proto.Mesh Mesh {
      get { return mesh_; }
      set {
        mesh_ = value;
      }
    }

    /// <summary>Field number for the "location_request" field.</summary>
    public const int LocationRequestFieldNumber = 300;
    private global::Holoscanner.Proto.LocationRequest locationRequest_;
    public global::Holoscanner.Proto.LocationRequest LocationRequest {
      get { return locationRequest_; }
      set {
        locationRequest_ = value;
      }
    }

    /// <summary>Field number for the "location_response" field.</summary>
    public const int LocationResponseFieldNumber = 400;
    private global::Holoscanner.Proto.LocationResponse locationResponse_;
    public global::Holoscanner.Proto.LocationResponse LocationResponse {
      get { return locationResponse_; }
      set {
        locationResponse_ = value;
      }
    }

    public override bool Equals(object other) {
      return Equals(other as Message);
    }

    public bool Equals(Message other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (Type != other.Type) return false;
      if (DeviceId != other.DeviceId) return false;
      if (!object.Equals(Mesh, other.Mesh)) return false;
      if (!object.Equals(LocationRequest, other.LocationRequest)) return false;
      if (!object.Equals(LocationResponse, other.LocationResponse)) return false;
      return true;
    }

    public override int GetHashCode() {
      int hash = 1;
      if (Type != global::Holoscanner.Proto.Message.Types.Type.ACK) hash ^= Type.GetHashCode();
      if (DeviceId != 0) hash ^= DeviceId.GetHashCode();
      if (mesh_ != null) hash ^= Mesh.GetHashCode();
      if (locationRequest_ != null) hash ^= LocationRequest.GetHashCode();
      if (locationResponse_ != null) hash ^= LocationResponse.GetHashCode();
      return hash;
    }

    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    public void WriteTo(pb::CodedOutputStream output) {
      if (Type != global::Holoscanner.Proto.Message.Types.Type.ACK) {
        output.WriteRawTag(8);
        output.WriteEnum((int) Type);
      }
      if (DeviceId != 0) {
        output.WriteRawTag(16);
        output.WriteUInt32(DeviceId);
      }
      if (mesh_ != null) {
        output.WriteRawTag(162, 6);
        output.WriteMessage(Mesh);
      }
      if (locationRequest_ != null) {
        output.WriteRawTag(226, 18);
        output.WriteMessage(LocationRequest);
      }
      if (locationResponse_ != null) {
        output.WriteRawTag(130, 25);
        output.WriteMessage(LocationResponse);
      }
    }

    public int CalculateSize() {
      int size = 0;
      if (Type != global::Holoscanner.Proto.Message.Types.Type.ACK) {
        size += 1 + pb::CodedOutputStream.ComputeEnumSize((int) Type);
      }
      if (DeviceId != 0) {
        size += 1 + pb::CodedOutputStream.ComputeUInt32Size(DeviceId);
      }
      if (mesh_ != null) {
        size += 2 + pb::CodedOutputStream.ComputeMessageSize(Mesh);
      }
      if (locationRequest_ != null) {
        size += 2 + pb::CodedOutputStream.ComputeMessageSize(LocationRequest);
      }
      if (locationResponse_ != null) {
        size += 2 + pb::CodedOutputStream.ComputeMessageSize(LocationResponse);
      }
      return size;
    }

    public void MergeFrom(Message other) {
      if (other == null) {
        return;
      }
      if (other.Type != global::Holoscanner.Proto.Message.Types.Type.ACK) {
        Type = other.Type;
      }
      if (other.DeviceId != 0) {
        DeviceId = other.DeviceId;
      }
      if (other.mesh_ != null) {
        if (mesh_ == null) {
          mesh_ = new global::Holoscanner.Proto.Mesh();
        }
        Mesh.MergeFrom(other.Mesh);
      }
      if (other.locationRequest_ != null) {
        if (locationRequest_ == null) {
          locationRequest_ = new global::Holoscanner.Proto.LocationRequest();
        }
        LocationRequest.MergeFrom(other.LocationRequest);
      }
      if (other.locationResponse_ != null) {
        if (locationResponse_ == null) {
          locationResponse_ = new global::Holoscanner.Proto.LocationResponse();
        }
        LocationResponse.MergeFrom(other.LocationResponse);
      }
    }

    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            input.SkipLastField();
            break;
          case 8: {
            type_ = (global::Holoscanner.Proto.Message.Types.Type) input.ReadEnum();
            break;
          }
          case 16: {
            DeviceId = input.ReadUInt32();
            break;
          }
          case 802: {
            if (mesh_ == null) {
              mesh_ = new global::Holoscanner.Proto.Mesh();
            }
            input.ReadMessage(mesh_);
            break;
          }
          case 2402: {
            if (locationRequest_ == null) {
              locationRequest_ = new global::Holoscanner.Proto.LocationRequest();
            }
            input.ReadMessage(locationRequest_);
            break;
          }
          case 3202: {
            if (locationResponse_ == null) {
              locationResponse_ = new global::Holoscanner.Proto.LocationResponse();
            }
            input.ReadMessage(locationResponse_);
            break;
          }
        }
      }
    }

    #region Nested types
    /// <summary>Container for nested types declared in the Message message type.</summary>
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
    public static partial class Types {
      public enum Type {
        ACK = 0,
        MESH = 10,
        LOCATION_REQUEST = 11,
        LOCATION_RESPONSE = 12,
      }

    }
    #endregion

  }

  #endregion

}

#endregion Designer generated code