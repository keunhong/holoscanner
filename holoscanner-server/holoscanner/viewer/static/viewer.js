let ProtoBuf = dcodeIO.ProtoBuf;
let builder = ProtoBuf.loadProtoFile("static/holoscanner.proto");
let Holoscanner = builder.build("Holoscanner");

var socket = new WebSocket('ws://127.0.0.1:8889');

socket.binaryType = "arraybuffer";

socket.onmessage = function (e) {
    if (e.data instanceof ArrayBuffer) {
        let message = Holoscanner.Proto.Message.decode(e.data);
        console.log(message);
        console.log(message.getDeviceId());
        // let mesh = message.getMesh()
        // console.log(message.getDeviceId());
        // console.log(mesh.getFacesList());
    }
};

