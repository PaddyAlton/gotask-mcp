# gotask-mcp

A Model Context Protocol (MCP) Server for [Taskfile](https://taskfile.dev/)/`go-task`.

## Prerequisites

This project and the `mcp` CLI rely on your having the dependency management tool `uv` installed. You can install via e.g. `brew install uv` for Homebrew users. [See here for alternatives](https://docs.astral.sh/uv/getting-started/installation).

You will also need to have `Taskfile` installed. `brew install go-task` will work if you are a `Homebrew` user.
[See here for alternatives](https://taskfile.dev/installation).

## Quickstart for Cursor IDE

0. ensure you have the prerequisites installed
1. clone down this repository
2. ensure you have a suitable `Taskfile.yml` in your working project (you can use the example in this project for inspiration)
3. in Cursor settings > MCP Servers, start a server with the following command:

`uv run --with mcp --directory /path/to/gotask-mcp mcp run /path/to/gotask-mcp/src/server.py`

It is recommended to copy the contextual rule in `.cursor/rules/tool-use-rule.mdc` into your working project (or write a similar rule). The Cursor Agent will need some instructions if it is to use the tools properly.

## Details

A task runner (such as `Taskfile`) is a means of defining and running short commands that do regularly required, simple or complex work.

Such tasks can be an important part of the development cycle, for example autofixes and QA checks. Therefore it would seem useful if coding agents powered by generative AI could run these tasks at the appropriate time. The way to achieve this is with an MCP server that provides tools for running such tasks.

The server is designed to run in an isolated environment and to have contextual information about the working project passed in by the Client (tested with Cursor IDE Agent)

1. a tool to retrieve a list of available tasks
2. a tool to run a named task

The Cursor Agent is expected to pass in the working directory path as an input to these tools, which allows the tools to read the project `Taskfile.yml`.

_(N.B. at the time of writing MCP resources don't work very well with Cursor IDE - the first tool would ideally be implemented as a resource, not a tool)_
