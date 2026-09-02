import time 
from .scanner import busca_pasta

def benchmark_threads(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: list[int]
) -> list[dict]:
        resultado = []
        for conta_threads in n_threads:
            print(
                f"Testando {n_threads} thread(s)..."
        )

        tempo_inicial = time.perf_counter()

        equivalencia = busca_pasta(
            pasta=pasta,
            tipo_pesq=tipo_busca,
            termo_busca=termo_busca,
            n_threads=n_threads
        )

        tempo_final = time.perf_counter()

        tempo_tot = tempo_final - tempo_inicial

        arq_escaneados = conta_arqs(pasta)

        if tempo_tot > 0:
            arq_p_seg = (
                arq_escaneados / tempo_tot
            )
        else:
            arq_p_seg = 0

        resultado.append({
            "threads": n_threads,
            "tempo": tempo_tot,
            "arquivos escaneados": arq_escaneados,
            "equivalentes": len(equivalencia),
            "arquivos por segundo": arq_p_seg
        })

        print(
            f"  Tempo: {tempo_tot:.4f}s"
        )

        print(
            f"  Arq/seg: "
            f"{arq_p_seg:.2f}"
        )

        print(
            f"  Equivalentes: {len(equivalencia)}"
        )

        return resultado

def conta_arqs(folder: str) -> int:
    from pathlib import Path

    return sum(
        1
        for caminho in Path(folder).rglob("*")
        if caminho.is_file()
    )