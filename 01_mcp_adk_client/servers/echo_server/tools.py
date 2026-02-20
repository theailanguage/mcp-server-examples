"""
This module contains the business logic for tools provided by the Echo Server.

Separating tool logic (the 'how') from the MCP registration (the 'what') is a 
best practice in agent development. It makes the code more testable, modular, 
and easier to maintain.
"""

def echo(text: str) -> str:
    """
    A simple function that returns the input text prefixed with 'Echo: '.
    
    Students: In a real-world scenario, this function could perform complex 
    calculations, query a database, or call an external API. 
    The key is that this function doesn't care about MCP; it just takes 
    inputs and returns outputs.
    
    Args:
        text: The text to be echoed.
    
    Returns:
        A string containing the echoed text.
    """
    return f"Echo: {text}"
