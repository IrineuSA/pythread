

from scanner.scanner import busca_pasta
from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visual.graficos import gerar_graficos


    #Conf
    def _criar_configuracoes(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Configuração da pesquisa",
            padding=10
        )
        frame.pack(
            fill="x"
        )
        frame.columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            frame,
            text="Pasta:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )
        ttk.Entry(
            frame,
            textvariable=self.pasta_var
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            frame,
            text="Procurar...",
            command=self.selecionar_pasta
        ).grid(
            row=0,
            column=2,
            padx=(8, 0),
            pady=5
        )

        ttk.Label(
            frame,
            text="Tipo:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )

        tipo_combo = ttk.Combobox(
            frame,
            textvariable=self.tipo_busca_var,
            values=list(
                self.tipo_busca_map.keys()
            ),
            state="readonly"
        )

        tipo_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )

        tipo_combo.bind(
            "<<ComboboxSelected>>",
            self.tipo_busca_alterado
        )

        ttk.Label(
            frame,
            text="Termo:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=5
        )

        self.termo_entry = ttk.Entry(
            frame,
            textvariable=self.termo_busca_var
        )
        self.termo_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5
        )
        # Botões

        botoes = ttk.Frame(frame)

        botoes.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(10, 0)
        )

        self.botao_pesquisar.pack(
            side="left"
        )

        self.botao_benchmark = ttk.Button(
            botoes,
            text="Benchmark + Gerar Gráficos",
            command=self.iniciar_benchmark
        )

        self.botao_benchmark.pack(
            side="left",
            padx=10
        )