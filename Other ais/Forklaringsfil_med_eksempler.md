# Gennemgang af villager-retask-segmentet — version 2

Denne version bygger videre på den tidligere gennemgang, men tilføjer for hvert undersegment en lille boks med:

- **Input**: hvad blokken tager ind
- **Beslutning**: hvad blokken afgør
- **Output**: hvad blokken efterlader til næste blok

Målet er, at du kan læse hvert undersegment som en lille selvstændig enhed.

## Hvad segmentet samlet gør

Segmentet består af to hoveddele:

1. **Den delte retask-motor** (`Rule #3408` til `Rule #3572`), som prøver at omplacere **én konkret villager** til en ønsket ressource.
2. **Caller- og oprydningslaget** (`Rule #9407` til `Rule #9503`), som vælger kandidater, kalder motoren, håndterer fejl, prøver fallback-rækkefølger mellem ressourcer og opdaterer resource-availability-flags.

---

# Kendte eksterne inputs som ikke sættes i segmentet

Disse variable/flags/timere bliver **læst**, men ikke **sat** i dette segment. Når de nævnes under de enkelte undersegmenter, er det disse der refereres til.

## Goals
- `gl-wood-dropoff-support-count`

## Flags
- `fl-food-idle-farm-mode`
- `fl-wood-town-center-fallback-mode`  
  (samme flag-slot bruges under to navne i filen)
- `fl-opening-wood-priority`
- `fl-midgame-wood-support-a`
- `fl-midgame-wood-support-b`
- `fl-retask-workflow-handoff`

## Timere
- `food-stay-put-timer`

---

# Del A — Den delte retask-motor (`Rule #3408`–`Rule #3572`)

Denne del er den egentlige “funktion”, som andre regler kalder, når de vil prøve at flytte en bestemt villager til en bestemt ressource.

## A1. Indgang, tidlige aborter og grundinitialisering (`Rule #3408`–`Rule #3415`)

### Regler
- `Rule #3408`
- `Rule #3409`
- `Rule #3410`–`Rule #3413`
- `Rule #3414`
- `Rule #3415`

### Formål
Denne blok gør tre ting:

1. **Stopper tidligt**, hvis kaldet ikke bør køres.
2. **Sætter standardværdier** for den ressource der forsøges retasket til.
3. **Indlæser al nødvendig state** om den valgte villager.

### Input → beslutning → output
> **Input**  
> - target-ressource (`gl-target-resource`)  
> - valgt villager-id  
> - global food-/wood-mode  
> - `gl-wood-dropoff-support-count`
>
> **Beslutning**  
> - skal kaldet aborteres straks?  
> - skal wood behandles som en mere begrænset/fallback-præget ressource?  
> - hvilke basisværdier skal bruges for den valgte target-ressource?  
> - er source-villagerens tag overhovedet gyldigt for motoren?
>
> **Output**  
> - initialiserede tærskler og balanceværdier  
> - indlæst villager-state  
> - enten fortsættelse til næste blok eller tidlig retur

### Hvad der konkret besluttes
- `Rule #3408` afbryder straks, hvis food-retask er blokeret af den aktuelle idle-farm-situation, eller hvis villager-id'et er ugyldigt.
- `Rule #3409` markerer wood-retask som mere begrænset, hvis AI'en mangler normalt wood-dropoff-support.
- `Rule #3410`–`#3413` sætter en startvægt for ressource-balance afhængigt af om målet er food, wood, stone eller gold.
- `Rule #3414` læser den konkrete villagers nuværende rolle, gather-type, tag, position og move-target.
- `Rule #3415` stopper flowet, hvis villagerens tag ikke er et tag denne motor må håndtere.

### Hvorfor det er vigtigt for resten
Hele resten af motoren antager, at disse ting allerede er kendt:
- hvad target-ressourcen er
- hvem source-villageren er
- hvad den laver nu
- hvilke grænser der skal bruges i sammenligningerne

Hvis denne blok aborterer, bliver selve retask-søgningen aldrig forsøgt.

