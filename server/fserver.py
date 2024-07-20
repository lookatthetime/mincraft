from flask import Flask, request
import json
from socket import gethostbyname, gethostname

print(f"\n---\nRunning server on IP: {gethostbyname(gethostname())}\n---\n")

# if needed: run with 'python3 -m flask --app server/fserver.py run --host=0.0.0.0 --port=PUT_PORT_HERE'

class info:
    world = []

# Worldgen Stuff
world_size = int(input("World Size:"))
for x in range(world_size):
    for z in range(world_size):
        info.world.append([x, 0, z, "stone.png"])

app = Flask(__name__)

@app.route("/world", methods=['GET']) # methods=['GET']
def get_world():
    return json.dumps(info.world)

@app.route("/placed", methods=['POST'])
def block_placed():
    params = {
        'x': request.values.get('x'),
        'y': request.values.get('y'),
        'z': request.values.get('z'),
        'tex': request.values.get('tex')
    }
    info.world.append(
        [int(float(params["x"])), int(float(params["y"])), int(float(params["z"])), params["tex"]]
    )
    return ""

@app.route("/destroyed", methods=['POST'])
def block_destroyed():
    params = {
        'x': request.values.get('x'),
        'y': request.values.get('y'),
        'z': request.values.get('z'),
        'tex': request.values.get('tex')
    }
    info.world.remove(
        [int(float(params["x"])), int(float(params["y"])), int(float(params["z"])), params["tex"]]
    )
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=input("Run on port: "))