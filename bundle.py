import os
from pathlib import Path

# config:
IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__', 
    '.idea', '.vscode', 'build', 'dist', 'vendor', 'target', 'out'
}

ALLOWED_EXTENSIONS = {
    '.py', '.java', '.js', '.jsx', '.ts', '.tsx', 
    '.cpp', '.h', '.hpp', '.c', '.php', '.css', 
    '.html', '.ini', '.json', '.md', '.go', '.rs', '.scss'
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

def bundle_project(root_dir, output_file):
    root_path = Path(root_dir).resolve()
    output_path = Path(output_file).resolve()
    script_path = Path(__file__).resolve()
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # write header and directory tree
        outfile.write("===================================================================\n")
        outfile.write(f"PROJECT CONTEXT: {root_path.name}\n")
        outfile.write("===================================================================\n\n")
        
        outfile.write("## DIRECTORY STRUCTURE:\n")
        outfile.write("```\n")
        outfile.write(f"{root_path.name}/\n")
        outfile.write(generate_tree(root_path, ignore_dirs=IGNORE_DIRS))
        outfile.write("```\n\n")
        
        outfile.write("## SOURCE CODE:\n\n")
        
        # files
        for path in sorted(root_path.rglob('*')):
            # skip ignored dirs
            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            if path.resolve() == script_path:
                continue
                
            # check if the file has a target file extension
            if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
                if path == output_path:
                    continue
                    
                try:
                    rel_path = path.relative_to(root_path)
                    
                    # format code blocks
                    outfile.write(f"### FILE: {rel_path}\n")
                    outfile.write(f"```{path.suffix.lstrip('.')}\n")
                    
                    # read content and replace error bytes
                    content = path.read_text(encoding='utf-8', errors='replace')
                    outfile.write(content)
                    
                    if not content.endswith('\n'):
                        outfile.write('\n')
                        
                    outfile.write("```\n\n")
                    print(f"Bundled: {rel_path}")
                    
                except Exception as e:
                    print(f"Error reading {path.name}: {e}")

if __name__ == "__main__":
    # uses current directory as project root folder, you can change this
    TARGET_PROJECT = "." 
    OUTPUT_FILENAME = "project_context.md"
    
    print(f"scanning directory: {Path(TARGET_PROJECT).resolve()}")
    bundle_project(TARGET_PROJECT, OUTPUT_FILENAME)
    print(f"\ncontext saved to {OUTPUT_FILENAME}")