### Eksterne inputs brugt her
- `fl-food-idle-farm-mode`
- `gl-wood-dropoff-support-count`

---

## A2. Normalisering af nuværende rolle og same-resource-abort (`Rule #3416`–`Rule #3423`)

### Regler
- `Rule #3416`
- `Rule #3417`
- `Rule #3418`
- `Rule #3419`–`Rule #3422`
- `Rule #3423`

### Formål
Denne blok afgør, om villageren **allerede i praksis arbejder tæt nok på den ønskede ressource**, så man ikke bør flytte den.

### Input → beslutning → output
> **Input**  
> - villagerens nuværende rolle, gather-type og position  
> - target-ressource  
> - `food-stay-put-timer`
>
> **Beslutning**  
> - skal food-roller have ekstra tolerance for at blive stående?  
> - hvilken bred ressourcefamilie tilhører villageren i praksis?  
> - er dette et same-resource-tilfælde der bør afbrydes?
>
> **Output**  
> - normaliseret “aktuel ressourcefamilie”  
> - opdateret stay-put-tolerance  
> - enten abort eller fortsættelse

### Hvad der konkret besluttes
- `Rule #3416`–`#3418` udvider “bliv hvor du er”-tolerancen for bestemte food-roller.
- `Rule #3419`–`#3422` oversætter konkrete villager-roller til de brede ressourcefamilier:
  - farmer / forager / shepherd → `food`
  - lumberjack → `wood`
  - stone miner → `stone`
  - gold miner → `gold`
- `Rule #3423` stopper retask-forsøget, hvis source-villageren allerede matcher målressourcen og er tæt nok på sin nuværende situation.

### Hvorfor det er vigtigt for resten
Denne blok er grunden til, at motoren ikke bare aggressivt flytter villagers hele tiden. Den fungerer som en **same-resource-beskyttelse**.

### Eksterne inputs brugt her
- `food-stay-put-timer`

---

## A3. Retagging og valg af lokal søgeradius (`Rule #3424`–`Rule #3430`)

### Regler
- `Rule #3424`
- `Rule #3425`–`Rule #3429`
- `Rule #3430`

### Formål
Denne blok forbereder den lokale søgning efter et godt arbejdsanker ved at:
- sætte villageren ind i søgestaten
- sørge for at dens work-group-tag kan genopbygges korrekt
- beregne første lokale søgeradius

### Input → beslutning → output
> **Input**  
> - valgt source-villager  
> - nuværende tag/group-state  
> - position og move-target
>
> **Beslutning**  
> - hvordan skal villageren re-tagges eller klargøres til senere group-oprydning?  
> - hvor bred skal første lokale søgning være?
>
> **Output**  
> - seedet lokal søgestate  
> - klargjort work-group-state  
> - beregnet lokal radius til anker-søgning

### Hvad der konkret besluttes
- `Rule #3424` seed'er søgestaten med den villager der skal behandles.
- `Rule #3425`–`#3429` håndterer work-group-oprydning/genopbygning, så villageren senere kan placeres i den rigtige bucket.
- `Rule #3430` beregner hvor bredt den første lokale søgning efter ankre skal være.

### Hvorfor det er vigtigt for resten
Hvis AI'en skal vælge et godt nyt arbejdssted, skal den først definere **hvilket område omkring villageren** der er relevant.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i denne blok.

---

## A4. Valg af lokale ankre efter ressource (`Rule #3431`–`Rule #3438`)

### Regler
- `Rule #3431`
- `Rule #3432`
- `Rule #3433`
- `Rule #3434`
- `Rule #3435`
- `Rule #3436`
- `Rule #3437`
- `Rule #3438`

### Formål
Denne blok vælger **hvilken slags lokale ankre** der giver mening at søge omkring.

