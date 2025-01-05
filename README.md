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

<ins>**Soul Knight**</ins>

Soul Knight je roguelike strieľačka z pohľadu zhora, ktorá ponúka procedurálne generované levely a rôzne herné štýly. Z tejto hry Voidwalker čerpá:
- Procedurálne generované dungeony
- Systém rôznych nepriateľov s unikátnymi vzorcami útoku
- Progresiu cez jednotlivé úrovne

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

### **2.2 Základné mechaniky**
- **Bullet Time**: spomalenie času pre strategické rozhodovanie
- **Magický útok**: kruhový útok poškodzujúci okolných nepriateľov
- **Procedurálna generácia**: každý level je unikátny vďaka BSP algoritmu
- **A\* pathfinding**: implementácia hľadania najkratšej cesty pre nepriateľov
- **Variabilní nepriatelia**:
  - Stalker: prenasleduje hráča a útočí zblízka
  - Wizard: útočí na diaľku magickými projektilmi
  - Sharpshooter: strieľa presné projektily z väčšej vzdialenosti

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
- Ambiente zvuky dungeonov
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