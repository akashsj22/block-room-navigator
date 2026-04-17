from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from code import build_building_graph, get_shortest_path, validate_room, identify_block, ROOM_CLUSTERS

app = FastAPI(title="PRP Campus Navigator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://block-room-navigator.vercel.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPH = build_building_graph()



def parse_room(value: str):
    return int(value) if value.isdigit() else value


def build_steps(path: list) -> list:
    display_steps = []
    i = 0
    while i < len(path):
        node = path[i]
        if isinstance(node, str) and node.startswith("Lift_"):
            lift_nodes = []
            while i < len(path) and isinstance(path[i], str) and path[i].startswith("Lift_"):
                lift_nodes.append(path[i])
                i += 1
            from_floor = lift_nodes[0].split("_")[1]
            to_floor   = lift_nodes[-1].split("_")[1]
            label = (
                f"Take Lift (stay on {to_floor})"
                if from_floor == to_floor
                else f"Take Lift: {from_floor} → {to_floor}"
            )
            display_steps.append({"type": "transit", "label": label})
        elif isinstance(node, str) and node.startswith("Stairs_"):
            stair_nodes = []
            while i < len(path) and isinstance(path[i], str) and path[i].startswith("Stairs_"):
                stair_nodes.append(path[i])
                i += 1
            from_floor = stair_nodes[0].split("_")[1]
            to_floor   = stair_nodes[-1].split("_")[1]
            label = (
                f"Use Stairs (stay on {to_floor})"
                if from_floor == to_floor
                else f"Use Stairs: {from_floor} → {to_floor}"
            )
            display_steps.append({"type": "transit", "label": label})
        else:
            block = identify_block(node)
            display_steps.append({"type": "room", "room": str(node), "block": block})
            i += 1
    return display_steps



@app.get("/api/rooms")
def list_rooms():
    rooms = []
    for block, nodes in ROOM_CLUSTERS.items():
        for n in nodes:
            rooms.append({"room": str(n), "block": block})
    return rooms


@app.get("/api/navigate")
def navigate(start: str, end: str):
    start_node = parse_room(start)
    end_node   = parse_room(end)

    if not validate_room(start_node):
        raise HTTPException(status_code=404, detail=f"Room '{start}' not found.")
    if not validate_room(end_node):
        raise HTTPException(status_code=404, detail=f"Room '{end}' not found.")

    path, weight = get_shortest_path(GRAPH, start_node, end_node)

    if not path:
        raise HTTPException(status_code=404, detail="No path found between these rooms.")

    steps = build_steps(path)
    return {"start": start, "end": end, "total_weight": weight, "steps": steps}



app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def index():
    return FileResponse("index.html")
