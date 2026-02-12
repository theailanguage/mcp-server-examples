# MCP Terminal Workspace

This workspace contains a set of Model Context Protocol (MCP) servers and tools designed to empower AI agents with system-level capabilities, specifically terminal access.

## 🏗 Project Structure

This repository follows a hierarchical structure for better organization of MCP servers.

- `servers/`: Contains individual MCP server implementations.
  - [`terminal_server/`](servers/terminal_server/README.md): A server providing a tool to execute shell commands.
- `requirements.txt`: Global dependencies for the project.
- `ATTRIBUTION.md`: Open-source credits and trademark disclaimers.
- `LICENSE`: Project licensing information.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `pip` (Python package installer)

### Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠 Architecture Topology

The workspace is designed to be extensible. Each directory under `servers/` represents a standalone MCP server that can be integrated with clients like Claude Desktop or Google ADK-based agents.

```text
Root
├── servers/
│   └── terminal_server/ (Logic for shell execution)
├── requirements.txt
└── ATTRIBUTION.md
```

## 📚 Documentation

Detailed documentation for each server can be found in their respective directories. For the terminal server, refer to [servers/terminal_server/README.md](servers/terminal_server/README.md).

## ⚖️ License and Attributions

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
Refer to [ATTRIBUTION.md](ATTRIBUTION.md) for information regarding third-party frameworks like the Google ADK and the Model Context Protocol.
