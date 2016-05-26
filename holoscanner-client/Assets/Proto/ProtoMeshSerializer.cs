using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public static class ProtoMeshSerializer {
    public static byte[] Serialize(Mesh mesh, Quaternion q, Vector3 v, uint id, bool islast, bool isfirst)
    {
        IEnumerable<Holoscanner.Proto.Vec3D> vertices = mesh.vertices.Select(x => {
            Holoscanner.Proto.Vec3D ret = new Holoscanner.Proto.Vec3D();
            ret.X = x.x;
            ret.Y = x.y;
            ret.Z = x.z;
            return ret;
        });
        Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
        msg.Type = Holoscanner.Proto.Message.Types.Type.MESH;
        msg.Mesh = new Holoscanner.Proto.Mesh();
        
        msg.Mesh.Vertices.Add(vertices);
        msg.Mesh.Triangles.Add(mesh.triangles);
        msg.Mesh.CamPosition = new Holoscanner.Proto.Vec3D();
        msg.Mesh.CamPosition.X = v.x;
        msg.Mesh.CamPosition.Y = v.y;
        msg.Mesh.CamPosition.Z = v.z;
        msg.Mesh.CamRotation = new Holoscanner.Proto.Vec4D();
        msg.Mesh.CamRotation.X = q.x;
        msg.Mesh.CamRotation.Y = q.y;
        msg.Mesh.CamRotation.Z = q.z;
        msg.Mesh.CamRotation.W = q.w;

        // FIXME - Fill in fields properly -------------------------------------------------------
#if !UNITY_EDITOR
        //msg.DeviceId = Windows.System.Profile.HardwareIdentification.getPackageSpecificToken().Id;
#else
        //msg.DeviceId = 0;
#endif
        msg.Mesh.Timestamp = (ulong)(System.DateTime.UtcNow - new System.DateTime(1970, 1, 1)).TotalMilliseconds;
        msg.Mesh.MeshId = id;
        msg.Mesh.IsLast = islast;
        msg.Mesh.IsFirst = isfirst;
        //msg.Mesh.CamPosition;
        // end FIXME -----------------------------------------------------------------------------
        return Google.Protobuf.MessageExtensions.ToByteArray(msg);
    }
    public static byte[] DataRequest()
    {
        Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
        msg.Type = Holoscanner.Proto.Message.Types.Type.GAME_STATE_REQUEST;
        return Google.Protobuf.MessageExtensions.ToByteArray(msg);
    }
    public static Holoscanner.Proto.Message parseMesssage(byte[] data)
    {
        return Holoscanner.Proto.Message.Parser.ParseFrom(data);
    }
    public static Mesh Deserialize(Holoscanner.Proto.Message msg)
    {
        Mesh m = new Mesh();
        // FIXME
        return m;
    }
}