### Input → beslutning → output
> **Input**  
> - target-ressource  
> - lokal radius  
> - wood-support-state og globale wood-modifiers
>
> **Beslutning**  
> - skal der søges omkring mining dropoffs, lumber camps, farms, TC eller mills?  
> - skal wood bruge normal eller fallback-geografi?  
> - skal food bruge farms først eller hoppe direkte til bredere ankre?
>
> **Output**  
> - en lokal liste af mulige ankre  
> - eventuelt justeret task-tolerance  
> - en valgt geometrisk ramme for næste blok

### Hvad der konkret besluttes
- `Rule #3432` søger town center / mining-dropoff-ankre til stone og gold.
- `Rule #3433` tillader town center som wood-fallback-anker, hvis normalt wood-support mangler.
- `Rule #3434` søger normale lumber-camp-ankre til wood.
- `Rule #3435` søger farms først for food.
- `Rule #3436` kan springe den brede food-ankersøgning over, hvis food-situationen kræver en alternativ gren.
- `Rule #3437` søger town center og mill som food-ankre.
- `Rule #3438` gør task-overbelastning mere tolerant i bestemte økonomiske situationer.

### Hvorfor det er vigtigt for resten
Denne blok afgør **hvilken geografi motoren bruger**.

### Eksterne inputs brugt her
- `gl-wood-dropoff-support-count`
- `fl-wood-town-center-fallback-mode`
- `fl-opening-wood-priority`
- `fl-midgame-wood-support-a`
- `fl-midgame-wood-support-b`

---

## A5. Lokal anker-scoring og valg af bedste anker (`Rule #3439`–`Rule #3473`)

### Regler
- `Rule #3439`–`Rule #3440`
- `Rule #3441`–`Rule #3473`

### Formål
Denne store blok gennemgår de fundne lokale ankre én for én og prøver at vælge **det bedste anker** at søge videre omkring.

### Input → beslutning → output
> **Input**  
> - lokal ankerliste fra A4  
> - source-villagerens position og state  
> - crowding/task-data for hvert anker
>
> **Beslutning**  
> - hvilket anker scorer bedst samlet set?  
> - skal søgningen recenteres omkring en bestemt kandidat?  
> - er ingen af de fundne ankre gode nok?
>
> **Output**  
> - bedste anker gemt i state  
> - recenteret søgeområde  
> - eller signal om at næste blok må forsøge bredere fallback

### Hvad der konkret besluttes
Blokken gør i praksis dette:
1. rydder og sorterer den lokale ankerliste
2. itererer gennem hvert muligt anker
3. læser data om hvert anker
4. scorer det ud fra ting som:
   - afstand til villageren
   - crowding / task-belastning
   - antal tilknyttede resource targets
   - nærhed til relevante ressourceobjekter
   - balance-prioritet mellem ressourcer
5. gemmer det bedste anker fundet indtil videre
6. recenterer søgningen omkring den valgte kandidat

### Hvorfor det er vigtigt for resten
Det er her motoren går fra “der er nogle mulige arbejdsområder” til “**dette** er det mest lovende område at søge ressourcer i”.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs er centrale her.

---

## A6. Hurtig resource-søgning omkring valgt anker (`Rule #3474`–`Rule #3489`)

### Regler
- `Rule #3474`–`Rule #3475`
- `Rule #3476`–`Rule #3484`
- `Rule #3485`–`Rule #3489`

### Formål
Denne blok prøver først en **relativt lokal og hurtig søgning** efter brugbare resource-targets omkring det valgte anker.

### Input → beslutning → output
> **Input**  
> - valgt anker fra A5  
> - target-ressource  
> - lokale crowding-/pathing-filtre
>
> **Beslutning**  
> - findes der hurtigt et godt resource-target tæt på ankeret?  
> - skal søgningen udvides en smule?  
> - skal kandidater fjernes pga. task-belastning eller dårlig pathing?
>
> **Output**  
> - en første filtreret resource-liste  
> - eller signal om at sidste brede søgning er nødvendig

