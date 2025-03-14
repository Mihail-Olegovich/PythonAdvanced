# LaTeX Generator

Простая библиотека для генерации LaTeX кода.

## Установка

```bash
pip install latex-generator-itmo-kulyaskin
```

## Использование

### Генерация таблиц

```python
from latex_generator import generate_table


data = [
    ["Имя", "Возраст", "Город"],
    ["Иван", "25", "Москва"],
    ["Мария", "30", "Санкт-Петербург"]
]


latex_table = generate_table(
    data,
    caption="Пример таблицы с данными пользователей",
    label="tab:users"
)

print(latex_table)
```

### Генерация изображений

```python
from latex_generator import generate_image

latex_image = generate_image(
    "cat.png",
    caption="Котик",
    label="fig:cat",
    width="0.8\\textwidth"
)

print(latex_image)
```