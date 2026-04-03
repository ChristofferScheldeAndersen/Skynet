# Villager retask-segment — kort overblik

Denne version er lavet til hurtigt overblik over segmentets hoveddele.
Den er bevidst kort og fokuserer på formål, flow og afhængigheder.

## Hovedidé
Segmentet samler AI-logik for at:
- finde villagers der bør korrigeres eller omplaceres
- vælge en målressource
- prøve retask til den ressource
- fallbacke til andre ressourcer hvis det fejler
- sætte cooldowns når forsøg mislykkes
- håndtere enkelte recovery-/vill-hopping-situationer

## Segmentets hovedblokke

### 1. Retask-motoren
**Kerneområde:** den tidligere “indre” funktion for omplacering af én villager.

Formål:
- modtage en target-resource
- læse data om den valgte villager
- afgøre om retask skal fortsætte eller afbrydes
- finde passende lokale ankre og konkrete ressourcetargets
- udstede den faktiske ordre
- returnere status til caller-laget

Praktisk betydning:
- dette er den del der faktisk forsøger at flytte en konkret villager
- den afgør ikke selv i stort omfang *hvem* der skal flyttes eller *hvilken* fallback-rækkefølge der skal prøves

### 2. Candidate selection / cleanup
**Kerneområde:** caller-reglerne omkring retask-motoren.

Formål:
- finde villagers der ser fejlplacerede, fastlåste eller korrigerbare ud
- filtrere byggere, kampenheder og andre dårlige kandidater fra
- udvælge en kandidat og sende den ind i retask-motoren

Praktisk betydning:
- segmentet retasker ikke bare vilkårlige villagers
- det prøver først at finde villagers hvor en korrektion faktisk giver mening

### 3. Resource fallback-kæder
**Kerneområde:** reglerne omkring caller-return og alternative ressourceforsøg.

Formål:
- prøve en primær målressource først
- hvis det fejler, prøve andre ressourcer i en fast rækkefølge
- bruge forskellige fallback-kæder afhængigt af villagerens oprindelige rolle

Typisk mønster:
- food-lignende villager: prøv food, derefter andre eco-jobs
- wood-lignende villager: prøv wood først, derefter alternativer
- gold og stone har tilsvarende egne fallback-kæder

Praktisk betydning:
- AI’en “opgiver” ikke straks når første retask-forsøg fejler
- den prøver at genbruge villageren i en anden økonomisk rolle

### 4. Cooldown-logik
**Kerneområde:** reglerne efter mislykkede retask-forsøg.

Formål:
- sætte timere når bestemte typer retask-korrektioner fejler
- forhindre spam af de samme forsøg igen og igen

Praktisk betydning:
- stabiliserer workflowet
- reducerer overreaktion og unødigt gentagne retask-forsøg

### 5. Same-resource vs cross-resource retask
**Kerneidé:** motoren skelner mellem to typer korrektion.

**Cross-resource retask**
- villageren flyttes fra én ressourcekategori til en anden
- eksempel: food -> wood eller wood -> gold

**Same-resource retask**
- villageren bliver i samme overordnede ressourcekategori
- men bliver “rettet” til et bedre target eller en mere passende opgave inden for den kategori
- eksempel: food -> food eller wood -> wood med ny destination

Praktisk betydning:
- segmentet er ikke kun et jobskifte-system
- det er også et oprydningssystem inden for samme ressource

### 6. Food-normalisering
**Særlig detalje i logikken:** food behandles bredere end de andre ressourcer.

Food omfatter typisk flere jobtyper:
- farmer
- forager
- shepherd
- i visse dele også hunter/fisherman-lignende fødelogik

Praktisk betydning:
- food-retask er mere kompleks end wood/gold/stone
- AI’en prøver ofte at undgå unødvendig retask hvis villageren allerede er “food nok”

### 7. Wood / drop-site / vill-hopping recovery
**Udvidet blok:** den tilføjede gren omkring original Rule #3531–3572.

Formål:
- håndtere særlige recovery-situationer omkring villagers, drop-sites og nærliggende arbejdsområder
- især relevant når en tidligere lokal search eller unload-relateret gren ikke lykkes pænt

Praktisk betydning:
- fungerer som ekstra recovery-lag
- hjælper workflowet videre i tilfælde hvor den mere direkte gren ikke fandt en god løsning

## Eksterne inputs der stadig bruges
Disse læses i segmentet, men sættes ikke i segmentet selv:

### Goals
- `gl-wood-dropoff-support-count`

### Flags
- `fl-food-idle-farm-mode`
- `fl-wood-town-center-fallback-mode`
- `fl-opening-wood-priority`
- `fl-midgame-wood-support-a`
- `fl-midgame-wood-support-b`

### Timers
- `food-stay-put-timer`

Praktisk betydning:
- segmentet er meget tæt på at være selvstændigt
- men nogle globale inputs fra resten af AI’en påvirker stadig adfærden

## Hvad der stadig ikke er taget med
Den største bevidste udeladelse er grenen der starter ved original **Rule #9524**.

Den gren virker som:
- ressource-prioritering
- resource-ranking
- availability-/selection-logik

Praktisk betydning:
- den påvirker *hvilke* ressourcer der prioriteres
- men ikke direkte selve mekanikken for at retaske en konkret villager

## Den bedste måde at tænke segmentet på
Segmentet kan læses som tre lag:

1. **Udvælgelse**
   - find villagers der bør undersøges eller korrigeres

2. **Retask-motor**
   - prøv at sende den valgte villager til et passende target

3. **Fallback og recovery**
   - hvis første forsøg fejler, prøv andre ressourcer, vent lidt, eller brug recovery-grene

## En kort mental model
Hvis du vil forstå segmentet hurtigt, så læs det som:

- find en mulig problem-villager
- afgør hvad den ideelt burde lave
- prøv at sende den derhen
- hvis det ikke lykkes, prøv en anden ressource eller recovery-gren
- hvis intet virker, sæt cooldown og gå videre

## Anbefalet læserækkefølge
For overblik giver det bedst mening at læse i denne rækkefølge:

1. caller / candidate selection
2. retask-motoren
3. fallback-kæderne
4. cooldown-reglerne
5. 3531–3572 recovery-grenen
6. til sidst de eksterne input-afhængigheder
