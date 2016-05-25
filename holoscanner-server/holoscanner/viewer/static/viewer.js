let ProtoBuf = dcodeIO.ProtoBuf;
let builder = ProtoBuf.loadProtoFile("static/holoscanner.proto");
let Holoscanner = builder.build("Holoscanner");

let renderer = new THREE.WebGLRenderer();

let scene = new THREE.Scene();


let clientColors = [
    '#bbdefb', '#e1bee7', '#f48fb1', '#e6ee9c'
];

let numClients = 0;
let clients = {};
let targets = [];
let floorPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshBasicMaterial({
      color: 0xff0000,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.2
    }));
floorPlane.rotation.x = Math.PI / 2;
let ceilingPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshBasicMaterial({
      color: 0x00ff00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.2
    }));
ceilingPlane.rotation.x = Math.PI / 2;

var socket = new WebSocket('ws://drell.cs.washington.edu:8889');
socket.binaryType = "arraybuffer";
socket.onmessage = function (e) {
  if (e.data instanceof ArrayBuffer) {
    let message = Holoscanner.Proto.Message.decode(e.data);
    console.log(message);

    if (message.type === Holoscanner.Proto.Message.Type.MESH) {
      handleNewMesh(message.device_id, message.mesh);
    } else if (message.type === Holoscanner.Proto.Message.Type.GAME_STATE) {
      handleGameState(message.game_state);
    } else if (message.type === Holoscanner.Proto.Message.Type.CLEAR_MESHES) {
      clearAllMeshes();
      handleGameState(message.game_state);
    }
  }
};

function handleNewMesh(device_id, pbMesh) {
  if (!(device_id in clients)) {
    clients[device_id] = {
      "meshes": [],
      "color": clientColors[numClients++]
    };
  }

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
    color: clients[device_id]["color"],
    side: THREE.DoubleSide
  });
  geometry.computeFaceNormals();
  let mesh = new THREE.Mesh(geometry, material);
  mesh.scale.x = mesh.scale.y = mesh.scale.z = 1.0;
  mesh.device_id = device_id;
  mesh.name = device_id + "_" + clients[device_id]["meshes"].length;
  scene.add(mesh);
  clients[device_id]["meshes"].push(mesh);
}

function handleGameState(pbGameState) {
  if (pbGameState == null) {
    console.log('Game state is null.');
    return;
  }
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
    console.log(client);
    let clientColor = (client.device_id in clients)
        ? clients[client.device_id]["color"]
        : 0xffffff;
    let client_el = $('<div>').addClass('scoreboard-client');
    client_el.css('color', clientColor);
    client_el.text("[" + client.device_id + "]: " + client.score);
    scoreboard_el.append(client_el);
  }

  for (let client_id in clients) {
    let exists = false;
    for (let pbClient of pbGameState.clients) {
      console.log(pbClient.device_id, client_id);
      exists |= (pbClient.device_id === client_id);
    }
    if (!exists) {
      for (let mesh of clients[client_id]["meshes"]) {
        scene.remove(mesh);
      }
      delete clients[client_id];
    }
  }

  for (let i in pbGameState.targets) {
    let target = pbGameState.targets[i];
    let geom = new THREE.SphereGeometry(0.1, 32, 32);
    let color = (i == 0) ? 0xff0000 : 0x00ff00;
    let material = new THREE.MeshPhongMaterial({color: color});
    
    let targetMesh;
    // if (i == 0) {
    //   targetMesh = new THREE.PointLight(0xff0000, 0.5, 0, 10);
    //   targetMesh.add(new THREE.Mesh(
    //       geom, new THREE.MeshPhongMaterial({color: 0xff00ff})));
    // } else {
      targetMesh = new THREE.Mesh(geom, material);
      material.transparent = true;
      material.opacity = 0.5;
    // }
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

  let light = new THREE.PointLight(0xffffff, 0.4, 0);
  light.position.set(0, 10, 0);
  scene.add(light);

  let light2 = new THREE.PointLight(0xffffff, 0.4, 0);
  light2.position.set(100, 100, 0);
  scene.add(light2);

  let light3 = new THREE.PointLight(0xffffff, 0.4, 0);
  light3.position.set(-100, 100, 0);
  scene.add(light3);

  let light4 = new THREE.PointLight(0xffffff, 0.4, 0);
  light4.position.set(-100, -100, 0);
  scene.add(light4);

  let light5 = new THREE.PointLight(0xffffff, 0.4, 0);
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
    clearAllMeshes();
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
  $('#plane-checkbox').change(function () {
    floorPlane.visible = this.checked;
    ceilingPlane.visible = this.checked;
  });
  $('#mesh-doubleside-checkbox').change(function () {
    let self = this;
    forEachMesh(function (mesh) {
      mesh.material.side = (self.checked) ? THREE.DoubleSide : THREE.FrontSide;
    })
  });
});


function forEachMesh(func) {
  for (let client_id in clients) {
    for (let mesh of clients[client_id]["meshes"]) {
      func(mesh);
    }
  }
}

function clearAllMeshes() {
  forEachMesh(function (mesh) {
    scene.remove(mesh);
  });
  for (let client_id in clients) {
    clients[client_id]["meshes"].length = 0;
  }
}