### Hvad der konkret besluttes
- `Rule #3474` snapshotter den første søgestate.
- `Rule #3475` springer videre, hvis den hurtige nærsøgning allerede gav gode kandidater.
- `Rule #3476` gør søgningen lidt bredere.
- `Rule #3477`–`#3480` søger ressourceobjekter afhængigt af target-ressourcen.
- `Rule #3481`–`#3483` filtrerer listen på, hvor travle objekterne er.
- `Rule #3485`–`#3488` laver lokale probe-punkter og buildability/pathing checks for at fjerne dårlige mål.
- `Rule #3489` går videre, hvis der stadig er gyldige targets tilbage.

### Hvorfor det er vigtigt for resten
Denne blok er “find hurtigt noget godt i nærheden”. Hvis den lykkes, undgår man bredere og dyrere fallback-søgninger.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i denne blok.

---

## A7. Sidste brede resource-søgning før dispatch (`Rule #3490`–`Rule #3497`)

### Regler
- `Rule #3490`–`Rule #3494`
- `Rule #3495`
- `Rule #3496`
- `Rule #3497`

### Formål
Hvis de tidligere passes ikke fandt noget robust mål, laver denne blok en **bredere sidste søgning**, og hvis det lykkes, sendes villageren afsted.

### Input → beslutning → output
> **Input**  
> - target-ressource  
> - valgt anker / recenteret søgeområde  
> - resultatet af hurtigsøgningen
>
> **Beslutning**  
> - skal filtrene løsnes yderligere?  
> - findes der nu et gyldigt endeligt target?  
> - skal hele retasken fejle hårdt?
>
> **Output**  
> - konkret dispatch-ordre til villageren  
> - eller endelig failure-status

### Hvad der konkret besluttes
- `Rule #3490`–`#3493` kører en sidste brede søgning for den relevante ressource.
- `Rule #3494` løsner filteret en sidste gang.
- `Rule #3495` snapshotter den endelige kandidatliste.
- `Rule #3496` aborterer med hård fejl, hvis intet mål findes.
- `Rule #3497` vælger et endeligt target, sender villageren derhen og rydder dens gamle work-tag.

### Hvorfor det er vigtigt for resten
Det er her selve retasken faktisk bliver til en konkret **ordre**.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i denne blok.

---

## A8. Succesretur og strukturbaseret fallback (`Rule #3498`–`Rule #3517`)

### Regler
- `Rule #3498`–`Rule #3502`
- `Rule #3503`–`Rule #3512`
- `Rule #3513`–`Rule #3517`

### Formål
Denne blok håndterer to ting:
1. normal retur efter succesfuld dispatch
2. en ekstra strukturbaseret fallback, hvis den normale rute ikke fandt et godt resource-target

### Input → beslutning → output
> **Input**  
> - resultatet af dispatch-forsøget  
> - group-state  
> - wood-support / fallback-tilstand
>
> **Beslutning**  
> - kan motoren returnere med succes med det samme?  
> - skal der prøves en ekstra strukturbaseret fallback?  
> - kan et fallback-anker give et sidste brugbart target?
>
> **Output**  
> - succesretur til caller  
> - eller dispatch via fallback-struktur  
> - eller videre mod failure/recovery

### Hvad der konkret besluttes
- `Rule #3498`–`#3502` genskaber group-state efter normal succes og returnerer.
- `Rule #3503`–`#3504` afgør om structure-fallback overhovedet giver mening.
- `Rule #3505`–`#3511` laver en resource-søgning omkring et valgt fallback-anker.
- `Rule #3512` sender villageren afsted via denne fallback-rute.
- `Rule #3513`–`#3517` genskaber grupper og returnerer efter fallback-succes.

### Hvorfor det er vigtigt for resten
Dette er motorens “anden chance”, når normal anker- og målvalg ikke er nok.

### Eksterne inputs brugt her
- `gl-wood-dropoff-support-count`
- indirekte samme wood-fallback-mode som tidligere, fordi wood-support bestemmer om fallback-grenen aktiveres

---

## A9. Endelig failure og unload-support-grenen (`Rule #3518`–`Rule #3526`)

