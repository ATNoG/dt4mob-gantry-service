import asyncio

from app.bridge_service import BridgeService

if __name__ == "__main__":
    bridge_service = BridgeService()
    asyncio.run(bridge_service.run())
