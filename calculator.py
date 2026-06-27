import math

class History:
    def __init__(self):
        self._history=[]
    def add_records(self,category,operation,result):
        self._history.append({"category":category,"operation":operation, "result":result})
    def show(self):
        """Выводит на экран всю историю: категории, операции и результаты."""
        if not self._history:
            print("История операций пуста.")
            return

        print("\n===== ИСТОРИЯ ОПЕРАЦИЙ =====")
        # Проходим циклом по каждому словарю в списке
        for record in self._history:
            # Достаем значения по ключам: 'category', 'operation', 'result'
            category = record["category"]
            operation = record["operation"]
            result = record["result"]

            # Выводим красивую строку со всеми данными
            print(f"[{category}] | {operation} = {result}")
    def clear(self):
        self._history=[]
        

class BasedCalculator:
    def __init__ (self,history):
        self._history=history
    def AddOperation(self,a,b):
        x=a+b
        self._history.add_records(category="Арифметика", operation=f"{a}+{b}", result=x)
    def SubOperation(self,a,b):
        x=a-b
        self._history.add_records(category="Арифметика", operation=f"{a}-{b}", result=x)
    def MulOperation(self,a,b):
        x=a*b
        self._history.add_records(category="Арифметика", operation=f"{a}*{b}", result=x)
    def DivOperation(self,a,b):
        x=a/b
        self._history.add_records(category="Арифметика", operation=f"{a}/{b}", result=x)

    
class TrigCalculator:
    def __init__ (self,history):
        self._history=history
        
    def SinOperationGrad(self, deg):
        rad = math.radians(deg)
        x = math.sin(rad)
        # Округлим для красивой записи в историю
        rad_round = round(rad, 4)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"sin({deg}° | {rad_round} рад)", result={x_round})
        
    def SinOperationRad(self, rad):
        deg = math.degrees(rad)
        x = math.sin(rad)
        deg_round = round(deg, 2)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"sin({rad} рад | {deg_round}°)", result={x_round})

        
    def CosOperationGrad(self, deg):
        rad = math.radians(deg)
        x = math.cos(rad)
        rad_round = round(rad, 4)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"cos({deg}° | {rad_round} рад)", result={x_round})

        
    def CosOperationRad(self, rad):
        deg = math.degrees(rad)
        x = math.cos(rad)
        deg_round = round(deg, 2)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"cos({rad} рад | {deg_round}°)", result={x_round})

        
    def TanOperationGrad(self, deg):
        # Проверка: тангенс не существует при 90, 270, -90 и т.д. градусах
        if deg % 180 == 90:
            print(f"Ошибка: tan({deg}°) не существует!")
            return
        rad = math.radians(deg)
        x = math.tan(rad)
        rad_round = round(rad, 4)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"tan({deg}° | {rad_round} рад)", result={x_round})

        
    def TanOperationRad(self, rad):
        # Проверка: тангенс не существует, если угол равен pi/2 + pi * k
        # Переводим в градусы для точной и простой проверки деления на 180
        deg = math.degrees(rad)
        if round(deg, 2) % 180 == 90:
            print(f"Ошибка: tan({rad} рад) не существует!")
            return
        x = math.tan(rad)
        deg_round = round(deg, 2)
        x_round = round(x, 4)
        self._history.add_records(category="Тригонометрия", operation=f"tan({rad} рад | {deg_round}°)", result={x_round})

    # Обратные функции принимают число (значение от -1 до 1) и возвращают угол
    def AsinOperation(self, value):
        if not -1 <= value <= 1:
            print(f"Ошибка: значение для asin должно быть в диапазоне от -1 до 1 (передано {value})")
            return
        rad = math.asin(value)
        deg = math.degrees(rad)
        self._history.add_records(category="Тригонометрия", operation=f"asin({value})", result=f"{round(deg, 2)}°={round(rad, 4)} рад")


    def AcosOperation(self, value):
        if not -1 <= value <= 1:
            print(f"Ошибка: значение для acos должно быть в диапазоне от -1 до 1 (передано {value})")
            return
        rad = math.acos(value)
        deg = math.degrees(rad)
        self._history.add_records(category="Тригонометрия", operation=f"acos({value})", result=f"{round(deg, 2)}°={round(rad, 4)} рад")
        

    def AtanOperation(self, value):
        # Арктангенс определен для любого числа
        rad = math.atan(value)
        deg = math.degrees(rad)
        self._history.add_records(category="Тригонометрия", operation=f"atan({value})", result=f"{round(deg, 2)}°={round(rad, 4)} рад")

        
