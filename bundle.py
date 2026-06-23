import os
from pathlib import Path

# Configuration: Customize these lists to match your stack
IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__', 
    '.idea', '.vscode', 'build', 'dist', 'vendor', 'target'
}

ALLOWED_EXTENSIONS = {
    '.py', '.java', '.js', '.jsx', '.ts', '.tsx', 
    '.cpp', '.h', '.hpp', '.c', '.php', '.css', 
    '.html', '.ini', '.json', '.md', '.go', '.rs'
}

def generate_tree(dir_path, prefix="", ignore_dirs=None):
    """Generates a visual string representation of the directory structure."""
    if ignore_dirs is None:
        ignore_dirs = set()
    
    markdown_tree = ""
    try:
        entries = sorted(list(dir_path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        entries = [e for e in entries if e.name not in ignore_dirs]
        
        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            
            markdown_tree += f"{prefix}{connector}{entry.name}\n"
            
            if entry.is_dir():
                nested_prefix = prefix + ("    " if is_last else "│   ")
                markdown_tree += generate_tree(entry, nested_prefix, ignore_dirs)
    except PermissionError:
        pass
    return markdown_tree