### Regler
- `Rule #3518`
- `Rule #3519`
- `Rule #3520`–`Rule #3526`

### Formål
Denne blok sætter endelig fejlstatus og forsøger derefter en særskilt **unload-support-oprydning**, hvis workflowet er i den rigtige globale tilstand.

### Input → beslutning → output
> **Input**  
> - mislykket retask  
> - intern return/failure-state  
> - TC/garrison-situation
>
> **Beslutning**  
> - skal motoren bare returnere med failure?  
> - eller skal den først forsøge unload-support omkring TC/garrison?
>
> **Output**  
> - failure-status  
> - eller overgang til unload-support-grenen

### Hvad der konkret besluttes
- `Rule #3518` sætter den endelige failure code for mislykket retask.
- `Rule #3519` afgør om unload-support-grenen er aktiv for dette flow.
- `Rule #3520`–`#3526` finder TC'er med garrisoned villagers og bruger timerstyring til at forsøge unload-support eller forberede den.

### Hvorfor det er vigtigt for resten
Retask-motoren slutter altså ikke bare med “mislykkedes”. Den kan først prøve en lille TC/garrison-oprydning.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs fra listen bruges her direkte; grenen afhænger mest af intern state og SN 82-style kontrollogik.

---

## A10. Vill-hopping recovery-grenen (`Rule #3531`–`Rule #3572`)

### Regler
- `Rule #3531`–`Rule #3534`
- `Rule #3535`–`Rule #3544`
- `Rule #3545`–`Rule #3560`
- `Rule #3561`–`Rule #3572`

### Formål
Denne gren er en særskilt recovery-rutine, som forsøger at redde villagers ud af en dårlig lokal arbejds- eller TC-situation, især når almindelig retask og unload-support ikke har været nok.

### Input → beslutning → output
> **Input**  
> - source-town-center / gather-point-state  
> - nearby villagers  
> - garrison-/crowding-situation
>
> **Beslutning**  
> - er der nok pres eller fastlåsning til at recovery-grenen skal bruges?  
> - hvilken villager er den bedste kandidat til at blive “hoppet” videre?  
> - hvilket nyt mål eller gather-point hjælper bedst?
>
> **Output**  
> - en rescue-/redirect-ordre til en kandidatvillager  
> - eller retur uden ændring hvis recovery ikke giver mening

### Hvad der konkret besluttes
Blokken gør i praksis dette:
1. måler presset omkring et source-town-center og nærliggende food-style workers
2. afgør om der er grund til en “vill-hopping rescue”
3. tæller og filtrerer nearby workers
4. vælger en passende kandidat
5. finder et nyt mål / gather point / arbejdsretning
6. giver kandidaten en ordre der hjælper den videre ud af den dårlige situation
7. returnerer til caller

### Hvorfor det er vigtigt for resten
Denne gren er ikke den normale retask-rute. Den er snarere et **redningsspor**, når villagers er fastlåst, garrison-relaterede, dårligt placerede eller på anden måde ikke løses af den normale motor.

### Eksterne inputs brugt her
Ingen af de tidligere fundne eksterne inputs er tydeligt centrale her; grenen bruger primært lokal search-state og interne mål-goals.

---

# Del B — Caller- og oprydningslaget (`Rule #9407`–`Rule #9503`)

Denne del vælger hvilke villagers der skal sendes ind i motoren, hvilke ressourcer der skal prøves, hvilke fallback-forsøg der skal laves, og hvornår systemet sætter cooldowns.

## B1. Første cleanup-pass: tag vs. faktisk arbejde (`Rule #9407`–`Rule #9426`)

### Regler
- `Rule #9407`–`Rule #9421`
- `Rule #9422`
- `Rule #9423`–`Rule #9426`

### Formål
Denne blok leder efter villagers, hvor **tagget ressource** og **faktisk udført arbejde** ikke matcher. Derefter forsøger den at rette dem ved at kalde den delte retask-motor.

