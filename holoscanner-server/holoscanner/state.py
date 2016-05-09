import threading


class GameState:
    meshes = []
    lock = threading.RLock()

    def new_mesh(self, mesh):
        with self.lock:
            self.meshes.append(mesh)
            print(len(self.meshes))
