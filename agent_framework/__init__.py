"""
RustChain Agent Framework Package

Framework for building AI agents that interact with the RustChain network.

This package provides:
    - Base agent classes for RustChain integration
    - Utility functions for attestation and mining
    - API clients for network interaction
    - Event handlers for blockchain events

Example:
    ```python
    from rustchain_agent_framework import BaseAgent, RustChainClient
    
    class MyAgent(BaseAgent):
        async def on_epoch_change(self, epoch_data):
            # Handle epoch change
            pass
    ```
"""

__version__ = "1.0.0"
__author__ = "RustChain Community"
__all__ = []

# Note: Import specific modules as needed
# from .agent import BaseAgent
# from .client import RustChainClient
