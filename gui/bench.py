import threading
from tkinter import ttk
from tkinter import messagebox

from scanner.benchmark import (
    benchmark_threads,
    melhor_resultado
)
from visual.graficos import gerar_graficos