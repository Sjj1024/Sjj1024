import asyncio
import json
import uuid
from dataclasses import dataclass
from typing import Dict, Optional

import websockets
from websockets.server import WebSocketServerProtocol

HOST = "0.0.0.0"
PORT = 8765


@dataclass
class ClientInfo:
    websocket: WebSocketServerProtocol
    player_id: str
    player_name: str
    index: int


class GameServer:
    def __init__(self) -> None:
        self.clients: Dict[WebSocketServerProtocol, ClientInfo] = {}

    # 处理每个客户端的连接
    async def handler(self, websocket: WebSocketServerProtocol) -> None:
        client: Optional[ClientInfo] = None
        try:
            async for message in websocket:
                response = await self.process_message(websocket, message)
                if isinstance(response, ClientInfo):
                    client = response
                elif response is not None:
                    await websocket.send(response)
        except websockets.ConnectionClosed:
            pass
        finally:
            if client:
                await self.unregister_client(client)

    # 处理收到的消息
    async def process_message(self, websocket: WebSocketServerProtocol, message: str) -> Optional[ClientInfo]:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            return await self.error_message(websocket, "无效的JSON格式")

        message_type = data.get("type")
        if not message_type:
            return await self.error_message(websocket, "消息缺少type字段")

        if message_type == "connect":
            return await self.register_client(websocket, data)

        if websocket not in self.clients:
            return await self.error_message(websocket, "请先发送connect消息建立连接")

        client = self.clients[websocket]
        if data.get("playerId") != client.player_id:
            return await self.error_message(websocket, "playerId不匹配")

        if message_type in {"gameMessage", "collaborationData"}:
            await self.broadcast(message, exclude=client)
        elif message_type == "playerCountRequest":
            await self.send_player_count(websocket)
        else:
            await self.error_message(websocket, f"未知的消息类型: {message_type}")
        return None

    # 注册客户端
    async def register_client(self, websocket: WebSocketServerProtocol, data: Dict) -> Optional[ClientInfo]:
        player_id = data.get("playerId")
        player_name = data.get("playerName")
        if not player_id or not player_name or not self.is_valid_uuid(player_id):
            await self.error_message(websocket, "无效的连接消息，缺少必要字段或playerId格式错误")
            await websocket.close(code=1008, reason="无效的连接信息")
            return None

        if any(info.player_id == player_id for info in self.clients.values()):
            await self.error_message(websocket, "playerId已存在")
            await websocket.close(code=1008, reason="playerId已存在")
            return None

        index = self.allocate_index()
        client = ClientInfo(websocket=websocket, player_id=player_id, player_name=player_name, index=index)
        self.clients[websocket] = client

        await websocket.send(json.dumps({
            "type": "connected",
            "playerId": player_id,
            "playerName": player_name,
            "index": index,
            "playerCount": len(self.clients)
        }))
        await self.broadcast_player_state()
        print(f"玩家 {player_name} (ID: {player_id}, index: {index}) 已连接")
        return client

    # 注销客户端
    async def unregister_client(self, client: ClientInfo) -> None:
        if client.websocket in self.clients:
            del self.clients[client.websocket]
            print(f"玩家 {client.player_name} (ID: {client.player_id}) 已断开连接")
            await self.broadcast_player_state()

    # 广播消息给所有客户端，排除指定客户端（如果有）
    async def broadcast(self, message: str, exclude: Optional[ClientInfo] = None) -> None:
        tasks = []
        for info in self.clients.values():
            if exclude and info.websocket == exclude.websocket:
                continue
            tasks.append(self.safe_send(info.websocket, message))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    # 广播玩家状态更新
    async def broadcast_player_state(self) -> None:
        payload = json.dumps({
            "type": "playerCount",
            "count": len(self.clients),
            "players": [
                {
                    "playerId": info.player_id,
                    "playerName": info.player_name,
                    "index": info.index
                }
                for info in self.clients.values()
            ]
        })
        await self.broadcast(payload)

    # 发送当前玩家数量给指定客户端
    async def send_player_count(self, websocket: WebSocketServerProtocol) -> None:
        payload = json.dumps({
            "type": "playerCount",
            "count": len(self.clients)
        })
        await self.safe_send(websocket, payload)

    # 安全发送消息，处理连接关闭异常
    async def safe_send(self, websocket: WebSocketServerProtocol, message: str) -> None:
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

    # 发送错误消息
    async def error_message(self, websocket: WebSocketServerProtocol, message: str) -> Optional[str]:
        error_payload = json.dumps({
            "type": "error",
            "message": message
        })
        await self.safe_send(websocket, error_payload)
        return None

    # 分配最小可用索引
    def allocate_index(self) -> int:
        used_indices = sorted(info.index for info in self.clients.values())
        index = 0
        for used in used_indices:
            if used == index:
                index += 1
            else:
                break
        return index

    # 验证UUID格式
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False


# 启动WebSocket服务器
async def main() -> None:
    server = GameServer()
    async with websockets.serve(server.handler, HOST, PORT):
        print(f"WebSocket服务器已启动，监听 ws://{HOST}:{PORT}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器已停止")
