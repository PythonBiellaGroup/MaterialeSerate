import asyncio
import datetime

import httpx
import bs4
from colorama import Fore

# Older versions of python require calling loop.create_task() rather than on asyncio.
# Make this available more easily.
global loop


async def get_html(num_episodio: int) -> str:
    print(Fore.YELLOW + f"Ricerca HTML dell'episodio {num_episodio}", flush=True)

    url = f'https://talkpython.fm/{num_episodio}'

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        return resp.text


def get_titolo(html: str, num_episodio: int) -> str:
    print(Fore.CYAN + f"Ricerca TITOLO dell'episodio {num_episodio}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


async def get_range_titoli():
    
    tasks = []
    # Mantenere range piccolo per eviatare DDoS del sito
    for n in range(328, 338):
        tasks.append((n, loop.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        title = get_titolo(html, n)
        print(Fore.WHITE + f"Titolo trovato: {title}", flush=True)


def main():
    t0 = datetime.datetime.now()

    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_range_titoli())    
    
    dt = datetime.datetime.now() - t0
    print(f"Eseguito in {dt.total_seconds():.2f} sec.")


if __name__ == '__main__':
    main()
