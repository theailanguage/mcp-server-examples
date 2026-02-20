"""
Direct MCP Client Manager Interface (Non-Agentic).

This script demonstrates how to interact with MCP servers programmatically using 
 the 'low-level' MCPClientManager, without the involvement of an AI agent.

Key concepts for students:
1.  **Programmatic Control**: Calling tools based on hardcoded logic or direct user input.
2.  **Explicit Discovery**: Manually listing and inspecting available tools.
3.  **Protocol Transparency**: Seeing the raw inputs and outputs of MCP tool calls.
"""

import asyncio
import logging
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.logging import RichHandler

# Import our custom manager
from mcp_client.manager import MCPClientManager

# --- INITIALIZATION ---

# Setup logging to stderr using Rich
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=Console(stderr=True))]
    )

console = Console()

async def main():
    setup_logging()
    
    # Header explaining the purpose of this script
    console.print(Panel.fit(
        "[bold cyan]MCP Client Manager Interface[/bold cyan]\n"
        "This program interacts with MCP servers [bold green]programmatically[/bold green].\n"
        "It does NOT use an AI agent. It connects directly via the MCPClientManager.",
        border_style="cyan"
    ))

    config_path = "config.json"
    manager = MCPClientManager(config_path)

    try:
        # 1. LOAD CONFIGURATION
        console.print("[yellow]Loading configuration...[/yellow]")
        manager.load_config()

        # 2. CONNECT TO SERVERS
        console.print("[yellow]Connecting to MCP servers...[/yellow]")
        await manager.connect_to_all()
        
        if not manager.sessions:
            console.print("[bold red]Error: No MCP servers connected. Check your config.json and server paths.[/bold red]")
            return

        # 3. DISCOVER TOOLS
        console.print("[yellow]Discovering available tools...[/yellow]")
        tools = await manager.list_all_tools()
        
        if not tools:
            console.print("[bold yellow]No tools found on the connected servers.[/bold yellow]")
        else:
            table = Table(title="Available MCP Tools", show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan")
            table.add_column("Description")
            
            for tool in tools:
                table.add_row(tool.name, tool.description or "No description")
            
            console.print(table)

        # 4. INTERACTIVE TOOL EXECUTION (Hardcoded for Echo Tool)
        console.print("\n[bold green]Ready to execute tools![/bold green]")
        
        while True:
            # Ask the user what they want to echo
            user_input = Prompt.ask("[bold blue]Enter text to echo (or 'exit' to quit)[/bold blue]")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue

            try:
                console.print(f"[cyan]Calling 'echo_tool' with argument: '{user_input}'...[/cyan]")
                
                # We call the tool programmatically. 
                # Note: We must know the tool name and the argument structure.
                result = await manager.call_tool(
                    tool_name="echo_tool", 
                    arguments={"text": user_input}
                )
                
                # Check the result. MCP tool results often contain a list of content blocks.
                # Here we expect a simple text response.
                if result.content:
                    # In MCP, content is usually a list of TextContent or ImageContent.
                    # FastMCP tool results are typically wrapped in types.TextContent.
                    for block in result.content:
                        if hasattr(block, 'text'):
                            console.print(Panel(
                                f"Successfully executed!\n\n[bold white]{block.text}[/bold white]",
                                title="Server Response",
                                border_style="green"
                            ))
                else:
                    console.print("[yellow]Tool executed but returned no content.[/yellow]")
                    
            except Exception as e:
                console.print(f"[bold red]Error calling tool:[/bold red] {e}")

    except FileNotFoundError as e:
        console.print(f"[bold red]Configuration error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
    finally:
        # 5. SHUTDOWN
        console.print("[yellow]Shutting down connections...[/yellow]")
        await manager.shutdown()
        console.print("[bold cyan]Goodbye![/bold cyan]")

if __name__ == "__main__":
    # Ensure the script runs within an async loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass # Handle Ctrl+C gracefully
