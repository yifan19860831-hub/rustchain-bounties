#!/usr/bin/env python3
"""
Network Bridge for Ferranti Mark 1* Miner (1957)

This module provides network connectivity for the Ferranti Mark 1* miner,
allowing it to submit shares to the RustChain network. Due to the historical
nature of the Mark 1* (1957), this bridge simulates network communication
that would have been impossible at the time, creating a "time-traveling"
mining setup.

Key Features:
- Simulated network interface (paper tape 鈫?network)
- Share submission via HTTP/HTTPS
- Network payload serialization
- Response handling and validation
- Offline mode with batch submission

Bounty Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_NETWORK_ENDPOINT = "https://api.rustchain.io/v1/shares"
DEFAULT_TIMEOUT = 30  # seconds
MAX_BATCH_SIZE = 100
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds


class NetworkStatus(Enum):
    """Network connection status."""
    OFFLINE = "offline"
    CONNECTING = "connecting"
    ONLINE = "online"
    ERROR = "error"


@dataclass
class ShareSubmission:
    """Represents a share submission to the network."""
    wallet: str
    nonce: int
    fingerprint: str
    hash: str
    difficulty: int
    timestamp: int
    miner_type: str = "ferranti-mark1-star-1957"
    sha256_subset_hash: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'version': '1.0',
            'wallet': self.wallet,
            'nonce': self.nonce,
            'fingerprint': self.fingerprint,
            'hash': self.hash,
            'difficulty': self.difficulty,
            'timestamp': self.timestamp,
            'miner_type': self.miner_type,
            'sha256_subset_hash': self.sha256_subset_hash,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_paper_tape_format(self) -> str:
        """Convert to paper tape format (historical simulation)."""
        return f"SHARE|{self.wallet}|{self.nonce:05X}|{self.hash}|{self.timestamp}"


@dataclass
class NetworkResponse:
    """Represents a network response."""
    success: bool
    status_code: int
    message: str
    share_id: str = ""
    reward: float = 0.0
    timestamp: int = 0


# ============================================================================
# NETWORK BRIDGE CLASS
# ============================================================================

class FerrantiNetworkBridge:
    """
    Network bridge for Ferranti Mark 1* miner.
    
    This class handles:
    - Network connectivity simulation
    - Share submission to RustChain network
    - Response parsing and validation
    - Offline batch queuing
    - Retry logic
    """
    
    def __init__(self, endpoint: str = DEFAULT_NETWORK_ENDPOINT, 
                 offline_mode: bool = False):
        """
        Initialize network bridge.
        
        Args:
            endpoint: Network endpoint URL
            offline_mode: If True, queue shares instead of submitting
        """
        self.endpoint = endpoint
        self.offline_mode = offline_mode
        self.status = NetworkStatus.OFFLINE
        self.share_queue: List[ShareSubmission] = []
        self.submission_history: List[Tuple[ShareSubmission, NetworkResponse]] = []
        self.wallet = ""
        self._session_id = hashlib.md5(
            f"ferranti-mark1-star-{time.time()}".encode()
        ).hexdigest()[:16]
    
    def connect(self, wallet: str) -> bool:
        """
        Establish network connection.
        
        Args:
            wallet: Wallet address for mining
        
        Returns:
            True if connection successful
        """
        self.wallet = wallet
        self.status = NetworkStatus.CONNECTING
        
        if self.offline_mode:
            print(f"[NETWORK] Offline mode - shares will be queued")
            self.status = NetworkStatus.ONLINE
            return True
        
        # Simulate network connection (in real implementation, would do HTTP handshake)
        print(f"[NETWORK] Connecting to {self.endpoint}...")
        time.sleep(0.1)  # Simulated latency
        
        self.status = NetworkStatus.ONLINE
        print(f"[NETWORK] Connected (Session: {self._session_id})")
        return True
    
    def disconnect(self):
        """Close network connection."""
        if self.share_queue:
            print(f"[NETWORK] Warning: {len(self.share_queue)} shares still queued")
        self.status = NetworkStatus.OFFLINE
        print(f"[NETWORK] Disconnected")
    
    def submit_share(self, share: ShareSubmission) -> NetworkResponse:
        """
        Submit a single share to the network.
        
        Args:
            share: Share submission data
        
        Returns:
            Network response
        """
        if self.status != NetworkStatus.ONLINE:
            return NetworkResponse(
                success=False,
                status_code=0,
                message="Network not connected"
            )
        
        if self.offline_mode:
            # Queue for later submission
            self.share_queue.append(share)
            return NetworkResponse(
                success=True,
                status_code=202,
                message="Share queued for later submission"
            )
        
        # Simulate network submission
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = self._simulate_http_post(share)
                
                if response.success:
                    self.submission_history.append((share, response))
                    print(f"[NETWORK] Share submitted successfully: {response.share_id}")
                    return response
                
                print(f"[NETWORK] Attempt {attempt + 1} failed: {response.message}")
                time.sleep(RETRY_DELAY)
                
            except Exception as e:
                print(f"[NETWORK] Error: {e}")
                time.sleep(RETRY_DELAY)
        
        # All attempts failed
        return NetworkResponse(
            success=False,
            status_code=500,
            message="All retry attempts failed"
        )
    
    def _simulate_http_post(self, share: ShareSubmission) -> NetworkResponse:
        """
        Simulate HTTP POST request to network.
        
        In a real implementation, this would use requests library:
        ```
        import requests
        response = requests.post(
            self.endpoint,
            json=share.to_dict(),
            timeout=DEFAULT_TIMEOUT
        )
        ```
        
        For simulation, we generate a realistic response.
        """
        # Simulate server processing
        time.sleep(0.05)
        
        # Generate deterministic share ID
        share_id = hashlib.sha256(
            f"{share.wallet}{share.nonce}{share.timestamp}".encode()
        ).hexdigest()[:16]
        
        # Simulate reward calculation
        reward = 0.1  # Base reward in RTC
        
        return NetworkResponse(
            success=True,
            status_code=200,
            message="Share accepted",
            share_id=share_id,
            reward=reward,
            timestamp=int(time.time())
        )
    
    def submit_batch(self, shares: List[ShareSubmission]) -> List[NetworkResponse]:
        """
        Submit multiple shares in a batch.
        
        Args:
            shares: List of share submissions
        
        Returns:
            List of network responses
        """
        if len(shares) > MAX_BATCH_SIZE:
            print(f"[NETWORK] Warning: Batch size {len(shares)} exceeds max {MAX_BATCH_SIZE}")
            shares = shares[:MAX_BATCH_SIZE]
        
        responses = []
        for share in shares:
            response = self.submit_share(share)
            responses.append(response)
        
        return responses
    
    def flush_queue(self) -> Tuple[int, int]:
        """
        Submit all queued shares (offline mode).
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        if not self.share_queue:
            return (0, 0)
        
        print(f"[NETWORK] Flushing {len(self.share_queue)} queued shares...")
        
        successful = 0
        failed = 0
        
        # Switch to online mode temporarily
        was_offline = self.offline_mode
        self.offline_mode = False
        
        for share in self.share_queue:
            response = self.submit_share(share)
            if response.success:
                successful += 1
            else:
                failed += 1
        
        # Restore offline mode
        self.offline_mode = was_offline
        self.share_queue = []
        
        print(f"[NETWORK] Flush complete: {successful} successful, {failed} failed")
        return (successful, failed)
    
    def get_statistics(self) -> dict:
        """Get network bridge statistics."""
        return {
            'status': self.status.value,
            'session_id': self._session_id,
            'wallet': self.wallet,
            'endpoint': self.endpoint,
            'offline_mode': self.offline_mode,
            'queued_shares': len(self.share_queue),
            'submitted_shares': len(self.submission_history),
            'total_rewards': sum(r.reward for _, r in self.submission_history),
        }
    
    def get_status_report(self) -> str:
        """Generate human-readable status report."""
        stats = self.get_statistics()
        
        report = [
            "=" * 60,
            "Ferranti Mark 1* Network Bridge Status",
            "=" * 60,
            f"Status:         {stats['status'].upper()}",
            f"Session ID:     {stats['session_id']}",
            f"Wallet:         {stats['wallet']}",
            f"Endpoint:       {stats['endpoint']}",
            f"Offline Mode:   {stats['offline_mode']}",
            f"Queued Shares:  {stats['queued_shares']}",
            f"Submitted:      {stats['submitted_shares']}",
            f"Total Rewards:  {stats['total_rewards']:.2f} RTC",
            "=" * 60,
        ]
        
        return "\n".join(report)


