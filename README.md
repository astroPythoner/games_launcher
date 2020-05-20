# Game launcher für pygame

# Ausführen
```
python3 main.py
```

# Notwendige Bibliotheken
- pygame

***

# Verwendung
![image not found](https://raw.githubusercontent.com/astroPythoner/games_launcher/master/joystickpins/tastaturbelegung.png)

Wähle ein Spiel uns starte es mit Enter auf einer Tastatur oder A auf einen Controller. Spiele die eine Tastatur als Controller unterstützten und meine joystickpins-Bibliothek verweden sind wie im Bild oben gemappt. Spiele können aber auch eine spezielle Tastatur oder Maus Unterstützung besitzten. Wähle die Ansicht im Launcher durch Klicken auf die Namen der Ansichten ganz oben oder durch linke und rechte Schulter auf einen Controller.

# Spiele erstellen/hinzufügen

Ein Spiel wird dann erkannt, wenn es im gleichen Ordner wie die main.py liegt und selber auch eine main.py besitzt. Beispielsweise könnte ein Spiel wie im folgenden Bild dargestellt aussehen:

![image not found](https://raw.githubusercontent.com/astroPythoner/games_launcher/master/example_game.png)

In dem Ordner EXAMPLE_GAME liegt das Spiel. Es entält:
- main.py ist die Hauptdatei. Mit ihr wird das Spiel gestartet. 
- Eine README.md wird auch im launcher angezeigt. 
- Das title_image.png ist das Bild, mit dem das Spiel im launcher dargestellt wird. Es sollte 1920x1280 Pixel groß sein.
- in info.json stehen weitere Attribute, die im launcher dargestellt werden. Das Format dieser Datei ist wie folgt:

```
{
  "name": "Name des Spiels",
  "description": "kurze Beschreibung des Spiels",
  "type": "Spielgattung",
  "author": "Entwickler",
  "players": "1 to 2", #Beispiel für ein bis 2 Spieler
  "playable with": ["Controller","Tastatur als Controller"] # Beispiel, wenn joystickpins verwendet wird
}
```

Die Spiele können auch zwei meiner Projekte verwenden: 
- Mein [joystickpins projekt](https://github.com/astroPythoner/joystickpins) Projekt für eine einfache Verwendung von Kontrollern und Tastaturen im Spiel.
- Mein [moving background](https://github.com/astroPythoner/pygame_background_animation) Projekt um schnell und einfach animierte Hintrgünde in Spielen zu erstellen.

Wenn du bisher noch nie pygame verwendet hast ist dieser Videokurs sehr hilfreich https://www.youtube.com/watch?v=VO8rTszcW4s&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw

Eine Dokumentation über pygame findest du hier https://www.pygame.org/docs/

# Beispielaussehen
![](https://raw.githubusercontent.com/astroPythoner/games_launcher/master/example_list_view.png)
![](https://raw.githubusercontent.com/astroPythoner/games_launcher/master/example_side_view.png)
![](https://raw.githubusercontent.com/astroPythoner/games_launcher/master/example_brick_view.png)
