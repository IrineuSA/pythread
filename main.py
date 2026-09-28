from scanner.benchmark import (
    benchmark_threads,
    pico_performance
)

from visual.graficos import gerar_graficos


resultados = benchmark_threads(
    pasta=r"",
    tipo_busca="",
    termo_busca="",
    n_threads=[
        1,
        2,
        4,
        8,
        16,
        32,
        64
    ],
)

melhor, resultado_pos_pico = pico_performance(resultados)

print("\n========== ANALISE ==========")

print(
    f"Melhor numero de threads: "
    f"{melhor['threads']}"
)

print(
    f"Pico: "
    f"{melhor['arquivos por segundo']:.2f} arq/seg"
)

gerar_graficos(
    resultados,
    salvar=True
)