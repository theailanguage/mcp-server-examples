"""
This module implements a 'low-level' MCP Client Manager.

While frameworks like the Google Agent Development Kit (ADK) provide 
high-level abstractions for connecting to MCP servers, it's essential for 
students to understand how the underlying protocol works.

This manager demonstrates:
1.  **JSON-RPC Sessions**: How a client communicates with a server using JSON-RPC over STDIO.
2.  **Lifecycle Management**: Using `AsyncExitStack` to ensure all connections are properly closed.
3.  **Tool Discovery**: How a client 'asks' a server what capabilities it has.
4.  **Multiplexing**: Connecting to and managing multiple servers simultaneously.
"""

import asyncio
import json
import logging
import sys
import os
from typing import Dict, List, Optional
from contextlib import AsyncExitStack, asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import mcp.types as types

logger = logging.getLogger("mcp-client-manager")

class MCPClientManager:
    """
    Manages connections to multiple MCP servers via STDIO.
    
    Students: This class acts as the 'bridge' between your application 
    logic and the external MCP server processes.
    """
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.sessions: Dict[str, ClientSession] = {}
        # AsyncExitStack is a powerful tool to manage multiple async context managers.
        # It ensures that even if one connection fails, others are cleaned up correctly.
        self.exit_stack = AsyncExitStack()
        self._server_params: Dict[str, StdioServerParameters] = {}

    def load_config(self):
        """Loads the MCP server configurations from config.json."""
        if not os.path.exists(self.config_path):
            logger.error(f"Config file not found: {self.config_path}")
            raise FileNotFoundError(f"Config file {self.config_path} not found.")

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                servers = config.get("mcpServers", {})
                for name, info in servers.items():
                    # StdioServerParameters defines HOW to start the server process.
                    self._server_params[name] = StdioServerParameters(
                        command=info["command"],
                        args=info.get("args", []),
                        env=info.get("env")
                    )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse config JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    async def connect_to_all(self):
        """
        Connects to all configured MCP servers.
        
        This method spawns the server processes and establishes JSON-RPC sessions.
        """
        for name, params in self._server_params.items():
            try:
                logger.info(f"Connecting to MCP server '{name}' using command: {params.command} {' '.join(params.args)}")
                
                # stdio_client creates the transport layer (pipes to the process).
                transport = await self.exit_stack.enter_async_context(stdio_client(params))
                read, write = transport
                
                # ClientSession creates the protocol layer (handling JSON-RPC messages).
                session = await self.exit_stack.enter_async_context(ClientSession(read, write))
                
                # 'initialize' is a required step in the MCP protocol handshake.
                await session.initialize()
                self.sessions[name] = session
                logger.info(f"Successfully connected to MCP server: {name}")
            except Exception as e:
                # We log warning but don't crash, allowing other servers to work.
                logger.warning(f"Ignoring server '{name}' because we were not able to connect to it: {e}")
                logger.debug(f"Command attempted: {params.command} {' '.join(params.args)}")

    async def list_all_tools(self) -> List[types.Tool]:
        """
        Aggregates tools from all connected servers.
        
        Students: This is how the agent 'sees' what it can do. 
        Each server returns a list of its tools, and we combine them.
        """
        all_tools = []
        for name, session in self.sessions.items():
            try:
                # Request the list of tools from the server via the session.
                result = await session.list_tools()
                for tool in result.tools:
                    all_tools.append(tool)
            except Exception as e:
                logger.error(f"Failed to list tools for {name}: {e}")
        return all_tools

    async def call_tool(self, tool_name: str, arguments: dict) -> types.CallToolResult:
        """
        Calls a tool on the appropriate server.
        
        It searches through active sessions to find which server owns the tool.
        """
        for server_name, session in self.sessions.items():
            try:
                tools_result = await session.list_tools()
                if any(t.name == tool_name for t in tools_result.tools):
                    # We found the server that has the tool. Execute it!
                    return await session.call_tool(tool_name, arguments)
            except Exception as e:
                logger.warning(f"Error checking tools on server {server_name}: {e}")
                continue
        
        raise ValueError(f"Tool {tool_name} not found on any active server session.")

    async def shutdown(self):
        """
        Closes all sessions and transports gracefully.
        
        Closing the exit_stack will trigger the __aexit__ methods of all 
        registered context managers in reverse order.
        """
        await self.exit_stack.aclose()
        logger.info("MCP connections closed.")