### Input → beslutning → output
> **Input**  
> - en bred villagerkandidatliste  
> - villager-tags  
> - faktisk gather-type / rolle
>
> **Beslutning**  
> - er der mismatch mellem tag og faktisk arbejde?  
> - skal denne kandidat springes over eller sendes til motoren?  
> - skal der sættes cooldown hvis forsøget mislykkes?
>
> **Output**  
> - retask-kald med tagget ressource som mål  
> - eller skip til næste kandidat  
> - eventuelt cleanup-cooldown

### Hvad der konkret besluttes
- bygger en kandidatliste af villagers med mistænkt mismatch
- normaliserer deres nuværende rolle/gather-type
- springer over kandidater der allerede ser korrekte ud
- kalder retask-motoren med villagerens tag som ønsket målressource
- sætter cooldown hvis forsøget fejler
- går videre til næste kandidat hvis forsøget lykkes eller hvis kandidaten springes over

### Hvorfor det er vigtigt for resten
Det er det første “oprydningslag”, som prøver at rette simple fejl mellem AI'ens klassificering af en villager og hvad villageren faktisk laver.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs er særligt afgørende i denne blok.

---

## B2. Andet cleanup-pass: aktive gatherers med mærkelig bevægelse (`Rule #9427`–`Rule #9440`)

### Regler
- `Rule #9427`–`Rule #9436`
- `Rule #9437`
- `Rule #9438`–`Rule #9440`

### Formål
Denne blok leder efter villagers som **formelt arbejder**, men hvis aktuelle move-target, afstand og gather-type tyder på at de alligevel er i en dårlig eller inkonsistent tilstand.

### Input → beslutning → output
> **Input**  
> - aktive gatherers  
> - move-target, afstand og gather-type  
> - thresholds for “for langt væk”
>
> **Beslutning**  
> - ser kandidaten fastlåst, ineffektiv eller inkonsistent ud?  
> - skal retask-motoren kaldes med justerede thresholds?  
> - skal der sættes separat cooldown ved fejl?
>
> **Output**  
> - retask-kald for suspekt aktiv gatherer  
> - eller skip  
> - eventuel second-cleanup-cooldown

### Hvad der konkret besluttes
- bygger en kandidatliste af aktive gatherers med suspekt target-/distance-adfærd
- tilpasser thresholds efter gather-type
- springer over villagers der stadig er tæt nok på et fornuftigt mål
- kalder retask-motoren med tunede thresholds
- sætter separat cooldown, hvis denne type oprydning fejler

### Hvorfor det er vigtigt for resten
Første cleanup-pass fanger “forkert mærkede” villagers. Denne anden pass fanger i stedet **villagers der stadig ser aktive ud, men i praksis er dårligt placeret**.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs er centrale her.

---

## B3. Bred fallback-kandidatudvælgelse (`Rule #9441`–`Rule #9464`)

### Regler
- `Rule #9441`–`Rule #9448`
- `Rule #9449`–`Rule #9456`
- `Rule #9457`–`Rule #9464`

### Formål
Denne blok forbereder en bredere sweep, hvor villagers der ikke blev løst i cleanup-passene, prøves gennem en fallback-kæde mellem ressourcer.

### Input → beslutning → output
> **Input**  
> - resterende candidates efter cleanup  
> - deres nuværende target og rolle  
> - farm/dropoff-relateret kontekst
>
> **Beslutning**  
> - er kandidaten stadig legitim dér hvor den er?  
> - hvilken ressourcefamilie hører den egentlig til?  
> - hvilken fallback-kæde skal den sendes ind i?
>
> **Output**  
> - kandidat routed til food-, wood-, gold- eller stone-kæden  
> - eller springes over hvis den stadig ser legitim ud

### Hvad der konkret besluttes
- bygger først en bred kandidatliste
- fjerner villagers der allerede er tæt nok på deres nuværende mål
- fryser resten i en gruppe for fallback-sweepet
- vælger kandidat for kandidat
- udleder hvilken ressourcefamilie kandidaten “egentlig” hører til
- tjekker om kandidatens nuværende target ser legitimt ud, især omkring farms og dropoff-strukturer
- ruter kandidaten ind i den passende fallback-kæde (food, wood, gold eller stone)

