import requests
import json
from server.client import GameClient

class SqliteFlaskClient(GameClient):
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.s = requests.Session()


    def get_world(self):
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world").text)


    def get_world_version(self):
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world_version").text)


    def get_world_edits(self, start: int=None) -> list[list[any]]:
        params = {} if start is None else {"start": start}
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world_edits", params=params).text)


    def send_block(self, position, tex):
        self.s.post(f"http://{self.ip}:{self.port}/placed", {
            "x": position[0],
            "y": position[1],
            "z": position[2],
            "tex": tex
        })

    def send_destroy(self, position, tex):
        self.s.post(f"http://{self.ip}:{self.port}/destroyed", {
            "x": position[0],
            "y": position[1],
            "z": position[2]
        })

if __name__ == "__main__":
    # ip = input("Server IP: ")
    # port = input("Listen on port: ")

    # while True:
    #     world = json.loads(requests.get(f"http://{ip}:{port}/world").text)
        
    #     # requests.get(f"http://{ip}:{port}/placed", [])
    #     requests.post(f"http://{ip}:{port}/placed", {
    #         "x": 0,
    #         "y": 0,
    #         "z": 0,
    #         "tex": "stone.png"
    #     })

    #     print(world)

    client = FlaskClient("127.0.0.1", "9000")

    while True:
        client.get_world()
        client.send_block(0, 0, 0, "grass.png")