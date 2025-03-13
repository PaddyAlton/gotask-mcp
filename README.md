# gotask-mcp

A Model Context Protocol (MCP) Server for [Taskfile](https://taskfile.dev/)/`go-task`.

## Prerequisites

This project and the `mcp` CLI rely on your having the dependency management tool `uv` installed. You can install via e.g. `brew install uv` for Homebrew users. [See here for alternatives](https://docs.astral.sh/uv/getting-started/inst
allation).

You will also need to have `Taskfile` installed. `brew install go-task` will work if you are a `Homebrew` user.
[See here for alternatives](https://taskfile.dev/installation/).

## Details

A task runner (such as `Taskfile`) is a means of defining and running short commands that do regularly required, simple or complex work.

Such tasks can be an important part of the development cycle, for example autofixes and QA checks. Therefore it would seem useful if coding agents powered by generative AI could run these tasks at the appropriate time. The way to achieve this is with an MCP server that provides tools for running such tasks.

Two servers are provided. The first, `src/server.py`, demonstrates the general principle. A target `Taskfile.yml` is parsed and each task is provided as a separate tool.

However, for many applications this is insufficient. Often one wishes to run a server in some isolated environment but it will need to read local project context (i.e. the local `Taskfile.yml`). The server in `src/cursor_server.py` was designed to be used with Cursor IDE. The Cursor Agent is provided with two tools:

1. a tool to retrieve a list of available tasks
2. a tool to run a named task

The Cursor Agent is expected to pass in the working directory path as an input to these tools, which allows the tools to read the project `Taskfile.yml`.

_(N.B. at the time of writing MCP resources don't work very well with Cursor IDE - the first tool would ideally be implemented as a resource, not a tool)_

## Further notes

Because there is no `yaml` parser in the Python standard library, since the taskrunner defines the tasks in a `Taskfile.yml`, the first MCP server has a dependency on `saneyaml`. This can lead to problems (difficulties getting it working with Cursor IDE for example).

At the moment the solution is to

1. clone down this project locally
2. install `mcp[cli]` in your working project
3. use the `--directory` option when starting the server with `uv` to point `uv` at _this_ project

To elaborate on (3), the full syntax is: `uv run --with mcp --directory /path/to/gotask-mcp mcp run /path/to/gotask-mcp/src/server.py`

This should not be a problem with the second server, because it does not parse `Taskfile.yml` directly.