### Hvorfor det er vigtigt for resten
Det er overgangsblokken mellem “oprydning” og “nu prøver vi systematisk alternative ressourcer”.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs er centrale her.

---

## B4. Food-fallback-kæden (`Rule #9465`–`Rule #9471`)

### Regler
- `Rule #9465`
- `Rule #9466`
- `Rule #9467`
- `Rule #9468`
- `Rule #9469`
- `Rule #9470`
- `Rule #9471`

### Formål
Når en kandidat klassificeres som food-family, prøver denne kæde en prioriteret række af målressourcer.

### Input → beslutning → output
> **Input**  
> - én kandidat i food-familien  
> - resultatstatus fra hver retask-prøve  
> - carry-/skip-logik mellem forsøg
>
> **Beslutning**  
> - kan kandidaten blive på food?  
> - hvis ikke, skal wood, gold eller stone prøves i stedet?  
> - hvornår skal kæden opgive og gå til fælles failure?
>
> **Output**  
> - succes via én af ressourcegrenene  
> - eller broad-fallback-failure

### Fallback-rækkefølge
1. food
2. wood (primær wood-mode)
3. wood (alternativ wood-mode)
4. gold
5. stone
6. fælles failure-håndtering

### Hvorfor den findes
Food-workers er de mest sammensatte, fordi food kan komme fra flere arbejdsformer. Derfor prøver kæden først at holde villageren i food, men har en fuld fallback-række hvis det ikke lykkes.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i selve kæden.

---

## B5. Wood-fallback-kæden (`Rule #9472`–`Rule #9479`)

### Regler
- `Rule #9472`
- `Rule #9473`
- `Rule #9474`
- `Rule #9475`
- `Rule #9476`
- `Rule #9477`
- `Rule #9478`
- `Rule #9479`

### Formål
Samme idé som food-kæden, men for wood-family villagers.

### Input → beslutning → output
> **Input**  
> - én kandidat i wood-familien  
> - resultatstatus fra hvert wood-/gold-/stone-/food-forsøg
>
> **Beslutning**  
> - kan kandidaten forblive i wood-familien?  
> - skal der prøves alternativ wood-mode?  
> - hvis wood ikke virker, hvilken ressource er næste bedste fallback?
>
> **Output**  
> - succes via en af fallback-prøverne  
> - eller broad-fallback-failure

### Fallback-rækkefølge
1. wood (primær wood-mode)
2. wood (alternativ wood-mode)
3. gold
4. stone
5. food
6. fælles failure-håndtering

### Hvorfor den findes
Wood-workers har ofte mere entydig rolle end food-workers, så kæden starter hårdt med wood, men har stadig flere alternativer hvis wood ikke virker.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i selve kæden.

---

## B6. Gold- og stone-fallback-kæderne (`Rule #9480`–`Rule #9495`)

### Regler
- `Rule #9480`–`Rule #9487` (gold-family)
- `Rule #9488`–`Rule #9495` (stone-family + fælles broad-fallback-failure)

### Formål
Disse to kæder gør det samme som de tidligere kæder, bare for gold- og stone-family villagers.

### Input → beslutning → output
> **Input**  
> - én kandidat i gold- eller stone-familien  
> - resultatstatus fra hvert fallback-forsøg
>
> **Beslutning**  
> - kan kandidaten blive i sin primære familie?  
> - hvis ikke, hvilke alternative ressourcer skal prøves i hvilken rækkefølge?  
> - hvornår skal hele broad fallback erklæres mislykket?
>
> **Output**  
> - succes via gold/stone/wood/food  
> - eller fælles failure-path

### Gold-rækkefølge
1. gold
2. wood (primær)
3. wood (alternativ)
4. stone
5. food
6. shared failure

### Stone-rækkefølge
1. stone
2. gold
3. wood (primær)
4. wood (alternativ)
5. food
6. shared failure

