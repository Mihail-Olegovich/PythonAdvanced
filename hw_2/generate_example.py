import os
import shutil
import subprocess

from latex_generator_itmo_kulyaskin import generate_image, generate_table


def save_to_tex_file(latex_content, filename):
    """
    Сохраняет LaTeX контент в файл с добавлением преамбулы и окружения документа.
    
    Аргументы:
        latex_content (str): LaTeX контент для сохранения.
        filename (str): Имя файла, в который нужно сохранить контент.
    """
    preamble = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T2A]{fontenc}
\\usepackage[russian]{babel}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{geometry}
\\geometry{a4paper, margin=1in}

\\title{Пример генерации таблицы и изображения}
\\author{Автоматический генератор LaTeX}
\\date{\\today}

\\begin{document}
\\maketitle

"""
    
    closing = """
\\end{document}"""
    
    full_content = preamble + latex_content + closing
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(full_content)

def generate_pdf(tex_file):
    """
    Генерирует PDF из TeX файла с помощью pdflatex.
    
    Аргументы:
        tex_file (str): Путь к TeX файлу.
    
    Возвращает:
        bool: True, если PDF был успешно сгенерирован, иначе False.
    """
    try:
        tex_dir = os.path.dirname(tex_file)
        

        if not shutil.which('pdflatex'):
            print("ВНИМАНИЕ: pdflatex не найден. PDF не может быть сгенерирован автоматически.")
            print("Вы можете вручную скомпилировать .tex файл после установки LaTeX дистрибутива.")
            return False
        
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', os.path.basename(tex_file)],
            cwd=tex_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Ошибка при генерации PDF: {result.stderr}")
            return False
        
        print(f"PDF успешно сгенерирован: {tex_file.replace('.tex', '.pdf')}")
        return True
    
    except Exception as e:
        print(f"Произошла ошибка при генерации PDF: {e}")
        return False

def main():

    sample_data = [
        ["Имя", "Возраст", "Город"],
        ["Иван", "25", "Москва"],
        ["Мария", "30", "Санкт-Петербург"], 
        ["Алексей", "22", "Казань"],
        ["Екатерина", "28", "Новосибирск"]
    ]
    
    latex_table = generate_table(
        sample_data,
        caption="Пример таблицы с данными пользователей",
        label="tab:users"
    )
    
    latex_image = generate_image(
        "cat.png",
        caption="Котик",
        label="fig:cat",
        width="0.8\\textwidth"
    )
    
    latex_content = """\\section{Пример таблицы}

Ниже представлена таблица, сгенерированная с помощью функции generate\\_table:

""" + latex_table + """

\\section{Пример изображения}

Ниже представлено изображение, сгенерированное с помощью функции generate\\_image:

""" + latex_image
    
    tex_file = "hw_2/artifacts/example.tex"
    
    save_to_tex_file(latex_content, tex_file)
    
    print(f"LaTeX файл успешно сгенерирован: {tex_file}")
    
    generate_pdf(tex_file)
    
if __name__ == "__main__":
    main()