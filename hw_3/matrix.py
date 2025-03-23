import numpy as np

# Глобальный кэш для хранения результатов матричного умножения
matrix_mult_cache = {}


class HashMixin:
    """
    Примесь для реализации хэш-функции матрицы.
    """
    def __hash__(self):
        """
        Простая хэш-функция, которая вычисляет сумму элементов на главной диагонали
        и элементов в первой строке.
        
        Такая функция не является константой, зависит от содержимого матрицы,
        но может давать коллизии (разные матрицы с одинаковым хэшем).
        """
        hash_value = 0
        rows, cols = self.shape
        
        for i in range(min(rows, cols)):
            hash_value += self.data[i][i]
        
        if rows > 0:
            hash_value += sum(self.data[0])
            
        return hash_value
    
    def __eq__(self, other):
        """
        Оператор равенства для сравнения матриц
        """
        if not isinstance(other, Matrix):
            return False
        
        if self.shape != other.shape:
            return False
        
        rows, cols = self.shape
        for i in range(rows):
            for j in range(cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
                    
        return True    


class Matrix(HashMixin):
    def __init__(self, data):
        """
        Инициализирует матрицу из двумерного списка или numpy массива
        """
        if isinstance(data, np.ndarray):
            self.data = data.tolist()
        elif isinstance(data, list):
            if not all(isinstance(row, list) for row in data):
                raise ValueError("Входные данные должны быть списком списков")
            self.data = data
        else:
            raise TypeError("Данные должны быть списком или numpy массивом")
        
        if len(self.data) > 0:
            row_len = len(self.data[0])
            if not all(len(row) == row_len for row in self.data):
                raise ValueError("Все строки матрицы должны иметь одинаковую длину")
    
    @property
    def shape(self):
        """
        Возвращает размерность матрицы в виде кортежа (строки, столбцы)
        """
        if not self.data:
            return (0, 0)
        return (len(self.data), len(self.data[0]) if self.data else 0)
    
    def __str__(self):
        """
        Строковое представление матрицы
        """
        return '\n'.join([str(row) for row in self.data])
    
    def __repr__(self):
        return f"Matrix({self.data})"
    
    
    def __add__(self, other):
        """
        Перегрузка оператора + для сложения матриц
        """
        if not isinstance(other, Matrix):
            raise TypeError("Можно складывать только с другой матрицей")
            
        if self.shape != other.shape:
            raise ValueError(f"Размерности матриц не совпадают: {self.shape} и {other.shape}")
        
        rows, cols = self.shape
        result = []
        
        for i in range(rows):
            new_row = []
            for j in range(cols):
                new_row.append(self.data[i][j] + other.data[i][j])
            result.append(new_row)
                
        return Matrix(result)
    
    def __mul__(self, other):
        """
        Перегрузка оператора * для поэлементного умножения матриц
        """
        if not isinstance(other, Matrix):
            raise TypeError("Можно выполнять поэлементное умножение только с другой матрицей")
            
        if self.shape != other.shape:
            raise ValueError(f"Размерности матриц не совпадают: {self.shape} и {other.shape}")
        
        rows, cols = self.shape
        result = []
        
        for i in range(rows):
            new_row = []
            for j in range(cols):
                new_row.append(self.data[i][j] * other.data[i][j])
            result.append(new_row)
                
        return Matrix(result)
    
    def __matmul__(self, other, use_cache=True):
        """
        Перегрузка оператора @ для матричного умножения с кэшированием
        
        Параметры:
        use_cache (bool): если True, используется кэширование, иначе - нет
        """
        if not isinstance(other, Matrix):
            raise TypeError("Можно выполнять матричное умножение только с другой матрицей")
            
        rows_a, cols_a = self.shape
        rows_b, cols_b = other.shape
        
        if cols_a != rows_b:
            raise ValueError(
                f"Неверные размерности для матричного умножения: "
                f"{self.shape} и {other.shape}"
            )
        

        if use_cache:
            cache_key = (hash(self), hash(other))
            if cache_key in matrix_mult_cache:
                print(f"Результат взят из кэша для хэшей {cache_key}")
                return matrix_mult_cache[cache_key]
        
        result = []
        
        for i in range(rows_a):
            new_row = []
            for j in range(cols_b):
                sum_val = 0
                for k in range(cols_a):
                    sum_val += self.data[i][k] * other.data[k][j]
                new_row.append(sum_val)
            result.append(new_row)
        
        matrix_result = Matrix(result)
        
        if use_cache:
            matrix_mult_cache[cache_key] = matrix_result
            
        return matrix_result


def hash_collision():
    
    A = Matrix([
        [3, 1, 2],
        [4, 5, 6],
        [7, 8, 9] 
    ])
    
    
    C = Matrix([
        [1, 3, 2],
        [4, 6, 6],
        [7, 8, 10] 
    ])
    
    print(f"Хэш матрицы A: {hash(A)}")
    print(f"Хэш матрицы C: {hash(C)}")
    
    if hash(A) != hash(C):
        raise ValueError(f"Хэши матриц A и C не совпадают: {hash(A)} != {hash(C)}")
    
    if A == C:
        raise ValueError("Матрицы A и C одинаковые, нужно найти разные матрицы")
    
    B = D = Matrix([
        [5, 1, 3],
        [4, 1, 2],
        [1, 6, 6]
    ])
    

    AB = A @ B  # Здесь используется кэш
    CD = C @ D  # Хэш A и C совпадает, поэтому без отключения кэша результат берется из кэша
    
    print(f"AB:\n{AB}")
    print(f"CD:\n{CD}")
    
    if AB == CD:
        print("Результаты совпадают из-за кэширования, вычисляем CD без кэша")
        CD = C.__matmul__(D, use_cache=False)
        print(f"CD без кэша:\n{CD}")
    
    if AB == CD:
        raise ValueError("Произведения A @ B и C @ D всё ещё дают одинаковый результат")
    
    return A, B, C, D, AB, CD


if __name__ == "__main__":
    # np.random.seed(0)
    
    # matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    # matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))
    
    # sum_result = matrix1 + matrix2
    # elem_mult_result = matrix1 * matrix2
    # matrix_mult_result = matrix1 @ matrix2
    
    # with open("artifacts/matrix+.txt", "w") as f:
    #     f.write(str(sum_result))
        
    # with open("artifacts/matrix*.txt", "w") as f:
    #     f.write(str(elem_mult_result))

    # with open("artifacts/matrix@.txt", "w") as f:
    #     f.write(str(matrix_mult_result))
        


    A, B, C, D, AB, CD = hash_collision()
    
    with open("artifacts/A.txt", "w") as f:
        f.write(str(A))
        
    with open("artifacts/B.txt", "w") as f:
        f.write(str(B))
        
    with open("artifacts/C.txt", "w") as f:
        f.write(str(C))
        
    with open("artifacts/D.txt", "w") as f:
        f.write(str(D))
        
    with open("artifacts/AB.txt", "w") as f:
        f.write(str(AB))
        
    with open("artifacts/CD.txt", "w") as f:
        f.write(str(CD))
            
    with open("artifacts/hash.txt", "w") as f:
        f.write(f"Хэш матрицы A: {hash(A)}\n")
        f.write(f"Хэш матрицы C: {hash(C)}\n")
        f.write(f"Хэш матрицы AB: {hash(AB)}\n")
        f.write(f"Хэш матрицы CD: {hash(CD)}")            
        

