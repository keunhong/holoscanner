let SOCKET_URL = 'ws://drell.cs.washington.edu:8889';
let CLIENT_COLORS = [
  '#64b5f6', '#ffb74d', '#aed581', '#f48fb1'
];

let ProtoBuf = dcodeIO.ProtoBuf;
let builder = ProtoBuf.loadProtoFile("static/holoscanner.proto");
let Holoscanner = builder.build("Holoscanner");
let Message = Holoscanner.Proto.Message;

let gRenderer = new THREE.WebGLRenderer();
let gScene = new THREE.Scene();

let gNumClients = 0;
let gClients = {};
let gTargets = [];
let gFloorPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshBasicMaterial({
      color: 0xff0000,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.2
    }));
gFloorPlane.rotation.x = Math.PI / 2;
let gCeilingPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshBasicMaterial({
      color: 0x00ff00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.2
    }));
gCeilingPlane.rotation.x = Math.PI / 2;

let gSocket = new ReconnectingWebSocket(SOCKET_URL, null, {
  binaryType: 'arraybuffer'
});
gSocket.onopen = function (e) {
  console.log('Websocket connected!');
};
gSocket.onclose = function (e) {
  console.log('Websocket connection lost, resetting!');
  resetAll();
};
gSocket.onmessage = function (e) {
  console.log(e);
  if (e.data instanceof ArrayBuffer) {
    let pbMessage = Holoscanner.Proto.Message.decode(e.data);
    // console.log(pbMessage);

    switch (pbMessage.type) {
      case Holoscanner.Proto.Message.Type.MESH:
        handleNewMesh(pbMessage.device_id, pbMessage.mesh);
        break;
      case Message.Type.GAME_STATE:
        handleGameState(pbMessage.game_state);
        break;
      case Message.Type.CLEAR_MESHES:
        console.log(pbMessage.device_id);
        if (pbMessage.device_id) {
          clearMeshes(pbMessage.device_id);
        }
        break;
      case Message.Type.CLIENT_POSITION:
        handleClientPosition(pbMessage.device_id, pbMessage.client_position);
        break;
      default:
        console.log('Unknown message type ' + pbMessage);
    }
  }
};

let gModelQuat = new THREE.Quaternion();
gModelQuat.setFromAxisAngle(new THREE.Vector3( 0, 0, 1 ), -Math.PI / 2);

function handleClientPosition(deviceId, pbClientPosition) {
  if (deviceId in gClients) {
    let client = gClients[deviceId];
    let p = pbClientPosition.position;
    let r = pbClientPosition.rotation;
    client["marker"].quaternion.set(r.x, r.y, r.z, r.w).multiply(gModelQuat);
    client["marker"].position.set(-p.x, p.y, -p.z);
  }
}

function resetAll() {
  clearAllMeshes();
  for (let target of gTargets) {
    gRenderer.remove(target);
  }
}

function handleNewMesh(deviceId, pbMesh) {
  if (!(deviceId in gClients)) {
    let geometry = new THREE.ConeGeometry( 0.1, 0.5, 10, 50 );
    let material = new THREE.MeshPhongMaterial( {color: 0xffff00} );
    let marker = new THREE.Mesh(geometry, material);
    gScene.add(marker);
    let clientIndex = gNumClients++;
    gClients[deviceId] = {
      "meshes": [],
      "newMeshes": [],
      "color": CLIENT_COLORS[clientIndex % CLIENT_COLORS.length],
      "index": clientIndex,
      "visible": true,
      "marker": marker
    };
  }

  let meshGeometry = new THREE.Geometry();
  for (let vertex of pbMesh.vertices) {
    meshGeometry.vertices.push(
        new THREE.Vector3(vertex.x, vertex.y, vertex.z));
  }
  for (let i = 0; i < pbMesh.triangles.length / 3; i++) {
    meshGeometry.faces.push(
        new THREE.Face3(
            pbMesh.triangles[i * 3],
            pbMesh.triangles[i * 3 + 1],
            pbMesh.triangles[i * 3 + 2]));
  }
  let meshMaterial = new THREE.MeshLambertMaterial({
    color: gClients[deviceId]["color"],
    side: ($('#mesh-doubleside-checkbox').prop('checked'))
        ? THREE.DoubleSide
        : THREE.FrontSide
  });
  meshGeometry.computeFaceNormals();
  let meshObj = new THREE.Mesh(meshGeometry, meshMaterial);
  meshObj.scale.x = meshObj.scale.y = meshObj.scale.z = 1.0;
  meshObj.device_id = deviceId;
  meshObj.name = deviceId + "_" + gClients[deviceId]["meshes"].length;
  meshObj.visible = gClients[deviceId]["visible"];
  gClients[deviceId]["newMeshes"].push(meshObj);

  if (pbMesh.is_last) {
    clearMeshes(deviceId);
    gClients[deviceId]["meshes"] = gClients[deviceId]["newMeshes"];
    gClients[deviceId]["newMeshes"] = [];
    for (let mesh of gClients[deviceId]["meshes"]) {
      gScene.add(mesh);
    }
  }
}