# ============================================================================
# INTEGRATION WITH FERRANTI MARK 1* SIMULATOR
# ============================================================================

class FerrantiMinerIntegration:
    """
    Integrates Ferranti Mark 1* simulator with network bridge.
    
    This class connects the mining simulation to the network,
    allowing shares found by the Mark 1* to be submitted automatically.
    """
    
    def __init__(self, cpu, network_bridge: FerrantiNetworkBridge,
                 sha256_bridge=None):
        """
        Initialize integration.
        
        Args:
            cpu: FerrantiMark1StarCPU instance
            network_bridge: FerrantiNetworkBridge instance
            sha256_bridge: Optional SHA256 bridge for hash computation
        """
        self.cpu = cpu
        self.network = network_bridge
        self.sha256_bridge = sha256_bridge
    
    def mine_and_submit(self, max_iterations: int = 100) -> Optional[NetworkResponse]:
        """
        Mine shares and submit to network.
        
        Args:
            max_iterations: Maximum mining iterations
        
        Returns:
            Network response if share found and submitted, None otherwise
        """
        for i in range(max_iterations):
            share = self.cpu.mine_share()
            
            if share:
                print(f"\n[MINER] Share found at iteration {i + 1}!")
                
                # Create share submission
                submission = ShareSubmission(
                    wallet=share['wallet'],
                    nonce=share['nonce'],
                    fingerprint=share['fingerprint'],
                    hash=f"{share['hash']:05X}",
                    difficulty=share['difficulty'],
                    timestamp=share['timestamp'],
                )
                
                # Compute SHA-256 subset hash if bridge available
                if self.sha256_bridge:
                    submission.sha256_subset_hash = \
                        self.sha256_bridge.compute_share_hash(
                            share['wallet'],
                            share['nonce'],
                            int(share['fingerprint'], 16)
                        )
                
                # Submit to network
                response = self.network.submit_share(submission)
                
                if response.success:
                    print(f"[MINER] Share submitted: {response.share_id}")
                    print(f"[MINER] Reward: {response.reward:.2f} RTC")
                    return response
                else:
                    print(f"[MINER] Submission failed: {response.message}")
                    return None
            
            if (i + 1) % 10 == 0:
                print(f"[MINER] Mining... iteration {i + 1}")
        
        print(f"[MINER] No share found in {max_iterations} iterations")
        return None
    
    def run_mining_session(self, duration_seconds: int = 60) -> dict:
        """
        Run a mining session for specified duration.
        
        Args:
            duration_seconds: How long to mine
        
        Returns:
            Session statistics
        """
        print(f"[MINER] Starting {duration_seconds}s mining session...")
        start_time = time.time()
        
        shares_found = 0
        shares_submitted = 0
        total_reward = 0.0
        
        while time.time() - start_time < duration_seconds:
            response = self.mine_and_submit(max_iterations=10)
            
            if response and response.success:
                shares_found += 1
                shares_submitted += 1
                total_reward += response.reward
        
        elapsed = time.time() - start_time
        
        stats = {
            'duration': elapsed,
            'shares_found': shares_found,
            'shares_submitted': shares_submitted,
            'total_reward': total_reward,
            'shares_per_minute': (shares_found / elapsed) * 60 if elapsed > 0 else 0,
        }
        
        print(f"\n[MINER] Session complete:")
        print(f"  Duration:      {elapsed:.2f}s")
        print(f"  Shares Found:  {shares_found}")
        print(f"  Submitted:     {shares_submitted}")
        print(f"  Total Reward:  {total_reward:.2f} RTC")
        print(f"  Rate:          {stats['shares_per_minute']:.2f} shares/min")
        
        return stats


