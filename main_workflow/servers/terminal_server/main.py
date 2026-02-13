import logging
import sys
from mcp.server.mcpserver import MCPServer

# Import the tool function. 
# We use a direct import here so the script can be run easily.
try:
    from tools import execute_command
except ImportError:
    # This handles cases where the script might be run as a module
    from .tools import execute_command

# 1. SETUP LOGGING
# We configure logging to output to sys.stderr. 
# In the Model Context Protocol (MCP), the 'stdio' transport uses sys.stdout 
# for the JSON-RPC messages that the server and client (like Claude) use to talk.
# Printing to stdout would break the connection.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("terminal_server")

# 2. INITIALIZE SERVER
# We create an instance of MCPServer. This object manages the tools,
# resources, and prompts that we want to expose to the LLM.
server = MCPServer(
    name="terminal_server",
    version="1.0.0",
    description="An MCP server that provides terminal access for command execution."
)

# 3. REGISTER TOOLS
# We use the @server.tool() decorator to turn a regular Python function 
# into a tool that the AI can call.
# The docstring of the function and the type hints are used by the server
# to describe the tool to the LLM automatically.
@server.tool()
def run_command(command: str) -> str:
    """
    Execute a shell command on the host system.
    
    Args:
        command: The full command string to execute in the terminal.
    """
    return execute_command(command)

# 4. ENTRY POINT
# The server.run() method starts the communication loop.
# 'stdio' transport means it listens for commands on stdin and replies on stdout.
if __name__ == "__main__":
    logger.info("Starting Terminal MCP Server...")
    # By default, MCPServer.run() handles the event loop for us.
    server.run(transport='stdio')
