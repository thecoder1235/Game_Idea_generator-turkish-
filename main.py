import json
import random
import time
import sys
import winsound
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

console = Console()

# JSON dosyasını yükle
with open("game_ideas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def play_sound():
    """Küçük bir 'ding' sesi çalar."""
    try:
        winsound.Beep(388, 220)
        winsound.Beep(220, 200)
    except:
        pass  # Linux/Mac'te hata olmasın diye

def typewriter(text, delay=0.005):
    """Metni yazı yazılır gibi ekrana basar."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def generate_game_idea(mechanic_count, genre=None, theme=None, location=None, tone=None, perspective=None):
    genre = next((g for g in data["genres"] if g["name"].lower() == genre.lower()), None) if genre else random.choice(data["genres"])
    theme = next((t for t in data["themes"] if t["name"].lower() == theme.lower()), None) if theme else random.choice(data["themes"])
    location = next((l for l in data["mekanlar"] if l["name"].lower() == location.lower()), None) if location else random.choice(data["mekanlar"])
    tone = next((t for t in data["tones"] if t["name"].lower() == tone.lower()), None) if tone else random.choice(data["tones"])
    perspective = next((p for p in data["perspectives"] if p["name"].lower() == perspective.lower()), None) if perspective else random.choice(data["perspectives"])

    mechanics = random.sample(data["mechanics"], k=min(mechanic_count, len(data["mechanics"])))

    mechanics_text = "\n".join(
        [f"• {m['name']} ({m.get('description', 'Açıklama yok')})" for m in mechanics]
    )

    idea_text = f"""
[bold yellow]🎮 Oyun Fikri 🎮[/bold yellow]

[bold cyan]Tür:[/bold cyan] {genre['name']} ({genre.get('description', 'Açıklama yok')})
[bold cyan]Tema:[/bold cyan] {theme['name']} ({theme.get('description', 'Açıklama yok')})
[bold cyan]Mekan:[/bold cyan] {location['name']} ({location.get('description', 'Açıklama yok')})
[bold cyan]Ton:[/bold cyan] {tone['name']} ({tone.get('description', 'Açıklama yok')})
[bold cyan]Bakış Açısı:[/bold cyan] {perspective['name']} ({perspective.get('description', 'Açıklama yok')})

[bold magenta]Mekanikler:[/bold magenta]
{mechanics_text}
"""
    return idea_text

def main():
    console.print(Panel.fit("🎲 [bold green]Game Idea Maker'e Hoş Geldin![/bold green] 🎲", border_style="green"))

    while True:
        console.print("\n[bold cyan]Filtre seçmek ister misin?[/bold cyan] (Enter = Hayır, E = Evet)")
        filtre = Prompt.ask("Seçimin", default="").lower()

        if filtre == "e":
            console.print("\n[bold cyan]Tamam, filtreleri girelim! (Boş bırakırsan rastgele olur)[/bold cyan]")
            genre = Prompt.ask("Tür (genre)", default="")
            theme = Prompt.ask("Tema (theme)", default="")
            location = Prompt.ask("Mekan", default="")
            tone = Prompt.ask("Ton", default="")
            perspective = Prompt.ask("Bakış açısı", default="")
        else:
            genre = theme = location = tone = perspective = None
            console.print("\n🎲 [italic]Filtre yok — tamamen rastgele bir fikir oluşturulacak.[/italic]")

        mechanic_count = IntPrompt.ask("\nKaç mekanik istersin?", default=2)

        console.print("\n[bold green]✨ Fikir oluşturuluyor...[/bold green]")
        time.sleep(0.5)
        play_sound()  # 🔊 Ses efekti
        time.sleep(0.2)

        idea = generate_game_idea(mechanic_count, genre, theme, location, tone, perspective)
        # Use rich to render markup/colors instead of writing raw text to stdout
        console.print(Panel.fit(idea, border_style="magenta"), markup=True)
        # küçük ses/efekt için hafif gecikme
        play_sound()
        time.sleep(0.1)

        console.print(Panel.fit("💡 [bold cyan]Yeni fikir oluşturuldu![/bold cyan]", border_style="blue"))

        again = Prompt.ask("\nYeni bir oyun fikri üretmek ister misin? (E/H)", choices=["e", "h"], default="e").lower()
        if again == "h":
            console.print("\n[bold red]👋 Görüşürüz, yaratıcılıkla kal![/bold red]")
            play_sound()
            break

if __name__ == "__main__":
    main()
