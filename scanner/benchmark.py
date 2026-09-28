import time
from .scanner import busca_pasta


def benchmark_threads(
    pasta: str,
    tipo_busca: str,
    termo_busca: str,
    n_threads: list[int],
    progresso=None
) -> list[dict]:

    resultado = []
    
    repeticoes = 10
    total_testes = len(n_threads)*repeticoes
    teste_atual=0

    if progresso:
        progresso(
            0,
            "Preparando benchmark..."
        )

    for conta_threads in n_threads:

        tempos = []
        velocidades = []

        equivalencia = None

        for repeticao in range(repeticoes):

            if progresso:
                progresso(
                    teste_atual / total_testes,
                    (
                        f"Testando {conta_threads} thread(s) "
                        f"- execução {repeticao + 1}/{repeticoes}..."
                    )
                )

            print(
                f"Testando {conta_threads} thread(s) "
                f"- execução {repeticao + 1}/{repeticoes}..."
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

            arq_escaneados = equivalencia[
                "arquivos pesquisados"
            ]

            if tempo_tot > 0:
                arq_p_seg = (
                    arq_escaneados / tempo_tot
                )
            else:
                arq_p_seg = 0

            tempos.append(tempo_tot)
            velocidades.append(arq_p_seg)

            teste_atual += 1

        tempo_medio = sum(tempos) / repeticoes

        velocidade_media = (
            sum(velocidades) / repeticoes
        )

        n_equivalentes = len(
            equivalencia["matches"]
        )

        resultado.append({
            "threads": conta_threads,
            "tempo": tempo_medio,
            "arquivos escaneados": arq_escaneados,
            "equivalentes": n_equivalentes,
            "arquivos por segundo": velocidade_media,
            "matches": equivalencia["matches"]
        })

        print(
            f"\nResultado médio para "
            f"{conta_threads} thread(s):"
        )

        print(
            f"  Tempo médio: {tempo_medio:.4f}s"
        )

        print(
            f"  Arq/seg médio: {velocidade_media:.2f}"
        )

        print(
            f"  Equivalentes: {n_equivalentes}"
        )

    if progresso:
        progresso(
            1.0,
            "Benchmark concluido."
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