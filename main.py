from scanner.benchmark import (
    benchmark_threads,
    calcular_performance
)


resultados = benchmark_threads(
    pasta="",
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
    ]
)

analise = calcular_performance(resultados)

print("\n========== ANALISE ==========")

print(
    f"Melhor numero de threads: "
    f"{analise['pico_threads']}"
)

print(
    f"Pico: "
    f"{analise['peak_throughput']:.2f} arq/seg"
)