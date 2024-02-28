import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:1998/ws"  # WebSocket server URI
    async with websockets.connect(uri) as websocket:
        while True:
            # Receive data from the WebSocket server
            data = await websocket.recv()
            print("Received:", data)

asyncio.run(receive_data())