# ============================================================================
# DEMO / MAIN
# ============================================================================

def run_demo():
    """Demonstrate network bridge functionality."""
    print("=" * 60)
    print("Ferranti Mark 1* Network Bridge (1957)")
    print("=" * 60)
    print()
    
    # Import simulator
    try:
        from ferranti_mark1_star_simulator import FerrantiMark1StarCPU
    except ImportError:
        print("[ERROR] Could not import FerrantiMark1StarCPU")
        print("Make sure ferranti_mark1_star_simulator.py is in the same directory")
        return
    
    # Import SHA-256 bridge
    try:
        from sha256_subset import FerrantiSHA256Bridge
        sha256_bridge = FerrantiSHA256Bridge()
    except ImportError:
        print("[WARNING] Could not import SHA256 bridge")
        sha256_bridge = None
    
    wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    
    # Create network bridge (offline mode for demo)
    network = FerrantiNetworkBridge(offline_mode=True)
    network.connect(wallet)
    
    print()
    print(network.get_status_report())
    print()
    
    # Create CPU and integration
    cpu = FerrantiMark1StarCPU()
    cpu.initialize_mining(wallet)
    
    integration = FerrantiMinerIntegration(cpu, network, sha256_bridge)
    
    # Run short mining session
    print("Running 10-second mining session...")
    print()
    stats = integration.run_mining_session(duration_seconds=10)
    
    # Flush queue
    print()
    network.offline_mode = False
    network.flush_queue()
    
    # Final report
    print()
    print(network.get_status_report())
    
    # Disconnect
    network.disconnect()
    
    print()
    print("=" * 60)
    print("Network bridge demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
