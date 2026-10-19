import tkinter as tk
from tkinter import ttk
from scanner.process import EstadoProcesso

class ProcessTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            padding=10
        )

        self.processos = {}
        self._criar_resumo()
        self._criar_fila()
        self._criar_tabela()

    def _criar_resumo(self):
        frame = ttk.Frame(self)
        frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.ready_label = ttk.Label(
            frame,
            text="READY: 0"
        )

        self.ready_label.pack(
            side="left",
            padx=10
        )

        self.running_label = ttk.Label(
            frame,
            text="RUNNING: 0"
        )

        self.running_label.pack(
            side="left",
            padx=10
        )

        self.terminated_label = ttk.Label(
            frame,
            text="TERMINATED: 0"
        )

        self.terminated_label.pack(
            side="left",
            padx=10
        )
        
        self.waiting_label = ttk.Label(
            frame,
            text="WAITING: 0"
        )

        self.waiting_label.pack(
            side="left",
            padx=10
        )

    def _criar_tabela(self):
        colunas = (
            "ordem",
            "pid",
            "arquivo",
            "tamanho",
            "estado"
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )

        self.tree.heading(
            "pid",
            text="PID"
        )

        self.tree.heading(
            "arquivo",
            text="Arquivo"
        )

        self.tree.heading(
            "estado",
            text="Estado"
        )

        self.tree.heading(
            "ordem",
            text="Ordem"
        )

        self.tree.heading(
            "tamanho",
            text="Tamanho"
        )

        self.tree.column(
            "tamanho",
            width=120,
            anchor="e"
        )

        self.tree.column(
            "ordem",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "pid",
            width=80
        )

        self.tree.column(
            "arquivo",
            width=600
        )

        self.tree.column(
            "estado",
            width=150
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

    def _criar_fila(self):
        frame=ttk.LabelFrame(
            self,
            text="Fila de Prontos"
        )
        frame.pack(
            fill="x",
            pady=(0,10)
        )
        self.ready_queue_label=ttk.Label(
            frame,
            text="Fila vazia",
            anchor="w"
        )
        self.ready_queue_label.pack(
            fill="x",
            padx=10,
            pady=10
        )
    
    def atualizar_processo(
        self,
        pid,
        arquivo,
        estado,
        ordem
    ):
        self.after(
            0,
            self._aplicar_atualizacao,
            pid,
            arquivo,
            estado,
            ordem
        )
    
    def _aplicar_atualizacao(
        self,
        pid,
        arquivo,
        estado,
        ordem
    ):
        self.processos[pid] = {
            "arquivo": arquivo,
            "estado": estado,
            "ordem": ordem
        }

        item_id = str(pid)

        try:
            tamanho = arquivo.stat().st_size
            tamanho_texto = self.formatar_tamanho(tamanho)
        except OSError:
            tamanho_texto = "N/D"

        valores = (
            ordem if ordem is not None else "-",
            pid,
            arquivo.name,
            tamanho_texto,
            estado.value
        )
        if self.tree.exists(item_id):
            self.tree.item(
                item_id,
                values=valores
            )
        else:
            self.tree.insert(
                "",
                "end",
                iid=item_id,
                values=valores
            )
        self._atualizar_resumo()
        self.ordenar_por_despacho()

    def _atualizar_resumo(self):
        ready=0
        running=0
        terminated=0
        waiting=0

        for processo in self.processos.values():
            estado = processo["estado"]
            if estado == EstadoProcesso.READY:
                ready += 1
            
            elif estado == EstadoProcesso.RUNNING:
                running += 1

            elif estado == EstadoProcesso.TERMINATED:
                terminated += 1
            
            elif estado == EstadoProcesso.WAITING:
                waiting += 1

        self.ready_label.config(
            text=f"READY: {ready}"
        )

        self.running_label.config(
            text=f"RUNNING: {running}"
        )

        self.terminated_label.config(
            text=f"TERMINATED: {terminated}"
        )

        self.waiting_label.config(
            text=f"WAITING: {waiting}"
        )

    def limpar(self):
        self.processos.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)
        self._atualizar_resumo()

    def atualizar_fila(self,pids):
        self.after(
            0,
            self._aplicar_fila,
            pids
        )
        self.ready_queue_label.config(
            text="Fila vazia"
        )

    def _aplicar_fila(self, pids):
        if not pids:
            texto = "Fila vazia"
        else:
            primeiros = pids[:15]

            texto = " → ".join(
                f"P{pid}"
                for pid in primeiros
            )

            if len(pids) > 15:
                texto += f" → ... ({len(pids)} na fila)"

        self.ready_queue_label.config(
            text=texto
        )

    def ordenar_por_despacho(self):
        itens = self.tree.get_children()

        def chave(item):
            pid = int(item)
            ordem = self.processos[pid]["ordem"]

            if ordem is None:
                return (1,pid)
            return (0, ordem)
        
        itens_ordenados = sorted(
            itens,
            key=chave
        )

        for indice,item in enumerate(itens_ordenados):
            self.tree.move(
                item,
                "",
                indice
            )

    @staticmethod
    def formatar_tamanho(tamanho):
        if tamanho < 1024:
            return f"{tamanho} B"

        if tamanho < 1024 ** 2:
            return f"{tamanho / 1024:.2f} KB"

        return f"{tamanho / (1024 ** 2):.2f} MB"