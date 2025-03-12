# gotask-mcp

A Model Context Protocol (MCP) Server for [Taskfile](https://taskfile.dev/)/`go-task`.

## Prerequisites

This project and the `mcp` CLI rely on your having the dependency management tool `uv` installed. You can install via e.g. `brew install uv` for Homebrew users. [See here for alternatives](https://docs.astral.sh/uv/getting-started/inst
allation).

You will also need to have `Taskfile` installed. `brew install go-task` will work if you are a `Homebrew` user.
[See here for alternatives](https://taskfile.dev/installation/).

## Details

A task runner (such as `Taskfile`) is a means of defining and running short commands that do regularly required, simple or complex work.

Such tasks can be an important part of the development cycle, for example autofixes and QA checks. Therefore it would seem useful if coding agents powered by generative AI could run these tasks at the appropriate time. The way to achieve this is with an MCP server that provides each defined task as a tool.

This is a demonstration project for now. It targets an example `Taskfile.yml` contained in the repo, whereas a production-ready version would need to read a custom file.
Further, a production-ready version will need some way to mark tasks as approved for automatic use.

## Further notes

Because there is no `yaml` parser in the Python standard library, since the taskrunner defines the tasks in a `Taskfile.yml`, the MCP server has a dependency on `saneyaml`. This can lead to problems (difficulties getting it working with `Cursor` IDE for example).

At the moment the solution is to

1. clone down this project locally
2. install `mcp[cli]` in your working project
3. use the `--directory` option when starting the server with `uv` to point `uv` at _this_ project

To elaborate on (3), the full syntax is: `uv run --with mcp --directory /path/to/gotask-mcp mcp run /path/to/gotask-mcp/src/server.py`
