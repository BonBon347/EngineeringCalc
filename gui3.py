import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import os
import sys

from calculator import EngineeringCalc

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Инженерный калькулятор 🌸")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Милые цвета
        self.colors = {
            'bg': '#FFF0F5',  # Лавандовый розовый
            'frame_bg': '#FFE4E1',  # Мятно-розовый
            'button': '#FFB6C1',  # Светло-розовый
            'button_hover': '#FF69B4',  # Ярко-розовый
            'text': '#8B008B',  # Темно-пурпурный
            'entry_bg': '#FFFFFF',  # Белый
            'title': '#DB7093',  # Бледно-розовый
            'result': '#FF1493'  # Глубокий розовый
        }
        
        # Установка шрифта Cute Pixel
        self.setup_fonts()
        
        self.calculator = EngineeringCalc()
        self.plot_functions = []

        self.create_widgets()
        self.update_history()
        
        # Установка стилей для ttk
        self.setup_styles()

    def setup_fonts(self):
        """Установка шрифта Cute Pixel"""
        # Проверяем, установлен ли шрифт в системе
        try:
            # Пытаемся загрузить шрифт из папки с программой
            font_paths = [
                "CutePixel.ttf",
                "CutePixel-Regular.ttf",
                os.path.join(os.path.dirname(__file__), "CutePixel.ttf"),
                os.path.join(os.path.dirname(__file__), "fonts", "CutePixel.ttf")
            ]
            
            font_loaded = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    # Для систем Windows
                    if sys.platform == "win32":
                        import ctypes
                        ctypes.windll.gdi32.AddFontResourceW(font_path)
                        # Перезагружаем шрифты для системы
                        import win32gui
                        win32gui.SendMessage(win32gui.HWND_BROADCAST, 0x001D, 0, 0)
                        font_loaded = True
                        break
                    # Для macOS и Linux
                    else:
                        font_loaded = True
                        break
            
            # Если шрифт не найден локально, используем системный
            if not font_loaded:
                self.font_family = "Comic Sans MS"  # Запасной милый шрифт
            else:
                self.font_family = "Cute Pixel"
                
        except Exception:
            # Если что-то пошло не так, используем стандартный милый шрифт
            self.font_family = "Comic Sans MS"
        
        # Создаем стили шрифтов
        self.fonts = {
            'title': (self.font_family, 16, 'bold'),
            'subtitle': (self.font_family, 13, 'bold'),
            'normal': (self.font_family, 11),
            'small': (self.font_family, 10),
            'result': (self.font_family, 12, 'bold'),
            'button': (self.font_family, 11, 'bold')
        }

    def setup_styles(self):
        """Настройка стилей для ttk виджетов"""
        style = ttk.Style()
        
        # Настройка для LabelFrame
        style.configure('Custom.TLabelframe', 
                       background=self.colors['frame_bg'],
                       foreground=self.colors['text'])
        style.configure('Custom.TLabelframe.Label',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['subtitle'])
        
        # Настройка для Button
        style.configure('Custom.TButton',
                       background=self.colors['button'],
                       foreground=self.colors['text'],
                       font=self.fonts['button'],
                       padding=10)
        style.map('Custom.TButton',
                 background=[('active', self.colors['button_hover'])])

    def create_widgets(self):
        # Настройка главного фона
        self.root.configure(bg=self.colors['bg'])
        
        # Создаем стильный заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=5)
        
        title_label = tk.Label(title_frame, 
                              text="🌸 Инженерный калькулятор 🌸",
                              font=self.fonts['title'],
                              fg=self.colors['title'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="✨ Сделано с любовью ✨",
                                 font=self.fonts['small'],
                                 fg=self.colors['text'],
                                 bg=self.colors['bg'])
        subtitle_label.pack()

        self.tabs = ttk.Notebook(self.root)
        self.tabs.configure(style='Custom.TNotebook')

        # Создаем вкладки с милым фоном
        tabs_data = [
            ("Арифметика", "🧮"),
            ("Тригонометрия", "📐"),
            ("Матрицы", "🔢"),
            ("Интегрирование", "∫"),
            ("Графики", "📊"),
            ("История", "📝")
        ]
        
        self.tab_frames = {}
        for tab_name, emoji in tabs_data:
            frame = tk.Frame(self.tabs, bg=self.colors['bg'])
            self.tabs.add(frame, text=f"{emoji} {tab_name}")
            self.tab_frames[tab_name] = frame

        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_arithmetic_tab()
        self.create_trigonometry_tab()
        self.create_matrix_tab()
        self.create_integration_tab()
        self.create_graph_tab()
        self.create_history_tab()

    def create_arithmetic_tab(self):
        frame = self.tab_frames["Арифметика"]
        
        title = tk.Label(frame, 
                        text="🧮 Арифметические операции",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=10)

        main_frame = tk.Frame(frame, bg=self.colors['frame_bg'], relief=tk.RIDGE, bd=5)
        main_frame.pack(pady=20, padx=30, fill="x")

        # Входные поля
        for i, (label_text, entry, default) in enumerate([
            ("Число A:", "entry_a", "10"),
            ("Число B:", "entry_b", "5")
        ]):
            tk.Label(main_frame, 
                    text=label_text,
                    font=self.fonts['normal'],
                    fg=self.colors['text'],
                    bg=self.colors['frame_bg']).grid(row=i, column=0, padx=10, pady=8, sticky="e")
            
            entry_widget = tk.Entry(main_frame, 
                                   font=self.fonts['normal'],
                                   bg=self.colors['entry_bg'],
                                   fg=self.colors['text'],
                                   relief=tk.FLAT,
                                   width=15)
            entry_widget.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            entry_widget.insert(0, default)
            
            if label_text == "Число A:":
                self.entry_a = entry_widget
            else:
                self.entry_b = entry_widget

        # Операция
        tk.Label(main_frame,
                text="Операция:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['frame_bg']).grid(row=2, column=0, padx=10, pady=8, sticky="e")
        
        self.arithmetic_op = ttk.Combobox(
            main_frame,
            values=["Сложение", "Вычитание", "Умножение", "Деление", "Степень"],
            state="readonly",
            width=15,
            font=self.fonts['normal']
        )
        self.arithmetic_op.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.arithmetic_op.current(0)

        # Кнопка
        btn = tk.Button(main_frame,
                       text="🌸 Вычислить",
                       font=self.fonts['button'],
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       relief=tk.RAISED,
                       bd=3,
                       cursor="hand2",
                       command=self.calculate_arithmetic)
        btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Результат
        self.arithmetic_result = tk.Label(frame,
                                         text="Результат: ",
                                         font=self.fonts['result'],
                                         fg=self.colors['result'],
                                         bg=self.colors['bg'])
        self.arithmetic_result.pack(pady=15)

    def create_trigonometry_tab(self):
        frame = self.tab_frames["Тригонометрия"]
        
        title = tk.Label(frame,
                        text="📐 Тригонометрические функции",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=10)

        main_frame = tk.Frame(frame, bg=self.colors['frame_bg'], relief=tk.RIDGE, bd=5)
        main_frame.pack(pady=20, padx=30, fill="x")

        # Угол
        tk.Label(main_frame,
                text="Угол/значение:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['frame_bg']).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        
        self.angle_entry = tk.Entry(main_frame,
                                   font=self.fonts['normal'],
                                   bg=self.colors['entry_bg'],
                                   fg=self.colors['text'],
                                   relief=tk.FLAT,
                                   width=15)
        self.angle_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.angle_entry.insert(0, "45")

        # Режим
        tk.Label(main_frame,
                text="Режим:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['frame_bg']).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        
        self.angle_mode = ttk.Combobox(
            main_frame,
            values=["Градусы", "Радианы"],
            state="readonly",
            width=15,
            font=self.fonts['normal']
        )
        self.angle_mode.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        self.angle_mode.current(0)

        # Функция
        tk.Label(main_frame,
                text="Функция:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['frame_bg']).grid(row=2, column=0, padx=10, pady=8, sticky="e")
        
        self.trig_op = ttk.Combobox(
            main_frame,
            values=["sin", "cos", "tan", "asin", "acos", "atan"],
            state="readonly",
            width=15,
            font=self.fonts['normal']
        )
        self.trig_op.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.trig_op.current(0)

        # Кнопка
        btn = tk.Button(main_frame,
                       text="🌸 Вычислить",
                       font=self.fonts['button'],
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       relief=tk.RAISED,
                       bd=3,
                       cursor="hand2",
                       command=self.calculate_trigonometry)
        btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Результат
        self.trig_result = tk.Label(frame,
                                   text="Результат: ",
                                   font=self.fonts['result'],
                                   fg=self.colors['result'],
                                   bg=self.colors['bg'])
        self.trig_result.pack(pady=15)

    def create_matrix_tab(self):
        frame = self.tab_frames["Матрицы"]
        
        title = tk.Label(frame,
                        text="🔢 Матричные операции",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=10)

        input_frame = tk.Frame(frame, bg=self.colors['bg'])
        input_frame.pack(pady=10, fill="x", padx=20)

        # Матрица A
        left_frame = tk.LabelFrame(input_frame,
                                  text="🌸 Матрица A",
                                  font=self.fonts['subtitle'],
                                  fg=self.colors['text'],
                                  bg=self.colors['frame_bg'],
                                  relief=tk.RIDGE,
                                  bd=3)
        left_frame.pack(side="left", padx=5, fill="both", expand=True)
        
        self.matrix_a_text = tk.Text(left_frame,
                                    height=5,
                                    width=20,
                                    font=("Courier", 10),
                                    bg=self.colors['entry_bg'],
                                    fg=self.colors['text'],
                                    relief=tk.FLAT)
        self.matrix_a_text.pack(padx=5, pady=5)
        self.matrix_a_text.insert("1.0", "[[1,2],[3,4]]")

        # Матрица B
        right_frame = tk.LabelFrame(input_frame,
                                   text="🌸 Матрица B",
                                   font=self.fonts['subtitle'],
                                   fg=self.colors['text'],
                                   bg=self.colors['frame_bg'],
                                   relief=tk.RIDGE,
                                   bd=3)
        right_frame.pack(side="right", padx=5, fill="both", expand=True)
        
        self.matrix_b_text = tk.Text(right_frame,
                                    height=5,
                                    width=20,
                                    font=("Courier", 10),
                                    bg=self.colors['entry_bg'],
                                    fg=self.colors['text'],
                                    relief=tk.FLAT)
        self.matrix_b_text.pack(padx=5, pady=5)
        self.matrix_b_text.insert("1.0", "[[5,6],[7,8]]")

        # Управление
        control_frame = tk.Frame(frame, bg=self.colors['bg'])
        control_frame.pack(pady=10)

        tk.Label(control_frame,
                text="Операция:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['bg']).grid(row=0, column=0, padx=5)
        
        self.matrix_op = ttk.Combobox(
            control_frame,
            values=["Сложение", "Вычитание", "Умножение", "Транспонирование A", 
                    "Определитель A", "Обратная A", "Умножить на скаляр A"],
            state="readonly",
            width=20,
            font=self.fonts['normal']
        )
        self.matrix_op.grid(row=0, column=1, padx=5)
        self.matrix_op.current(0)

        tk.Label(control_frame,
                text="Скаляр:",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['bg']).grid(row=0, column=2, padx=5)
        
        self.scalar_entry = tk.Entry(control_frame,
                                    width=8,
                                    font=self.fonts['normal'],
                                    bg=self.colors['entry_bg'],
                                    fg=self.colors['text'],
                                    relief=tk.FLAT)
        self.scalar_entry.grid(row=0, column=3, padx=5)
        self.scalar_entry.insert(0, "2")

        btn = tk.Button(control_frame,
                       text="🌸 Вычислить",
                       font=self.fonts['button'],
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       relief=tk.RAISED,
                       bd=3,
                       cursor="hand2",
                       command=self.calculate_matrix)
        btn.grid(row=0, column=4, padx=10)

        # Результат
        result_frame = tk.LabelFrame(frame,
                                    text="🌸 Результат",
                                    font=self.fonts['subtitle'],
                                    fg=self.colors['text'],
                                    bg=self.colors['frame_bg'],
                                    relief=tk.RIDGE,
                                    bd=3)
        result_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.matrix_result_text = tk.Text(result_frame,
                                         height=6,
                                         font=("Courier", 10),
                                         bg=self.colors['entry_bg'],
                                         fg=self.colors['text'],
                                         relief=tk.FLAT)
        self.matrix_result_text.pack(fill="both", expand=True, padx=5, pady=5)

    def create_integration_tab(self):
        frame = self.tab_frames["Интегрирование"]
        
        title = tk.Label(frame,
                        text="∫ Численное интегрирование",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=10)

        main_frame = tk.Frame(frame, bg=self.colors['frame_bg'], relief=tk.RIDGE, bd=5)
        main_frame.pack(pady=20, padx=30, fill="x")

        # Поля ввода
        fields = [
            ("Функция f(x):", "func_entry", "x**2 + 3*x", 30),
            ("Нижний предел (a):", "lower_entry", "0", 15),
            ("Верхний предел (b):", "upper_entry", "2", 15),
            ("Шагов (n):", "steps_entry", "1000", 15)
        ]
        
        for i, (label, attr, default, width) in enumerate(fields):
            tk.Label(main_frame,
                    text=label,
                    font=self.fonts['normal'],
                    fg=self.colors['text'],
                    bg=self.colors['frame_bg']).grid(row=i, column=0, padx=10, pady=8, sticky="e")
            
            entry = tk.Entry(main_frame,
                            font=self.fonts['normal'],
                            bg=self.colors['entry_bg'],
                            fg=self.colors['text'],
                            relief=tk.FLAT,
                            width=width)
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            entry.insert(0, default)
            setattr(self, attr, entry)

        # Кнопка
        btn = tk.Button(main_frame,
                       text="🌸 Вычислить интеграл",
                       font=self.fonts['button'],
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       relief=tk.RAISED,
                       bd=3,
                       cursor="hand2",
                       command=self.calculate_integral)
        btn.grid(row=4, column=0, columnspan=2, pady=15)

        # Результат
        self.integral_result = tk.Label(frame,
                                       text="Результат: ",
                                       font=self.fonts['result'],
                                       fg=self.colors['result'],
                                       bg=self.colors['bg'])
        self.integral_result.pack(pady=15)

    def create_graph_tab(self):
        frame = self.tab_frames["Графики"]
        
        title = tk.Label(frame,
                        text="📊 Построение графиков",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=5)

        input_frame = tk.Frame(frame, bg=self.colors['bg'])
        input_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(input_frame,
                text="Функции (через запятую):",
                font=self.fonts['normal'],
                fg=self.colors['text'],
                bg=self.colors['bg']).pack(side="left", padx=5)
        
        self.functions_entry = tk.Entry(input_frame,
                                       width=50,
                                       font=self.fonts['normal'],
                                       bg=self.colors['entry_bg'],
                                       fg=self.colors['text'],
                                       relief=tk.FLAT)
        self.functions_entry.pack(side="left", padx=5)
        self.functions_entry.insert(0, "np.sin(x), np.cos(x), x**2")

        btn = tk.Button(input_frame,
                       text="🌸 Построить",
                       font=self.fonts['button'],
                       bg=self.colors['button'],
                       fg=self.colors['text'],
                       relief=tk.RAISED,
                       bd=3,
                       cursor="hand2",
                       command=self.plot_graph)
        btn.pack(side="left", padx=5)

        self.graph_frame = tk.Frame(frame, bg=self.colors['bg'])
        self.graph_frame.pack(pady=10, fill="both", expand=True)

        self.graph_label = tk.Label(self.graph_frame,
                                   text="💝 Введите функции и нажмите 'Построить'",
                                   font=self.fonts['normal'],
                                   fg=self.colors['text'],
                                   bg=self.colors['bg'])
        self.graph_label.pack(expand=True)

    def create_history_tab(self):
        frame = self.tab_frames["История"]
        
        title = tk.Label(frame,
                        text="📝 История операций",
                        font=self.fonts['title'],
                        fg=self.colors['title'],
                        bg=self.colors['bg'])
        title.pack(pady=10)

        self.history_text = tk.Text(frame,
                                   height=20,
                                   font=("Courier", 10),
                                   bg=self.colors['entry_bg'],
                                   fg=self.colors['text'],
                                   relief=tk.FLAT,
                                   state="disabled")
        self.history_text.pack(pady=10, fill="both", expand=True, padx=20)

        button_frame = tk.Frame(frame, bg=self.colors['bg'])
        button_frame.pack(pady=5)

        btn1 = tk.Button(button_frame,
                        text="🌸 Обновить",
                        font=self.fonts['button'],
                        bg=self.colors['button'],
                        fg=self.colors['text'],
                        relief=tk.RAISED,
                        bd=3,
                        cursor="hand2",
                        command=self.update_history)
        btn1.grid(row=0, column=0, padx=5)
        
        btn2 = tk.Button(button_frame,
                        text="🌸 Очистить",
                        font=self.fonts['button'],
                        bg=self.colors['button'],
                        fg=self.colors['text'],
                        relief=tk.RAISED,
                        bd=3,
                        cursor="hand2",
                        command=self.clear_history)
        btn2.grid(row=0, column=1, padx=5)

    # Остальные методы остаются без изменений
    def calculate_arithmetic(self):
        try:
            a = float(self.entry_a.get().replace(",", "."))
            b = float(self.entry_b.get().replace(",", "."))
            op = self.arithmetic_op.get()

            if op == "Сложение":
                result = self.calculator.arithmetic.AddOperation(a, b)
            elif op == "Вычитание":
                result = self.calculator.arithmetic.SubOperation(a, b)
            elif op == "Умножение":
                result = self.calculator.arithmetic.MulOperation(a, b)
            elif op == "Деление":
                result = self.calculator.arithmetic.DivOperation(a, b)
            elif op == "Степень":
                result = self.calculator.arithmetic.power(a, b)

            self.arithmetic_result.config(text=f"Результат: {result} 🌟")
            self.update_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"😅 {str(e)}")

    def calculate_trigonometry(self):
        try:
            value = float(self.angle_entry.get().replace(",", "."))
            mode = self.angle_mode.get()
            op = self.trig_op.get()

            if op in ["asin", "acos", "atan"]:
                if op == "asin":
                    result = self.calculator.trigonometry.AsinOperation(value)
                elif op == "acos":
                    result = self.calculator.trigonometry.AcosOperation(value)
                elif op == "atan":
                    result = self.calculator.trigonometry.AtanOperation(value)
                self.trig_result.config(text=f"Результат: {result} 🌟")
            else:
                if mode == "Градусы":
                    if op == "sin":
                        result = self.calculator.trigonometry.SinOperationGrad(value)
                    elif op == "cos":
                        result = self.calculator.trigonometry.CosOperationGrad(value)
                    elif op == "tan":
                        result = self.calculator.trigonometry.TanOperationGrad(value)
                else:  # Радианы
                    if op == "sin":
                        result = self.calculator.trigonometry.SinOperationRad(value)
                    elif op == "cos":
                        result = self.calculator.trigonometry.CosOperationRad(value)
                    elif op == "tan":
                        result = self.calculator.trigonometry.TanOperationRad(value)
                self.trig_result.config(text=f"Результат: {result} 🌟")
            self.update_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"😅 {str(e)}")

    def _parse_matrix(self, text):
        text = text.strip().replace("\n", "")
        return eval(text)

    def calculate_matrix(self):
        try:
            A = self._parse_matrix(self.matrix_a_text.get("1.0", tk.END))
            B = self._parse_matrix(self.matrix_b_text.get("1.0", tk.END))
            op = self.matrix_op.get()

            if op == "Сложение":
                result = self.calculator.matrix.add_matrices(A, B)
            elif op == "Вычитание":
                result = self.calculator.matrix.subtract_matrices(A, B)
            elif op == "Умножение":
                result = self.calculator.matrix.multiply_matrices(A, B)
            elif op == "Транспонирование A":
                result = self.calculator.matrix.transpose(A)
            elif op == "Определитель A":
                result = self.calculator.matrix.determinant(A)
            elif op == "Обратная A":
                result = self.calculator.matrix.inverse(A)
            elif op == "Умножить на скаляр A":
                scalar = float(self.scalar_entry.get().replace(",", "."))
                result = self.calculator.matrix.multiply_by_scalar(A, scalar)

            self.matrix_result_text.delete("1.0", tk.END)
            if isinstance(result, list):
                formatted = "[" + "\n ".join(str(row) for row in result) + "]"
                self.matrix_result_text.insert("1.0", f"🌟 {formatted}")
            else:
                self.matrix_result_text.insert("1.0", f"🌟 {result}")

            self.update_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"😅 {str(e)}")

    def calculate_integral(self):
        try:
            func_str = self.func_entry.get()
            a = float(self.lower_entry.get().replace(",", "."))
            b = float(self.upper_entry.get().replace(",", "."))
            n = int(self.steps_entry.get())

            def f(x):
                return eval(func_str, {"__builtins__": {}}, {"math": math, "np": np, "x": x})

            result = self.calculator.integration.IntegrateOperation(f, a, b, n)
            self.integral_result.config(text=f"Результат: {result:.6f} 🌟")
            self.update_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"😅 {str(e)}")

    def plot_graph(self):
        try:
            funcs = [f.strip() for f in self.functions_entry.get().split(",")]
            
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor('#FFF0F5')
            ax.set_facecolor('#FFE4E1')
            
            x = np.linspace(-10, 10, 500)

            safe_dict = {
                "np": np, "math": math, "x": x,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
                "pi": math.pi, "e": math.e
            }

            colors = ['#FF1493', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            for i, func in enumerate(funcs):
                y = eval(func, {"__builtins__": {}}, safe_dict)
                ax.plot(x, y, label=f"y={func}", color=colors[i % len(colors)], linewidth=2)

            ax.axhline(0, color='#8B008B', linewidth=0.5, alpha=0.5)
            ax.axvline(0, color='#8B008B', linewidth=0.5, alpha=0.5)
            ax.grid(True, alpha=0.2, linestyle='--')
            ax.legend(facecolor='#FFF0F5', edgecolor='#FFB6C1')
            ax.set_title("🌸 Графики функций", fontsize=14, color='#DB7093')

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            self.calculator._history.add_records("Графики", f"Построено: {', '.join(funcs)}", "Успешно")
            self.update_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"😅 Ошибка построения: {str(e)}")

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        history = self.calculator._history._history
        if not history:
            self.history_text.insert(tk.END, "🌸 История пуста. Начните вычисления!")
        else:
            for i, record in enumerate(history, 1):
                self.history_text.insert(tk.END, 
                    f"{i:3}. [{record['category']:12}] {record['operation']} = {record['result']}\n")
        
        self.history_text.config(state="disabled")

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "🌸 Очистить историю?"):
            self.calculator._history.clear()
            self.update_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()