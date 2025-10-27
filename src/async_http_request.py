import asyncio
import json

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]

semaphore = asyncio.Semaphore(5)


async def fetch_urls(urls: list[str], file_path: str):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = fetch_url(session, url)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

    await write_to_file(results, file_path)


async def fetch_url(session, url):
    async with semaphore:
        try:
            async with session.get(url) as response:
                return {"url": url, "status": response.status}
        except Exception as e:
            return {"url": url, "error": str(e)}


async def write_to_file(results, file_path):
    with open(file_path, "w") as file:
        for result in results:
            result = json.dumps(result)
            file.write(result + "\n")


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "./results.json"))
