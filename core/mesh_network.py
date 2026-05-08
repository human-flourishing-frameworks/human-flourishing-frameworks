import asyncio

class MeshNetwork:
    def __init__(self):
        self.connected_peers = []
        self.known_peers = []
    
    async def discover_peers(self):
        return self.connected_peers
    
    async def connect_peer(self, peer_addr):
        if peer_addr not in self.connected_peers:
            self.connected_peers.append(peer_addr)
        return True
    
    async def sync_violations(self, peer):
        await asyncio.sleep(0.1)
        return True
    
    async def broadcast_violations(self):
        for peer in self.connected_peers:
            await asyncio.sleep(0.1)
        return True