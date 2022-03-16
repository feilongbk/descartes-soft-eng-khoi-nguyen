import aiohttp
import asyncio
import time

start_time = time.time()


async def main():
    result = list()
    async with aiohttp.ClientSession() as session:
        for number in range(1, 21):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                print(pokemon['name'])
                result.append(pokemon['name'])
    return result

result=asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
print(len(result))
print(result)