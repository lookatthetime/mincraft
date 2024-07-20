import requests
import json

class FlaskClient:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
    
    def get_world(self):
        return json.loads(requests.get(f"http://{self.ip}:{self.port}/world").text)
    
    def send_block(self, position, tex):
        requests.post(f"http://{self.ip}:{self.port}/placed", {
            "x": position[0],
            "y": position[1],
            "z": position[2],
            "tex": tex
        })
    
    def send_destroy(self, position, tex):
        requests.post(f"http://{self.ip}:{self.port}/destroyed", {
            "x": position[0],
            "y": position[1],
            "z": position[2],
            "tex": tex
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