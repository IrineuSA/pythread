import threading
from tkinter import ttk
from tkinter import messagebox

from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visual.graficos import gerar_graficos

class BenchmarkTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            padding=10
        )
        self._criar_progresso()
        self._criar_tabela()
        

    def _criar_progresso(self):
        self.status_label = ttk.Label(
            self,
            text="Pronto"
        )

        self.status_label.pack(
            anchor="w",
            pady=(0,5)
        )

        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )

        self.progress_bar.pack(
            fill="x",
            pady=(0,10)
        )
    
    def _atualizar_progresso(
        self,
        valor,
        mensagem
    ):
        self.after(
            0,
            self._aplicar_progresso,
            valor,
            mensagem
        )

    def _aplicar_progresso(
        self,
        valor,
        mensagem
    ):
        self.progress_bar["value"]=(
            valor*100
        )
        self.status_label.config(
            text=mensagem
        )

    def _criar_tabela(self):

        colunas = (
            "threads",
            "tempo",
            "arquivos",
            "encontrados",
            "throughput"
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )
        self.tree.heading(
            "threads",
            text="Threads"
        )
        self.tree.heading(
            "tempo",
            text="Tempo"
        )
        self.tree.heading(
            "arquivos",
            text="Arquivos"
        )
        self.tree.heading(
            "encontrados",
            text="Encontrados"
        )
        self.tree.heading(
            "throughput",
            text="Arquivos/s"
        )
        self.tree.pack(
            fill="both",
            expand=True
        )
        ttk.Label(
        self,
            text="Arquivos Encontrados"
        ).pack(
            anchor="w",
            pady=(10, 5)
        )
        self.matches_tree = ttk.Treeview(
            self,
            columns=(
                "nome",
                "caminho"
            ),
        show="headings",
        height=8
        )
        self.matches_tree.heading(
            "nome",
            text="Nome"
        )
        self.matches_tree.heading(
            "caminho",
            text="Caminho"
        )
        self.matches_tree.column(
            "nome",
            width=250
        )
        self.matches_tree.column(
            "caminho",
            width=600
        )
        self.matches_tree.pack(
            fill="both",
            expand=True
        )
        
    def executar(
        self,
        config,
        graph_dir,
        on_complete=None
    ):

        thread = threading.Thread(
            target=self._executar_thread,
            args=(
                config,
                graph_dir,
                on_complete
            ),
            daemon=True
        )
        thread.start()
    
    def _executar_thread(
        self,
        config,
        graph_dir,
        on_complete
    ):

        try:
            resultados = benchmark_threads(
                pasta=config["pasta"],
                tipo_busca=config["tipo_busca"],
                termo_busca=config["termo_busca"],
                n_threads=config["threads"],
                progresso=self._atualizar_progresso
            )

            self._atualizar_progresso(
                1.0,
                "Gerando gráficos..."
            )

            gerar_graficos(
                resultados,
                salvar=True,
                pasta_saida=str(graph_dir),
                mostrar=False
            )

            self._atualizar_progresso(
                1.0,
                "Concluído."
            )

            self.after(
                0,
                lambda:
                self._mostrar_resultados(
                    resultados,
                    on_complete
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda erro=erro:
                messagebox.showerror(
                    "Erro",
                    str(erro)
                )
            )

    def _mostrar_resultados(
        self,
        resultados,
        on_complete
  ):

            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for item in self.matches_tree.get_children():
                self.matches_tree.delete(item)                
            
            melhor = melhor_resultado(
                resultados
            )
            self.tree.tag_configure(
                "melhor",
                background="lightgreen",
                font=("TkDefaultFont", 10, "bold")
            )
                
            for resultado in resultados:
                tag = ()

                if resultado["threads"] == melhor["threads"]:
                    tag = ("melhor",)

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        resultado["threads"],
                        f"{resultado['tempo']:.4f}",
                        resultado[
                            "arquivos escaneados"
                        ],
                        resultado[
                            "equivalentes"
                        ],
                        f"{resultado['arquivos por segundo']:.2f}"
                    ),
                    tags=tag
                )

            if resultados:
                matches = resultados[0]["matches"]
                for caminho in matches:
                    self.matches_tree.insert(
                        "",
                        "end",
                        values=(
                            caminho.name,
                            str(caminho)
                        )
                    )
            melhor = melhor_resultado(
            resultados
        )
            messagebox.showinfo(
                "Benchmark concluído",
                (
                    f"Melhor resultado: "
                    f"{melhor['threads']} threads\n"
                    f"{melhor['arquivos por segundo']:.2f} "
                   "arquivos/s"
                )
            )

            if on_complete:
                on_complete()
