from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def search_file(path, search_type, search_term):
    try:
        if search_type == "extension":
            return path.suffix.lower() == search_term.lower()
        
        elif search_type == "filename":
            return search_term.lower() in path.name.lower()
        
        elif search_type == "text":
            try:
                with open(path,"r",encoding="utf-8",errors="ignore") as file:
                    return search_term.lower() in file.read().lower()
            except (UnicodeDecodeError,PermissionError):
                return False

    except (OSError,PermissionError):
         return False

    return False

