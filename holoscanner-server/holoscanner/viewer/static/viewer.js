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
  for (let i = 0; i < pbMesh.triangles.length / 3; i++) {
    geometry.faces.push(
        new THREE.Face3(pbMesh.triangles[i*3], pbMesh.triangles[i*3+1], pbMesh.triangles[i*3+2]));
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
  let scoreboard_el = $('#scoreboard');
  scoreboard_el.empty();
  scoreboard_el.append('<span>Client Scores</span>');
  for (let client of pbGameState.clients) {
    let client_el = $('<div>').addClass('scoreboard-client');
    client_el.text("[" + client.device_id + "]: " + client.score);
    scoreboard_el.append(client_el);
  }

  for (let i in pbGameState.targets) {
    let target = pbGameState.targets[i];
    let geom = new THREE.SphereGeometry(0.1, 32, 32);
    let color = (i == 0) ? 0xff0000 : 0x00ff00;
    let material = new THREE.MeshBasicMaterial({color: color});
    
    let targetMesh;
    if (i == 0) {
      targetMesh = new THREE.PointLight(
          0xff0000, 1.0 / pbGameState.targets.length, 0);
      targetMesh.add(new THREE.Mesh(
          geom, new THREE.MeshBasicMaterial({color: 0xff00ff})));
    } else {
      targetMesh = new THREE.Mesh(geom, material);
    }
    targetMesh.position.set(
        target.position.x, target.position.y, target.position.z);
    targetMesh.target_id = target.target_id;
    scene.add(targetMesh);
    targets.push(targetMesh);
  }
}

function initRenderer() {
  let container = $('#canvas');
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(container.width(), container.height());
  container.append(renderer.domElement);

  let ambientLight = new THREE.AmbientLight(0x333333);
  scene.add(ambientLight);

  let light = new THREE.PointLight(0xffffff, 0.5, 0);
  light.position.set(0, 10, 0);
  scene.add(light);

  let light2 = new THREE.PointLight(0xffffff, 0.1, 0);
  light2.position.set(100, 100, 0);
  scene.add(light2);

  let light3 = new THREE.PointLight(0xffffff, 0.1, 0);
  light3.position.set(-100, 100, 0);
  scene.add(light3);

  let light4 = new THREE.PointLight(0xffffff, 0.1, 0);
  light4.position.set(-100, -100, 0);
  scene.add(light4);

  let light5 = new THREE.PointLight(0xffffff, 0.1, 0);
  light5.position.set(100, -100, 0);
  scene.add(light5);

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
}

let test;
$(document).ready(function () {
  initRenderer();

  $('#reset-meshes').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.CLEAR_MESHES;
    test = message;
    socket.send(message.toArrayBuffer());
    for (let mesh of meshes) {
      scene.remove(mesh);
    }
    meshes.length = 0;
    console.log('Meshes cleared.');
  });
  
  $('#reset-game-state').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.CLEAR_GAME_STATE;
    test = message;
    socket.send(message.toArrayBuffer());
    console.log('Game state cleared.');
  });
  $('#update-targets').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.UPDATE_TARGETS;
    test = message;
    socket.send(message.toArrayBuffer());
    console.log('Game state cleared.');
  });
  $('#acquire-target').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.TARGET_FOUND;
    message.target_id = targets[0].target_id;
    socket.send(message.toArrayBuffer());
    console.log('Acquired target ' + message.target_id);
  });
});
