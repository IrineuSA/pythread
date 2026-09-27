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
            f"Testando {conta_threads} thread(s)..."
        )

        tempo_inicial = time.perf_counter()

        equivalencia = busca_pasta(
            pasta=pasta,
            tipo_busca=tipo_busca,
            termo_busca=termo_busca,
            n_threads=conta_threads
        )

        tempo_final = time.perf_counter()

        tempo_tot = tempo_final - tempo_inicial

        arq_escaneados = equivalencia["arquivos pesquisados"]
        n_equivalentes = len(equivalencia["matches"])

        if tempo_tot > 0:
            arq_p_seg = (
                arq_escaneados / tempo_tot
            )
        else:
            arq_p_seg = 0

        resultado.append({
            "threads": conta_threads,
            "tempo": tempo_tot,
            "arquivos escaneados": arq_escaneados,
            "equivalentes": n_equivalentes,
            "arquivos por segundo": arq_p_seg,
            "matches": equivalencia["matches"]
        })

        print(
            f"  Tempo: {tempo_tot:.4f}s"
        )

        print(
            f"  Arq/seg: {arq_p_seg:.2f}"
        )

        print(
            f"  Equivalentes: {n_equivalentes}"
        )

    return resultado


def conta_arqs(folder: str) -> int:

    from pathlib import Path

    return sum(
        1
        for caminho in Path(folder).rglob("*")
        if caminho.is_file()
    )


def melhor_resultado(resultados: list[dict]) -> dict:

    if not resultados:
        raise ValueError(
            "Nenhum resultado disponivel."
        )

    return max(
        resultados,
        key=lambda result:
        result["arquivos por segundo"]
    )


def calcular_performance(
    base: dict,
    current: dict
) -> float:

    tempo_base = base["tempo"]
    tempo_atual = current["tempo"]

    if tempo_base == 0:
        return 0.0

    return (
        (tempo_base - tempo_atual)
        / tempo_base
    ) * 100


def pico_performance(
    resultados: list[dict]
) -> tuple[dict, list[dict]]:

    melhor_result = melhor_resultado(resultados)

    menor_result = []

    pico = False

    for resultado in resultados:

        if resultado["threads"] == melhor_result["threads"]:
            pico = True
            continue

        if pico:
            menor_result.append(resultado)

    return melhor_result, menor_result