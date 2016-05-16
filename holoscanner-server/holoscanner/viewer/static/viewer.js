let ProtoBuf = dcodeIO.ProtoBuf;
let builder = ProtoBuf.loadProtoFile("static/holoscanner.proto");
let Holoscanner = builder.build("Holoscanner");

let renderer = new THREE.WebGLRenderer();
let scene = new THREE.Scene();

let meshes = [];
let targets = [];
let floorPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshLambertMaterial({
      color: 0x55ff55,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.5
    }));
floorPlane.rotation.x = Math.PI / 2;
let ceilingPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshLambertMaterial({
      color: 0x5555ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.5
    }));
ceilingPlane.rotation.x = Math.PI / 2;

var socket = new WebSocket('ws://drell.cs.washington.edu:8889');
socket.binaryType = "arraybuffer";
socket.onmessage = function (e) {
  if (e.data instanceof ArrayBuffer) {
    let message = Holoscanner.Proto.Message.decode(e.data);
    console.log(message);

    if (message.type === Holoscanner.Proto.Message.Type.MESH) {
      handleNewMesh(message.mesh);
    } else if (message.type === Holoscanner.Proto.Message.Type.GAME_STATE) {
      handleGameState(message.game_state);
    }
  }
};

function handleNewMesh(pbMesh) {
  let geometry = new THREE.Geometry();
  for (let vertex of pbMesh.vertices) {
    geometry.vertices.push(
        new THREE.Vector3(vertex.x, vertex.y, vertex.z));
  }
  for (let face of pbMesh.faces) {
    geometry.faces.push(
        new THREE.Face3(face.v1, face.v2, face.v3));
  }
  let material = new THREE.MeshLambertMaterial({
    color: 0xffffff,
    side: THREE.DoubleSide
  });
  geometry.computeFaceNormals();
  let mesh = new THREE.Mesh(geometry, material);
  mesh.scale.x = mesh.scale.y = mesh.scale.z = 1.0;
  scene.add(mesh);
  meshes.push(mesh);
}

function handleGameState(pbGameState) {
  console.log(pbGameState);
  floorPlane.position.y = pbGameState.floor_y;
  ceilingPlane.position.y = pbGameState.ceiling_y;

  for (let target of targets) {
    scene.remove(target);
  }
  targets.length = 0;

  for (let target of pbGameState.targets) {
    console.log(target);
    let targetMesh = new THREE.Mesh(
        new THREE.SphereGeometry(0.1, 32, 32),
        new THREE.MeshLambertMaterial({
          color: 0xffff00
        }));
    targetMesh.position.set(
        target.position.x, target.position.y, target.position.z);
    scene.add(targetMesh);
    targets.push(targetMesh);
  }
}


$(document).ready(function () {
  let container = $('#canvas');
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(container.width(), container.height());
  container.append(renderer.domElement);

  var sphere = new THREE.SphereGeometry(0.5, 16, 8);

  let ambientLight = new THREE.AmbientLight(0x333333);
  scene.add(ambientLight);

  let light = new THREE.PointLight(0xffffff, 0.5, 0);
  light.add(new THREE.Mesh(sphere, new THREE.MeshBasicMaterial({color: 0xff0040})));
  light.position.set(0, 10, 0);
  scene.add(light);

  let light2 = new THREE.PointLight(0xffffff, 0.5, 0);
  light2.add(new THREE.Mesh(sphere, new THREE.MeshBasicMaterial({color: 0xff0040})));
  light2.position.set(100, 100, 0);
  scene.add(light2);

  let light3 = new THREE.PointLight(0xffffff, 0.5, 0);
  light3.add(new THREE.Mesh(sphere, new THREE.MeshBasicMaterial({color: 0xff0040})));
  light3.position.set(-100, 100, 0);
  scene.add(light3);

  let camera = new THREE.PerspectiveCamera(
      75, container.width() / container.height(), 0.1, 1000);
  camera.position.x = 0;
  camera.position.y = 0;
  camera.position.z = 5;
  scene.add(camera);
  scene.add(floorPlane);
  scene.add(ceilingPlane);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.25;

  function render() {
    requestAnimationFrame(render);
    renderer.render(scene, camera);
  }

  render();
});