### Hvorfor de findes
Caller-laget forsøger systematisk at **genbruge en villager i anden økonomi**, hvis dens oprindelige ressource ikke giver et brugbart target lige nu.

### Eksterne inputs brugt her
Ingen af de kendte eksterne inputs bruges direkte i selve kæderne.

---

## B7. Broad-fallback-cooldown og resource-availability-opdatering (`Rule #9495`–`Rule #9503`)

### Regler
- `Rule #9495`
- `Rule #9496`
- `Rule #9497`
- `Rule #9498`
- `Rule #9499`
- `Rule #9500`
- `Rule #9501`
- `Rule #9502`
- `Rule #9503`

### Formål
Denne blok afslutter broad-fallback-sweepet ved at:
- sætte cooldown når hele fallback-kæden mislykkes
- bruge et forsøg og gå videre til næste kandidat
- opdatere globale resource-availability-flags
- og til sidst eventuelt håndtere global handoff til en endnu ikke inkluderet gren

### Input → beslutning → output
> **Input**  
> - samlet resultat af broad fallback  
> - kandidatbudget / loop-state  
> - resource-availability-flags  
> - `fl-retask-workflow-handoff`
>
> **Beslutning**  
> - skal der sættes broad-fallback-cooldown?  
> - skal næste kandidat prøves?  
> - hvilke resource-availability-flags skal opdateres?  
> - skal flowet overgives til den udeladte `#9524`-gren?
>
> **Output**  
> - opdateret global availability-state  
> - næste kandidat eller slut  
> - eventuelt hop til `#9524`

### Hvad der konkret besluttes
- `Rule #9495`–`#9497` styrer broad-fallback-cooldown og kandidatbudget.
- `Rule #9498`–`#9502` opdaterer resource-availability-flags for food, wood, stone og gold.
- `Rule #9503` hopper videre til den **ikke inkluderede** `#9524`-gren, hvis den globale handoff-flag siger det.

### Hvorfor det er vigtigt for resten
Dette er stedet hvor segmentet både lukker sweepet og opdaterer den globale opfattelse af hvilke ressourcer der stadig er realistiske.

### Eksterne inputs brugt her
- `fl-retask-workflow-handoff`

### Bemærkning om manglende logik
Dette undersegment er det eneste sted i den nuværende fil, hvor der stadig peges på den **udeladte #9524-gren**. Hvis man hårdkoder resource-prioritering uden den gren, er det her overgangen skal erstattes eller ignoreres.

---

# Kort læseplan

Hvis du vil forstå segmentet trin for trin, er denne rækkefølge den mest naturlige:

1. **A1–A2**: Forstå hvornår motoren aborterer tidligt, og hvordan den normaliserer den nuværende villager.
2. **A3–A5**: Forstå hvordan et godt lokalt anker vælges.
3. **A6–A8**: Forstå hvordan motoren prøver at finde et konkret resource-target og dispatch'e villageren.
4. **A9–A10**: Forstå de særlige recovery-spor efter failure.
5. **B1–B2**: Forstå de to cleanup-pass der vælger hvilke villagers der skal rettes.
6. **B3**: Forstå hvordan broad fallback-kandidater udvælges og klassificeres.
7. **B4–B6**: Forstå fallback-rækkefølgerne for hver ressourcefamilie.
8. **B7**: Forstå cooldown, availability-opdatering og det sidste hop mod den udeladte prioriteringsgren.

---

# Kort konklusion

Segmentet er nu tæt på at være en komplet, selvstændig beskrivelse af **direkte villager retasking og recovery**:

- den delte motor forsøger at flytte én villager på en kontrolleret måde
- caller-laget finder de rigtige kandidater og prøver ressourcefamilier i fallback-rækkefølger
- den vigtigste resterende ydre afhængighed er ikke flere lokale retask-regler, men snarere:
  - de få eksterne flags/goals/timere nævnt øverst
  - samt den udeladte `#9524`-gren til ressourceprioritering
