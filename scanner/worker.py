from pathlib import Path

def busca_arq(
    caminho_arq: Path,
    tipo_busca: str,
    termo_pesq: str
) -> bool:
    try:
        if tipo_busca == "filename":
            return termo_pesq.lower() in caminho_arq.name.lower()
        elif tipo_busca == "extension":
            extencao = termo_pesq.lower()
            if not extencao.startswith("."):
                extencao = "." + extencao
            return caminho_arq.suffix.lower() == extencao
        elif tipo_busca == "text":
            try:
                with open(caminho_arq,"r",encoding="utf-8",errors="ignore") as file:
                    for linha in file:
                        if termo_pesq.lower() in linha.lower():
                            return True
            except (PermissionError,OSError):
                return False 
            return False
        else:
            raise ValueError(
                f"Tipo de pesquisa desconhecido: {tipo_busca}"
            )

    except(PermissionError,OSError):
        return False