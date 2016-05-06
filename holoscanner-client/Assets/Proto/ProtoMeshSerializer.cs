using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public static class ProtoMeshSerializer {
    public static byte[] Serialize(Mesh mesh)
    {
        IEnumerable<Holoscanner.Proto.Vec3D> vertices = mesh.vertices.Select(x => {
            Holoscanner.Proto.Vec3D ret = new Holoscanner.Proto.Vec3D();
            ret.X = x.x;
            ret.Y = x.y;
            ret.Z = x.z;
            return ret;
        });
        List<Holoscanner.Proto.Face> faces = new List<Holoscanner.Proto.Face>();
        for (int i = 0; i < mesh.triangles.Length; i+=3)
        {
            Holoscanner.Proto.Face f = new Holoscanner.Proto.Face();
            f.V1 = (uint) mesh.triangles[i];
            f.V2 = (uint) mesh.triangles[i + 1];
            f.V3 = (uint) mesh.triangles[i + 2];
            faces.Add(f);
        }

        Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
        msg.Type = Holoscanner.Proto.Message.Types.Type.MESH;
        msg.Mesh = new Holoscanner.Proto.Mesh();
        msg.Mesh.Vertices.Add(vertices);
        msg.Mesh.Faces.Add(faces);
        // FIXME - Fill in fields properly -------------------------------------------------------
#if !UNITY_EDITOR
        //msg.DeviceId = Windows.System.Profile.HardwareIdentification.getPackageSpecificToken().Id;
#else
        msg.DeviceId = 0;
#endif
        msg.Mesh.Timestamp = (ulong)(System.DateTime.UtcNow - new System.DateTime(1970, 1, 1)).TotalMilliseconds;
        msg.Mesh.MeshId = 0;
        //msg.Mesh.CamPosition;
        //msg.Mesh.CamRotation;
        // end FIXME -----------------------------------------------------------------------------

        byte[] msgbytes = Google.Protobuf.MessageExtensions.ToByteArray(msg);
        byte[] lenbytes = System.BitConverter.GetBytes((ulong) msgbytes.Length);
        byte[] retbytes = new byte[lenbytes.Length + msgbytes.Length];
        lenbytes.CopyTo(retbytes, 0);
        msgbytes.CopyTo(retbytes, lenbytes.Length);
        return retbytes;
    }

    public static Mesh Deserialize(byte[] data)
    {
        Holoscanner.Proto.Message msg = Holoscanner.Proto.Message.Parser.ParseFrom(data);

        Mesh m = new Mesh();
        // FIXME
        return m;
    }

}
