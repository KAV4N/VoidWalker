# **Voidwalker - Game Design Document**

Na danom repozitári sa nachádza implementácia hry v Pygame, ktorá kombinuje prvky rychlej akcie s roguelike elementmi. Hra kladie dôraz na dynamický pohyb a taktické využitie schopností v procedurálne generovaných úrovniach.

**Autor**: Patrik Kavan

**Vybraná téma**: One level, but constantly changing

---
## **1. Úvod**
Voidwalker je akčná roguelike hra z pohľadu zhora, kde hráč ovláda mystického bojovníka prechádzajúceho procedurálne generovanými dungeonmi. Hra kombinuje rýchlu akciu štýlu Ghostrunner s roguelike mechanikami podobnými Soul Knight, vytvárajúc jedinečný herný zážitok.

### **1.1 Inšpirácia**
<ins>**Ghostrunner**</ins>

Ghostrunner je akčná hra zameraná na rýchly pohyb a precízne súboje, kde jedna chyba znamená smrť. Z tejto hry Voidwalker preberá:
- Rýchly a plynulý pohyb
- Bullet time mechaniku pre strategické rozhodovanie
- Dôraz na vyhýbanie sa nepriateľským útokom
<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/76118d7bb1e989a11daccd0d86e987d268e77ae4/media/ghostrunner.jpg" alt="Ghostrunner">
  <br>
  <em>Obrázok  1 Ukážka hry Ghostrunner</em>
</p>

<ins>**Soul Knight**</ins>

Soul Knight je roguelike strieľačka z pohľadu zhora, ktorá ponúka procedurálne generované levely a rôzne herné štýly. Z tejto hry Voidwalker čerpá:
- Procedurálne generované dungeony
- Systém rôznych nepriateľov s unikátnymi vzorcami útoku
- Progresiu cez jednotlivé úrovne
<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/76118d7bb1e989a11daccd0d86e987d268e77ae4/media/soulknight.jpg" alt="Soul Knight">
  <br>
  <em>Obrázok 2 Ukážka hry Soul Knight</em>
</p>


### **1.2 Herný zážitok**
Cieľom hry je, aby hráč prežil a postupoval cez generované dungeony, pričom musí čeliť rôznym typom nepriateľov. Kľúčovými prvkami sú:
- Rýchly a plynulý pohyb po mape
- Strategické využívanie bullet time schopnosti
- Vyhýbanie sa nepriateľským projektilov
- Efektívne využívanie útočných schopností

### **1.3 Vývojový softvér**
- **PyCharm**: vývojové prostredie
- **Audacity**: úprava zvukových efektov

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč ovláda Voidwalkera, mystickú bytosť s schopnosťou manipulovať s časom. Postupuje cez procedurálne generované dungeony, bojuje s nepriateľmi a snaží sa dostať čo najhlbšie do podzemia.

<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/f5c20e67b09e3db9c9e74df2408622fb7a37654e/media/gameplay_example.gif" alt="VoidWalker">
  <br>
  <em>Obrázok 3 Ukážka hry VoidWalker</em>
</p>

### **2.2 Základné mechaniky**
- **Bullet Time**: spomalenie času pre strategické rozhodovanie
- **Magický útok**: kruhový útok poškodzujúci okolných nepriateľov
- **Procedurálna generácia**: každý level je unikátny vďaka BSP algoritmu
- **A\* pathfinding**: implementácia hľadania najkratšej cesty pre nepriateľov
- **Variabilní nepriatelia**:
<br>
<br>

**Stalker**: prenasleduje hráča a útočí zblízka
- životy: nesmrtelný
- poškodenie: 5
- útok: každú sekundu
<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/76118d7bb1e989a11daccd0d86e987d268e77ae4/media/stalker.png" alt="Stalker">
  <br>
  <em>Obrázok 4 Stalker</em>
</p>
<br>

**Wizard**: útočí na diaľku magickými projektilmi, ktoré hádže veľkou rýchlosťou na hráča
- životy: 1
- poškodenie: 1 (zásah projektilu)
- útok: každú 0.5 sekundu
<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/76118d7bb1e989a11daccd0d86e987d268e77ae4/media/wizard.png" alt="Wizard">
  <br>
  <em>Obrázok 5 Wizard</em>
</p>
<br>

**Sharpshooter**: jeho rýchlosť streľby je pomalá, ale strieľa presné a rýchle projektily z väčšej vzdialenosti
- životy: 1
- poškodenie: 1 (zásah projektilu)
- útok: každých 5.0 sekúnd
<p align="center">
  <img src="https://github.com/KAV4N/VoidWalker/blob/76118d7bb1e989a11daccd0d86e987d268e77ae4/media/sharpshooter.png" alt="Sharpshooter">
  <br>
  <em>Obrázok 6 Sharpshooter</em>
</p>


### **2.3 Návrh tried**
- **Game**: hlavná herná logika a správa herných stavov
- **Player**: ovládanie hráča, pohyb a schopnosti
- **DungeonGenerator**: generovanie levelov pomocou BSP
- **Camera**: sledovanie hráča a správa zobrazenia
- **Enemies**: hierarchia nepriateľských jednotiek
- **Weapons**: systém zbraní a projektily

---
## **3. Grafika**

### **3.1 Vizuálny štýl**
Hra využíva minimalistický pixel art štýl s dôrazom na čitateľnosť:
- Tmavé pozadie pre atmosféru dungeonov
- Jasné efekty pre zvýraznenie akcií
- Farebné rozlíšenie nepriateľov
- Vizuálna spätná väzba pri používaní schopností

### **3.2 Animácie**
- Plynulé animácie pohybu postáv
- Vizuálne efekty pre bullet time
- Časticové efekty pre útoky a zranenia
- Animované projektily

---
## **4. Zvuk**

### **4.1 Hudba**
- Atmosférická hudba v menu
- Dynamická hudba počas hrania
- Špeciálne hudobné efekty počas bullet time

### **4.2 Zvukové efekty**
- Zvuky útokov a zbraní
- Ambientné zvuky dungeonov
- Zvukové signály pre bullet time
- Zvuky zranenia a smrti

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
- Zdravie zobrazené pomocou sŕdc
- Indikátor nabíjania útoku
- Ukazovateľ bullet time
- Minimalistické menu

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **WASD/Šípky**: pohyb postavy
- **Space**: útok
- **Left Shift**: aktivácia bullet time
- **Escape**: menu/ukončenie

<ins>**Myš**</ins>
- Určuje priblíženie kamery