function handleGameState(pbGameState) {
  if (pbGameState == null) {
    console.log('Game state is null.');
    return;
  }
  console.log(pbGameState);
  gFloorPlane.position.y = pbGameState.floor_y;
  gCeilingPlane.position.y = pbGameState.ceiling_y;

  for (let target of gTargets) {
    gScene.remove(target);
  }
  gTargets.length = 0;
  let scoreboardElem = $('#scoreboard')
      .empty();
  for (let pbClient of pbGameState.clients) {
    console.log(pbClient);
    let clientColor = (pbClient.device_id in gClients)
        ? gClients[pbClient.device_id]["color"]
        : 0xffffff;
    let clientDiv = $('<div>')
        .addClass('scoreboard-client')
        .css('color', clientColor);

    let clientLabel = "[" + pbClient.device_id + "]: " + pbClient.score;
    if (pbClient.device_id !== '__server__'
        && pbClient.device_id in gClients) {
      let client = gClients[pbClient.device_id];
      let clientCheckbox = $("<input type='checkbox'>")
          .prop('id', 'client-' + client["index"] + '-checkbox')
          .prop('checked', client["visible"])
          .change(function () {
            client["visible"] = this.checked;
            for (let mesh of gClients[pbClient.device_id]["meshes"]) {
              mesh.visible = this.checked;
            }
          });
      clientDiv.append(clientCheckbox);
      clientLabel = $('<label>')
          .prop('for', clientCheckbox.attr('id'))
          .append(clientLabel);
    }
    clientDiv.append(clientLabel);
    if (pbClient.is_ready) {
      clientDiv.append(
          "<span class='client-status client-ready'>✓</span>");
    } else {
      clientDiv.append(
          "<span class='client-status client-not-ready'>✗</span>");
    }
    scoreboardElem.append(clientDiv);
  }

  for (let clientId in gClients) {
    let exists = false;
    for (let pbClient of pbGameState.clients) {
      exists |= (pbClient.device_id === clientId);
    }
    if (!exists) {
      for (let mesh of gClients[clientId]["meshes"]) {
        gScene.remove(mesh);
      }
      gScene.remove(gClients[clientId]["marker"]);
      delete gClients[clientId];
    }
  }

  for (let targetIdx in pbGameState.targets) {
    let pbTarget = pbGameState.targets[targetIdx];
    let geom = new THREE.SphereGeometry(0.1, 32, 32);
    let color = (targetIdx == 0) ? 0xff0000 : 0x00ff00;
    let material = new THREE.MeshPhongMaterial({color: color});
    let targetMesh = new THREE.Mesh(geom, material);
    material.transparent = true;
    material.opacity = 0.5;
    targetMesh.position.set(
        pbTarget.position.x, pbTarget.position.y, pbTarget.position.z);
    targetMesh.target_id = pbTarget.target_id;
    gScene.add(targetMesh);
    gTargets.push(targetMesh);
  }
}

function newLight(color, intensity, x, y, z) {
  let light = new THREE.PointLight(color, intensity, 0);
  light.position.set(x, y, z);
  return light;
}

function initRenderer() {
  let container = $('#canvas');
  gRenderer.setPixelRatio(window.devicePixelRatio);
  gRenderer.setSize(container.width(), container.height());
  container.append(gRenderer.domElement);

  let ambientLight = new THREE.AmbientLight(0x333333);
  gScene.add(ambientLight);

  let lights = [
    newLight(0xffffff, 0.4, 0, 10, 0),
    newLight(0xffffff, 0.4, 100, 100, 0),
    newLight(0xffffff, 0.4, -100, 100, 0),
    newLight(0xffffff, 0.4, -100, -100, 0),
    newLight(0xffffff, 0.4, 100, -100, 0)
  ];
  
  for (let light of lights) {
    gScene.add(light);
  }

  let camera = new THREE.PerspectiveCamera(
      75, container.width() / container.height(), 0.1, 1000);
  camera.position.set(0, 0, 5);

  gScene.add(camera);
  gScene.add(gFloorPlane);
  gScene.add(gCeilingPlane);

  controls = new THREE.OrbitControls(camera, gRenderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.25;

  function render() {
    requestAnimationFrame(render);
    gRenderer.render(gScene, camera);
  }
  render();
}

$(document).ready(function () {
  initRenderer();

  $('#reset-meshes').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.CLEAR_MESHES;
    gSocket.send(message.toArrayBuffer());
    clearAllMeshes();
    console.log('Meshes cleared.');
  });

  $('#reset-game-state').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.CLEAR_GAME_STATE;
    gSocket.send(message.toArrayBuffer());
    console.log('Game state cleared.');
  });
  $('#update-gTargets').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.UPDATE_TARGETS;
    gSocket.send(message.toArrayBuffer());
    console.log('Game state cleared.');
  });
  $('#acquire-target').click(function () {
    let message = new Holoscanner.Proto.Message();
    message.type = Holoscanner.Proto.Message.Type.TARGET_FOUND;
    message.target_id = gTargets[0].target_id;
    gSocket.send(message.toArrayBuffer());
    console.log('Acquired target ' + message.target_id);
  });
  $('#floor-checkbox').change(function () {
    gFloorPlane.visible = this.checked;
  });
  $('#ceiling-checkbox').change(function () {
    gCeilingPlane.visible = this.checked;
  });
  $('#mesh-doubleside-checkbox').change(function () {
    let self = this;
    for (let client_id in gClients) {
      for (let mesh of gClients[client_id]["meshes"]) {
        mesh.material.side = (self.checked) ? THREE.DoubleSide : THREE.FrontSide;
      }
    }
  });
});


function clearAllMeshes() {
  for (let client_id in gClients) {
    for (let mesh of gClients[client_id]["meshes"]) {
      gScene.remove(mesh);
    }
  }
  for (let client_id in gClients) {
    gClients[client_id]["meshes"].length = 0;
  }
}

function clearMeshes(deviceId) {
  console.log('Clearing meshes for client ' + deviceId);
  for (let mesh of gClients[deviceId]["meshes"]) {
    gScene.remove(mesh);
  }
  gClients[deviceId]["meshes"].length = 0;
}
