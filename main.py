from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import database

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
app = FastAPI(title="Live Auction Engine")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    current_auction = database.get_auction(1)
    if current_auction:
        await websocket.send_json({
            "event": "init",
            "auction": current_auction
        })

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            auction_id = payload.get("auction_id")
            bidder = payload.get("bidder")
            amount = float(payload.get("amount", 0))

            auction = database.get_auction(auction_id)
            if auction and amount > auction["current_price"]:
                database.place_bid(auction_id, bidder, amount)
                await manager.broadcast({
                    "event": "new_bid",
                    "auction_id": auction_id,
                    "bidder": bidder,
                    "current_price": amount
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
