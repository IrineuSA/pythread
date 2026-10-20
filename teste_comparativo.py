from scanner.benchmark import benchmark_comparativo
from visual.graficos import grafico_comparativo

resultados = benchmark_comparativo(
    pasta=r"E:\Downloads\Warhammer Universe\Necromunda\Necromunda",
    tipo_busca="extension",
    termo_busca=".pdf",
    n_threads=[1, 2, 4],
    max_io=1
)

for algoritmo, medicoes in resultados.items():

    print(f"\nAlgoritmo: {algoritmo}")

    for resultado in medicoes:
        print(
            f"Threads: {resultado['threads']} | "
            f"Retorno médio: "
            f"{resultado['tempo medio retorno'] * 1000:.3f} ms"
        )

grafico_comparativo(
    resultados,
    salvar=True,
    pasta_saida="graficos",
    run_id="teste_comparativo"
)