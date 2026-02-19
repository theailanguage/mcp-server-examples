# MCP Terminal Workspace

This workspace contains a set of Model Context Protocol (MCP) servers and tools designed to empower AI agents with system-level capabilities, specifically terminal access. This project demonstrates how to build a robust MCP server using the high-level `MCPServer` implementation.

## 🏗 Project Structure

This repository follows a hierarchical structure for organizing MCP servers.

- `servers/`: Contains individual MCP server implementations.
  - `terminal_server/`: A server providing a tool to execute shell commands.
- `requirements.txt`: Global dependencies for the project.
- `ATTRIBUTION.md`: Open-source credits and trademark disclaimers.
- `LICENSE`: Project licensing information.

## 🛠 Architecture Topology

The workspace is designed to be extensible. Each directory under `servers/` represents a standalone MCP server that can be integrated with clients like Claude Desktop or Google ADK-based agents.

```text
Root
├── servers/
│   └── terminal_server/ (Logic for shell execution)
├── requirements.txt
├── ATTRIBUTION.md
└── LICENSE
```

---

# 🖥 Terminal MCP Server

The Terminal MCP Server allows an AI (like Claude) to interact with your computer's terminal using the high-level `MCPServer` implementation.

## 🛠 Tools

### `execute_command`
Executes a shell command within the configured workspace and returns its output or error message. This tool is the primary way for the AI to interact with the host system.
- **Arguments**: 
    - `command` (string): The full shell command to execute.

---

## 🚀 Getting Started

### 1. Install Dependencies

Change to the directory with the code you have cloned using PowerShell (Windows) or Terminal (MacOS) and run the install command.

Note: This installs MCP version 2 (specified in requirements.txt), allowing Claude to run the server.

**WINDOWS**

```powershell
cd C:\<PROJECT_PATH>\mcp-v2-server-examples\01_terminal_server
pip install -r requirements.txt
```

**MACOS**

```bash
cd /Users/<PROJECT_PATH>/mcp-v2-server-examples/01_terminal_server
pip3 install -r requirements.txt
```
(Or use `pip` if `pip3` is not found)

### ⚠️ 2. Configure Workspace (Very Important)

The tool needs a specific folder to save files. Without this setup, the tool will fail. Choose ONE of the two methods below.

#### Method A: Create Default Folder (Easiest)

Simply create a folder named `workspace` inside an `mcp` folder in your user directory. The code will automatically look here if no environment variable is set.

**MacOS/Linux:**
`~/mcp/workspace`

**Windows:**
`C:\Users\<YOUR_USERNAME>\mcp\workspace`

#### Method B: Set Custom Path (.env)

If you want to use a specific existing folder, open the `.env` file in the project and add the variable below.

**MacOS / Linux Example:**
`TERMINAL_WORKSPACE=/Users/jdoe/projects/my_mcp_workspace`

**Windows Example:**
`TERMINAL_WORKSPACE=C:\\Users\\jdoe\\projects\\my_mcp_workspace`

**Important:** On Windows, you must use double backslashes (`\\`) in the `.env` file.

---

### 💻 Steps for Windows Users


1. Please go to the menu button on the top left in Claude Desktop.
2. Then select **File** > click **Settings**.
3. In the settings window, click **Developer** on the left.
4. At the bottom/in middle of the resulting window there is an **Edit Config** button - click that.
5. This will open the folder where this file is located. This folder should be `C:\Users\<YourUserName>\AppData\Roaming\Claude`.
   *Claude should create the file automatically if not present when you follow these steps!*
6. Now look for `claude_desktop_config.json` here. Just in case it is not present, create a new file.
7. Copy the config as given below to the file. Note that windows has a different path naming convention, hence the difference!
8. Once done, restart Claude Desktop by clicking menu on top left, then **File** and then **Exit**. Do not close from task bar as that does not properly quit Claude desktop. Then start it again and you should see the terminal tool in the chat box icon for controls near bottom left of the chat box.

#### `claude_desktop_config.json` content for Windows

```json
{
  "mcpServers": {
    "terminal": {
      "command": "python",
      "args": ["C:\\<PROJECT_PATH>\\mcp-v2-server-examples\\01_terminal_server\\servers\\terminal_server\\main.py"]
    }
  }
}
```

---

## ⚠️ Safety Warning
This server allows the AI to run **any** command on your computer within the workspace. This is powerful but dangerous. 
- **Never** run this server on a public network.
- **Always** monitor what commands the AI is suggesting before you let it run them.
- In a real-world application, you should restrict the commands the server is allowed to run.

---

## ⚖️ License and Attributions

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
Refer to [ATTRIBUTION.md](ATTRIBUTION.md) for information regarding third-party frameworks like the Google ADK and the Model Context Protocol.
