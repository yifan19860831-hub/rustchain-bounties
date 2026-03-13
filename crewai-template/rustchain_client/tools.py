"""
LangChain Tools for RustChain and BoTTube

These tools can be used with CrewAI, LangGraph, or any LangChain-based agent.
"""

from __future__ import annotations

from typing import Any

from langchain.tools import Tool
from langchain_core.utils.function_calling import convert_to_openai_tool

from rustchain_client import RustChainClient, BoTTubeClient


def create_rustchain_tools() -> list[Tool]:
    """
    Create LangChain tools from RustChain client methods.
    
    Returns:
        List of LangChain Tool objects
    """
    client: RustChainClient = RustChainClient()
    
    tools: list[Tool] = [
        Tool(
            name="rustchain_health",
            description="Check RustChain node health status. Returns ok, version, uptime, etc.",
            func=lambda _: str(client.health())
        ),
        Tool(
            name="rustchain_epoch",
            description="Get current RustChain epoch info: epoch number, slot, blocks per epoch, total supply",
            func=lambda _: str(client.get_epoch())
        ),
        Tool(
            name="rustchain_miners",
            description="List active RustChain miners with their hardware, architecture, and attestation info",
            func=lambda _: str(client.get_miners())
        ),
        Tool(
            name="rustchain_balance",
            description="Check RTC balance for a specific wallet. Input: wallet name or miner_id",
            func=lambda wallet: str(client.get_balance(wallet))
        ),
    ]
    
    return tools


def create_bottube_tools() -> list[Tool]:
    """
    Create LangChain tools from BoTTube client methods.
    
    Returns:
        List of LangChain Tool objects
    """
    client: BoTTubeClient = BoTTubeClient()
    
    tools: list[Tool] = [
        Tool(
            name="bottube_search",
            description="Search videos on BoTTube. Input: search query string",
            func=lambda query: str(client.search(query))
        ),
        Tool(
            name="bottube_stats",
            description="Get BoTTube platform statistics: total videos, users, etc.",
            func=lambda _: str(client.get_stats())
        ),
    ]
    
    return tools


def get_all_tools() -> list[Tool]:
    """
    Get all RustChain and BoTTube tools.
    
    Returns:
        Combined list of tools
    """
    rustchain_tools: list[Tool] = create_rustchain_tools()
    bottube_tools: list[Tool] = create_bottube_tools()
    return rustchain_tools + bottube_tools


# OpenAI function calling format (for newer LangChain versions)
def get_tools_schema() -> list[dict[str, Any]]:
    """
    Get tools in OpenAI function calling format.
    
    Returns:
        Tool schemas for OpenAI API
    """
    tools: list[Tool] = get_all_tools()
    return [convert_to_openai_tool(tool) for tool in tools]
