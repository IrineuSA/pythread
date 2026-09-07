from pathlib import Path
import matplotlib.pyplot as plt

def gera_grafico(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "resultados"
) -> None:
    threads = [
        resultado["threads"]
        for resultado in resultados
    ]

    throughput = [
        resultado["arquivos por segundo"]
        for resultado in resultados
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(
        threads,
        throughput,
        marker="o"
    )

    plt.title(
        "Desempenho / Número de Threads"
    )

    plt.xlabel("Número de Threads")
    plt.ylabel("Arquivos por Segundo")

    plt.xticks(threads)
    plt.grid(True)
    plt.tight_layout()

    if salvar:
        _salvar_grafico(
            pasta_saida,
            "throughput_threads.png"
        )

    plt.show()

def grafico_tempo(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "graficos"
) -> None:
    threads = [
        resultado["threads"]
        for resultado in resultados
    ]

    tempos = [
        resultado["tempo"]
        for resultado in resultados
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(
        threads,
        tempos,
        marker="o"
    )

    plt.title(
        "Tempo de Execução / Número de Threads"
    )

    plt.xlabel("Número de Threads")
    plt.ylabel("Tempo de Execução (s)")
    plt.xticks(threads)
    plt.grid(True)
    plt.tight_layout()

    if salvar:
        _salvar_grafico(
            pasta_saida,
            "tempo_threads.png"
        )
    plt.show()

def grafico_performance_relativa(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "graficos"
) -> None:
    threads = []
    performance = []

    for i in range(1, len(resultados)):

        anterior = resultados[i - 1]
        atual = resultados[i]

        vel_anterior = anterior[
            "arquivos por segundo"
        ]

        vel_atual = atual[
            "arquivos por segundo"
        ]

        if vel_anterior == 0:
            percentual = 0
        else:
            percentual = (
                (vel_atual - vel_anterior)
                / vel_anterior
            ) * 100

        threads.append(
            atual["threads"]
        )

        performance.append(
            percentual
        )

    plt.figure(figsize=(10, 6))
    plt.bar(
        [str(thread) for thread in threads],
        performance
    )
    plt.axhline(
        y=0,
        linewidth=1
    )
    plt.title(
        "Variação de Performance entre Threads"
    )
    plt.xlabel("Número de Threads")
    plt.ylabel("Variação de Performance (%)")
    plt.tight_layout()

    if salvar:
        _salvar_grafico(
            pasta_saida,
            "performance_relativa.png"
        )

    plt.show()

def _salvar_grafico(
    pasta_saida: str,
    nome_arquivo: str
) -> None:
    pasta = Path(pasta_saida)

    pasta.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.savefig(
        pasta / nome_arquivo,
        dpi=300
    )
