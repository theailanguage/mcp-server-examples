import subprocess
import os
import platform

def execute_command(command: str) -> str:
    """
    Executes a shell command and returns its output or error message.
    
    This function is designed to be used as an MCP tool. It allows the AI
    to interact with the host system's terminal.
    
    Args:
        command (str): The full shell command to execute.
        
    Returns:
        str: The standard output (stdout) of the command, or a descriptive 
             error message if the command fails.
    """
    
    # STUDENT NOTE: Safety is paramount when running shell commands.
    # In a production environment, you should strictly validate or 
    # sanitize the 'command' string to prevent command injection attacks.
    # For this educational example, we execute the command as provided.
    
    try:
        # We use subprocess.run to execute the command.
        # - shell=True: Allows us to pass the command as a string, exactly as 
        #   you would type it in a terminal.
        # - capture_output=True: Tells Python to catch both stdout and stderr 
        #   so we can return them to the AI.
        # - text=True: Returns the output as a string instead of bytes.
        # - timeout=30: Prevents the server from hanging if a command runs 
        #   too long (e.g., 'ping' without a count).
        
        print(f"[*] Executing command: {command}") # Logging for the server console
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # If the command was successful (return code 0)
        if result.return_code == 0:
            # Return the output. If it's empty, let the AI know.
            return result.stdout if result.stdout.strip() else "Command executed successfully with no output."
        else:
            # If the command failed, return the error message from stderr.
            return f"Error (Exit Code {result.returncode}):\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: The command timed out after 30 seconds."
    except Exception as e:
        # Catch-all for other potential issues like missing permissions or binary not found.
        return f"An unexpected error occurred: {str(e)}"

# This file does NOT initialize the server. It only defines the 'logic' or 'tools'.
# This separation of concerns makes the code easier to test and maintain.
