from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from scanner.benchmark import calcular_performance


def gera_grafico(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "resultados",
    run_id: str = ""
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
            "throughput_threads.png",
            run_id
        )

def grafico_tempo(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "graficos",
    run_id: str = ""
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
            "tempo_threads.png",
            run_id
        )

def grafico_performance_relativa(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "graficos",
    run_id: str = ""
) -> None:
    threads = []
    performance = []

    base = next(
        resultado
        for resultado in resultados
        if resultado["threads"] == 1
    )

    for atual in resultados:

        percentual = calcular_performance(
            base,
            atual
        )

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
        "Performance em Relação a 1 Thread"
    )

    plt.xlabel("Número de Threads")

    plt.ylabel(
        "Melhoria em Relação a 1 Thread (%)"
    )

    plt.tight_layout()

    if salvar:
        _salvar_grafico(
            pasta_saida,
            "performance_relativa.png",
            run_id
        )

def gerar_graficos(
    resultados: list[dict],
    salvar: bool = False,
    pasta_saida: str = "graficos",
    mostrar: bool = True
) -> None:
    if not resultados:
        raise ValueError(
            "Nenhum resultado disponivel"
        )

    run_id = datetime.now().strftime(
        "%d-%m-%Y_%H-%M"
    )

    gera_grafico(
        resultados,
        salvar,
        pasta_saida,
        run_id
    )

    grafico_tempo(
        resultados,
        salvar,
        pasta_saida,
        run_id
    )

    grafico_performance_relativa(
        resultados,
        salvar,
        pasta_saida,
        run_id
    )

    if mostrar:
        plt.show()
    else:
        plt.close("all")

def _salvar_grafico(
    pasta_saida: str,
    nome_arquivo: str,
    run_id: str
) -> None:
    pasta = Path(pasta_saida)

    pasta.mkdir(
        parents=True,
        exist_ok=True
    )

    nome = Path(nome_arquivo)

    novo_nome = (
        f"{nome.stem}_{run_id}"
        f"{nome.suffix}"
    )

    plt.savefig(
        pasta / novo_nome,
        dpi=300
    )
