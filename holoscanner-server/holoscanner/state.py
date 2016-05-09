import threading
import asyncio
import copy


class GameState:
    meshes = []
    lock = threading.RLock()
    queue = asyncio.Queue()

    def new_mesh(self, mesh):
        with self.lock:
            self.meshes.append(mesh)
            print(len(self.meshes))
        self.queue.put_nowait(mesh)


game_state = GameState()