import matplotlib.pyplot as plt
import numpy as np


class InteractiveGraphCalculator:
    """Графический калькулятор с поддержкой общей истории."""

    def __init__(self, history):
        self._history = history

        self.functions_to_plot = []
        self.plots_data = []
        self.current_index = 0

        self.x = np.linspace(-10, 10, 500)

        self.fig = None
        self.ax = None

    def PlotOperation(self, *functions):
        """
        Построение одного или нескольких графиков.

        Пример:
        calc.graph.PlotOperation(
            "np.sin(x)",
            "np.cos(x)",
            "x**2"
        )
        """

        self.functions_to_plot = list(functions)
        self.plots_data = []
        self.current_index = 0

        self.fig, self.ax = plt.subplots(figsize=(11, 6))
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

        self.prepare_data()

        if self.plots_data:
            self.update_graph()
            plt.show()
        else:
            print("Нет корректных функций для построения.")

    def prepare_data(self):

        for expr in self.functions_to_plot:

            try:

                y = eval(
                    expr,
                    {"__builtins__": None},
                    {"np": np, "x": self.x}
                )

                self.plots_data.append({
                    "expr": expr,
                    "y": y,
                    "type": "single"
                })

                self._history.add_records(
                    "Графики",
                    f"Построение y={expr}",
                    "Успешно"
                )

            except Exception as e:

                self._history.add_records(
                    "Графики",
                    f"Построение y={expr}",
                    f"Ошибка: {type(e).__name__}"
                )

                print(f"Ошибка в функции {expr}")

        if self.plots_data:
            self.plots_data.append({
                "type": "history"
            })

    def update_graph(self):

        self.ax.clear()

        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")
        self.ax.grid(True)

        current = self.plots_data[self.current_index]

        if current["type"] == "single":

            self.ax.plot(
                self.x,
                current["y"],
                linewidth=2,
                label=f"y={current['expr']}"
            )

            self.ax.set_title(
                f"График {self.current_index+1} из {len(self.plots_data)-1}\n"
                "Пробел — следующий график"
            )

            y = current["y"][np.isfinite(current["y"])]

            if len(y):

                self.ax.set_ylim(
                    max(np.min(y)-1, -20),
                    min(np.max(y)+1, 20)
                )

            self.ax.legend()

        else:

            ymin = -5
            ymax = 5

            for plot in self.plots_data[:-1]:

                self.ax.plot(
                    self.x,
                    plot["y"],
                    label=f"y={plot['expr']}"
                )

                y = plot["y"][np.isfinite(plot["y"])]

                if len(y):

                    ymin = min(ymin, np.min(y)-1)
                    ymax = max(ymax, np.max(y)+1)

            self.ax.set_ylim(
                max(ymin, -30),
                min(ymax, 30)
            )

            self.ax.set_title(
                "Все графики\nПробел — вернуться к первому"
            )

            self.ax.legend(
                bbox_to_anchor=(1, 1),
                loc="upper left"
            )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        self.fig.canvas.draw()

    def on_key(self, event):

        if event.key == " ":

            self.current_index += 1

            if self.current_index >= len(self.plots_data):
                self.current_index = 0

            self.update_graph()


class IntegrationCalculator:
    def __init__(self, history):
        self._history = history

    def IntegrateOperation(self, func, a, b, n=1000):
        if n <= 0:
            raise ValueError("Количество шагов разбиения должно быть больше нуля!")
        
        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)
        
        result = total * h
        func_name = getattr(func, '__name__', 'f(x)')
        self._history.add_records(category = "Интегрирование", operation = f"∫ от {a} до {b} для {func_name} (n={n})", result = result)
        return result



def func1(x):
    return x**2 + 3*x

def func2(x):
    return x**2 + 3*x + 1

def func3(x):
    return x**3 - 2*x + 5

def func4(x):
    return math.sin(x) + math.cos(x)

def func5(x):
    return 2*x**2 - 4*x + 1

def square(x):
    return x**2

def sine(x):
    return math.sin(x)

def exp_plus_x(x):
    return math.exp(x) + x

def linear(x):
    return 3*x + 1

def polynomial(x):
    return x**4 - 2*x**3 + 3*x**2 - 4*x + 5


