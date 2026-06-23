# LLM Project Bundler

<p align="left">
   <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-blue.svg" />
   <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" />
</p>

A lightweight, zero-dependency Python utility that recursively scans your project directory, visualizes your folder structure, and compiles your entire codebase into a single formatted Markdown (`.md`) file. 

Perfect for feeding massive codebase context into AI models (like ChatGPT, Claude, or Gemini) without the hassle of copying and pasting dozens of individual files.

## Features

* **Directory Tree:** Auto-generates a visual file hierarchy at the top of the file so the AI understands your project's architecture before reading the code.
* **Syntax-Highlighted Markdown:** Automatically wraps each file's source code in its native Markdown code block (e.g., `py` `js`, `scss`).
* **Smart Ignored Directories:** Built-in skipping for heavy build artifacts, environments, and hidden folders (`node_modules`, `venv`, `dist`, `out`, `.git`, etc.).
* **Encoding-Safe:** Replaces invalid characters instead of crashing when encountering weirdly encoded files.

## Configurability

The script is intentionally simple, but a few settings can be adjusted directly in `bundle.py` near the top of the file and near the bottom of the script:

* **`IGNORE_DIRS`** controls which folders are skipped while walking the project tree.
* **`ALLOWED_EXTENSIONS`** controls which file types are included in the final bundle.
* **`TARGET_PROJECT`** sets the root directory to scan. By default, this is the current directory (`.`).
* **`OUTPUT_FILENAME`** sets the name of the generated Markdown file. By default, this is `project_context.md`.

If you want different behavior, edit those constants before running the script.

## Usage

1. Drop the script (e.g., `bundle.py`) into the root directory of your project.
2. Open your terminal in given project and run:
```bash
   python bundle.py