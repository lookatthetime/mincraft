import requests
import json
from client import GameClient

class SqliteFlaskClient(GameClient):
    def __init__(self, ip, port, name, session_id, player_tex) -> None:
        self.ip = ip
        self.port = port
        self.s = requests.Session()
        self.name = name
        self.session = session_id
        self.tex = player_tex


    def get_world(self):
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world").text)


    def get_world_version(self):
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world_version").text)


    def get_world_edits(self, start: int=None) -> list[list[any]]:
        params = {} if start is None else {"start": start}
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/world_edits", params=params).text)
    

    def get_players(self):
        return json.loads(self.s.get(f"http://{self.ip}:{self.port}/player").text)


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

    # POST /block -> id (could be x, y, z, coordinates)
    # PUT /block/x,y,z
    # DELETE /block/x,y,z
    # GET /block/x,y,z


    def send_player(self, position, tex):
        resp = self.s.put(f"http://{self.ip}:{self.port}/player/{self.name}", {
            "x": position[0],
            "y": position[1],
            "z": position[2],
            "tex": self.tex,
            "session_id": self.session
        })
        if resp.status_code == 401:
            raise RuntimeError("Player Already Claimed")

    # client:
    # make session id (could be uuid)
    # player = PUT /player/ingram {session_id: session id}
    # ... play ...
    # player.relinquish() (just sends PUT with session id None)

    # server code:
    # if player exists:
        # if player.session_id:
            # return error
        # else:
            # update with session_id
    # else:
        # create player with name 'name'


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

    client = SqliteFlaskClient("127.0.0.1", "8080", "blah", None, "notattex")

    client.send_player((0, 135, 2394), "notattex")
    print(client.get_players())