class MatrixCalculator:
    def __init__ (self,history):
        self._history=history

    @property
    def history(self):
        return self._history
    def _validate_matrix(self, matrix, name="Матрица"):
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise ValueError(f"{name} должна быть списком списков.")
        if len(matrix) == 0 or len(matrix[0]) == 0:
            raise ValueError(f"{name} не может быть пустой.")
        row_len = len(matrix[0])
        for i, row in enumerate(matrix):
            if len(row) != row_len:
                raise ValueError(f"{name}: строка {i} имеет длину {len(row)} вместо {row_len}.")
            if not all(isinstance(x, (int, float)) for x in row):
                raise ValueError(f"{name}: все элементы должны быть числами.")
    def _same_size(self, A, B):
        return len(A) == len(B) and len(A[0]) == len(B[0])
    def add_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if not self._same_size(A, B):
            raise ValueError("Матрицы должны быть одного размера для сложения.")
        rows, cols = len(A), len(A[0])
        result = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]
        self._history.add_records("Матрицы", f"Сложение\n{A}\n+\n{B}", result)
        return result
    def subtract_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if not self._same_size(A, B):
            raise ValueError("Матрицы должны быть одного размера для вычитания.")
        rows, cols = len(A), len(A[0])
        result = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]
        self._history.add_records("Матрицы", f"Вычитание\n{A}\n-\n{B}", result)
        return result
    def multiply_by_scalar(self, matrix, scalar):
        self._validate_matrix(matrix)
        rows, cols = len(matrix), len(matrix[0])
        result = [[matrix[i][j] * scalar for j in range(cols)] for i in range(rows)]
        self._history.add_records("Матрицы", f"Умножение на скаляр {scalar}\n{matrix}", result)
        return result
    def multiply_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if len(A[0]) != len(B):
            raise ValueError("Число столбцов A должно равняться числу строк B для умножения.")
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        self._history.add_records("Матрицы", f"Умножение\n{A}\n@\n{B}", result)
        return result
    def transpose(self, matrix):
        self._validate_matrix(matrix)
        rows, cols = len(matrix), len(matrix[0])
        result = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
        self._history.add_records("Матрицы", f"Транспонирование\n{matrix}", result)
        return result
    def determinant(self, matrix):
        self._validate_matrix(matrix)
        if len(matrix) != len(matrix[0]):
            raise ValueError("Определитель определён только для квадратных матриц.")
        def _det(m):
            if len(m) == 1:
                return m[0][0]
            if len(m) == 2:
                return m[0][0] * m[1][1] - m[0][1] * m[1][0]
            det_value = 0
            for col in range(len(m)):
                sign = (-1) ** col
                minor = [row[:col] + row[col+1:] for row in m[1:]]
                det_value += sign * m[0][col] * _det(minor)
            return det_value
        det_result = _det(matrix)
        self._history.add_records("Матрицы", f"Определитель\n{matrix}", det_result)
        return det_result
    def inverse(self, matrix):
        self._validate_matrix(matrix)
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Обратная матрица существует только для квадратных матриц.")
        det = self.determinant(matrix)
        if det == 0:
            raise ValueError("Матрица вырождена, обратной не существует.")
        cofactors = []
        for i in range(n):
            cofactor_row = []
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
                cofactor = ((-1) ** (i + j)) * self._det_without_history(minor)  # используем внутренний метод
                cofactor_row.append(cofactor)
            cofactors.append(cofactor_row)
        adjugate = [[cofactors[j][i] for j in range(n)] for i in range(n)]
        inv = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
        self._history.add_records("Матрицы", f"Обратная к\n{matrix}", inv)
        return inv
    def _det_without_history(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det_value = 0
        for col in range(len(matrix)):
            sign = (-1) ** col
            minor = [row[:col] + row[col+1:] for row in matrix[1:]]
            det_value += sign * matrix[0][col] * self._det_without_history(minor)
        return det_value





    
class EngineeringCalc:
    def __init__(self):
        self._history=History()
     # надо добавить остальные классы
        self.arithmetic=BasedCalculator(self._history)
        self.trigonometry=TrigCalculator(self._history)
        self.graph=InteractiveGraphCalculator(self._history)
        self.integration=IntegrationCalculator(self._history)
        self.matrix=MatrixCalculator(self._history)

    def show_history(self):
        self._history.show()


calc1 = EngineeringCalc()

calc1.arithmetic.AddOperation(42,25)
calc1.arithmetic.MulOperation(3,14)
calc1.trigonometry.CosOperationRad(1.0472)
calc1.trigonometry.AtanOperation(1)

calc1.integration.IntegrateOperation(func1,0,2)
A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
calc1.matrix.add_matrices(A, B)
calc1.show_history()

