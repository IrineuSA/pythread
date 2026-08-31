from pathlib import Path

def search_file(
    file_path: Path,
    search_type: str,
    search_term: str
) -> bool:
    try:
        if search_type == "filename":
            return search_term.lower() in file_path.name.lower()
        elif search_type == "extension":
            extension = search_term.lower()
            if not extension.startswith("."):
                extension = "." + extension
            return file_path.suffix.lower() == extension
        elif search_type == "text":
            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:
                    for line in file:
                        if search_term.lower() in line.lower():
                            return True
            except (PermissionError,OSError):
                return False 
            return False
        else:
            raise ValueError(
                f"Tipo de pesquisa desconhecido: {search_type}"
            )

    except(PermissionError,OSError):
        return False