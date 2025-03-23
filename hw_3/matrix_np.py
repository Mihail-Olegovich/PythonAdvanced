import numpy as np


class ArithmeticMixin:
    """Примесь для арифметических операций"""
    def __add__(self, other):
        """Операция сложения с другой матрицей"""
        if not isinstance(other, MatrixNP):
            raise TypeError("Можно складывать только с другой матрицей")
        if self.data.shape != other.data.shape:
            raise ValueError(f"Размерности матриц не совпадают: {self.data.shape} и {other.data.shape}")
        return MatrixNP(self.data + other.data)
    
    def __sub__(self, other):
        """Операция вычитания другой матрицы"""
        if not isinstance(other, MatrixNP):
            raise TypeError("Можно вычитать только другую матрицу")
        if self.data.shape != other.data.shape:
            raise ValueError(f"Размерности матриц не совпадают: {self.data.shape} и {other.data.shape}")
        return MatrixNP(self.data - other.data)
    
    def __mul__(self, other):
        """Операция поэлементного умножения с другой матрицей или на скаляр"""
        if isinstance(other, MatrixNP):
            if self.data.shape != other.data.shape:
                raise ValueError(f"Размерности матриц не совпадают: {self.data.shape} и {other.data.shape}")
            return MatrixNP(self.data * other.data)
        elif isinstance(other, (int, float)):
            return MatrixNP(self.data * other)
        else:
            raise TypeError("Умножение поддерживается только с матрицей или числом")
    
    def __rmul__(self, other):
        """Операция умножения на скаляр справа"""
        if isinstance(other, (int, float)):
            return MatrixNP(other * self.data)
        return NotImplemented
    
    def __truediv__(self, other):
        """Операция деления матрицы на матрицу или скаляр"""
        if isinstance(other, MatrixNP):
            if self.data.shape != other.data.shape:
                raise ValueError(f"Размерности матриц не совпадают: {self.data.shape} и {other.data.shape}")
            return MatrixNP(self.data / other.data)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Деление на ноль")
            return MatrixNP(self.data / other)
        else:
            raise TypeError("Деление поддерживается только с матрицей или числом")
    
    def __matmul__(self, other):
        """Операция матричного умножения с другой матрицей"""
        if not isinstance(other, MatrixNP):
            raise TypeError("Можно выполнять матричное умножение только с другой матрицей")
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError(
                f"Неверные размерности для матричного умножения: "
                f"{self.data.shape} и {other.data.shape}"
            )
        return MatrixNP(self.data @ other.data)
    
    def __pow__(self, power):
        """Возведение матрицы в степень"""
        if not isinstance(power, int):
            raise TypeError("Степень должна быть целым числом")
        
        if power < 0:
            raise ValueError("Степень должна быть неотрицательной")
        
        if power == 0:
            rows, cols = self.data.shape
            if rows != cols:
                raise ValueError("Только квадратная матрица может быть возведена в нулевую степень")
            return MatrixNP(np.eye(rows))
        
        if power == 1:
            return MatrixNP(self.data.copy())
        
        rows, cols = self.data.shape
        if rows != cols:
            raise ValueError("Только квадратная матрица может быть возведена в степень")
        
        result = self.data.copy()
        for _ in range(power - 1):
            result = result @ self.data
        
        return MatrixNP(result)
    
    def transpose(self):
        """Транспонирование матрицы"""
        return MatrixNP(self.data.T)


class IOFileMixin:
    """Примесь для работы с файлами"""
    def save_to_file(self, filename):
        """Сохраняет матрицу в текстовый файл"""
        with open(filename, "w") as f:
            f.write(str(self))


class DisplayMixin:
    """Примесь для отображения"""
    def __str__(self):
        """Строковое представление матрицы"""
        return np.array2string(self.data, precision=4, suppress_small=True)
    
    def __repr__(self):
        """Представление для отладки"""
        return f"MatrixNP({self.data})"


class PropertyMixin:
    """Примесь для свойств"""
    @property
    def shape(self):
        """Возвращает размерность матрицы"""
        return self.data.shape
    
    @property
    def rows(self):
        """Возвращает количество строк"""
        return self.data.shape[0]
    
    @property
    def cols(self):
        """Возвращает количество столбцов"""
        return self.data.shape[1]
    
    def get_element(self, i, j):
        """Получить элемент матрицы по индексам"""
        return self.data[i, j]
    
    def set_element(self, i, j, value):
        """Установить элемент матрицы по индексам"""
        self.data[i, j] = value


class MatrixNP(ArithmeticMixin, IOFileMixin, DisplayMixin, PropertyMixin):
    """Класс матрицы с использованием примесей"""
    def __init__(self, data):
        """
        Инициализирует матрицу из двумерного списка или numpy массива
        """
        if isinstance(data, np.ndarray):
            self.data = data
        elif isinstance(data, list):
            self.data = np.array(data)
        else:
            raise TypeError("Данные должны быть списком или numpy массивом")
        
        if len(self.data.shape) != 2:
            raise ValueError("Матрица должна быть двумерной")


if __name__ == "__main__":
    np.random.seed(0)
    
    matrix1 = MatrixNP(np.random.randint(0, 10, (10, 10)))
    matrix2 = MatrixNP(np.random.randint(0, 10, (10, 10)))
    
    matrix1.save_to_file("artifacts/matrix_np1.txt")
    matrix2.save_to_file("artifacts/matrix_np2.txt")
    

    sum_result = matrix1 + matrix2
    sub_result = matrix1 - matrix2
    elem_mult_result = matrix1 * matrix2
    matrix_mult_result = matrix1 @ matrix2
    scalar_mult_result = matrix1 * 2
    transpose_result = matrix1.transpose()
    # Для возведения в степень используем квадратную матрицу
    power_result = MatrixNP(np.random.randint(0, 5, (5, 5))) ** 2
    div_result = matrix1 / matrix2
    
    sum_result.save_to_file("artifacts/matrix_np+.txt")
    sub_result.save_to_file("artifacts/matrix_np-.txt")
    elem_mult_result.save_to_file("artifacts/matrix_np*.txt")
    matrix_mult_result.save_to_file("artifacts/matrix_np@.txt")
    scalar_mult_result.save_to_file("artifacts/matrix_np_scalar.txt")
    transpose_result.save_to_file("artifacts/matrix_np_transpose.txt")
    power_result.save_to_file("artifacts/matrix_np_power.txt")
    div_result.save_to_file("artifacts/matrix_np_div.txt")
