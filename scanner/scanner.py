from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .worker import tipo_busca

def busca_pasta( pasta: str, tipo_pesq: str, termo_busca: str, n_threads: int ):
    arquivos = [ caminho for caminho in Path(pasta).rglob("*") if caminho.is_file() ]
    resultado = []

    with ThreadPoolExecutor( max_workers=n_threads ) as executor:
        futuros = [ executor.submit( tipo_busca, caminho_arq, tipo_pesq, termo_busca ) for caminho_arq in arquivos ]

        for caminho_arq, futuro in zip(arquivos, futuros): 
            if futuro.result(): resultado.append(caminho_arq) 
            
    return resultado