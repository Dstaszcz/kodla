import discord
import os
from discord.ext import commands
from pytube import Search
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Zalogowaliśmy się jako {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send(f'Cześć, jestem bot{bot.user}!')


@bot.command()
async def heh(ctx, count_heh=10):
    await ctx.send("he" * count_heh)


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def odejmowanie(ctx, left: int, right: int):
    """Odejmowanie two numbers together."""
    await ctx.send(left - right)


@bot.command()
async def pokaz(ctx):
    lista = os.listdir('memy')
    await ctx.send(lista)


@bot.command(name='play')
async def play(ctx, *, query: str):
    """Wyszukuje i uruchamia link do filmiku na YouTube."""
    try:
        # Wyszukiwanie filmiku na YouTube
        search = Search(query)
        video = search.results[0]  # Wybieramy pierwszy wynik
        video_url = f"https://www.youtube.com/watch?v={video.video_id}"

        await ctx.send(f"Znalazłem filmik: {video.title}\n{video_url}")
    except Exception as e:
        await ctx.send(f"Nie udało się znaleźć filmiku. Błąd: {e}")


@bot.command(name='rickroll')
async def rickroll(ctx, member: discord.Member):
    """Wysyła Rickroll w wiadomości prywatnej do wskazanego użytkownika."""
    try:
        # Link do "Never Gonna Give You Up"
        rickroll_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        # Wysyłanie wiadomości prywatnej
        await member.send(f"Cześć {member.name}! Mam coś dla Ciebie: {rickroll_url}")

        # Potwierdzenie w kanale tekstowym
        await ctx.send(f"Rickroll wysłany do {member.mention}!")
    except discord.Forbidden:
        await ctx.send(f"Nie mogę wysłać wiadomości do {member.mention}, ma wyłączone wiadomości prywatne.")
    except Exception as e:
        await ctx.send(f"Coś poszło nie tak: {e}")


@bot.command()
async def game(ctx, *, game_name):
    """
    Wyszukuje link do gry na podstawie podanej nazwy.
    """
    try:
        # Tworzenie zapytania do Google
        query = f"{game_name} site:github.com"
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        # Pobieranie wyników wyszukiwania
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Wyszukiwanie pierwszego linku
        search_results = soup.find_all("a")
        for link in search_results:
            href = link.get("href")
            if "url?q=" in href and "webcache" not in href:
                # Wyciąganie właściwego linku
                result = href.split("url?q=")[1].split("&")[0]
                await ctx.send(f'Link do kodu gry "{game_name}": {result}')
                return

        await ctx.send(f'Nie znaleziono wyników dla gry "{game_name}". Spróbuj innej nazwy.')
    except Exception as e:
        await ctx.send("Wystąpił błąd podczas wyszukiwania. Spróbuj ponownie.")
        print(e)


@bot.command()
async def mem(ctx, image_name: str):
    with open(f'memy/{image_name}.jpg', 'rb') as f:
        # Zapiszmy przekonwertowany plik biblioteki Discord w tej zmiennej!
        picture = discord.File(f)
    await ctx.send(file=picture)


bot.run()
