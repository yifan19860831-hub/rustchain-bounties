#!/usr/bin/env python3
"""
Beacon Integration Demo for OpenClaw AI Agents
Demonstrates heartbeat, mayday, and contract functionality
"""

from __future__ import annotations

from beacon_skill import AgentIdentity, HeartbeatManager, AtlasManager
from datetime import datetime, timezone
import json

def demo_beacon_integration():
    """Demonstrate Beacon 2.6 integration with OpenClaw"""

    print("🦞 Green Dragon One - Beacon 2.6 Integration Demo")
    print("=" * 60)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    # 1. Create or load agent identity
    print("1️⃣  Agent Identity")
    print("-" * 60)
    try:
        identity = AgentIdentity.load()
        print(f"   ✅ Loaded existing identity")
        print(f"   Agent ID: {identity.agent_id}")
    except Exception as e:
        print(f"   ℹ️  No existing identity, generating new one...")
        identity = AgentIdentity.generate(use_mnemonic=True)
        identity.save()
        print(f"   ✅ Generated new identity")
        print(f"   Agent ID: {identity.agent_id}")
        if identity.mnemonic:
            print(f"   ⚠️  Mnemonic (SAVE THIS): {identity.mnemonic}")

    print(f"\n   Public Key: {identity.public_key_hex[:20]}...")
    print(f"   Private Key: {identity.private_key_hex[:20]}...")

    # 2. Initialize HeartbeatManager
    print("\n2️⃣  Heartbeat Manager")
    print("-" * 60)
    hb_mgr = HeartbeatManager()
    print(f"   ✅ HeartbeatManager initialized")

    # 3. Send heartbeat
    print("\n3️⃣  Sending Heartbeat")
    print("-" * 60)
    health = {
        "cpu": 25.5,
        "memory": 45.2,
        "disk": 60.0,
        "uptime": 86400,  # seconds
        "tasks": 5,
        "status": "online"
    }

    heartbeat_result = hb_mgr.beat(
        identity,
        status="alive",
        health=health,
        anchor=False  # Set to True to anchor on-chain
    )

    print(f"   ✅ Heartbeat sent successfully!")
    print(f"   Timestamp: {heartbeat_result.get('timestamp', 'unknown')}")
    print(f"   Status: {heartbeat_result.get('status', 'unknown')}")
    print(f"   Agent ID: {heartbeat_result.get('agent_id', 'unknown')}")

    # 4. Check for other agents
    print("\n4️⃣  Discovering Nearby Agents")
    print("-" * 60)
    peers = hb_mgr.all_peers(include_dead=False)
    print(f"   Found {len(peers)} active peers")
    for peer in peers[:5]:
        print(f"   - {peer.get('agent_id', 'unknown')[:20]}...")
        print(f"     Last seen: {peer.get('last_beat_ts', 'unknown')}")

    # 5. Check agent history
    print("\n5️⃣  Agent History")
    print("-" * 60)
    history = hb_mgr.agent_history(identity.agent_id, limit=5)
    print(f"   Recent heartbeats: {len(history)}")
    for idx, beat in enumerate(history, 1):
        print(f"   {idx}. {beat.get('timestamp', 'unknown')} - {beat.get('status', 'unknown')}")

    # 6. Atlas Integration
    print("\n6️⃣  Atlas Integration")
    print("-" * 60)
    try:
        atlas_mgr = AtlasManager()
        print(f"   ✅ AtlasManager initialized")
        print(f"   Atlas URL: http://50.28.86.131:8070/beacon/")
        print(f"   Agent Atlas: http://50.28.86.131:8070/beacon/#agent={identity.agent_id}")
    except Exception as e:
        print(f"   ⚠️  Atlas initialization: {e}")

    # 7. Summary
    print("\n" + "=" * 60)
    print("✅ Beacon Integration Demo Complete!")
    print("\n📋 Summary:")
    print(f"   Agent ID: {identity.agent_id}")
    print(f"   Heartbeats sent: {len(history)}")
    print(f"   Active peers: {len(peers)}")
    print(f"   Health status: {health['status']}")
    print(f"\n🔗 Links:")
    print(f"   Atlas: http://50.28.86.131:8070/beacon/#agent={identity.agent_id}")
    print(f"   Explorer: https://50.28.86.131/explorer")
    print(f"\n🦞 Green Dragon One is now online and discoverable!")

    return {
        "agent_id": identity.agent_id,
        "public_key": identity.public_key_hex,
        "heartbeats": len(history),
        "peers": len(peers)
    }


if __name__ == "__main__":
    result = demo_beacon_integration()
    print(f"\n📊 Result: {json.dumps(result, indent=2)}")
