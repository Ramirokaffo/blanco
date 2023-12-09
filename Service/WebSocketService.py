import json
import secrets
import asyncio
from tkinter import Tk

import websockets

from Service.QRCodeService import QRCodeService
from Service.WIFIService import WIFIService


class WebSocketService:
    qr_code_path = QRCodeService.create_code(f"{WIFIService.get_local_ip()}:9090")
    service = None
    connected = set()

    def __init__(self, ip: str = None, port: int = 9090):
        self.start_serve = websockets.serve(self.handler, "", port)
        self.port = port
        self.ip = ip
        WebSocketService.service = self

    async def handler(self, websocket, path):
        WebSocketService.connected.add(websocket)
        data = await websocket.recv()
        print(data)
        event = {"type": "serveur"}
        await websocket.send(json.dumps(event))
        print("jai exec")
        await websocket.wait_closed()
        print('oui ici')

    async def send_data(self, data):
        for con in WebSocketService.connected:
            con.send(data)

    async def connect(self, ip: str = None):
        if not ip:
            self.ip = WIFIService.get_local_ip()
        else:
            self.ip = ip
        print(self.ip)
        WebSocketService.qr_code_path = QRCodeService.create_code(f"{self.ip}:{self.port}")
        async with websockets.serve(self.handler, self.ip, self.port):
            await asyncio.Future()

    def start_server(self, ip: str = None):

        if not ip:
            self.ip = WIFIService.get_local_ip()
        else:
            self.ip = ip
            print(self.ip)
        self.start_serve = websockets.serve(self.handler, self.ip, self.port)
        WebSocketService.qr_code_path = QRCodeService.create_code(f"{self.ip}:{self.port}")

        # asyncio.get_event_loop().run_until_complete(self.start_serve)
        # asyncio.get_event_loop().run_until_complete(self.start_serve)
        asyncio.get_event_loop().run_forever()
        # self.start_serve.ws_server.close()
        # WebSocketService.qr_code_path =
        # print("Je suis dans start_server", )
        # return WebSocketService.qr_code_path

# asyncio.run(WebSocketService().connect())
# WebSocketService.service.start_serve()
WebSocketService()
# mainloop()