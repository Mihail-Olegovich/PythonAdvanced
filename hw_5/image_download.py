import argparse
import asyncio
import os
from pathlib import Path

import aiohttp


async def download_ai_face(
    session: aiohttp.ClientSession, index: int, folder: str
) -> str:
    """Скачивает сгенерированное ИИ изображение лица с thispersondoesnotexist.com."""
    url = "https://thispersondoesnotexist.com"

    filename = os.path.join(folder, f"ai_face_{index}.jpg")

    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                with open(filename, "wb") as f:
                    f.write(content)
                print(f"Скачано изображение {index}. Размер: {len(content)} байт")
                return filename
            else:
                print(f"Ошибка при скачивании изображения {index}: {response.status}")
                return None
    except Exception as e:
        print(f"Исключение при скачивании изображения {index}: {e}")
        return None


async def main(count: int):
    artifacts_folder = "hw_5/artifacts"
    Path(artifacts_folder).mkdir(exist_ok=True)

    connector = aiohttp.TCPConnector(
        ssl=False,
        limit=5,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for i in range(1, count + 1):
            await asyncio.sleep(1.0)
            tasks.append(download_ai_face(session, i, artifacts_folder))

        downloaded_files = await asyncio.gather(*tasks)

        successful_downloads = [f for f in downloaded_files if f]
        print(f"\nСкачивание завершено!")
        print(f"Успешно скачано: {len(successful_downloads)} из {count} изображений")
        print(f"Файлы сохранены в папке: {os.path.abspath(artifacts_folder)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скачивание AI-сгенерированных лиц с thispersondoesnotexist.com"
    )
    parser.add_argument("count", type=int, help="Количество изображений для скачивания")
    args = parser.parse_args()

    if args.count <= 0:
        print("Количество изображений должно быть положительным числом!")
    else:
        asyncio.run(main(args.count))