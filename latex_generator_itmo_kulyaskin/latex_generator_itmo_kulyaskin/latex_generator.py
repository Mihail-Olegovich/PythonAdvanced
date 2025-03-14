def generate_table(data, caption=None, label=None):
    """
    Функция для генерации LaTeX кода таблицы.
    
    Аргументы:
        data (list): Двумерный список, представляющий данные таблицы.
        caption (str, optional): Подпись к таблице.
        label (str, optional): Метка для перекрестных ссылок.
    
    Возвращает:
        str: Строка, содержащая LaTeX код таблицы.
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Данные должны быть непустым двумерным списком")

    num_columns = len(data[0])
    
    column_format = "|" + "|".join(["c"] * num_columns) + "|"
    
    def escape_latex(text):
        """Экранирование специальных символов LaTeX."""
        if not isinstance(text, str):
            text = str(text)
        replacements = {
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "{": "\\{",
            "}": "\\}",
            "~": "\\textasciitilde{}",
            "^": "\\textasciicircum{}"
        }
        return "".join(replacements.get(c, c) for c in text)
    
    def create_row(row):
        """Создание строки таблицы."""
        return " & ".join(escape_latex(cell) for cell in row) + " \\\\"
    
    rows = [create_row(row) for row in data]
    
    rows_with_lines = ["\\hline"] + [f"{row}\n\\hline" for row in rows]
    
    tabular_content = "\n".join(rows_with_lines)
    
    tabular = f"\\begin{{tabular}}{{{column_format}}}\n{tabular_content}\n\\end{{tabular}}"
    
    table_elements = ["\\begin{table}[h]", "\\centering", tabular]
    
    if caption:
        table_elements.append(f"\\caption{{{escape_latex(caption)}}}")
    
    if label:
        table_elements.append(f"\\label{{{label}}}")
    
    table_elements.append("\\end{table}")
    
    return "\n".join(table_elements) 


def generate_image(image_path, caption=None, label=None, width=None, height=None, placement="h"):
    """
    Функция для генерации LaTeX кода для включения изображения.
    
    Аргументы:
        image_path (str): Путь к изображению.
        caption (str, optional): Подпись к изображению.
        label (str, optional): Метка для перекрестных ссылок.
        width (str, optional): Ширина изображения (например, "0.8\\textwidth").
        height (str, optional): Высота изображения (например, "5cm").
        placement (str, optional): Параметр размещения для окружения figure.
    
    Возвращает:
        str: Строка, содержащая LaTeX код для включения изображения.
    """
    if not image_path:
        raise ValueError("Путь к изображению не может быть пустым")
    
    def escape_latex(text):
        """Экранирование специальных символов LaTeX."""
        if not isinstance(text, str):
            text = str(text)
        replacements = {
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "{": "\\{",
            "}": "\\}",
            "~": "\\textasciitilde{}",
            "^": "\\textasciicircum{}"
        }
        return "".join(replacements.get(c, c) for c in text)
    
    options = []
    if width:
        options.append(f"width={width}")
    if height:
        options.append(f"height={height}")
    
    options_str = f"[{', '.join(options)}]" if options else ""
    
    include_graphics = f"\\includegraphics{options_str}{{{image_path}}}"
    
    figure_elements = [f"\\begin{{figure}}[{placement}]", "\\centering", include_graphics]
    
    if caption:
        figure_elements.append(f"\\caption{{{escape_latex(caption)}}}")
    
    if label:
        figure_elements.append(f"\\label{{{label}}}")
    
    figure_elements.append("\\end{figure}")
    
    return "\n".join(figure_elements)