import json
from socket import gethostbyname, gethostname
import sqlite3
from os.path import exists

from flask import Flask, request, abort

print(f"\n---\nRunning server on IP: {gethostbyname(gethostname())}\n---\n")

# if needed: run with 'python3 -m flask --app server/sqlite_server.py run --host=0.0.0.0 --port=PUT_PORT_HERE'

app = Flask(__name__)

if not exists("/tmp/mincraft.db"):
    with sqlite3.connect("/tmp/mincraft.db") as con:
        print("Creating new 10x10 world.")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS world_edit(x INTEGER, y INTEGER, z INTEGER, texture TEXT)")
        for x in range(10):
            for z in range(10):
                cur.execute(f"INSERT INTO world_edit (x, y, z, texture) VALUES ({x}, 0, {z}, 'stone.png')")

        cur.execute("CREATE TABLE IF NOT EXISTS player(x INTEGER, y INTEGER, z INTEGER, texture TEXT, name TEXT UNIQUE, session_id TEXT)")
else:
    print("Using existing world.")


@app.route("/world", methods=['GET']) # methods=['GET']
def get_world():
    with sqlite3.connect("/tmp/mincraft.db") as con:
        world = con.cursor().execute(
            "SELECT x, y, z, texture FROM world_edit WHERE rowid IN (SELECT MAX(rowid) FROM world_edit GROUP BY x, y, z) AND texture IS NOT NULL")
        return json.dumps(world.fetchall())


@app.route("/world_edits", methods=['GET']) # methods=['GET']
def get_world_edits():
    start = request.args.get("start", default=0, type=int)
    with sqlite3.connect("/tmp/mincraft.db") as con:
        world_edits = con.cursor().execute(f"SELECT x, y, z, texture, rowid FROM world_edit WHERE rowid >= {start} ORDER BY rowid ASC")
        return json.dumps(world_edits.fetchall())


@app.route("/world_version", methods=['GET'])
def get_world_version():
    with sqlite3.connect("/tmp/mincraft.db") as con:
        world_version = con.cursor().execute("SELECT IFNULL(MAX(rowid), 0) FROM world_edit")
        return json.dumps(world_version.fetchone()[0])


@app.route("/placed", methods=['POST'])
def block_placed():
    with sqlite3.connect("/tmp/mincraft.db") as con:
        x = request.values.get('x')
        y = request.values.get('y')
        z = request.values.get('z')
        tex = request.values.get('tex')
        con.cursor().execute(f"INSERT INTO world_edit (x, y, z, texture) VALUES ({x}, {y}, {z}, '{tex}')")
        return ""


@app.route("/destroyed", methods=['POST'])
def block_destroyed():
    with sqlite3.connect("/tmp/mincraft.db") as con:
        x = request.values.get('x')
        y = request.values.get('y')
        z = request.values.get('z')
        con.cursor().execute(f"INSERT INTO world_edit (x, y, z, texture) VALUES ({x}, {y}, {z}, NULL)")
        return ""


@app.route("/player/<name>", methods=['PUT'])
def put_player(name):
    with sqlite3.connect("/tmp/mincraft.db") as con:
        x = request.values.get('x')
        y = request.values.get('y')
        z = request.values.get('z')
        tex = request.values.get('tex')
        session_id = request.values.get('session_id')
        player = con.cursor().execute(f"SELECT session_id FROM player WHERE name = '{name}'").fetchone()
        if player is not None and (session_id is not None and player[0] is not None and player[0] != session_id):
            abort(401, description="Player in use in another session.")
        elif player is not None:
            if session_id is None:
                con.cursor().execute(f"UPDATE player SET x = {x}, y = {y}, z = {z}, texture = '{tex}', session_id = NULL WHERE name = '{name}'")
            else:
                con.cursor().execute(f"UPDATE player SET x = {x}, y = {y}, z = {z}, texture = '{tex}', session_id = '{session_id}' WHERE name = '{name}'")
            return ""
        else:
            con.cursor().execute(f"INSERT INTO player (x, y, z, texture, session_id, name) VALUES ({x}, {y}, {z}, '{tex}', '{session_id}', '{name}')")
            return ""


@app.route("/player", methods=['GET'])
def get_players():
    with sqlite3.connect("/tmp/mincraft.db") as con:
        players = con.cursor().execute(f"SELECT x, y, z, texture, session_id, name FROM player ORDER BY rowid ASC")
        return json.dumps(players.fetchall())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=input("Run on port: "))
