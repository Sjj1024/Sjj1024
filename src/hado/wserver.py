import asyncio
import websockets
import json
from uuid import UUID
from typing import Dict, Set

# 存储连接的客户端和玩家信息
# 结构: {websocket对象: (player_id, player_name)}
connected_clients: Dict[websockets.WebSocketServerProtocol, tuple[str, str]] = {}


def is_valid_uuid(uuid_str: str) -> bool:
    """验证UUID格式是否有效"""
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False


async def broadcast_player_count():
    """向所有连接的客户端广播当前玩家数量"""
    player_count = len(connected_clients)
    message = json.dumps({
        "type": "playerCountUpdate",
        "count": player_count,
        "players": [
            {"playerId": pid, "playerName": pname}
            for _, (pid, pname) in connected_clients.items()
        ]
    })

    # 向所有连接的客户端发送更新
    for websocket in connected_clients:
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            pass


async def handle_message(websocket, message):
    """处理收到的消息并根据类型进行相应处理"""
    try:
        data = json.loads(message)
        message_type = data.get("type")

        # 验证消息基本结构
        if not message_type:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "消息缺少type字段"
            }))
            return

        # 处理连接消息
        if message_type == "connect":
            player_id = data.get("playerId")
            player_name = data.get("playerName")

            # 验证连接消息的有效性
            if not player_id or not player_name or not is_valid_uuid(player_id):
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "无效的连接消息，缺少必要字段或playerId格式错误"
                }))
                await websocket.close(code=1008, reason="无效的连接信息")
                return

            # 检查playerId是否已存在
            for existing_id, _ in connected_clients.values():
                if existing_id == player_id:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "playerId已存在"
                    }))
                    await websocket.close(code=1008, reason="playerId已存在")
                    return

            # 存储客户端信息
            connected_clients[websocket] = (player_id, player_name)
            print(f"玩家 {player_name} (ID: {player_id}) 已连接")

            # 广播玩家数量更新
            await broadcast_player_count()

        # 处理游戏消息 - 广播给其他所有客户端
        elif message_type == "gameMessage":
            player_id = data.get("playerId")

            # 验证发送者是否已连接
            if websocket not in connected_clients:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "请先发送connect消息建立连接"
                }))
                return

            # 验证playerId匹配
            if connected_clients[websocket][0] != player_id:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "playerId不匹配"
                }))
                return

            # 广播消息给所有其他客户端
            for client in connected_clients:
                if client != websocket:  # 排除发送者
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass

        # 处理AR协作数据 - 广播给其他所有客户端
        elif message_type == "collaborationData":
            player_id = data.get("playerId")

            # 验证发送者是否已连接
            if websocket not in connected_clients:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "请先发送connect消息建立连接"
                }))
                return

            # 验证playerId匹配
            if connected_clients[websocket][0] != player_id:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "playerId不匹配"
                }))
                return

            # 广播数据给所有其他客户端
            for client in connected_clients:
                if client != websocket:  # 排除发送者
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass

        # 处理未知类型消息
        else:
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"未知的消息类型: {message_type}"
            }))

    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "message": "无效的JSON格式"
        }))
    except Exception as e:
        await websocket.send(json.dumps({
            "type": "error",
            "message": f"处理消息时发生错误: {str(e)}"
        }))


async def handle_client(websocket):
    """处理客户端连接的主函数"""
    try:
        # 接收并处理消息
        async for message in websocket:
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed:
        print("客户端连接已关闭")
    finally:
        # 处理断开连接
        if websocket in connected_clients:
            player_id, player_name = connected_clients[websocket]
            del connected_clients[websocket]
            print(f"玩家 {player_name} (ID: {player_id}) 已断开连接")

            # 广播玩家数量更新
            await broadcast_player_count()


async def main():
    """启动WebSocket服务器"""
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket服务器已启动，监听端口 8765")
        await asyncio.Future()  # 保持服务器运行


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器已停止")