import argparse
import asyncio
import os
import time
from pathlib import Path

import aiohttp
import aiofiles


async def download_ai_face(
    session: aiohttp.ClientSession, index: int, folder: str
) -> str:
    """Скачивает сгенерированное ИИ изображение лица с thispersondoesnotexist.com."""    
    start_time = time.time()
    print(f"[{time.time():.2f}] Начинаю скачивание изображения {index}")
    
    url = "https://thispersondoesnotexist.com"
    filename = os.path.join(folder, f"ai_face_{index}.jpg")

    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                # Асинхронная запись файла
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(content)          
                elapsed = time.time() - start_time
                print(f"[{time.time():.2f}] Скачано изображение {index}. Размер: {len(content)} байт. Время: {elapsed:.2f} сек")
                return filename
            else:
                print(f"[{time.time():.2f}] Ошибка при скачивании изображения {index}: {response.status}")
                return None
    except Exception as e:
        print(f"[{time.time():.2f}] Исключение при скачивании изображения {index}: {e}")
        return None


async def main(count: int):
    start_time = time.time()
    print(f"[{time.time():.2f}] Начало выполнения")
    
    artifacts_folder = "hw_5/artifacts"
    
    # Создаем директорию до начала асинхронного кода
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: Path(artifacts_folder).mkdir(exist_ok=True, parents=True))
    
    # Устанавливаем больший лимит соединений
    connector = aiohttp.TCPConnector(
        ssl=False,
        limit=count,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        
        for i in range(1, count + 1):
            task = asyncio.create_task(download_ai_face(session, i, artifacts_folder))
            tasks.append(task)
            print(f"[{time.time():.2f}] Задача {i} создана")

        downloaded_files = await asyncio.gather(*tasks)

        successful_downloads = [f for f in downloaded_files if f]
        elapsed = time.time() - start_time
        print(f"\n[{time.time():.2f}] Скачивание завершено! Общее время: {elapsed:.2f} сек")
        print(f"Успешно скачано: {len(successful_downloads)} из {count} изображений")
        print(f"Файлы сохранены в папке: {os.path.abspath(artifacts_folder)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скачивание AI-сгенерированных лиц без ограничений"
    )
    parser.add_argument("count", type=int, help="Количество изображений для скачивания")
    args = parser.parse_args()

    if args.count <= 0:
        print("Количество изображений должно быть положительным числом!")
    else:
        asyncio.run(main(args.count))