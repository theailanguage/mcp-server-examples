import subprocess
import logging
import sys

# Configure logging to send messages to stderr.
# This is CRITICAL for MCP servers using the STDIO transport,
# because stdout is reserved for JSON-RPC communication protocol messages.
# If we print to stdout, we will corrupt the protocol stream.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("terminal_server")

def execute_command(command: str) -> str:
    """
    Executes a shell command and returns the output.
    
    This function uses the 'subprocess' module, which is the standard Python way 
    to interact with the operating system's command line.
    
    Args:
        command (str): The shell command to run (e.g., 'ls -la', 'dir', 'uname -a').
        
    Returns:
        str: The combined output of stdout and stderr from the command.
    """
    logger.info(f"Executing command: {command}")
    
    try:
        # subprocess.run is a high-level function that runs a command and waits for it to finish.
        # - capture_output=True: Grabs both stdout (regular output) and stderr (error output).
        # - text=True: Returns the output as a string instead of raw bytes.
        # - shell=True: Allows us to pass a single string command as if we typed it in a terminal.
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=False  # We handle the error ourselves via return value
        )
        
        # Combine stdout and stderr to provide full context to the LLM.
        output = result.stdout
        if result.stderr:
            output += f"\n--- Standard Error ---\n{result.stderr}"
            
        # If the command failed (exit code != 0), we still return the output
        # but the LLM will see the error message in the stderr block.
        return output if output.strip() else "Command executed with no output."
        
    except Exception as e:
        # If something goes wrong with the subprocess call itself (e.g. command not found)
        logger.error(f"Failed to execute command: {str(e)}")
        return f"Error executing command: {str(e)}"
