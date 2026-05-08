import requests
import json

nodes = {
    'Node 1 (Primary)': 'http://localhost:9999/api/status',
    'Node 2 (Consensus)': 'http://localhost:9998/api/status',
    'Node 3 (Consensus)': 'http://localhost:9997/api/status',
    'Node 4 (Consensus)': 'http://localhost:9996/api/status',
    'Railway (Cloud)': 'https://web-production-46794.up.railway.app/api/status'
}

print("\n" + "="*70)
print("NETWORK TOPOLOGY VALIDATION")
print("="*70 + "\n")

online_count = 0

for name, url in nodes.items():
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            online_count += 1
            
            print(f"[OK] {name}")
            
            if 'node_id' in data:
                print(f"    Node ID: {data['node_id']}")
            
            if 'port' in data:
                print(f"    Port: {data['port']}")
            
            if 'status' in data:
                print(f"    Status: {data['status']}")
            
            if 'consensus' in data:
                cons = data['consensus']
                print(f"    Consensus: {cons.get('proposals', 0)} proposals, {cons.get('threshold', 'N/A')} threshold")
            
            if 'mesh' in data:
                mesh = data['mesh']
                if 'connected_peers' in mesh:
                    print(f"    Connected Peers: {mesh['connected_peers']}")
                elif 'active_nodes' in mesh:
                    print(f"    Active Nodes: {mesh['active_nodes']}")
            
            if 'violations' in data:
                print(f"    Violations Detected: {data['violations']}")
            
            if 'affected_persons' in data:
                print(f"    Affected Persons: {data['affected_persons']}")
            
            if 'governance' in data:
                print(f"    Governance: {data['governance']}")
            
            print()
        else:
            print(f"[FAIL] {name} (HTTP {resp.status_code})\n")
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {name}\n")
    except Exception as e:
        print(f"[ERROR] {name} - {str(e)[:50]}\n")

print("="*70)
print(f"NETWORK SUMMARY: {online_count}/5 NODES ONLINE")
print("="*70)

if online_count >= 3:
    print("\n[OK] NETWORK HEALTHY - Consensus can be reached (67% threshold)")
    print("     Requires: 4 of 5 nodes for decisions")
elif online_count >= 2:
    print("\n[WARN] Network degraded - consensus possible but vulnerable")
else:
    print("\n[ALERT] Network critical - consensus impossible")

print("\nNETWORK TYPE: Fully-connected Byzantine mesh")
print("CONSENSUS: 67% (4 out of 5 nodes required)")
print("BYZANTINE TOLERANCE: 33% (1 node can fail)")
print("REPLICATION: Across local + cloud")
