# Backgammon
## Stručný popis zadání:
Vytvořte implementaci hry vrhcáby, která podporuje hru dvou hráčů či hru proti jednoduché umělé inteligenci.

### Povinně implementovaná funkčnost:
- generování hodu kostkami
- výpis všech možných tahů hráče
- jednoduchá umělá inteligence, která náhodně volí jeden z platných tahů
- trasování chodu každého jednotlivého kamene (od vstupu z baru po vyhození/vyvedení), herní pole se chovají jako zásobník
- uložení a obnova stavu hry (s návrhem vlastního JSON formátu pro uložení)

### Co musí zobrazovat displej (výpis na standardním vstupu)
- výsledky hodů kostkami
- pozice všech kamenů na desce (včetně těch "na baru")
- stručný komentář toho, co se ve hře událo a nemusí být zřejmé ze zobrazení na desce (kámen vstoupil do hry, byl "vyhozen", opustil hru, hráč nemůže hrát tj. ani házet, pod.)
- počet vyvedených kamenů
- po výhře typ výhry
- po ukončení se zobrazí statistika o všech kamenech ve hře (zvlášť pro bílého a černého), například:
    - počet kamenů vyhozených, vyvedených a opuštěných
    - průměrná životnost kamene v tazích

### Nepovinná funkčnost:
- GUI rozhraní
- inteligentnější AI

## Implementované třídy:
- Hra (Herní deska)
- obsahuje:
- HerníPole (modifikovaný zásobník, lze vkládat jen kameny stejných barev)
- Dvojkostka (vrací seznam možných dvojic či čtveřic)
- Bar (továrna na herní kameny, s řízenou produkcí)
- Herní kámen (s pamětí, kde se postupně nacházel)
- Hráč:
    - odvozené třídy:
    - KonzolovýHráč
    - AIHráč

# Tento projekt
## Třídy
### Třídy game.py
- Keys
- Bar
- Home(Bar)
- Game
- Checker
- Point
- Player
- ConsolePlayer(Player)
- AIPlayer(Player)
### Třídy graphics.py
- Text
- Display
### Třídy dice.py
- Dice
- DoubleDice

## Návod
1. K úspěšnému spuštění hry potřebujete soubory: *main.py*, *game.py*, *graphics.py*, *filesystem.py*, *dice.py*, *verification.py*
2. Spustit *main.py*
3. Výběr grafického módu zadejte *1* nebo *2*
4. Hlavní menu
    1. Nová hra
        - Dále se vybere zda-li chcete hrát proti počítači nebo hru dvou hráčů.
        - Hrajete pomocí čísel a klávesy ENTER
        - Pro ukončení zadejte 0 a stiskněte ENTER
        - Pro zrušení tahu pouze ENTER
        - Hra se pokaždé uloží
    2. Načíst hru
        - Zobrazí se výběr dostupných savů
        - Spustí se hra
    3. O autorovi
        - Zobrazí se informace o autorovi
    4. Ukončit

## Nastavení
- Maximální počet savů lze nastavit prostřednictvím souboru config.ini ve stejné složce, pokud ve složce není, hru jste zatím nespustili, nebo soubor byl odstraněn