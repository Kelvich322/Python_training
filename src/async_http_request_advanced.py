import asyncio
import json

import aiofiles
import aiohttp

semaphore = asyncio.Semaphore(5)


def gen_url(file_with_urls):
    with open(file_with_urls) as file:
        for url in file.read().splitlines():
            yield url.strip()


async def fetch_urls(file_with_urls: str, file_path: str):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30)
    ) as session:
        async with aiofiles.open(file_path, "w") as output_file:
            for url in gen_url(file_with_urls):
                result = await fetch_url(session, url)
                await output_file.write(json.dumps(result) + "\n")


async def fetch_url(session, url):
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        content = await response.text()
                        parsed_json = json.loads(content)
                        return {url: parsed_json}
                    except json.JSONDecodeError:
                        return {url: {"error": "Invalid JSON"}}
                else:
                    return {url: {"status": response.status}}
        except Exception as e:
            return {url: {"error": str(e)}}


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "./results.jsonl"))
