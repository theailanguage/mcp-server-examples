"""
This module contains the logic for resources provided by the Echo Server.

Resources are a fundamental concept in the Model Context Protocol (MCP). 
While tools are for 'actions', resources are for 'data'. An agent can 
request the content of a resource whenever it needs specific background information.
"""

def connection_status() -> str:
    """
    Returns a simple status message indicating the server is operational.
    
    Students: Resources are often used to expose logs, configuration data, 
    or even real-time streams of information. By providing this as a 
    resource, the AI agent can check if the server is healthy without 
    you having to write a specific 'check_health' tool.
    
    Returns:
        A string message.
    """
    return "Successfully connected to Echo Server"
