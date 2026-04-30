27-03-26
I dag har vi brugt en del tid på at omskrive Immortals villager retasking kode til noget mere læseligt. Vi har også prøvet at køre koden uden det store resultat, men det kunne man heller ikke have forventet ville virke. Nu er vi et sted, hvor det ville være fedt hvis vi kunne få dele af koden til at virke. Men selv når alt er navngivet mere logisk synes jeg stadig koden er virkeligt svær at læse og forstå, selv i små bidder. Derfor tænker jeg nok vi er nødt til at bevæge os væk fra at prøve at få Immortals kode til at virke og i stedet tænke at vi selv skal skrive koden, men at vi jo så løbende kan sammenligne vores kode med Immortals og se hvad den gør anderledes og få ideer løbende. Det er nok den mest realistiske fremgangsmåde med tænke på de betydelige begrænsninger chat gpt trods alt har med det her.

Målet bliver i første omgang at løse følgende opgaver på en måde der er kortfattet og let at rette til. Vi kan altid tilføje ting senere og det gør ikke noget hvis vi går lidt på kompromis med effektiviteten i første omgang. Der kommer nok under alle omstændigheder til at være ting, der skal laves om.

# 1
Okay, men hvad kunne så være en god pathway? Jeg tænker et okay sted at starte kunne være bare at starte med at give alle vills et wood-group group-flag og finde alle vills der ser ud til at lave forbudte handlinger og give dem en stop command. Det kan formentlig gøres i få regler.
- Opgaven er som sådan løst. Den tydeligste egde case vi lige nu ikke håndterer er når en villager får en kommando til et random point. Men det tænker jeg fint vi kan vente med.
- Immortal gruger også object-data-gather type som jeg godt kunne tilføje, men det virker ikke nødvendigt for nu.

# 2
Næste skridt kunne oplagt være en form for forsimplet group opdeler til testing, der sørger for at villagers får den rigtige gruppe i starten af vores scenario. Det skal bare været helt simpelt og midlertidigt og vil lade os teste andre mere interesante ting. Vi kan oplagt også give dem kontroll groups så vi kan se deres nummer in-game.
- Endte med at tage overraskende lang tid fordi jeg lavede mange dumme fejl, vi skal ikke blive ved så sent en anden gang. Virker ikke for sten men det er lige meget nu her da det alligevel bare er midlertidigt.

# 3
Når alle vills har et udgangspunkt kan vi skrive et helt simpelt script der gennemgår vills én af gangen og for hver vill der ser ud til at have en forkert target ressource giver vi den en stop command.
- allerede gjort

# 4
Her kunne man overveje at spørge chat gpt hvordan vores approach adskiller sig fra immortals og se om noget skal justeres inden vi går videre.

# 5
Når vi har valgt en villager der skal retaskes kan vi så få den til at blive dette ved at vælge den bedste ressource i nærheden. I starten kan vi fint gøre dette lidt simpelt og så gradvist øge kompleksiteten ud fra de råd vi får af chat gpt om hvordan immortal gør det. Her bør vi også overveje om vi skal have flere food sources med i vores testing scenario allerede nu.
Jeg har nu læst lidt på Immortals approach. Immortal starter med at finde det bedste anchor/dropsite ud fra afstand, crowding og available res omkring denne. Herefter findes target kandidater inden for relevant radius der gradvist øges. Når der rent faktisk er en mindst én brugbar kandidat vælges den tættes. Der er altså IKKE en direkte mekanisme til at undgå at mange vills sendes til samme område i samme pass. Jeg tænker dog oplagt at vi kan have oprydningskode inden for samme resource der gradvist kan fixe dette senere. Lad os starte med at bygge den simple version af ovenstående.
Jeg synes dog ikke denne logik er så overbevisende ift. farms, hvor det er ret skidt, hvis der bliver sendt en villager for meget afsted. Nu hvor jeg har adgang til 16000 goals kunne jeg jo i teorien sagtens holde styr på hvilke targets der allerede er blevet retasket til og inkludere det i koden. Det bliver mere komplekst, men jeg tror jeg gør det sværere for mig selv i sidste ende, hvis ikke jeg tænker det ind fra starten. Det er nok også nødt til at være en del af koden der vælger bedste anchor. Lad os prøve at skrive noget pseudokode:
1. Vi gennemgår grupperne én af gangen.
2. Først findes alle mulige anchors/dropsites. 
3. Anchors scores ud fra distance, res availability og crowding, hvor sidstenævnte tillægger vills der er retargetet dertil i aktuelle pass. Dette skal helst foregå uden at lave lag.
4. Vi vælger bedste anchor og finder relevante target omkring det i et loop der starter med lav search radius, der gradvist øges. Hver kandidat får tjekket pathability (hvis vi kan) og object-data-task-count, der ideelt også bør medtage om vi allerede har targetet en villager dertil, men dette kan dog i højere grad justeres senere end det kan for anchors.
5. Når vi har én eller flere relevante targets vælger vi det target der er tættest på anchor uden score i første omgang.


hmm... hvad kunne i teorien være en god måde at holde styr på objekter vi allerede har retasked det her pass? Jeg tænker primært det er vigtigt at det virker for farms, for resten er det nok mindre vigtigt. Er det måske bare lettest at reserverer 200 goals til at gemme retarget targets for det seneste pass. Det burde jo ikke være noget der giver lag med tanke på at vi sjældent kommer til at retarget alt for mange på en gang alligevel. Men det er nok den bedste måde. Lad os starte med at få wood til at fungere uden og så kigge på farms derefter og implimentere det i den omgang.


Okay. Vi kan nu sende vills til et nogenlunde relevant dropsite. Der er stadig en masse finetuning der mangler samt andre detaljer, men tror det giver mening at gå til retasking før vi kigger på de ting.

hvis vi skal starte med en helt simpel version kan vi jo bare bruge samme søgekriterier som vi brugte til at finde træer omkring dropsite, fjerne dem med mere end én villager tilknyttet og sortere efter præcis afstand. Herfra tjekker vi så bare index 0 objektet indtil vi finder et objekt der ikke er palisade blokeret og vælger det.

Godt. Nu virker retasking som sådan for wood vills selvom der er mange ting der mangler. Det første jeg tænker vi bør kigge på er det med at vi lige nu potentielt retasker alle vills til det samme træ tættest på en given lumber-camp. Det mest ideelle ville være hvis vi kunne tælle til maks 2 per træ, alternativt er det letteste nok helt bare at fjerne dem vi har retasked til, men lad os prøve det ideelle først. Hvordan kan vi gøre det på en måde der ikke laver lag?

Vi kunne starte med for hver ny vill der skal retaskes at tjekke om det samme target fremgår 2 gange af vores gemte id goals. Hvis det gør ved vi at det bare skal fjernes i sidste ende, noget der kan gøres hurtigt inden vi tjekker med palisades osv. Hmm... tror det bliver for besværligt ift. hvor vi er lige nu. Lad os bare sige at der helt generelt ikke må sendes mere end 1 villager til samme target i samme pass. Så kan vi let bare køre et indirect goal loop

Okay. Jeg har fået den del til at virke, men har også encountered et uventet issue. Hvis jeg retasker en gruppe wood vills der allerede er ved en woodline vil de med stor sansynlighed ikke gå tilbage til de targets de er tættest på, men derimod gå lidt rundt og bumpe ind i hinanden inden de finder deres endelige træ. Desuden har de det med at sprede sig mere ud end det er optimalt. Dette er ikke helt optimalt for min aktuelle test, men spørgsmålet er i hvor høj grad det er et problem i en realistisk game situation, hvor den situation formentlig ikke vil være særlig hyppig. Er ikke sikker på om det er et problem eller ej. Nu har jeg gjort så target sorteres efter vill distance hvis vill er inden for 3 tiles af dropsite. Det er nok ret fint indtil videre.

Okay. Nu må næste oplagte skridt være at retasking også skal virke for de andre resourcer. Tror faktisk allerede det har fået mig til at lande på et godt kompromis. Der skal kun fjernes targets der allerede er valgt dette pass hvis en villager er mere end 3 tiles fra dropsite og har god tid til at gå til det rigtige sted. Ellers kan den lige så godt blive hvor den er og arbejde der.

# 6
Når den grundlæggende retasking fra én ressource til en anden fungerer som ønsket kunne man oplagt kigge ind i retasking inden for samme ressource. Her er det nok lettest at starte med wood og slutte på food.

# 7
Når villagers i hver gruppe virker til effektivt at kunne finde relevante targets uanset, hvad vi gør med dem kan vi kigge på at sætte nogle tal for hvordan ressource fordelingen burde være og hvordan vi vil have den til at være. I første omgang er det jo bare at ændre nogle tilfældige vills fra en gruppe med for mange til en gruppe der mangler og være sikre på de vælger noget relevant.

# 8
Når vills opføre sig rigtigt ved gruppeskift skal vi så sørge for at gruppeskiftet ikke er tilfældigt. Dvs. at vi skal lave et system der finder den bedste vill til at skifte gruppe og skifter dennes gruppe.

Den simple case er jo når vi bare har en ny villager der skal have en gruppe. Selvom der på sigt godt her kunne vælges en gruppe der minimerer walking time for denne vill kan vi nok fint starte med bare at lade den komme i den gruppe der mangler noget. Den mere komplekse case er så til gengæld den hvor vi har for mange vills i en gruppe og for få i en anden. Lad os sige at der skal flyttes en villager fra wood gruppen til gold gruppen. Hvordan vælger vi hvilken villager der skal flyttes? Man kunne lave en scoring af de mulige dropsites og kombinere denne med villagerens til dropsitet. Den kombination, der giver den bedste score er så den villager der skal skifte gruppe. Jeg har tidligere tænkt at dette system nok bør have mulighed for at være lidt afventende således at små ubalancer kan rettes af kommende producerede vills og kun de støre ubalaner kræver den her slags retasking. 

# 9
Når ovenstående fungerer skal vi tilføje mere robusthed, hvis f.eks. ikke der er mulighed for at tage den ønskede mængde af en ressource.



Har hele dagen i dag. Med lidt held og god arbejdsmoral burde jeg kunne nå hovedparten af disse:


- renskrivning med bedre navne og forsimplinger.

Okay. Vi har forbedret navne lidt og ladet chat gpt komme med forslag til forenklinger og strukturændringer, men det virker som om der ikke er nogen vej udenom at jeg selv bør gøre dette. Jeg tænker oplagt vi kan forsøge at gøre dette sammen med at vi indfører backup targets. Det kommer formentlig til at tage nogle timer, så lad os indstille os på det.


- Sørg for vills også kan retaske til en anden res, hvis der ikke er et ordentligt target.

Det her er nok det mest komplicerede jeg kommer til at gøre i dag og jeg tror det giver fin mening at bruge chat gpt, om ikke andet så til at foreslå en oplagt fremgangsmåde til implimentering.

Okay. Der er stadig flere bugs, men har fundet følgende so far:
1. der var nogle regler der fik sat dropsite som target via index goal hvilket stoppede noget i at virke
2. der var en anden regel der krævede dropsite id var sat sidst i koden som fik den til at glemme villager id.
3. der er behov for en mekanisme der stopper loopet når en vill allerede er på sin backup res (igang), helst noget der har medregnet om vill er idle.

hmm... når jeg tænker lidt over det, så er det jo faktisk ikke helt lige til at afgøre om vi er på en anden ressource end den planmæssige på grund af tidligere backup eller ej. Jeg tænker nok ikke vi kommer uden om at sætte et non-temp goal. Så hvis vi har en vill der ikke kan retaskes til sin hovedressource skal der på en eller anden måde sættes et goal der angiver hvilken res backup der VAR available, f.eks. wood og stoppe loopet hvis en villager allerede har den target res. Det ville jo så være noget der skulle køre første gang en vill fejlede grund loopet og ville ofte bare gå til den første backup. Vi risikerer selvfølgelig at første backup res ikke har plads nok?... spørgsmålet er om vi skal acceptere det eller ej? Lad os spørge hvad immortal gør efter mad.

Okay. Immortal virker bl.a. til at have løst det ved at have food nederst i heirakiet for alle non food vills. wood går til guld der er næstlettest at overloade, guld går også til wood og stone går til guld, men der er heller ikke særligt mange stone vills.

food-worker: food → wood → gold → stone
wood-worker: wood → gold → stone → food
gold-worker: gold → wood → stone → food
stone-worker: stone → gold → wood → food

Okay. Så vi siger altså at når først vi rammer fallback koden og finder en gyldig fallback res, så holder vi os til denne fallback res for de resterende vills resten af dette pass og accepterer at der er en teoretisk mulighed for at vores fallback res ikke kan overloades med alle de intenderede vills. På sigt kunne man jo også forestille sig at den ønskede vill fordeling også afspejler hvilke res der faktisk er tilgængelige, men det tænker jeg ikke vi kan gå mere ind i for nu.



#
Jeg har vedhæftet min age of empires 2 ai. Læg mærke til at starten af ai'en indeholder kommentarer der beskriver hvordan ai kode skal skrives og goals skal navngives:
Jeg er i gang med at lave en feature til min ai hvor der kan vælges en backup ressource hvis den ønskede ressource ikke er tilgængelig. Lige nu virker det sådan at hvis villageren ikke har sin ønskede ressource som target så bliver den retargeted til den første valid backup ressource. Problemet er at der ikke er noget der lige nu stopper vills fra at retarget sig selv til den samme backupressource hvert pass eller at retaske sig selv mellem 2 backupressorcer hvert andet pass. Jeg ønsker i stedet en logik der gør følgende:

- Hvis en villager fra en gruppe får brug for at tage en backup ressource gemmes denne ressource for denne gruppe for resten af det pass. Hvis villageren allerde har den ressource som target skal der ikke gives en kommando. Og hvis der er flere villagers i samme gruppe der skal tjekkes samme pass skal de kun retaskes hvis den oprindeligt ønskede ressource er tilgængelig for dem eller hvis den gemte backupressource er tilgængelig. Vi ignorerer med andre ord de resterende backups fra det øjeblik vi succesfuldt har retasked en villager til en backupressource ud fra en antagelse om at der altid vil være tilstrækkeligt af vores backupressource. Denne antagelse kan vi godt stole på sålænge vi bruger disse rækkefølger for backupressourcer:

food-worker: food → wood → gold → stone
wood-worker: wood → gold → stone → food
gold-worker: gold → wood → stone → food
stone-worker: stone → gold → wood → food

Giv mig en version af min kode der opfører sig som jeg ønsker, hvor du har ændret så lidt som overhovedet muligt og hvor du har kommenteret alle ændrede linjer startende med *** så jeg tydeligt kan se hvad du har ændret.
#



Sådan!!! Det tog hele dagen men det lykkedes. Er i tvivl om det ville have gået hurtigere uden chat gpt eller om jeg stadig ville stuggle uden. Det vigtigste er at det virker nu. Der var ret mange bugs der skulle ryddes af vejen, flere af dem lå der allerede inden chat gpt kom igang, men var bare ikke opdaget. Nu mangler der bare at få ryddet op og fjernet comments. Det tager nok noget tid at gøre ordentligt og bør helt sikkert gemmes til i morgen.

De næste 5 punkter ser (med mulighed for at jeg virkelig jinxer det) ret lette ud at klare og burde alle kunne nås i morgen.

Det sidste punkt er sådan set ikke noget jeg behøver gøre nu. Scriptet kommer til at virke fint uden, så måske vi hellere skulle arbejde henimod de ting der mangler for at vi kan teste skypanda med DUC eco. Jeg tænker det er en bedre plan.










Okay. Det her er et punkt der kræver at jeg er ret godt inde i de forskellige underdele af koden og at disse er til at finde let rundt i. Derfor kunne det formentlig være et ret fint tidspunkt allerede før vi går videre med dette at få ryddet lidt op i koden og navngivning så det er så intuativt som muligt. I samme omgang synes jeg vi skal skrive en oversigt som pseudokode og/eller nogle kommentarer så det bliver tydeligt hvad vi har og hvad vi skal tilføje.

Godt. Så helt overordnet har vi aktuelt følgende struktur:

# Struktur
Først sættes der konstanter og villager groups som forberedelse.

for group in villager groups:
    for villager in group:
        if villager has wrong target:
            for dropsites in villager group dropsites:
                find best dropsite
            find best target
            order villager to target

Det er vel sådan den mest forsimplede oversigt jeg kan lave. Den skal så ændres til noget i stil med

for group in villager groups:
    for villager in group:
        ***for res in group res order***
            if villager has wrong target:
                for dropsites in villager group dropsites:
                    find best dropsite
                ***if no dropsites:***
                    ***check next res in group res order***
                find best target
                order villager to target







det er nok heromkring vi kan begynde at tænke i at teste med skypanda og andre mere realistiske cases.. 



immortals rækkefølge
food-worker: food → wood → gold → stone
wood-worker: wood → gold → stone → food
gold-worker: gold → wood → stone → food
stone-worker: stone → gold → wood → food

Tænker det mest relevante at starte med kunne være at prøve at få en backup til at virke fra food til wood. Det er nok noget af det jeg hyppigst vil opleve.


okay. lad os sige alle vills vil på food, men at der ikke er nok targets. Hvad gør vi så? Tja... vi opdager det ved at vi ikke har fundet et valid dropsite, så det kan vi have en regel der tjekker som så hopper baglæns og samtidigt sætter en række goals der sørger for at loopet køres med de nye relevante værdier.

# lag
Vi ser ud til at have ca. 0.1 ms per retasked vill for et lille simpel empire wars setup, vel at mærke på min laptop med omkring 1000 benchmark score. Det lyder jo ret godt, men vi kommer nok ikke uden om også at teste på et stort map med mange unit og 200 vills. 


Hmm... Det var en god ide at lave den her test. Vi har et problem. Der kan kun være 60 units i en search group. Men min performance optimerede kode har aktuelt ikke taget dette into account. Kunne godt være ret besværligt at fikse.
Samtidigt kan jeg konstatere at det i dette scenario tager 5-10 gange så lang tid at retaske 20 vills sammenlignet med et lille scenario. Vi kan nok godt forvente at det her kan komme til at tage som minimum en god del af dagen i morgen at fixe, men det er helt klart noget der skal fixes så tidligt i processen som muligt, så grunddesignet er godt nok fra start.
Selv om det er lidt træls ift. lag delen, så må jeg sige at hvad angår de res vills retasker til, så ser det skide godt ud.



# ideer til lag optimering:
- sæt en grænse for hvor mange af de tætteste valid dropsites der kan tjekkes
- delete invalid dropsites
- Giv mulighed for at forlade dropsite loopet tidligt, hvis der findes ét der er "godt nok"
- Overvej om der er situationer, hvor vi kan foretage en hurtigere/simplere evaluering.
- 




Okay. Har tænkt lidt og umiddelbart er problemet nok lidt mindre end først antaget. For der burde kun være et sted i den semifærdige kode, hvor search groups kan blive større end 60 og det er villager loopet inden for hver enkelt gruppe. Det kunne være oplagt at starte med at få kode til at virke og så derfra se hvilken metode der lagger mindst. Vi bør herunder nok lave nogle mere generelle lag tests, så vi ved hvordan vi ideelt bør designe koden fremadrettet.


180 vills med remove group flag metode: 6-8 ms
180 vills med set group metode: 3-5 ms

Det vil sige at vi spare ca. 3 ms hvert script fread på at bruge set group metoden. Og det er vel at mærke noget der kører HVER eneste script run. 3-5 ms er stadig ret meget. Okay, ny vigtig pointe: grunden til det tager 3-5 ms er at en betydelig del af gold vills er på wood og derfor forsøger at retaske til guld. Hvis alle vills er korrekt retasked ender vi på 0-1, typisk 1 ms, hvilket absolut er acceptabelt.

Der er flere mulige løsninger ift. de forkert retaskede vills. 
- Først og fremmest skal jeg finde ud af hvorfor de ikke selv finder et ordentligt target, for der burde være nok.
- Sekundært kunne man have et pre script der kører inden det store loop, der tjekker om nogle ressourcer er utilgængelige og hvis de er så kan vi sørge for at vi ikke forsøger at retaske vills på den ressource i det store loop.

Okay. Vills finder ikke et ordentligt target fordi crowding er underprioriteret i controll center, men også fordi vi kun tillader 2 vills at arbejde på en gold tile hvilket er for lidt. 3 giver bedre mening. Det kan være at dette giver problemer ift overloading af tiles der er svære at tilgå, men så må vi tage den case når vi kommer til den. For nu tror jeg det er fint.

Har i øvrigt forsøgt mig med at stoppe loopet inden der tjekkes for backupressourcer, men har ikke kunnet vise at det gør en forskel så det dropper vi.


Okay. Næste skridt er selve retasking delen:
60 wood vills: 103 ms
60 food vills: 16 ms
60 gold vills 60 ms
Det er helt åbenlyst for meget. Lad os prøve at sænke antallet af potentielle dropsites, der overvejes til 3:
60 wood vills: 15 ms
60 food vills: 7 ms
60 gold vills 18 ms
Det hjælper helt klart.

Jeg har også en teori om at det kunne give mening at stoppe med at lede efter nye dropsites hvis et minimumskrav er opfyldt, men det er svært at vise uden at gøre det ordentligt.

Der kan formentlig også laves nogle early exit løsninger hvor vi ofte kan undgå det støre loop for hver villager der skal retaskes. Jeg synes dog heller ikke vi behøver supporte retasking af 60 vills i et pass på under 10 ms. Det er næppe noget der skal køre hvert pass og næppe for så mange vills. Så for nu tænker jeg at et fint mål kan være at holde det under 20 ms for 60 vills og det tror jeg fint vi kan med de ideer jeg har klar.

Alt i alt er det tydeligt at det at fixe compatability med over 60 vills på en ressource og at få lag ned i et acceptabelt niveau er en større opgave i sig selv og formentlig noget der vil tage flere dage. Men det giver mening at klare nu, så det gør vi.


Vi havde stadig 3-4 ms, hvoraf det meste viste sig at være den midlertidig start indeler. Når jeg fjerner den får jeg 1-2 ms, lidt tættere på 1 ms. Jeg ville foretrække at det var 0 ms, når nu det kommer til at køre hele tiden, men med tanke på at det her er en low en laptop med 200 villagers, der kører under 1 ms når jeg har mere realistiske 140 vills, så burde det være godt nok. I hvert fald for nu.


Hmm.. det med at fjerne lag når mange vills er på en backup res gruppe er at lave et lille script der tjekker for hver 4 res om de er available ud fra samme kriterier som jeg søger med og så sekundært skal denne info indsættes i det store loop. Jeg tænker dog godt vi kan vente med dette. Vi snakker formentligt om ca. 1 ms i de værste tilfælde og jeg kunne godt forestille mig at en del af de conditions der skal bruges til at styre det kommer til at blive ændret sidenhen alligevel. Så lad os bare vente med den for nu.



Okay. Retasking lag, det er særligt wood der er problemet.
- Base line for retasking af 68 vills til wood: 102 ms i gennemsnit.
- Efter early exit: 19ms i gennemsnit. (3 for food og gold.)
- Efter prioritering af nedcuttede tættere færre træer: 8ms i gennemsnit.

Godt. Nu har vi acceptable tal for nu. Vi kommer nok til at skulle tilbage og vurdere om vi har ofret for meget på pressicionsfronten, men ift. lag er det smukt nu.

Det virker ikke til at hjælpe at analysere færre dropsites når vi har early exit. Eftersom det er wood der klart er den eneste flaskehals nu, kunne det give mening at kigge mere specifikt på det. Jeg tænker at det faktum at der er flere objekter i spil kunne være relevant. Der er også flere typer af søgninger. 
- det hjælper at søge efter 10 frem for 40
- det hjælper også at søge en type af træer frem for både cut og uncut.
- det hjælper at lave én søgning i det mindre område uden den anden søgning i yderområdet.

Jeg tænker oplagt vi kan lægge ovenstående info sammen.

Okay. Ideen bliver i første omgang early exit i dropsite kode hvis:
- Res found er over 0
- res-dropsite-precise-distance er under 500
- crowding er under 20
- (dropsites evalueres med tætteste først så dette medtages automatisk.)


Okay. Jeg er tilfreds på lag fronten for nu. Det endte faktisk med at gå hurtigere end jeg havde regnet med hvilket var super fedt. Jeg tænker vi er et sted nu, hvor lag ikke burde blive et problem.


# Nygrouping af vills
Tror vi skal lave det så vi i stedet kører to halvstore loops, der så kan køre 4 underloops med de 4 60-unit-groups, så vi undgår at skulle søge efter 200 vills en masse gange.

Hmm... det er vist lidt mere bøvlet at omskrive end som så, da jeg i høj grad har regnet search groups ind i det hele. Jeg er lidt for træt i hovedet til at gøre det ordentligt nu. Det er nok et godt sted at starte i morgen, når jeg er frisk. Her bør jeg som det første læse den gamle kode grundigt igennem så jeg forstår hvad den forsøger at gøre og så formentlig omskrive det fra bunden.


# Ungrouped vills: Valg af vills til regrouping
Ummiddelbart er dette simpelt: Ungrouped vills skal derhen hvor de mangler. Der er dog en lille detalje: Med flere tc's er der en chance for at nogle res er væsentligt tættere på bestemte tc's. Man kunne forestille sig en situation, hvor der mangler guld og vi har et tc der er bygget på guld, men den aktuelle nyeste vill er spawnet ved et andet tc. Ideelt set vil vi gerne give vores system mulighed for at tage højde for dette og have en afventende approach. Jeg tror dog også det er en ting vi godt kan vente med for nu. Det er trods alt noget der også skal testes i real games og først når vi har flere tc's.

# Mismatched vills: Valg af vills til regrouping
En del af denne kode vil minde om koden der vælger dropsite for retasking vills, men mit bud er at der alligevel er tilstrækkeligt med forskelle til at det vil være mere besværligt at lave det til en fælles kode.
Min umiddelbare ide er følgende:
1. Find alle deficit res dropsites og sorter dem efter distance til position self. Gem evt. som search group.
2. Loop gennem dropsites mens der søges efter et lille antal nearby vills i lav radius. Øg gradvist søge radius indtil vills findes. (evt. kunne det være hurtigere med search groups og remove objects end med søgninger. Det må vi teste)
3. Når der findes mindst én vill tjekkes for andre faktorer så som crowding, res (potentielt til flere vills) og res distance med et minimumsmål.
4. (her kunne evt. laves et score loop, men synes vi venter med det)
5. Når vi har lavgt et dropsite sorteres vills efter afstand og der skiftes id på så mange som der er brug for.
6. Hvis der mangler flere vills fortsætter det større loop.





# Andre food sources
Okay. Hvad mangler vi?
- fish
- chicken, deer
- boar
- sheep
Jeg tænker at fish med fordel kan filtreres ud fra samme logik som berries.
De resterende kategorier tænker jeg indtil videre kun vi skal medtage, hvis de er døde. Nogle fair object-data-task grænser kunne være:
- fish: maks 3
- chicken/deer: maks 4
- sheep: maks 7
- boar: maks 8
Jeg tænker at et distance filter på 5 burde være rigtig fint. For nu tænker jeg at vi venter med at indkoperere prioritering af en food source over en anden. Det kommer formentlig til at være lettere at justere i rigtige games alligevel.

Okay. Aktuelt ignorere den sheep, vi må se videre på det.




Godt. Nu mangler vi bare en stor grundig oprydning og opsætning af github. Begge dele kan oplagt klares seperat fra at køre spillet og er nok oplagte ting at kigge på i bussen og på andre pause tidspunkter.



Hvorfor er det at jeg kun har min goal naming convention for temp goals? Det er klart at risikoen for at have konflikter er langt større når de samme goal constants skal sættes flere gange. Men selv non-temp goals kan vel også have naming konflikter, der kan give bugs. Så jeg synes egentlig vi skal ændre på det paradigme så alle modul goals har deres eget suffix. Det gør det også mere overskueligt, hvis et modul goal skal bruges af et andet modul. 


Nu har vi oprettet et nyt github Repo. Jeg synes vi inden vi er hjemme igen godt kan lave en lidt mere udførlig semi ambitiøs plan for yderligere læringsrelaterede ting jeg vil have ind over det her projekt. Copilot er formentlig det mest oplagte.




Jeg tænker umiddelbart at det nok giver god mening at gå ret hurtigt hen over de næste mange punkter på listen så vi kan komme igang med reel integration. Så kan vi komme tilbage til at lave det "perfekte" boar lure, deer lure og sheep kontrol, når vi ved lidt bedre, hvad behovende til disse i virkeligheden er. Det samme med organisering af kode og den slags. Lad os ikke blive hængende for længe i tingene.



Okay. Lad os kigge på boar lure. Tænker vi burde kunne lave det langt simplere, men stadig mere effektivt end reho:
- Vi starter med at vælge den boar der er tættest på position-flank inden for 35 tiles
- Vi finder den nærmeste food vill med maks hp, gemmer dennes ID og giver en attack command til boaren (den bør nok tømme sin carry først)
- Vi finder det nærmeste hø. eller ve. hjørne af town centret. Hvis boaren targetter vores vill og vores vill ikke targetter det nærmeste tc hjørne gives vores vill en move command dertil.
- Når vores vill er inden for 1 tile af det ønskede hjørne sammenlignes boar og vill position og vores vill sendes i en linje direkte væk fra boaren gennem det ønskede slut punkt.
- Når vores vill er på det ønskede punkt garrisonner vi 5 vills i tc og skyder boaren
- Når boaren er på det ønskede punkt garisonner vi den sidste vill.
- Når boaren er på 16 hp eller mindre ungarissoner vi med boar som target.











Jeg har ændret planen og er gået direkte til integration med skynetmoduler og panda tuto. Jeg tror det giver god mening at komme væk fra urealistiske scenarier med det samme, så jeg ikke bruger for meget tid på kode der alligevel skal ændres. Og ganske rigtigt er der allerede temmeligt mange uforudsete bugs. Tænker bare vi må tage dem én af gangen med de vigtigste først:
- Vills skal kunne tage stragglers



Okay. Jeg har fundet problemet og lavet en lappeløsning, men ærlig talt, bør vi nok have en mere langsigtet plan for hvordan vi gerne vil håndtere valg af dropsites, særligt lumbercamps.

Jeg tænker egentlig at den lappeløsning jeg har lavet kan være ret fin, så længe systememt kan genkende at der er tale om et fallback og kan give en passende penalty.
Jeg tænker også at nu kunne være et fint tidspunkt at kigge på sådanne bonusser og penalties.

Vi bør også overveje hvad der er den bedste måde at flytte initielle straggler vills til lumber camp. For nu tænker jeg egentlig bare en regel, der giver dem en stop command en enkelt gang er fin. På sigt, skal vi jo alligevel have sektioner der retasker vills inden for samme res område, men der er vi ikke endnu.


Okay. Næste problem er at vi ikke samler guld. Vi får ikke engang vills i gold group? Virker stadig ikke



Godt. Vi kan nu komme feudal age uden game breaking bugs. Der er stadig flere åbenlyse ting, der skal fixes og vi kan oplagt lige overveje rækkefølgen af disse. Valg af builders burde være relativt simpelt og er vel oplagt nok at starte med. Det der primært skærer i øjnene aktuelt er food vill retasking. Det er aktuelt en kæmpe rodebutik og det giver god mening, for vi har ikke kodet det endnu eller bestemt os for hvordan det skal være. Så lad os starte med lige at gøre det.

- Sheep bør tages i midterste nederste del. Næste sheep stilles klar når aktuelle sheep/boar er under f.eks. 75 food. En vill sendes til at dræbe næste sheep når aktuelle sheep/boar når under 10 food. Vi dræber ikke nye sheep hvis vi har boars klar.
- Boars bør tages i siderne. Til at starte med dræber vi boars med luring vill + 5 øvrige via tc trick.
- Deer dræbes med 2 vills via tc hop, når de er under tc. 
- Hvis vi har flere food sources under tc prøver vi at sprede vills ud. F.eks. 4 på boar, 3 på sheep, 2 på deer. Retasking sker fra de targets med flest vills på. 
- Der tilstræbes at vælge vills hvis target allerede har lav food left til at retaske/dræbe
- Retasking til berries kan oplagt ske gradvist, f.eks. ud fra at antallet af food vills under tc relativt til antallet af døde dyr med tilstrækkelig food left under tc. F.eks. kunne man sige at hvis vi har mere end 7 vills og kun ét target under tc så bør overskydende sendes på berries, guidet af om vi har reservesheep klar. Hvis vi har 2 targets kunne det hedde 9 vills. Og hvis vi har 3 targets (f.eks. ved mange deer under tc) kunne det hedde 11.


Okay. Lad os se hvor langt vi kan komme med early food eco i dag. Jeg overvejer om ikke retasking logikken kunne være relevant at sende til den aktuelle retasking kode. Men før vi når dertil bør vi nok få skrevet sheep, boar og deer koden. Lad os starte med sheep.

Lige nu er der ikke nogen begrænsning på valg af scouting sheep. Dette er selvfølgelig en fejl og et dårligt design og i virkeligheden bør scouting koden blive styret af goals sat i den generelle sheep controll. Denne kode kan oplagt ligge helt uden for DUC eco tænker jeg. Vi skal have et system der sætter næste sheep klar og gemmer det's id. De resterende sheep kan fint samles i en kugle bag tc som i Reho. Drab på næste sheep kan også oplagt ske i samme kode. Lad os få det lavet.

Okay. Så hvornår har vi nok sheep i reserve til at scoute? Tja... første faktor er vel food for det aktuelle boar/sheep som vi så kan lægge sammen med det kommende sheeps food plus aktuel reserve. Størrelsen på dette tal kan vi dividere med antallet af aktive vills under tc og få et mål for hvor lang tid vi kan fortsætte med aktuelle hastighed. Dette tal kan vi så sammenligne med den tid det vil tage for det tætteste scouting sheep at komme hjem og have en hvis buffer.

Sheep controll har indtil videre vist sig overraskende bøvlet. Prøvede at droppe at have next sheep, men det virker til at have været en fejl. Kigger lige på cheese on toast kode engang.


Endelig! Det tog godt nok lang tid bare at få det allermest basale sheep setup til at virke. Jeg mangler stadig en del, men det grundlæggende ser i det mindste ud til at virke nu.


Godt. Nu kan vills ikke tage forkerte sheep og der bliver altid dræbt nye sheep. Der er nogle skønhedsfejl der skal rettes, men ellers begynder det at ligne noget. 
Vi mangler stadig en mekanisme der sikrer at scouting sheep konverteres til reservesheep, når det er nødvendigt. Det kan vi dog godt vente med for nu.

Tænker næste oplagte skridt er deer luring, da det er super simpelt og bør kunne klares meget hurtigt. Derefter kigger vi på boar luring, der i første omgang måske bare skal være en helt simpel version, der vælger de "rigtige vills"? Om vi gør det fuldt eller halvt nu er ikke så vigtigt, men jeg tænker ret snart at vi gerne vil have kigget på food-to-food retasking og det kræver at deer og boar lure ikke retakser forkerte vills og at deers og boars ender de rigtige steder. Så det bliver fokus resten af dagen.


Okay. Animal controll er langt fra perfekt, men den er god nok nu til at vi kan begynde at kigge på intern retasking. Det virker også ret tydeligt at vi nok er nødt til lave en stying af hvornår der lures nye deers og boars, da vi ellers risikerer en del unødvendig rot. Vi bør lige tænke os godt om ift. hvordan vi bedst gør dette på en måde der kan håndtere et bredt udsnit af situationer.

Jeg tænker som udgangspunkt vi bør tage boars før deers, da disse potentielt kan blive lamed. Vi kan oplagt scoute modstanderen inden vi pusher deers som default og når så vi pusher deers, kan vi sørge for ikke at skubbe næste deer før vi er klar, f.eks. at vi ikke har en deer med over 120 food under tc samtidigt med en boar med over 120 food under tc inkl en der er på vej ind. Jeg tænker det er fint at der er 2 targets under tc samtidigt, men helst ikke mere end det. Derfor skal vi også sørge for at secondary boar lures kan forsinkes om nødvendigt. Det mest oplagte er nok at prøve at udregne hvornår vi kommer til at have brug for den næste boar og så tage den 2 sekunder tidligere plus at vi tjekker at vi ikke har en masse andre dyr der rådner under tc, hvilket vi dog ikke burde have.

Vi når ikke mere i dag, men vi er et ret godt sted nu, hvor vi har en masse mindre ting, der bare må tages en af gangen indtil vi løber tør for ting.


Okay. Lad os starte med at sørge for vi lure boars på et passende tidspunkt. Derefter gør vi det samme for deer. Og så tilføjer vi det vigtigste animal retasking.

Det var faktisk overraskende besværligt. Koden er lidt ustabil og halvfærdig nu, men jeg tænker stadig at det giver udemærket mening at gå videre til det vigtigste food-to-food retasking nu. Formentligt lidt sideløbende med at jeg implimenterer det rigtige boar lure, da dette formentlig kommer til at ændre en del på timings. Så måske vi i virkeligheden lige bør starte med det.


    Vi har et problem ift. at hvis der er mange vills på et sheep og boar er langt væk er det ikke sikkert boaren kan lures inden sheep er dødt, hvilket så gentager sig for det næste sheep. Det må kunne lade sig gøre at regne fremad således at vi medtager det kommende sheeps food i dette tilfælde. Men hvordan? Når først det nye sheep er taget skal vi jo ikke medregne det næste igen? 

I går har jeg for første gang i noget tid haft en mindre produktiv arbejdsprocess. Tror det handler en del om at der har været mange ting jeg ikke kunne sætte på formel. Vi har heldigvis en god liste af oplagte emner at starte på der burde bryde gårsdagens stime.


Okay. Grundlæggende animal controll virker ret godt nu. Der kan stadig laves lidt skønhedsting, men det er nogenlunde. De næste ting der skal kigges på er:
- V idle gold vills
- V next sheep må ikke kunne blive fanget
- V vills på wrong sheep skal retaskes og ikke have stop command

Okay. Det tog også længere tid end ventet, men fik lært at bruge break points, så det var også fint. Næste skridt bliver retasking af food vills hvor vi skal have justeret parametrende der vælger targets en hel del og samtidigt have et seperat script der kan finde food vills der bør blive retasked, i første omgang bare food vills der skal retaskes fra dyr der allerede har mange vills til dyr der er ved at rådne og burde have flere. Kommer formentligt til at tage noget tid at lave ordentligt, så det bliver nok først når vi er hjemme igen.


Okay. Hvordan kan vi på en nogenlunde simpel måde afgøre om deer lure bør udsættes? Jeg tænker at udregningen bør kigge på hvor meget food der er under tc. Dette tal kan evt. justeres for gather rates, farms og incoming boars. Jeg tænker at det der primært bør fokuseres på er de dyr der kommer til at rådne, så farms er nok mindre vigtige i den henseende. Det samlede tal skal så divideres med antallet af vills der kan samle det op. Det vil så give et tal for hvor lang tid det vil tage at færdiggøre de resterende døde dyr under tc. Vi kan passende starte med at udregne dette tal og se hvad det siger. Samtidigt kan vi evt. også udregne hvor lang tid det tager at pushe den næste deer. For de første deer er det ikke så vigtigt, men for deer der er langt væk kan det jo godt give mening at skubbe dem tidligt, selvom vi har meget food under tc.



Vi skal lige have fixet så at vills i tc medregnes i udregningen.


Okay. Skidegodt! Vi er nu klar til at kigge på food retasking mere generelt, særligt ift at prioritere mellem døde dyr, farms og berries. Det er egentlig ikke fordi det er helt skidt som det er lige nu, men vi kan nok også kun teste det ordentligt ved at variere build orderen lidt. Lige nu har vi f.eks. så få under tc at det sjældent giver mening at prioritere farms og berries, da vi gerne vil undgå rot. Så måske vi skal prøve at sende flere på food inden vi tester videre. Det burde også give mere realistiske conditions overall. Som udgangspunkt tænker jeg at animals under tc's skal have et mål for deres saturation. Hvis en threshold for denne saturation nås skal vi begynde at target farms og når der ikke er flere farms at target skal vi target berries. Så egentligt relativt simpelt på papiret. Det svære bliver at få det til at passe ind i den større retasking engine. 

Okay. Nu virker det som sådan ret fint at delay deer luring, men i virkeligheden ville det jo være bedre, hvis vi brugte den ekstra tid på at tage deers fra 2nd deer patch. Det kræver en ordentlig beslutningsprocess. Først og fremmest skal kommende boars medregnes i den samlede buffertid for hvor længe vi kan udskyde deer lure. Så er udregningen også nødt til at være koordineret med selve scouting scriptet så der scoutes videre indtil deer lure skal begyndes. Og så er deer luring også nødt til at committe til én beslutning af gangen så vi ikke risikere at der spildes en masse tid på at ombestemme sig. Det er lidt mere ambitiøst, men hvis vi skal tage 2nd deer patch på en ordentlig måde er vi også nødt til at inverstere den tid fra starten. Skal vi så gøre det nu eller skal vi starte med generel food retasking? Det er vel hip som hap. Tror det giver fin mening at kigge videre på deer lure, når nu vi har det frisk i hukommelsen.

Okay. Vi skal have et goal der fortæller scouting scriptet hvornår der skal lures deers. I virkeligheden bør denne kode nok være en del af scout priority scriptet da det kun har med scout priority beslutningen at gøre. 

Vi har nok brug for at kunne vurdere om vi har fundet en secondary patch.

Hmm... Tror det kommer til at tage temmelig lang tid at få op at køre. Far deer lure giver også risiko for at scout bliver stuck hvilket vi bliver nødt til også at fixe i deer luring. Lad os bare sige at vi gemmer det til et senere tidspunkt. Det er ikke essentielt for initial release.


Okay. Noget jeg i hvert fald kan se kan forbedres markant er farm retasking. Når en ny farm er bygget virker det ærligt talt lidt tilfældigt hvem der bliver sendt til at arbejde på den. Og det giver måske egentlig mening for der er ikke nogen mekanismer til at tjekke om den første villager vi retasker er den der er tættest på den pågældende farm, så hvis en anden vill får farmen som target, så er det jo ligesom det. Vi kunne prøve at løse det i vores retasking engine, men en væsentligt simplere løsning ville jo være hvis vi kunne sætte en shift command når farmen bygges. Lad os lige teste det engang.

WOW!!! Keystates er VIRKELIGT effektive til at få farm builders til at arbejde på farms efterfølgende. Man skal bare have en mellem move command for at det virker. Det er lidt hacky, men meget effektivt.


Okay. Vi skal stadig have sørget for at berries får lavere prioritet generelt så det kun er i særlige tilfælde de skal vælges. Lad os sætte en ramme engang. Berries skal som udgangspunkt KUN vælges hvis en vill er lige ved siden af, f.eks. en mill-builder, eller hvis tc er for crowded, eller hvis der ikke er andre muligheder. Med det i mente tænker jeg det bedste testing scenario bør teste alle disse på én gang. Mill builder giver sig selv. tc crowding kræver mange vills på food uden vi bygger farms hvilket også dækker når der ikke er andre muligheder. 
- Så vores scenario der tjekker at vills går på berries når de skal kan bare være at vi sender næsten alt på food og ikke lure deers eller bygger farms.
- Vi skal også tjekke at vills ikke går på berries når de ikke skal. Det tjekker vi egentlig allerede ret godt, men jeg tænker at det kunne være fint at prøve at lave en 18 pop+ loom build som testing scenarie til det.



Jeg tænker jeg burde kunne blive klar til endelig integration i de første 2 ai's inden for de næste 2 dage. Så én dag med integration, og til sidst 2 dage til at lave en arena ai og til at optimere skynet til den. Med alt det burde jeg kunne være nogenlunde klar til showcase om en uge. Måske lidt optimistisk, men vi skal jo lægge cuttet et eller andet sted.


Hmm... Hvordan får vi bedst deer uden om forhindringer? Det er jo især forrests der er problemet. Her er et forslag:
- lav et tjek for om vi er på vej til at pushe ind i en forrest. F.eks. scan for træer i retningen fra deer mod tc 7 tiles fremme i en 5 tile radius. Hvis vi finder mere end 6 træer er vi på vej ind i en forrest.
- Hvis vi er på vej ind i en forrest findes et cross punkt 5 tiles til hver side og path distance for hvert punkt til tc udregnes. Den mindste value vælges som cross retning
- der laves cross tiles med gradvist øget værdi (7 tiles frem, 5 tiles radius) indtil vi ikke længere er på vej ind i en forrest. destinationspunktet udskiftes med dette punkt



Okay. Vi skal kigge på chickens. Vi kan sådan set allerede tage dem. Udfordringerne er at få dræbt den første chicken og at sørge for at der sendes et passende antal vills derhen på et passende tidspunkt. Og så skal vi selvfølgelig også kunne bygge en mill der.

- Lad os starte med at få dræbt den første chicken. Jeg tænker at hvis der findes en chicken inden for 4 tiles af et dropsite samtidigt med at ingen chickens nær det dropsite er døde eller har en vill der targeter den, så skal vi bare dræbe den chicken med den nærmeste food vill.


Har lige lavet den første test med panda tuto mod samme ai med skynet modulerne. Forbedringen er der, den vinder konsekvent, men den er heller ikke mere end forventet. omkring 600 res efter 15 min og 1000 res efter 20 min og derfra bliver den omkring 1000 res. 
Der er stadig lidt ift. chickens jeg lige må fixe i morgen, men ingen tvivl om at den er mærkbart bedre. Jeg tror også at forskellen kommer til at være mere markant, når vi går over til ai's der faktisk er lavet til at have en tight eco. 


Okay. Maks 3 vills per chicken. Problemet er at vi ikke har en let måde at skelne mellem chicken og deer når de er døde. Den bedste måde jeg kan komme på er vel at chickens vil være omkring en mill og deers vil være omkring tc. Endnu simplere er det nok at sige at deers er inden for f.eks. 8 tiles af position-self og chickens er længere væk end 8 tiles. Det kan dog give udfordringer ift. at tage deers uden at pushe dem. Jeg tror at det er den løsning vi må gå med for nu og så må vi vurdere løsninger på mere wacky maps seperat.


Okay. Vi må ikke bygge dropsites tæt på modstanderen. Jeg tænker jeg har en god plan: Vi starter med at samle alle enemy tc's, castles, towers i en search-group. I vores building engine skal vi så blot tjekke hvor langt vores checkpoint er fra den nærmeste af disse. Det burde være ok hurtigt.


Har fået fjernet en masse lag fra early scouting. Jeg synes stadig bygninger giver for store lag spikes. Særligt normale bygninger og lumber camps vil jeg gerne have lidt ned. 
- Kunne man have en early exit funktion, hvis der findes et godt nok building spot?
- Jeg bør tjekke hvor meget farming-spot testing bidrager til lag
- Jeg bør teste hvor meget tjek af nearby res og dropsites bidrager til lag
Okay. Konklusionen er at det eneste der rykker er at justere på grundparametrerne. Jeg har justeret lidt så jeg tager det værste, men føler ikke det er muligt at forbedre yderligere uden at forringe resultatet i uacceptabel grad. Så jeg bliver nok nødt til at gentænke systemet. 
Et alternativt system kunne være at tjekke zoner omkring villagers. Jeg kan dog også se en del problemer ved sådan et system.
Det vigtige er at systemet skal kunne være effektivt både early og late game uden at lagge i nogen af dem. Man kunne evt. starte med at tjekke nogle små lovende områder først, f.eks. omkring 8 punkter omkring tc og omkring de 10 vills der er tættest på tc, men som ikke har en mill eller et tc inden for ugyldig range og som ikke har en tidligere valgt eller andet punkt inden for range. Man kunne også lige lerpe 2 tiles mod tc fra hver vill først så der er bedre chance for ikke at tjekke gather områder. Systemet kunne så have et early exit hvis nogle grundparametre er mødt, hvilket burde være ret effektivt når de områder vi tjekker fra start kommer til at være relevante. Man kunne også overveje om det kunne hjælpe at smide nogle random tal ind et sted i ligningen. Hvis så ikke det lykkedes at bygge en bygning, så har jeg stadig mit aktuelle system som backup og hvis det nye system virker i de fleste tilfælde, så kan vi godt acceptere at backupsystemet er lidt mere upræcist end det er nu eller at det til tider laver halvstore lagspikes.

Det nuværende system tjekker (2*25)^2 + (26^2) = ca. 2500 + 500 == 3000 punkter. Det er jo faktisk relativt lidt, når jeg tænker på hvor meget lag jeg får. Tjekker lige om det virkeligt kan passe. Ja, den er god nok. Men det er indholdet i loopet der gør det. F.eks. giver et 50 gange 50 loop 0-1 ms mens et med et can build line tjek tager 6-7 ms. Ville man kunne lave et hurtigt tjek der kunne discarde det meste tidligt? Okay følgende er i hvert fald en god ide:

(defrule
(or(up-point-distance gl-checked-tile-x--ss2 gl-position-self-x < 8)
(up-point-distance gl-checked-tile-x--ss2 gl-position-self-x > 20))
=>
(set-goal gl-temp 1)
)

Point distance er i hvert fald en del hurtigere og det er tilsyneladende ligemeget om der er langt mellem de points man tjekker. Jeg tror der er en del at hente her, så længe min endelige løsning også har backups.



Okay. Her er den samlede ide:
- Der kører et ydre loop af 2 omgange. Det ydre loop får sat en max og min distance hver gang.
- 1. gang sættes min distance til 9 (7 de første 10 sek) og max til 20. Distancerne øges dog begge med antal bygninger inkl. farms over 15 divideret med en faktor, f.eks. 10. På den måde stiger town size gradvist med antal bygninger og vi evaluerer de mest relevante steder først. Maks x og y sættes som max distancen og øges med 1 hver gang. 
- Loopet starter med et distance tjek relativt til tc. Hvis vi er uden for grænserne genstartes der.
- Herefter tjekkes om vi er tæt på tc's (ikke det første) eller mills via vores 1. search group. Hvis vi er genstarter vi.
- Herefter tjekkes om vi er tæt på andre dropsites, guld eller sten via en 2. search group. Hvis vi er genstarter vi.
- Herefter tjekkes score. Hvis scoren er bedre end tidl bedste, tjekkes om vi er nær wood. Hvis ikke tjekkes om bygningen kan bygges. Hvis alle tests bestås opdateres scoren.
- Hvis det fundne punkt overholder en række mindste krav godtages det og vi dropper anden gang af loopet.
- 2. gang sættes max x og y til 40 med increments af 3. Vi laver samme tjek for om vi er tæt på tc/mill, men ellers tjekkes alle punkter. Igen tjekker vi kun om bygningen kan bygges hvis scoren slår de tidligere.

Har lige lavet en test af konceptet og det ser ud til at virke mega godt. Nu skal vi bare bygge det. Tror det letteste er at tage grundskelettet fra det originale loop, kopiere det og rette det til. Så risikerer jeg nok ikke at lave helt så mange fejl.

Har ombestemt mig. Jeg laver det fra bunden. Det gamle ville tage for lang tid at sætte sig fuldt ind i.


En lille ting er at score beregningen gerne vil se hvor langt væk den tætteste villager er. Det er fint når vi kun har få vills men med 140 vills der skal sorteres efter tætteste bliver det langsomt. Måske vi bare skal fjerne vills mere end f.eks. 12 tiles væk og hvis der så ikke er nogen kan vi genstarte. Kommer lige i tanke om at vi jo får lidt svært ved at gøre dette via search groups. Så kræver det i hvert fald at vi bruger flere. Men det kan vi vel også godt. Så 4 search groups, der alle tjekker om der er mindst én potentiel builder inden for rækkevidde og hvis ikke så genstartes loopet. Hvis der er så kan vi jo passende finde tætteste vill i hver af de 4 grupper og bruge det lavest fundne tal til scoren.


Okay. Jeg har lavet udgangspunktet for loopet nu. Der mangler stadig lige et par gennemlæsninger og defconsts før det er klar og det bliver i morgen. Men jeg har en forventning om at det kommer til at være MEGET hurtigere end det nuværende system. Når så det virker kan vi tilføje 2. backup run.



# resultater for 10* run af house placement:
- Tomt loop: 5-10 ms
- point contains: 16-18 ms (fjerner 217 men vi har heller ikke en base)
- builder: 28-29 ms (fjerner 2493, men vil nok være en del færre i en rigtig base)
- home distance: 11-13 ms (fjerner 984)
- dropsites: 24-30 ms (fjerner 60, men vil nok fjerne en helt del flere i late game)
- score: 38-46 ms (fjerner 2489)
- wood og build-line: 320 ms (designet så de fjerner 0)

Ovenstående er fra start og ikke mid-late game så det skal tages med et gran salt, men det giver en umiddelbar ide om hvor effektive de forskellige filtre er. 
- Home distance fjerner 30% og tager suverænt kortest tid, så den bør helt klart være første filter.
- Point contains er næsthurtigst, men fjerner heller ikke så mange. Jeg tror dog den vil fjerne langt flere i late game. Vi kan også udvide den til at tjekke flere tiles eller gøre så den tjekker all-unit-class, der dog også kan exkludere enkelte relevante punkter med f.eks. planter.
- dropsite og builder er ca. lige langsomme, hvilket giver god mening da de gør det samme. Men builder fjerner 80% mens dropsites fjerner få procent. Selvom dropsites fjerner mere i late game kommer det næppe til at være lige så meget. Man kunne overveje om det i virkeligheden er hurtigere at bruge point distance for farm dropsites som i det gamle system, men det er næppe det vigtigste at fokusere på. Dropsites skal tydeligvis være noget af det sidste. Måske endda senere end score?
- Wood og build-line hører helt sikkert til i slutningen.

Okay. Man kan formentlig vinde noget på kun at tjekke de search groups der faktisk

Okay. Den nye engine for standard bygninger burde være over 4 gange hurtigere end den gamle. Jeg ville gerne have haft det endnu længere ned, men det her er nok det, der er muligt og 2-3 ms for en bygning en gang imellem er helt klart acceptabelt. Nu mangler vi bare at få overført de sidste ting fra den gamle version og erstattet den endegyldigt.


Hmm... Kan se vi løber tør for building spots late game gennem en kombination af at de tætte fjernes og de resterende er for langt væk fra vills. Jeg tænker det med at fjerne de tætte nok uanset hvad er noget der skal skrues ned for. Men jeg tænker også at vi skal have et second run, hvor vi kun tjekker hvert andet punkt og dropper eller slækker på en del af eksklusionskriterierne så vi er sikre på bygningen kan bygges. Det vil nok også give god mening permanent at øge max-vill-distance hver gang building placement fejler, så det huskes til næste gang. Eksklusionen af farmers som potentielle builders bør også være styret af om vi allerede har idle farms og bør nok også være noget der løsnes op for i 2nd run.

En ting vi også har glemt lidt i den seneste del af udvikllingen er muligheden for at lave early exit hvis vi finder et punkt der er "godt nok". 

Når jeg fjerner minimum distance løber vi tilsyneladende ikke tør for building spots. Det er jo meget fint, men det øger så også bare antallet af punkter betydeligt fra 1700 i starten til 6400 til sidst. Hvis vi skal have så mange punkter med er vi også nødt til at acceptere en mindre præcision for nogen ting. Det ender aktuelt i 15-20 ms per bygning i stedet for de 5-6 ms vi starter med. Jeg tænker egentlig fint vi kan øge minimum distance, så længe det sker i et ordentligt tempo. Der er desuden intet behov for at øge max distance så hurtigt som vi gør. Vi bygger meget sjældlent uden  for 25.


Hmm... på trods af alle mine heuristicks har vi stadig et problem med for mange can-build-line-checks i late game. Det er sgu nok noget vi bør klare med point contains? Når jeg kigger på basen studser jeg ret meget over hvor få object rejections der er. Ja okay... point-contains virker kun for en bygnings main tile, hvilket ikke er det jeg skal bruge. Det er fint for træer, men ikke synderligt effektivt til bygninger. Vi kunne evt. tjekke nærmeste bygning via en search group, finde (precise) afstanden til bygningen og se om vi overlapper medregnet størrelsen af bygningen + vores egen. Alt for vores egen bygning kan vi udregne tidligt. Så hvis vi skal bygge et house ved vi at vi skal bruge en buffer radius på minimum 2. Hvis vi sammenligner med et andet house skal afstanden mellem de to nok i virkeligheden være minimum 3 tiles for at de ikke blokerer hinanden. For de fleste andre bygninger vil tallende være større. Så som prove of concept kunne vi fint starte med bare at se om det virker for denne grænse.

Okay. Det hjalp en del, men der er stadig mange points det ikke fanger.


Okay. At forhindre main building engine i at lave større lag spikes på min bærbare viste sig at være særdeles udfordrende og selvom jeg helt sikkert har gjort det MEGET bedre havde jeg stadig håbet på bedre. Vi mangler stadig en backup løsning til når der ikke kan placeres en bygning. Men ellers tænker jeg det er på tide at komme videre. Det åbenlyse at gå videre med er jo de andre bygninger der giver lag spikes. For at jeg ikke bliver stuck bør jeg nok mere gå efter det lavthængende frugt og så ellers komme hurtigt videre.


Okay, så fallback plan:
- Fallback kommer til at køre med den normale max radius + 10
- Fallback kommer til at køre med random øget tile steps med 1-5. Så hvis den normale radius er 30 og gennemgår 60*60=3600 punkter gennemgår fallback 80 gange 80 dividerert med 3 = 2100 punkter.
- Vi bruger ikke builder rejections til fallback reglerne. Derfor nedsættes multiplieren herfor også betragteligt. 
- Vi bruger early exit med en lavere grænse, f.eks. 12 for ikke at ende på for mange build line checks.
Tænker ovenstående burde sikre at der findes et punkt relativt hurtigt.

Okay. Building placement er acceptabel nu. Der er stadig ting der kan justeres løbende, men den fejler ikke og den laver ikke alt for store spikes og laver generelt stadig gode placeringer. Jeg tænker ikke det giver mening at gå alt for meget mere i detaljer, før vi kan teste på arena i late game.



Okay. Lumber camps. Jeg vil helst minimere hvor meget grundighedsparametrende skal nedsættes, for de fører virkelig til bedre camps. Der er meget stor forskel på hvor lang tid det tager early game og mid-late game. Dark age tager lige nu omkring 25 ms mens sen feudal tager 150 ms. Det siger sig selv at det er alt for meget. 

# Opmærksomhedspunkter til lumber camps:
- Der startes med can-build-line check -> bør forudgåes af point-contains tree class. Det bedste er nok i virkeligheden at tjekke alle 4 tiles for lumbercampen med point-contains.
- Lumber camps bruger 4 wood searches med 40 targets til at lave score. Det virker godt, men de tal burde kunne bringes ned. F.eks. ved at fjerne søgninger fra træer der allerede er fældet.
- Herefter følger 6 searches for lcs og tcs. Her kan vi oplagt bruge search groups i stedet.
- Der søges også efter 3 andre res, hvor der med fordel kunne bruges en search group
- Antallet af områder der overvejes kan selvfølgelig også sænkes om nødvendigt.


Hmm... Jeg skal have en plan for hvordan jeg kan inkluderer cut down trees i scoren på en måde, der ikke bliver for CPU dyr. Jeg kan komme på 2 umiddelbare problemer ved at udelade den:
- Hvis der kun er cut down trees kan vi ikke bygge lcs
- Hvis vi skal rebuild en lc på en woodline
Den bedste løsning jeg umiddelbart kan komme på er at danne en search group ud fra en søgning omkring grundtræet i det område vi søger. Den vil så kunne holde op til 60 træer i alt. Det vil være nok til rebuild lc. Hvis det giver problemer ift. den anden case kan vi lave et fallback til

Vi skal finde ud af om vi kan searche efter lidt færre end 40 træer med samme outcome. Hmm... Det kan vi sgu nok ikke. Det er ret tæt på fuld udnyttelse.


Hmm... Selv når vi kun søger efter live trees og fjerner alle andre søgninger og build line checks spiker tiden stadig voldsomt til 80 ms late game. Så der er stadig noget vi har overset der giver en hulens masse lag. Jeg tror ikke der er nogen vej uden om at vi må genbesøge koden og forstå den og så kan vi formentlig findes noget der kan gøres smartere så vi ikke skal lave så mange søgninger.

Okay. Koden der finder lovende træområder virker umiddelbart fin nok. Den kunne formentlig blive en smule hurtigere, men det er ikke her flaskehalsen er. Mit bedste bud på hvorfor tiden exploderer lategame er at der findes flere skove. Umiddelbart virker tallet 20 meget højt sat ift. at der virker til at være rigeligt med gode kandidater. Jeg tænker også at vi nok med fordel kan ekskludere med en større radius end den vi søger med når vi skal vælge nye punkter, uden at jeg kan udelukke at dette kan give dårligere performance. Jeg tænker i hvert fald at vi er nødt til at have en eller anden mekanisme der kan frasortere områder, der ikke ser lovende ud.

En mulighed kunne være at oprette exclusion points der ikke bruges til at tjekke senere, men som bare sørger for vi ignorerer områder, der ser dårlige ud.

Det virker umiddelbart som om vi godt kan slippe afsted med at øge distancen hvortil tidligere punkter skal fjerne træer fra søgningen. Lige nu øger vi den fra 5 til 10, hvilket er meget, men umiddelbart ser jeg ikke større problemer herved. Grænsen mellem lumbercamps bør til gengæld ikke øges over de 5 da det giver en række issues.

Jeg ville dog stadig gerne have mulighed for at fjerne de punkter hvor vi har en skov hvis lumber camp gør at der ikke er potentiale for at lave en ny lumber camp. 


Okay. Jeg har fundet noget der virker til at være en ret fin løsning der forhindrer spikes i at blive større i late game. Det kommer nok til at kræve lidt løbende debugging og jeg kan også forestille mig nogle corner cases, hvor der kommer til at være brug for en fallback af en art. Men grundlæggende fungerer det sådan at vi nu kun finder 5 forrestområder i stedet for 20. Reglerne for hvornår et træ kan vælges til et område er kraftigt snørret ind, så der nu ikke kan vælges et træ inden for 10 tiles af et andet valgt træ og træet skal have mindst 22 træer omkring sig når man har fjernet alle træer inden for 5 tiles radius af nærmeste lumber-camp. Det betyder at en skov der allerede er saturated med lumber camps typisk ikke vurderes og da alle punkter har masser af træer omkring sig er vi ikke bange for at finde et punkt for langt ude i kanten af skoven. Vi kunne nok godt optimerer en del yderligere i lumber camp koden, men jeg tror hellere vi må komme videre og så tage corner cases når vi når til dem. Vi har fået lag spikes ned fra 125 ms til 10-25 ms, hvilket er fint nok for nu. 

Nu må vi lige fjerne en masse debug chat og så se om der er andet der lagger i uacceptabel grad.

Jeg kan i hvert fald se at scouting stadig er en synder. Late game, hvor vi ikke scouter længere går der 3 ms med det. Så det må være næste ting at kigge på.

Måske skal vi sætte en bagatelgrænse for lag så vi ikke bliver ved for evigt. Hvad med at sige at vi skal have average script time ned på 2 ms eller mindre. Så kan der stadig være spikes over 10 ms, men hvis gennemsnittet ligger så lavt, så kommer det ikke til at lagge. Og hvis jeg kan fjerne den lag der kommer fra scouting modulet er vi der nok allerede. Lad os sige det.


Okay. Scouting. Lad os finde ud af hvad der er galt. Som udgangspunkt bør der slet ikke komme noget lag fra scouting scriptet efter minut 8 når enemy er scouted. Og det bør desuden være slukket når ikke scouting units gives commands eller hvis de ikke eksisterer.

Okay, så der går for meget tid med scouting setup 0-1 ms. Desuden går der også 0-1 ms med sheep når de ikke er der. Scouting map ligger omkring 2 ms og kører kun når command gives så det er fint.

Okay. Scouting er fixet. Vi er nu på avg 3 ms. Lad os sige det er fint for nu.



# Ting der skal fixes inden integration med 2 ai's
- V Deer luring har et problem. Vores tjek for om deers er lured færdigt vil trigger hvis vi har set 1 deer og den så forsvinder af syne uden at kunne findes med up-find-remote. Et langt bedre system ville nok være at gemme fundne dyrs id i goals eller en search group.
- V Deer lure skal kunne komme uden om forhindringer
- V Gør deer lure mere sikkert kommer uden om forhindringer.
- V Boar lure må ikke faile med 8.0 speed
- V Undgå at garrison berry vills til at skyde boar.
- V Få scout til ikke at prøve lure chickens
- V Få chicken vills til at gå til en død chicken når de har tc som target med under 35 food så de ikke ender med at skyde for mange nye.
- V Sørg for at der bygges en chicken mill, når der er chickens.
- V scout prøver stadig sjældne gange at pushe chickens? 
- V Sørg for at en chicken max kan have 3 vills på sig når vills retaskes. (husk ikke at retaske til chickens med under 10 carry)
- V Sørg for at chickens får høj prioritet når der er 6 eller flere food vills omkring tc.
- V boars tages nogen gange ikke selvom de kan. Interval bør nok øges lidt? Det samme bør nok ske for kill sheep? I det mindste for hurtig speed
- V Nogen gange ignorerer vills under tc boaren efter færdiggjort sheep og går på berries i stedet?
- V elefanter der er langt væk kan ikke lures med aktuelt system. Vi er nødt til at have en backup til at sætte en ny luring vill. Der bør også være en backup når boar kommer uden for tc range
- V Camps bør ikke bygges i modstanderens base (mining camps)
- Vscout bør scoute enemy tidligt på chicken arabia

- tjek lag igennem
- Vi er ved at være der hvor det kun er et spørgsmål om tid før det kæmpe rod jeg har ift. goal constant values i forskellige script giver endnu flere bugs end det allerede gør. Jeg bliver nødt til at ryde op i det inden jeg går videre til nye ting. Oprydningen bør nok også indeholde gennemgang af ting, der kan skrives simplere, kortere, mere robust eller bedre ift. lag. Det er dog også ok at gemme noget af dette, da jeg stadig kommer til at udsætte ting.


Okay. Sikring af boar lures ved elefanter.
- Først og fremmest skal vi have en mekanisme der tjekker om der er et problem. Jeg tænker at hp under 15 når boar er inden for en hvis distance fra tc nok er en god trigger.
- Når vores trigger er aktiv skal vi tjekke om der er andre foodies tæt på der kan angribe vores boar. Hvis der er vælger vi en der angriber boaren. Hvis en vill der ikke er luring vill bliver targetet af boaren forvandles den til luring vill.
- Når vores trigger er aktiv og vi ikke har foodies tæt på til at angribe boaren skal vi ejecte 1 vill med mest hp.


hmm... Der er stadig nogle små ungarrison issues, men jeg tror jeg ser om det rent faktisk kommer til at bugge ud og



# Kommende:
- V retasking på dyr der er ved at dø for at undgå rot
- V Udskyd deer lure, når der allerede er rigeligt med dyr under tc
- V du har glemt at sætte focus player i din sidste find remote search
- generel retasking af food vills skal have parametre justeret, så animals vægtes højt, derefter farms og først til sidst berries
- Sørg for også at lure 2nd deer patch. Hvis vi har overskydende buffer tid, bør dette gøres først.



# Derefter:
- få vills direkte på food fra start
- Læg en plan for når mange vills retasker til guld/stone/berries og nogle vælger en dårlig res tile.
- Gennemcheck forskellige commands så du ikke sender builders og luring vills på andre opgaver.
- Når ovenstående er klaret kan vi oplagt også opdatere så vi kan håndtere chickens. Der er i øvrigt heller ingen grund til at scouten ikke skal kunne lure 2nd deer patch.




Okay. Jeg har en fin rimelig simpel ide ift. retasking på dyr for at undgå rot. Vi starter med at finde alle døde dyr og fjerne dem med carry under 15 eller som er for langt fra tc. Så gemmer vi deres id, deres carry og deres task count via indirect id's. Vi gemmer op til 10. Så kører vi et 2D loop med et "from" og et "to" dyr og udregner scorer for hver og opdaterer løbende den bedste scorer sålænge de to sammenlignede dyr ikke er det samme. . Scoren for "to" udregnes som negativ carry ganget med max(0, )(3- task count). "From" regnes som positiv carry ganget med task count. Scorer ganges med 1,15 for deers og 1,5 for boars. Til sammenlignes task count mellem det bedst "to" og "from" dyr og hvis "to" dyret har mindst 2 flere vills vælges den vill der er nærmest "to" dyret og gives en kommandor. Id'et gemmes og de to task count goals opdateres. Hvis en vill retaskes på denne måde startes loopet forfra med de nye værdier indtil der ikke længere er vills at retaske.

Jeg har regnet ud at den måde vi gennemgår kombinationerne kan vi fint bare lægge combined score for både "from" og "to" sammen og vælge dem som et par hvor der er mindst 1 vill i overtal hos "from". 


Okay. Næste skridt her bliver at kigge koden igennem med egne øjne og derefter spørge gpt en sidste gang. Så kan vi derfra lave reelle tests. Vi skal nok komme videre med det i morgen.

Godt. Nu virker det umiddelbart som det skal. Man kan diskutere om algoritmen bør optimeres yderligere, men jeg tænker det er godt nok for nu.

Vi har stadig nogle problemer med sheep controll, der jo sådan set heller ikke er færdig. Så lad os kigge på det inden vi går videre til generel food retasking og mere afventende deer push.











Todo:
- V første house skal bygges af 2 vills
- V dropsites skal bygges med rette vills
- V bygninger skal bygges med rette vills
- V farms skal bygges med rette vills
- V bygninger inkl dropsites skal prøve at være længere fra dropsites som lumbercamps. Ideen er at vi helst skal undgå at give dårlig pathing fordi et dropsite har en anden bygning for tæt på.
- V Sørg for vills retargeter i stedet for at stoppe, når de har et forkert sheep target.

- Konverter scouting sheep til reserve, når nødvendigt


- Bedre boar lure, deer lure og sheep controll
- mere fornuftig retasking af food vills
- vills skal kunne sendes via ufærdige dropsites, men skal så også hjælpe med at bygge dem, hvis de er nær maks kapacitet.
- Evt. build order ændringer, f.eks. chicken mill
- berry mills skal være op ad berries
- find ud af hvorfor militia fixerer på enemy tc




# Plan
- V Ryd op og fjern chat og comments.
- V Sørg for at vi kan ændre ønsket eco forderling og vælge en tilfældig ny eller eksisterende villager for at opnå dette.
- V Tilføj lag detection
- V Fix issues related til max 60 unit i seach groups
- V Minimer lag for retasking ved at evaluere færre dropsites / acceptere tilstrækkeligt gode dropsites.
- V Få crowdin score til at fungere med ny search group logik
- V Få nygrouping af vills til at virke med max 60 i seatch group
- V Sørg for at der vælges den mest optimale villager når der skal skiftes gruppe og ikke bare den første tilfældige. ***Der er få ms lag ved store vandringer til wood, men inden for få acceptable ms*** 
- V Tilføj stone til koden
- V Tilføj instant dropoff (som kan slås fra) og sørg for at vills med carry > 0 ikke retaskes
- V Tilføj mulighed for en buffer ved små ubalancer mellem ønsket og effektive vill grupper. (hvis kommende vills kan retaskes er det oftest unødvendigt at retaske aktuelle)
- V kig på andre food sources (I første omgang kan det vel gøre ret simpelt ved bare at tilføje døde dyr inden for en hvis radius af tc som gyldige targets og så bruge den samlede mængde food i levende+døde dyr til at få et mål for ressource score.) ***Det virker som sådan, men der er nok en hel del ekstra der skal laves før det er brugbart***
- V hav en plan for hvis gather percentage sn's ikke sumerer til 100
- V tag støttehjulende af så vi kan fjerne alle game-time conditions. 



# todo inden jeg smutter i morgen (hvis jeg kan nå det)
- Få alle modul-konstanter til at have eget suffix, inkl goals
- Der er klart brugt for en generel oprydning af koden, goal navne mm. Kan formentlig fint gøres flere gange. Vi kan jo starte med en grov gennemgang.
- begynd at bruge github og arbejd mod integrering af mere ny læring.

# Næste faser
- update aoeaidatabase til at inkludere de seneste 2 civs.
- integrer med andre skynet moduler og udnyt group flags i building engine. (få også ryttet op i navne, hvis det ikke er gjort.)
- lav deer lure
- lav boar lure
- lav sheep controll
- håndter vills der selv går videre fra et sheep til det næste.
- Integrering i skypanda.
- Tilpasning til ægte games
- Integrering i 105
- lav Dumbo's Dream (arena boom into war elephants)
- Integrering i Dumbo's dream med tilpasning til arena

# Senere
- Ret til så vi ikke søger efter flere town centre og andre dropsites end vi faktisk har
- kør en ekstra runde hvor du søger efter valid dropsites med en langt højere radius efter res, i første omgang nok kun for wood.
- Sørg for units der tager backup res kun evalueres for hovedressourcen, hvis deres hovedressource faktisk er tilgængelig - (lige nu kan vi fremprovokere super meget lag når vi sætter 145 vills på guld i scenario og mange ender som lumberjacks via backup)
- I forlængelse af det forrige bør vi også sørge for at vills kan skifte gruppe selvom de ikke har en valid target res at skifte til, så de kan komme på en korrekt backup res. Lige nu kan de ofte i kraft af at koden der skifter gruppe tror der er nok selvom der ikke er.





# Intro
With Illuminatis recent rice to dominate other top ais on closed maps like arena and being a contender for having the strongest lategame of all top ais it seemed like a good time to get some real world data for this. The ELO estimates on the AI database are only really tested vs humans on open maps and thus does not account for the fact that many ais like the extreme DE AI will be stronger on closed maps where it is harder for an enemy to rush and they can take advantage of their strong late game. So I tried to gather some data for this with test games vs human players mainly in the 1100-1400 ELO range. 

# Test games
DE AI:
I had a 1100-1200 ELO player play the DE ai on arena without doing forward buildings before going imp. He won around half the games. However he said that he enver played any closed maps and was mainly doing feudal rushes on arabia, so a more balanced player of the same ELO would likely beat the DE ai more consistently

Illuminati:
It was a lot of fun testing Illuminati as it's quite different from the other top ais. 

I started by doing 2 test games against it myself. I'm around 1650 ELO so obviously the games weren't close. The first game I went for janisaries at home and made 2 petards to break Illuminatis wall. It didn't really offer any meaningfull resistance this game which was very short. The second game I went for a cuman boom while doing scouts to controll the relics. While the game was still quite one sided Illuminati offered alot more resistance this game and managed to hold around 10 minutes in imp. I intentionally didn't get any anti monk techs in order to test the strength of the monk micro. It turns out that the normal counter system of going light cav vs monk doesn't really work vs larger numbers of Illu monks which was a funny observation.

I had a 1300-1350 ELO player play vs Illuminati. He lost the first game like expected, but won the remaining ones after that. (without forward buildings)

# Reflections after testing
Getting human ELO estimates for AI playing strength is tricky partly due to the fact that ai strength can be largely dependent on the map, the civ matchup and the ability of the enemy to adapt to the predictable nature of the ai. This is more extreme for some ais than others. The DE ai is much stronger in the late game than in the early game. Bright spark is abnormly strong early in 1v1 skirm wars, but not nearly as strong in other matchups. For Illuminati its playing strength seems to varry based on such factors more so than any other multi purpose ai. (ais that play most civs and maps) This makes it difficult to give a simple ELO estimate. Instead having multiple estimates based on the settings and certain assumptions will give more of a complete picture.

Testing the late game of Illuminati vs the other top ais it does indeed seem to win consistently. However this is largely relying on two key factors:
1. The other top ais does not seem to account for super human monk micro in their priority of anti monk techs. If you force them to get these techs early (especially heresy) Illuminati no longer seems like the clear winner.
2. Super human monk micro is especially strong vs ais. Human players might accidently lose a few units to conversions but they won't consistently trickle in units to get converted one at a time like an ai would and they would know to target the monks first when engaging. 

Illuminati also has some weaknesses that are easier for humans to exploit than ais. Feudal tower defence without army is not really a thing in the human meta (except on certain special maps) because it's to easy to punish. For ai's deciding when to dive towers or to correctly path around them is much harder. Unlike ais the human team would also most likely also feudal rush the pockets in 4v4 which Illuminati would be fairly defenseless against in the 3 minute window before they gets their first monks and tc's out. And since the Illu flanks don't make army in feudal there is nothing stopping the human flanks from just going straight for the undefended pockets. 

So to summarise; if we give the ai one of its strongest civs, let it get to 200 pop without rushing, don't do forward buildings and don't do any anti monk techs Illuminati might be something like 1500-1600 human 1v1 ELO and the DE ai might be something like 1300 ELO. However this is a VERY unrealistic scenario against human players. We can asume that human players above 1100 ELO who has played an ai at least once, will try to counter the strengths of the ai by rushing it and getting anti monk techs when appropriate. With these assumptions we can make some reasonable estimates based on the actual games played:

# Human ELO conclusions
DE AI on arena: 1050-1100 (needs more data)
The sample size for this number is fairly small. It is mainly based on a 1150 ELO player who never played arena and mainly played open maps where he could feudal rush early. While him losing half the games points to a number around 1150 more data is needed to determine this. My gues is that players of lower ELO who are less of a one trick pony can beat the DE ai on arena, but more data is needed to say with any kind of certainty.

Illuminati on 1v1 arabia: 950 (same as the DE ai)
Going for a semifast castle age with tower defence on open land maps like arabia just isn't effective enough vs humans to allow Illuminati to get to its strong late game.

Illuminati on 4v4 arabia: 1050 (average 1v1 ELO of the human 4 player team)
A team of 4 human players with this 1v1 ELO would be expected to fairly easily kill 2 Illuminati players early and then get the anti-monk techs to win the late game around 50% of the time. This is only an estimate based on the 1v1 games since I don't have enough players to test it for real and thus is only speculative.

Illuminati on 1v1 arena where the enemy is NOT allowed to castle drop before going imp: 1300-1350
While Illuminati would likely win the first game against an unprepared human player of this ELO any subsequent games the human would know to rush and get anti monk techs and just in general to respect the monk micro of Illuminati. It should probably be mentioned in the description that this ELO only holds true if Illu isn't rushed with forward buildings which is a very common strategy in the human arena meta.

Illuminati on 4v4 arena where the enemy is NOT allowed to castle drop before going imp: 1400+
In bigger team games it gets increasingly more likely that some Illuminati players will get to their late game so I would expect it to perform stronger here compared to 1v1. 

Ideally we would want more data to test these things. But it's not that easy finding human players with the relevant ELO who altså wants to play vs ais to test these things.

















# Skynet planer
De første to ting, der springer i øjnene er at jeg nok heller vil prioritere build precision lidt højere ift. lag og at vi lige skal sørge for at building engine springes over, når man ikke har råd til bygningen.

Ellers er vi jo der hvor vi bare skal have ryttet op i goal values og så er vi klar til de ægte sjove ting.

- chicken drab iriterer mig stadig lidt
- Der bør nok være mulighed for at give food vills på wood en bonus for straggler (lettere at fixe med næste ais)

hmm... det endte med at være ret besværligt at håndtere wolves og min løsning har åbnet op for en række nye problemer. Hvordan kan jeg sørge for at vills under angreb og med lavt hp ikke sendes til wolf bygninger, men at wolf vills godt kan? Selvfølgelig. Vi kan bruge shift klik! Hvis vi shift-klikker den wolf vill der er tættest på wolfbygningen til bygningen med det samme når villen angriber wolfen burde det være løst.


Det ser fandme godt ud nu!

Næste skridt er simpelthen bare den store goal oprydning. Jeg tror det er ret fint at kigge på i morgen først på dagen, hvor jeg har energi til det.


Godt. Nu sker det. Den "lille" cleanup. Vi holder os primært til goalnavne og deres konstanter, men de mest åbenlyse ting samt strukturering af modulerne generelt kan vi fint klare også. Inden vi går videre bør vi nok lige beslutte et par ting. Jeg har tidligere haft nogle ideer til goal ranges og jeg kommer jo nok til at ændre dem alligevel, men jeg synes nu stadig godt vi kan lave en foreløbig plan, der vil gøre det lettere at scripte videre. Én af de observationer jeg har gjort mig er at det er rart med en buffer så hvert modul har mindst 100 goals at "vokse ud i". Med andre ord skal jeg ikke ændre alle andre konstanter hvis jeg på et senere tidspunkt vil udvide et modul med et par goals. Så længe det samlede antal moduler og brugte non temp goals er relativt småt tænker jeg det er en glimrende ide. Jeg synes også ideen om at have temp goals på 10000+ giver god mening fortsat.
Så er der endelserne på diverse goals. Lige nu har vi det kun på temp goals, men jeg tænker vi bør have en endelse der sikrer at heller ikke non-temp goals kan hedde det samme. Lad os satse på det.

Hvor skal goals defineres? Giver det bedst mening at have det hele samlet i starten eller at have et moduls temp goals defineret i modulet? Jeg tror det sikreste er at definere alt i starten. Det nedsætter risikoen for at jeg kommer til at jumpe henover definationer.

Skal non goal konstanter have deres egne endelser? Tja... enten det eller også skal alle konstant navne defineres globalt. Jeg føler det er en af de ting jeg gør mindre end andre, så det er måske fint at gemme til der er flere med på projektet.

Så er der search groups og særligt temp search groups. Så længe jeg holder mig til at bruge 1-4 til res groups så tænker jeg de øvrige numre kan være hvad som helst for nu. Jeg kunne forestille mig at 10-15 af search groups kommer til at bruges som temp groups, men igen er det noget der bør aftales i fællesskab og ikke noget jeg skal bruge tid på nu.

Okay. Lad os komme i gang.

Kan vi sige noget generelt om oplagt rækkefølge af nummerering af moduler? tja... Jeg tænker at DUC eco og DUC building engine er meget basale og nok er rare at have som noget af det første. Måske bare nummer #000 og #001. Resten må gerne være lidt rodet, det vigtigste er at de står i rækkefølge.


Vi har en bug hvor den primære normale building engine ikke kan placere bygninger. En oplagt årsag kunne være at det at de nye goal konstanter deles med andre temp goals giver nogle issues hvis disse ikke resettes i tilstrækkelig grad.


Okay. Næste skridt er at vi lige får opdateret building engine så der hoppes direkte til den bygning der skal bygges og derfra til slutningen af reglerne. Vi skal alligevel have det gjort så der er ingen grund til en masse lappeløsninger inden.



Selv med perfect kode til at skubbe deers uden om forhindringer kommer vi ikke uden om at de bliver stuck nogen gange. Vi skal derfor have en mekanisme der kan detecte dette og først "tænde" for den deer igen når den har flyttet sig et par tiles.

Hvordan dectecter vi så bedst en stuck deer? Timeren er den oplagte mulighed, men kan vi løse det uden? tja... i princippet kan vi vel bare sammenligne hvert tick og have en form for max count. Det virker mindre godt ved høj speed, men det sparer vel en timer. Vi kunne sige at vi sammenligner precise deer point med forrige precise deer point og gør det samme for scouten. Hvis ingen af dem har bevæget sig over 0,2 tiles de sidste 8 ticks har vi en stuck deer.

Det var overraskende let. Nu mangler vi egentlig bare et system der vælger én deer af gangen, helst den tætteste, committer til den og vælger en ny, når deer enten er stuck eller er taget. Det burde være ret let. I samme omgang bør vi helt klart lige få ryddet op i deer koden, der aktuelt er et kæmpe rod. 


# 105 skynet todo:
- V Det virker suboptimalt at vills ikke kan skifte gruppe, når der ikke er rest til dem?
- Opdateret deer luring skal lige have goal names renset.
- Scout skal kunne pushe nogle deers først, så scoute modstanderen og så pushe resten. 
- Der er nogen gange problemer med at få scouted tæt på map egde
- Id loopet i starten skal tilpasses banens størrelse og bør samles i så alt køres i et enkelt loop for alle dyr, hvor også boar og deer er splittet op.

- V Den anderledes rotting priority skal slås til og fra automatisk
- V stone mining camp bygges nogen gange af food vill
- V feudal age skal kunne queues mens man får loom
- V Det skal kunne erkendes at basen er fully scouted på cow maps.
- V Vills der tager wood som backup res skal gå efter stragglers.
- V drop off til feudal og vills skal kun ske når vi har nok.
- V Vills skal kunne tage res fra pending dropsites og hjælpe med at bygge dem færdigt.
- V vills skal stoppes fra at autoretaske til deers der er for langt væk
- V Lav trush gruppe og juster gather numbers derefter.
- V Fix åbenlyse bugs i 105 så den kan komme castle age uden dumme fejl. (builder vills skal garrison, food dropoff skal fortsætte, efter et givent antal skal alle vills på food, der skal bygges en gold mine, der skal bygges en chicken mill inden farms, food vills bør ikke kunne ende på stone, vi bør måske have lidt flere wood vills early så stragglers holder længere, vi kunne også overveje om 5 vills udretter noget 4 vills ikke kunne udrette, vills i forward group bør ekskluderes fra building placement og builder kode, early house bygges ofte det forkerte sted, gold vills skal laves meget senere)

- V gold og marked kan fint udsættes 3-4 vills
- V Der skal være en mekanisme til at undgå at queue vills når vi går castle age
- V Starting tower bør nok være 1-2 tiles længere væk
- V Der sendes stadig for mange vills på chickens
- V idle vills omkring chicken mill må ikke tælles med. De skal kunne retaskes på chickens.
- V tjek om watch towers kan bygges i egen base?
- V Der bygges ikke town-centers, farms eller villagers i castle age. Det virker til at gl-build sættes korrekt, men at town centers ikke placeres.
- V wheelbarrow ikke før 15 farms
- V horse collar og bit axe må ikke blokere wood fra første tower
- V Når tc's er oppe skal der vills på guld
- V færre på food når vi går castle age og flere på wood
- V flere på guld tidligere
- V send forward vills hjem når vi er på vej til castle age og lav transition væk fra stone, så vi ender med lige at have nok til 2 tc's.

# Hurtige build order fixes
- castle age dropoff virker ikke, men kan ikke se hvorfor???
- antallet af farms bør styres af antallet af vills i food group og ikke antal idle farms.
- Vi bør nok sætte et crowding limit på berries, så vi har vills på stragglers? f.eks. maks 6 på berries
- der bør laves lumber-camp replacements, når der er tilpas få træer tilbage omkring den oprindelige. I det hele tage kan vi fint bygge flere lumber camps. De betaler sig selv hjem
- Vi bør nok gå op til 140 vills
- Tilføj ram produktion igen.
- der bør gradvis gås over til 15% wood 40% food og 45% gold
- Sælg overskydende stone og køb evt. food/wood for det.
- Tilføj market rules så builden bliver mere smooth uden du skal bruge lang tid på det.
- Få de sidste eco upgrades
- fjern gradvist stone vills når stone count bliver for høj

- langt flere stables tidligere (sørg for ikke for mange farms så du kan)
- overgang til guld lidt senere
- bonus til lumber camps for close lumberjacks?

- tower-upgrade skal prioriteres
- brug for mindre wood late game og mere food
- byg flere camps late game







Hmm... Dele af det jeg laver lige nu begynder at være mere build order optimisation og mindre skynet relateret. Det er klart at build orderen skal være nogenlunde for at jeg kan teste skynet, men vi er også nødt til at holde fast i at der skal være plads til en en del upræcision. Måske vi i virkeligheden bare skal droppe imp. Jeg føler ikke det tilføjer noget ekstra til den skynet funktionalitet vi tester aktuelt. Lad os sige det. Det betyder så til gengæld at vi skal sætte fuld gang i knight produktionen. 




Vi har et issue, hvor hvis en bygning ikke kan bygges, så kan gl-build ikke ændres og vi kan derfor ikke bygge nogen bygninger. Hvordan fixer vi bedst det? En mulighed kunne være at give bygningen en 3 sekunders timeout med behov for at bekræfte at betingelserne for opførsel stadig er til stede.


Hmm... Hvor meget tænker vi det giver mening at ændre i castle age for 105? På den ene side kunne man argumentere for at det ikke er det der er fokus her, men når jeg tænker mere over det, så synes jeg det giver god mening at vi både kigger på base development og late game macro på åbne og lukkede maps. Og det synes jeg ikke helt vi fik gjort tilstrækkeligt med skypanda. Det kommer til at udsætte arena optimisation lidt, men mange af de ting, jeg kommer til at kigge på der, vil jeg jo så bare være på forkant med.

En af de grundlæggende ting, vi skal beslutte for den opdaterede 105 er hvor aggresiv vi vil have den til at være i castle age. De forward towers køber en masse tid og opgraderinger som bodkin arrow og guard tower giver mening at prioriterer højt uanset hvad imod andre ais. Men derudover er det nok begrænset, hvor meget de øvrige upgrades giver som ikke kan udrettes uden. Jeg tænker i hvert fald at det at få gang i 3 tc's giver bedre mening som næste skridt. Derefter tænker jeg oplagt vi kan bygge en masse knights og fortsætte mere i den retning der allerede sættes aktuelt. Jeg tænker også vi skal tilføje imp til builden og fremtidssikre guldsituationen en smule. Synes kun vi skal fokusere på de ting, der kan implimenteres hurtigt for nu, for der kommer til at blive ved med at være ting, der kan optimeres. Men det giver mening at sikre at vi supporter det fulde game. Så kan vi oplagt lave showcasen med en 1v1 på arena og en 4v4 på arabia med skynet på den ene side og 105 på den anden. Jeg synes magyars er en god civ at bruge fra nu af, da de ikke har nogen eco bonus og de har fulde paladin upgrades. Så kan vi altid bruge en stærkere civ senere, hvis det er.





Hvordan styrer vi bedst id for vores gruppe af vills der ikke har group-flag 1-4? Vi kan godt antage at det script der sætter et andet group flag for gruppen også selv kan finde ud af at sætte sine andre værdier derefter. Og i virkeligheden virker det nok mest logisk at tænke at vi ligesom skal tage de 5 vills fra et aktuelt group flag. Og hvor er det så mest logisk at tage dem fra? Tja... det lette hack er jo bare at sætte dem i gold group, da det vil få dem til at gå på stragglers og jeg aktuelt ikke har en anden god måde at gøre det på.

Derfra er næste skridt så bare at skifte deres group flag én af gangen til vi har de 5 vi skal bruge.




Okay. Send long distance gatherers til at bygge dropsites. Jeg tænker det handler om at få begrænset villager-grupperne så meget som muligt. Vi behøver jo ikke engang gøre det ressourcespecifikt. Selv en farm virker jo i princippet. Det handler bare om at detecte, når der er en pending dropoff building (i starten tænker jeg vi ekskluderer farms så koden ikke kører hele tiden) og så søge efter vills i nærheden af denne bygning med carry over 0. Vi kan godt antage at en sådan gruppe vills vil være relativt lille. Formentligt under 60 og vi kan derfor godt bare lave en temp search group, hvis det er. Er dog ikke sikker på det er nødvendigt. Vi skal bare sammenligne deres aktuelle position med deres destination og hvis vores vill skal gå mere end 4 tiles får den en command til vores pending dropsite i stedet. Det burde være ret simpelt at loope over.


Okay. Vi skal have en lidt mere bæredygtig løsning, der sikrer at vi ikke løber tør for targets under tc. Den aktuelle løsning er for hacky og unreliable. Én mulighed er at time det så vi lige præcis færdiggør den sidste boar inden vi klikker feudal. Den anden og mere permanente løsning er at kunne tage flere sheep på én gang. Hvis vi har en mekanisme der sørger for at have rigeligt vills på boar når vi overloader food generelt så bliver den første mekanisme vel i virkeligheden overflødig såfremt vi kan tage flere sheep på én gang. Så måske skal vi bare tage det nu, selvom det potentielt bliver relativt kompliceret. 

Så hvad kunne være en mekanisme til at tage flere sheep samtidigt? Man kunne nok forsimple det en del, hvis vi gjorde det relativt uafhængigt af den aktuelle sheep logik og bare valgte det tætteste reserve-sheep. Vi kunne så bare måle om der var mere end 1 dødt sheep med over 80 carry som mål for om et nyt bonus sheep skulle gøres klar og dræbes og så snart et bonus sheep ryger under denne værdi kunne vi stille det næste klar. Måske er det i virkeligheden bedre at bruge carry som mål for hvornår næste sheep skal dræbes ift. bonus sheep, da vi nok kommer til at have ret svært ved at vurdere hvor hurtigt det vil blive færdiggjort og alligevel vil accepterer en ret høj grad af rotting.

Så det vi tænker her er vel i virkeligheden at vi i stedet for den aktuelle løsning kører med den rotting efficient løsning lidt længere, f.eks. til 8 food vills og så når vi ikke længere har mere end 1 dyr med over x carry remaining sætter vi det ekstra bonus sheep i spil. 

Hvordan vil vi gerne have retasking til at fungerer mellem døde dyr når vi overloader? Hvad med at sige vi skal have maks 8-9 på boar og så må resten gå på sheep? Det er i hvert fald en mulighed. 

Vi skal nok regne med at sætte en del timer af til det her. At dømme efter hvor besværligt sheep controll har været indtil videre kunne det godt ende med at tage en stor del af en dag. Dermed giver det nok også mening at gemme til en dag som tirsdag, hvor jeg ikke har en bagkant? Alternativt mandag.















Okay. Nu er den opdaterede 105 build order god nok til de ting jeg tester. Vi kan selvfølgelig godt ændre ting i det omfang det er nødvendigt for at teste andet, men vi skal ikke optimere yderligere ellers. Det virker som sådan ret fint overordnet. Der er nogle ting jeg skal have fixet før release, som jeg lige så godt kan fixe nu. Det er generelt lidt større ting, som jeg bør være klar på at afsætte mere tid til.

Okay. Der er en del større ting, der hvis de skal fixes effektivt rent tidsmæssigt nok bør fixes i parallel. Så lad os lige committe til det.

Okay. pseudokode for builders på tc: 
Hvis vi finder et tc foundation med task count under 4 søger vi efter hvilke res der er tilgængelige omkring det og gemmer det i 4 goals. Når vi så skal finde builders fjerner vi alle vills over en given afstand væk samt alle vills der ikke matcher de tilgængelige res. Hvis ikke der findes vills og task count er under 0 skal der stadig være en backup, evt. én der bare sender 1 villager.

Okay. Pseudokode for at gemme stragglers i goals:
Vi søger efter træer (af begge typer?) inden for 10 tiles af starting tc. Hvert træ tjekkes for om det har et andet træ i sine 8 surrounding tiles. Hvis ikke gemmes det som en straggler. Lad os bare sige at vi kun behøver gemme op til 10 stragglers. Når en farm skal bygges findes 10 precise punkter for de stragglers der eksisterer og vi laver en samlet regel der tjekker at precise afstanden til alle disse for vores farm er 200 eller mere.










- V Der er stadig ofte problemer med chickens der bliver retargeted til berries. Tror jeg har regnet det ud. Et eller andet får chicken vills til at tro de må retaske og da chickens ser fuldt saturated ud er den eneste tilgængelige food source berries. Jeg må finde ud af hvad der får dem til at tro de må retaskes og se om jeg kan ekskludere dette fra reglerne der udregner chicken saturation.
- V Vi bør sørges for at wheel barrow prioriteres tidligere.

- V Fix så farms ikke fjerner stragglers.
- V Sørg for tc's ikke kan bygges tæt på map egde via bound point 
- V Shiftklik normale builders med carry over 0, hvis de har et target.
- V Send ekstra builders på tc's
- V lumberjacks har en tendens til ikke at ville arbejde ved nybyggede tc's
- V Fix vandring fra nybyggede lumbercamps - virker stadig ikke
- V normale bygninger bør nok også gives en bound point på 2.
- V farms skal prioriterer distance to position-self væsentligt lavere og til gengæld prioritere det at være omkring et tc højt, særligt ift castle age





# større skynet opdateringer i rækkefølge
Vi er efterhånden ved at være der, hvor mange af de ting vi fixer mere er i detaljespektret end det er essentielle ændringer. Det er stadig fint at fixe dem, men jeg tror også at jo længere ud i de specialiserede detaljer vi kommer, jo vigtigere bliver det at teste flere forskellige maps og builds samtidigt, så jeg ikke bare laver en arabia-bot. Derfor tænker jeg vi skal til at kigge på den sheep kontrol og så vi kan komme videre til de mere grundlæggende ting, der stadig skal klares.



- lumber camp replacements fokuserer for meget på mange nære vills og for lidt på god placering samt hvilke træer der allerede er dækket af lumber camps
- Antallet af tc builders varierer lidt meget

- Fjern debug chat - Tænker oplagt vi kan lave et system, hvor hovedparten af alle chatbeskeder kan aktiveres via et debug taunt og uden dette taunt er chatten minimal. Lad os bare arbejde hen imod det herfra.
- food-to-food retasking under overload bør prioritere mindst 8 vills på boars, mindst 3  og nok bare præcis 3 på deers og kun overskydende på sheep. I samme omgang bør vi se om vi kan undgå at vills aktivt retargetes til deer, hvis der allerede er 3 eller flere vills på deers, medmindre vi har meget deer food der rådner.
- Implimenter sheep controll der kan dræbe extra sheep når det er nødvendigt.
- Lav et backupsystem så bygninger, der ikke kan bygges sættes på pause og ikke blokerer for alle andre bygninger. Brug en counter frem for en timer.
- Når vi kigger på lag bør vi nok også få gjort så retask af vills til closer tiles ikke kører hver gang.
- Der er stadig lidt funny buisness med antal af tc builders og at de nogen gange ikke går på wood ved tc, men det er vist småting.
- deer lure bør føre til den del af tc hvor man kan arbejde og ikke toppen hvor vills skal løbe unødvendigt langt.

- Når vi har fået minimeret rot bør vi prøve at ramme en timing hvor berries bliver tømt lige inden vi klikker castle age.
- lad første towers afstand til enemy tc være styret af nærmeste enemy bygning således at der er mindst 11 tiles til nærmeste enemy bygning. - giver bedre mening at gemme til vi kan pushe deers af 2 omgange og har de andre grundting fixet
- Udnyt at du kan tjekke remote-total efter at have søgt efter 1 objekt for at vurdere om det giver mening at søge efter flere objekter til at nedsætte lag, særligt i building engine for tc.
- En anden mulighed der kunne fjerne lag for tc's og andre bygninger der ikke skal lave build line tjek i kanterne er at have et mini loop der tjekker up-point-contains for res og bygninger for alle punkter som bygningen kommer til at indeholde. Det kan sådan set også gøres for alle typer bygninger, men spørgsmålet er om det i virkeligheden er hurtigere?

- town-centre bør give mindre lag (giver omkring 100ms nu) og bør have en penalty for at være for tæt på map edge



Okay. Vi er kommet til det. Sheep kontrol. Vi kan passende starte med den simple del som bare er retasking af vills så boars prioriteres først. Og så skal vi tilføje at kunne dræbe multible sheep derfra.


(defrule
            (up-compare-goal gl-overload-food-build == YES)
            (up-set-target-object search-remote g: gl-to-animal-index__#000)
            (up-object-data object-data-class == livestock-class)
            =>
            (up-modify-goal gl-to-score__#000 c:= 2500)
        )

        (defrule
            (up-compare-goal gl-overload-food-build == YES)
            (up-set-target-object search-remote g: gl-from-animal-index__#000)
            (up-object-data object-data-class == livestock-class)
            (up-compare-goal gl-from-animal-task-count__#000 >= 6)
            =>
            (up-modify-goal gl-from-score__#000 c:+ 3000)
        )


Det er lidt svært lige at vurdere præcis hvor det skal ende, men lad os bare prøve at få gjort så det ekstra sheep kan blive dræbt og så tage den derfra. På den anden side... Det giver ikke mening at slå et så stort brød op, hvis jeg tænker at tage forbi Iris i eftermiddag og i øvrigt burde begynde at kigge på erhvervspraktik. Så måske vi i stedet lige skulle parkere det for nu og så kigge på sheep controll i morgen i stedet. Der skulle vi have hele dagen til det. Det tror jeg er bedre.



Vi kan også lige overveje et par af de finesser, der ikke er det vigtigste nu og her, men som jeg tænker vi skal have kigget på på et tidspuntk:
- Vills der kommer til at tage res unødvendigt langt fra et dropsite skal retaskes tættere på.
- Mining camps er lidt funky nogen gange. Vi kunne godt kigge på om de kunne blive lidt mere perfekte. Tror måske bare det kræver nogle finjusteringer i point ajustment.
- Vi kunne evt. se om man kunne bytte gruppe mellem 2 vills hvis den ene vill skal gå relativt langt for at nå sin target res relativt til en anden.
- Lav tc hopping så vills kan skyde genvej gennem tc's når det kan betale sig. Det ser ud til at man kan gøre det i 2 stadier. Et instant stadie så længe der kun er tale om en eller flere vills med samme target. Her skal vi bare have sat gather point og have tc på gather inside 0 så alle vills autogarrisoner til target. Den anden mulighed når vi skal håndtere flere på en gang kræver at vi har gather inside på 1 og så venter til næste tick, hvor vi kan give en back to work command.
Jeg tænker særligt det er brugbart til når en villager spawner på den forkerte side af tc så man slipper for at sætte et gather point. 

Jeg tænker særligt den første nok er noget jeg ikke kan lade være med at kigge på før release. Det er jo let nok når vi taler om straggler vills der pludselig er kommet langt på afveje og tager res et helt skørt sted. Men hvad med når vi sender 5 gold vills på samme tid og de spreder sig ud på for mange res tiles? Dem der tager længst væk gør jo ikke som sådan noget galt. Men hvordan kan vi få dem rettet? Det er jo svært når først villageren er der henne for så vælger den bare det nærmeste. Men vi burde jo allerede kunne detektere det inden villageren går derover. Hvis nu bare man lavede et tjek af hvert guld dropsite og fandt den tætteste available res. Så kunne vi se om der var vills der tog en res længere væk og hvis der er, så giver vi den en retask command. Det skal så enten kun gælde for vills der er mere end 4-5 tiles fra dropsitet eller også skal det med at tage tætteste res slås fra for non-wood. Lad os starte med den simple version og se om det overhovedet er nødvendigt at gøre mere.
Så hvis vi lige skal skrive det i pseudokode:

# pseudokode
- Loop gennem hver res og hvert dropsite for hver res. For hvert dropsite fjerner vi alle res med for høj task count (mener det er maks 3)
- sorter listen så nærmeste er tættest og tjek om tile er accessable. Find precise afstand til nærmeste accessable.
- find vills af gruppen der er mere end 5 tiles fra dropsite. Fjern dem der har carry over 0 eller eller som allerede har nærmeste available som target. De resterende vills sat i rækkefølge efter afstand til dropsite looper vi gennem for at se om nogen har et target med for stor precise afstand. Hvis der findes én der har for stor afstand sendes den på nærmeste available res tile og loopet stopper for den pågældende dropsite.
- Hvis der ikke findes en eneste vill at retaske sættes funktionen på pause de næste 5 ticks.









It looked like you played around with gather points and making a full DUC eco earlier. It makes alot of sense as a human player to start there when you wanna make fully optimised eco. I did so myself when I tried to make full DUC eco the first time. I'm around 1650 on DE so I was used to use the tc for a large part of rebalancing the eco. However it took me a painfull amount of time to realise that starting out with gather points when making an aoe2 ai is a trap.

The thing is that no matter what you are gonna need systems that can 







Okay. Lad os lige prøve at beskrive lidt detaljeret hvilken behavior vi ønsker:
Når vi har 8 eller færre vills under tc (+3 for deer) kører alt den gamle kode, hvor vi sparer på rot og ekstra vills sendes på berries når de er tilgængelige. De præcise tal kan varieres, men tænker nok det passer ret fint.
Når disse tal overgås går vi over i overload mode. Her skal der altid være mindst 2 targets med høj carry tilgængelige. Det betyder at next sheep hele tiden skal være klar det normale sted. Og så betyder det at hvis ikke en boar er klar, så gøres et bonus sheep i stedet klar. Vi kunne overveje at sætte et maks for gather rate på 8 vills, da der sjældent kan være flere på samme target. Dette kunne øge vinduet lidt for at ramme en god boar timing. Derudover skal vi nok prøve at gøre sådan at når vi er i gang med en boar allerede skal der ikke være en "for sen" timing at tage næste boar. Den præcise fordeling af vills på forskellige targets kan vi passe lidt til efterhånden. Minimumskravet er at begge boars skal være tømt inden vi klikker feudal med 18 pop + loom, men nok gerne et stykke tid før det. Dvs vores todo er:
- boar/sheep finishing rate cap på 8
- ingen "for sent" cap for boars, hvis vi allerede tager boar.
- bonus sheep rykkes til boarside, når den snart skal dø og dræbes med samme timing som det andet sheep.



Okay. Vi vidste det ville blive bøvlet og det er det. Der er en længere række af ting der skal fixes på én gang:
- V sheepscouting slås aktuelt til igen når det ikke skal?
- V Bonus sheep må ikke forhindre normale next sheep i at blive dræbt
- V Vi skal sikre at bonus sheep IKKE er låst inde mellem andre sheep.
- V Vi skal have dræbt bonus sheep (i god tid) - tænker at et fint tidspunkt er når boar er under 20 eller når sheep er under 15 food med højere tal hvis speed er høj.

Okay. Det begynder at ligne noget. Der er stadig en række bugs og den største er ikke så meget en bug som det er en manglende beslutning. Lige nu bliver vores overload goal styret af hvorvidt vi har en berry mill. Men vi er jo sådan set interesserede i at overloade selvom vi har denne. Det handler mere om hvorvidt vi har en berry mill når vi overloader første gang eller ej for hvis ikke, så skal vores overload goal vel bare blive ved at være slået til så længe der er over 8 food vills under tc? Det tænker jeg.


Okay. Det lykkedes at få doubble sheep inkluderet i sheep controll. Det var bøvlet som ventet og tog det meste af dagen, men det lykkedes. Der er stadig en del ting, der skal rettes til men det sværeste burde være ovre nu.

# todo
- bonus sheep bør være i den side, hvor der er flest vills
- det normale sheep sted bør være modsat af bonus sheep stedet, så vills ikke støder sammen
- bonus sheep skal først dræbes, når der er under x carry
- lav et mere stabilt system for food-to-food-retasking under overload
- Sørg for at det også virker som ønsket med cows/deers/elephants
- test på mange maps
- test build uden overload
- send flere på wood tidligt så der ikke kommer et kæmpe straggler boom
- barracks, gold-mining-camp og market timing bør ikke styres af farm count, men af noget der varierer mindre med map



































17-04-26
Planen herfra er:
- Oprydning med fokus på at strømligne goalnavne og konstanter. Det skal ikke være perfekt, men det skal være så der er styr på hvad der er temp og non temp goals uden konflikter.
- Test skynet med 105
- Lav dumbo's dream

Okay. De sidste uger har jeg været all in på DUC eco eventyret. Og jeg har været super god! Jeg har arbejdet som en sindsyg og været virkelig produktiv. Men der er heller ingen tvivl om at det har været en besættelse, der også er gået ud over andre ting. Jeg er ikke der, hvor jeg er bekymret her og nu og har lyst til at droppe projektet, slet ikke. Men jeg er der, hvor jeg tænker jeg bør sadle om ift. hvor meget af min tid og mit fokus jeg bruger på det. Det har været meget begrænset, hvor meget almennyttig programmering det er blevet til. Det er sådan set også okay. Jeg har hygget mig og jeg har fået et produkt ud af det. Jeg skal nok få styr på mit profesionelle liv når først jeg kommer igang. Det er mere mit sociale liv jeg tænker jeg nok ikke kan udsætte mere at kigge på. 

Det er ikke blevet bedre med kollektivet, tværtimod, men det er jo også et spørgsmål om tid før jeg flytter. Det er mere Iris jeg tænker jeg får problemer, hvis ikke jeg begynder at prioritere lidt mere. Jeg vil ikke sige jeg har været en dårlig kæreste de sidste uger til mdr, men jeg har heller ikke været en fantastisk kæreste. Jeg har allerede besluttet mig for at vi flytter sammen. Har jeg lyst til at flytte ind allerede fra August? Det er da et argument at det nok er lidt lettere for Iris at få til at hænge sammen. Jeg har sgu ret svært ved at mærke efter hvad jeg vil med noget som helst i øjeblikket. Det er jo ikke fordi jeg synes her er fedt i kollektivet og der er umiddelbart heller ikke noget der tyder på at det ville ændre sig betydeligt. Jeg tror jeg har lidt svært ved at mærke migselv i det. Til gengæld tror jeg at studiestart kunne være et ret godt argument for at flytte tidligere. Men om det ene eller andet tidspunkt lige er optimalt har jeg lidt svært ved at vurdere. Jeg vil i hvert fald gerne være på plads inden studiestart. 


19-04-26
Havde Iris med forbi højskolebanden igår. Jeg har det sgu lidt mærkeligt for tiden, både generelt og i mine relationer, inkl. med Iris. Det har også føltes som om noget har været off mellem os i går og i dag, men jeg følte ikke jeg havde overskudet til at italesætte det. Jeg synes det er svært at vurdere, om der er tale om nogle tegn jeg bør reagere på ift. mine egne følelser, fordi jeg jo har haft det mærkeligt i alle mine relationer det sidste halve års tid. Jeg synes ligesom ikke jeg kan afgøre om det i sidste ende har noget med Iris at gøre eller om det mere bare er et symptom på noget mere generelt dysfunktionelt i min måde at tilgå verden på. Det har været fedt at være så opslugt af ai scripting de sidste uger, men det har helt sikkert ikke gjort mig mere glad i mit sociale liv ellers. Måske snarere tværtimod, fordi jeg helt sikkert har været mindre tilstede i diverse sociale sammenhænge. Jeg har lidt tænkt det som at jeg snart var færdig med det store træk og at jeg jo alligevel skulle til at flytte, så at det ikke gjorde noget ift. kollektivet, men jeg kan godt mærke at den følelse jeg har haft ift. mig og Iris i går og i dag bestemt ikke er holdbar i længden. Og jeg kan også mærke at min generelle glæde og energi i dagligdagen det sidste halve år bestemt heller ikke er holdbar i længden. Nu har jeg givet mig selv fri den sidste halvanden måned. Det har været dejligt på mange måder, men det har jo ikke løst de grundlæggende problemer. Tværtimod har det til dels skabt nogle nye, fordi jeg på en eller anden måde er blevet endnu mindre entutiastisk når folk spørger hvordan det går og hvad jeg skal. Det er ikke en holdbar måde at leve sit liv på. Derfor synes jeg vi skal prøve at lægge en form for plan, startende med at stille det helt grundlæggende spørgsmål: "Hvad skal der ske i mit liv for at jeg kan være glad for min tilværelse?" Jeg ved det er et stort spørgsmål og det kan være svært at svare endegyldigt på så lad os prøve at fjerne barriererne og bare skrive lidt til skraldespanden og vælge de vigtigste ting ud.

- Masser af sport. Det er helt sikkert super vigtigt og jeg tror i min aktuelle situation oplagt der kunne være endnu mere.
- Jeg har brug for at have en grundlæggende følelse og tro på at fremtiden ser lys ud og at mine bedste dage er foran mig, både hvad angår arbejdsliv og privatliv.
- Jeg har brug for at føle mig elsket, forstået og værdsat og at føle at jeg har noget at bidrage med.
- Jeg har brug for ikke at gå og holde noget inde og skulle skjule og skamme mig over hvem jeg er.
- Jeg har brug for ikke at fryse og ikke at have smerter.
- Jeg har brug for at føle jeg kan opfylde de krav der stilles mig.
- Jeg har brug for at kunne tage nogle pauser i løbet af ugen uden at have dårlig samvittighed.
- Hvis jeg har en kæreste har jeg brug for at føle en højere grad af vished omkring at det er en jeg har lyst til at bruge resten af mit liv med.
- Jeg har brug for at kunne se mig selv i mit arbejde på længere sigt.
- Jeg har brug for at føle en grundlæggende boligmæssig og finansiel tryghed.

Når jeg kigger på ovenstående punkter er der ikke noget at sige til at jeg synes jeg går og har det mærkeligt. Der er ret få af punkterne som jeg synes jeg helt eller delvist opfylder. Og sammenlignet med de sidste mange år har jeg kun i meget dårlige perioder følt at jeg har kunnet tjekke lige så få boxe af. Nu til det endnu vigtigere spørgsmål: "Hvordan kan jeg så komme derhen, hvor tingene er anderledes?" Det er jo ret slående at samtlige af punkterne på papiret er rent følelsesmæssige og i højere grad handler om min opfattelse af virkeligheden end den faktiske virkelighed. Så i princippet kunne mange af dem være opfyldt, hvis bare min hjerne var et lidt bedre sted for tiden. Med andre ord er der ikke som sådan noget der burde stå i vejen for at jeg sagtens burde kunne vende skuden med den rette plan og den rette indstilling. Men det kræver også at jeg er villig til at gå ind i det med en betydelig grad af diciplin. 

Helt generelt passer det nok ret godt at man får, hvad man giver. Både ift. relationer, arbejde og andre aspekter i livet. Jeg kan altså ikke regne med at løsningerne bare dumper ned i favnen på mig. Jeg skal selv tage kontrol og ansvar for mit liv. Det virker nok for stort og uoverskueligt at skulle fixe alle punkter på én gang, men vi kan jo fint tage ét punkt af gangen og så gå videre, når jeg føler jeg kan overskue det. Og det mest presserende punkt lige nu er sgu nok Iris. 

Lad os starte med lige at slå en ting fast. Det faktum at du ikke føler dig sikker på at det er en god ide at du får børn er IKKE noget du skal føle skyld eller dårlig samvittighed over. Det er helt klart det der er den største udfordring i din relation til Iris, men det er ikke fordi du er forkert. Du har fuld ret til at vælge at du ikke vil have børn. Til gengæld har du også lige nu et ansvar over for dig selv ift. rent faktisk at finde ud af om du gerne vil have børn. Det er ikke noget du finder ud af fra den ene dag til den anden. Men hvis du skal blive mere glad i din dagligdag kræver det også at du bliver mere afklaret inden for de næste 6 mdr. Det at flytte ind sammen med Iris vil formentlig gøre dig klogere på nogle områder, men du bliver nødt til at gøre en mere helhjertet indsats for at prøve at sætte dig selv i nogle situationer, hvor du kan mærke rigtigt efter. Og jeg tror den kombination er det eneste jeg kan gøre for at min tvivl ikke skal æde mig op indefra. 
1. : Sæt en deadline, f.eks. nytår 2026-2027, hvor jeg skal have truffet den endelige beslutningen om hvorvidt jeg vil have børn med Iris. 
2. : Giv 100% af dig selv frem til den deadline på at blive afklaret. 
3. : (Jeg bliver nok også nødt til at fremstå mere sikker end jeg er over for Iris indtil jeg er endeligt afklaret)

Selvom spørgsmålet om børn fylder meget i vores relation, så er der også mange andre ting, der fylder:
- Min usikkerhed omkring hvorvidt jeg finder Iris tiltrækkende nok.
- Vores forskelle ift. interesser, social load og evne til at få de bedste sider frem i hinanden.
- Jeg kan helt sikkert også mærke at de svære snakke er begyndt at fylde mere og mere i vores relation, på en måde der påvirker mig negativt.
- Der er selvfølgelig også alle de positive ting, som vi får ud af vores forhold. For mit vedkommende handler det vel særligt om nærhed, følelse af at blive forstået og det at jeg ikke går og tænker på piger hele tiden. Så er der jo også mange af Iris personlige sider som jeg værdætter rigtig meget. Hendes omsorg, nus, at hun er så nem at være sammen med.

Jeg tror også det i høj grad frem til deadline er vigtigt at fokusere på at vi også gør ting som jeg rent faktisk gerne vil og ikke kun gør, fordi jeg tror det kan gøre Iris glad. Det er selvfølgeligt et kompromis vi skal finde, men jeg tror de sidste års dating på nogle punkter lidt har fået mig til at sætte lighedstegn mellem at jeg skal gøre mig umage og at sørge for pigen er glad og tilfreds. Men det er jo i virkeligheden kun halv effort, hvis jeg ikke også gør mig umage med at sørge for at skabe en relation, som jeg kan se migselv i. Det betyder ikke at vi ikke skal lave ting, primært for Iris skyld. Men det betyder at jeg også er nødt til at teste om det fungerer for Iris at indgå i det kompromis, der fungerer for mig.

Jeg har som nævnt en følelse af at jeg ikke rigtigt kan stole på det øjebliksbillede min hjerne aktuelt danner af det samlede billede. Jeg er stadig et ret skidt sted psykisk og føler nok først jeg kan stole på min egen vurdering, når jeg er lidt mere migselv igen. Ikke fordi alt skal være perfekt, men det bør dog være mere afbalanceret, end det er nu. For at komme til det sted igen, hvor jeg kan genoplive mine følelser for Iris lidt mere kræver det også at jeg gør mig mere umage end jeg gør lige nu. Så lad os prøve at lægge en mere konkret plan for dette:

På torsdag skal jeg lave overraskelse for Iris og det bliver den eneste dag, vi har sammen den her uge. Det er en mega oplagt mulighed for at starte processen. Så frem for at fokusere på alle de ting jeg har opstillet herover på én gang synes jeg at det oplagte sted at starte er at fokusere på denne dag og på at få startet en god process op omkring hele børnesituationen. I første omgang bør det nok bare være at ses med Kasper, Jesper, Frederikke og måske Lasse. Det skal ikke gå hurtigere end jeg kan overskue det, men det skal igangsættes. Det tænker jeg er planen for nu.

En sidste ting er at jeg skal tage en beslutning ift. flyttetidspunkt. Jeg hælder til at takke ja til at flytte ind fra august, men jeg tænker også at jeg skylder Iris, migselv og toppen at være afklaret inden på torsdag. Og så tænker jeg uanset hvad at søndag er en ret oplagt dag at melde ud til toppen at jeg flytter. Så igen ikke noget jeg behøver at beslutte her og nu, men noget jeg skal kigge på i løbet af de kommende dage.

Det ser ud til at vejret bliver rigtig godt fra tirsdag af, så jeg tænker oplagt at jeg kan tage rundt og planlægge skattejagten der. Onsdag kunne særligt være god og jeg kunne oplagt kombinere det med en klatretur med Mads. Inden jeg tager afsted, bør jeg dog have klargjort evt. poster så jeg kan have det hele med. Så lad os sige at den plan senest skal lægges tirsdag.

Okay. Det var Iris for nu. Jeg tænker også lige jeg bør forholde mig til min ledighedssituation. Hvad giver bedst mening? Altså hvis jeg skal kunne fokusere ordentligt på Iris og andre store spørgsmål den næste uge tror jeg egentlig det giver god menin at udsætte en uge endnu. Men så hedder det altså også at jeg melder mig ledig fra næste mandag senest, og evt. før. Lad os satse på det.

Hov. En sidste ting. Nu har jeg rent faktisk lagt en ret fin plan, men det hjælper ingenting, hvis jeg ikke følger op på den. Så lad os lige planlægge en specifik opfølgning:
- Jeg skriver til Kasper og mads NU.
- Jeg får klaret tjanser i dag så det ikke fylder i næste uge
- Jeg må gerne scripte, men jeg skal have ændret mine tankestrømme, så de handler mere om den virkelige verden fra nu af.
- Jeg planlægger torsdagen SENEST tirsdag, når jeg vågner.
- Jeg sætter mig og følger op på situationen med Iris fredag og lægger en videre plan derfra.
- Jeg melder mig ledig SENEST mandag om 8 dage.


20-04-26
Har færdiggjort en smule Rehoboam arbejde og er prøvede for sjov lige Skynet en enkelt gang bagefter. Det er bare en hel anden verden. Den er godt nok lækker at se på til sammenligning. Nå, men det er ikke det vi skal nu her. Den her uge er dedikeret primært til Iris og så er det mest den overskydende tid og energi der skal gå til andre ting. Så lad os lige færdiggøre Irisdelen af dagen og så kan vi lege bagefter.

Vi skal lave en kickass skattejagt til hende. Jeg har allerede tænkt på et par ting, men jeg tænker oplagt vi kan starte med at brainstorme videre. Vi skal ikke have alle tingene samlet i dag, men ideelt set skal vi nå til et punkt, hvor vi ved, hvad vi vil lægge i Iris lejlighed.

# Skattejagt ideer:
- Det skal ikke være kompliceret. Det skal være ting jeg ved Iris kan regne ud.
- Lav en flaskepost med en clue og gem den et sted ved stranden. Oplagt ved sydhavnstippen. Så kan vi også bade, hvis det er vejr til det.
- Find et godt klatretræ (kastellet eller sydhavnstippen?) og gem en clue i.
- Gem en clue et sted i Iris lejlighed/kælderrum.
- Skriv noget med maling, der bliver selvlysende når du bruger UV
- Kig i dine tidligere ideer.
- Jeg tænker oplagt at jeg kan grave skatten eller noget andet ned. Sydhavnstippen ville være lettest, men det er lidt ærgeligt, hvis det skal slutte derude. Så måske vi bare skal grave en clue ned?
- Brug din kodelås. Koden kunne være Iris fødselsdag
- Få lamaerne ind på en måde
- Når vi alligevel er ved sydhavnstippen kunne vi oplagt gemme noget tæt på boulders
- Vi kunne oplagt få teressen og solnedgang ind over på en eller anden måde.
- tegn lamaer på skattekortet



Hmm... Synes ideen med en selvlysende stift er mega god, men det ville jo nok fungere bedst ved Iris, hvilket jeg ikke kan nå i aften. Mon ikke vi kan finde et tidspunkt onsdag, hvor Iris ikke er hjemme og gøre det klar? Tænker vi lige kan kigge ind i røverkøb og tiger butikken og hvis ikke de har noget, så venter jeg bare.

Okay. Tænker jeg har nok til at prøve at samle tingene lidt. Jeg tænker at hovedparten af skattejagten kommer til at foregå ved sydhavnstippen. Det er oplagt med det gode vejr og det faktum at Iris elsker natur. Jeg tænker egentlig fint bare vi kan gå lidt rundt derude og så slutte hjemme ved iris, hvor jeg har gemt gaven, UV lampen og har skrevet hvor skatten ligger med selvlysende maling.

De præcise lokationer på sydhavstippen er mest oplagt at finde ud af onsdag. Hvis jeg tager der ud om formiddagen har jeg god tid til at få styr på det hele. 

0. Jeg henter Iris og fortæller hende at jeg har opdaget noget mystisk som hun hellere må komme og kigge med på. Vi kører ud til boulders hvor jeg viser hende en beretning fra en forlist bornholmer.
1. Beretningen peger i retning af et sted ved kysten hvor jeg har gemt en flaskepost. Tænker vi bader i samme omgang.
2. Flaskeposten indeholder selve skattekortet, som jeg har taget en kopi af for en sikkerheds skyld.
3. Skattekortet viser hvor der er begravet en kiste (nøgleboksen). Tænker det bliver tæt på lamaerne.  Du kan oplagt tegne dem på kortet
4. Sammen med nøgleboksen er der en clue der beskriver et træ. Oppe i træet er der en anden clue der leder til Iris fødselsdag
5. I boksen ligger en clue til et sted ved Iris, (Kælderrummet?) hvor jeg har gemt UV lampen og en ledetråd til at prøve den oppe i lejligheden.
6. Et sted i lejligheden har jeg skrevet med usynlig UV blæk at skatten ligger der, hvor vi skal se solnedgang sammen. Alternativt skal jeg nok gemme den lidt bedre.

Okay. Jeg tænker det nok er en ret fin længde. Hvad skal vi så have styr på herfra? Altså vi skal nok satse på at have alt klar til onsdag middag. Der er en del af ovenstående clues og remedier, der skal klargøres før vi tager af sted. Lad os lige starte med at kigge i Tiger og Røverkøb efter usynligt blæk.

Okay. Tænker oplagt at jeg både gemmer UV lampen og den hemmelige besked i kælderrummet. Og jeg tænker også oplagt at jeg kan gemme det hele lige inden jeg henter Iris. 

# remidier til onsdag
Jeg har bestilt en ysynlig blækstift. Er der andet jeg mangler af remedier til onsdag? 
- En flaske med låg.
- En snor til at sætte flasken fast med.
- En snor til at binde en besked fast til træet med.
- En pose til at pakke nøgleboksen ind
- En masse papir
- En ligther til at gøre skattekortet "ægte".
- skovl til at grave nøgleboksen ned
- Blyant kuglepen til at skrive med (og nok også et underlag at skrive/tegne på)
- En fuldt opladet mobil
- nøgleboksen
- klatreting
- volleyting


# Til torsdag:
- gaven
- uv lampen
- usynlig blæk stiften
- evt. backup usynlig blæk hvis det bliver nødvendigt.
- Iris ekstranøgle
- badetøj

# todo
skriv beretning fra forlist bornholmer.
Hmm... Tror næsten det letteste er bare at gøre det når jeg er derude.


21-04-26
Jeg tænker ideelt egentlig at jeg skal koble helt væk fra ai scripting, som minimum 3 døgn frem og hvad de store ryk angår frem til næste uge. Jeg har dog svært ved at genprogrammere min hjerne en dag som i dag, hvor det bare har fyldt fra start til slut. Mon ikke det mest effektive er at komme i nogle situationer, hvor jeg er mere tvunget til at være i nuet. Jeg tror ikke det er mega realistisk at jeg får tænkt nogle store forkromede tanker i aften, så fyldt med scripting som mit hovede er lige nu. Mere realistisk er det nok at få klaret nogle praktiske ting i stedet.

22-04-26
Det gik dårligt med at koble væk fra AI scripting i går. Jeg havde vel ikke så meget konkret andet at lave i gues. Det har jeg i dag og jeg er faktisk ved at være der, hvor jeg har småtravlt hvis jeg skal nå det hele. Lad os starte med remedier. Vi skal finde noget papir, en tør flaske og have sat nøgleboksens kode til Iris fødselsdag.

Hmm... har jeg brug for noget særligt til at sætte træposten fast med ud over snor? så skulle det være en strips eller et søm med en lille hammer. Kan vi vel godt tage med.

Vi holder os bare til snor. Det er fint. Lad os skrive lidt tekst:


# Beretning fra forlist Bornholmer
Skibet har slået læk og jeg frygter at vi ikke holder os oven vande til vi når hjem til Bornholm. I lyset af besægtningens mytteri har jeg ikke turet tage chancer. Kortet er ikke længere i min besiddelse, og hvis jeg aldrig ser det igen, håber jeg at det en dag vil blive fundet ved kysten af en værdig Bornholmer. Hvis mine beregninger er rigtige skulle vindretningen føre det i retning af sydhavnstippen.

Kaptajn E. Frendved

# Clue til træ
Specifikation af træ laver jeg derude. Noget med:
Svaret skal findes nærmere himlens højder, hvor trækronerne svajer i takt med vindens sus.

# Clue til Iris fødselsdag
Den dag en værdig Bornholmer kommer til verden kan kisten åbnes. (Indtil da skal ingen se den anden side.)

# Clue til Iris kælderrum
Jeg er så fuld så fuld, men det er også fordi din far har hældt så meget på mig. Og nu kommer der snart endnu en og fylder på mig? Jeg kan snart ikke mere...

# Clue til terasse
Her skal vi mange flere solnedgange sammen efter sommerferien <3




26-04-26
Okay. Lad os tage en pause og finde ud af, hvad der skal ske i dag. Vi skal beslutte 3 ting: Hvad skal vi lave? Vil jeg lave mad? Fortæller jeg i dag at jeg flytter?

Lad os starte med de første 2. Er der noget jeg har lyst til ud over at tage i biffen? Så skulle det være noget sportsagtigt, f.eks. badminton. Er det sjovt med den gruppe vi er? tja... måske? Alternativt kan vi se film. Det skal ikke absolut være en biograffilm. Hail Marry er ret lang og det bliver nok for sent hvis vi tager ind og ser den. Jeg tænker også gerne jeg vil se den med Iris. Er der en anden film jeg gerne vil se med gruppen? Vi kunne se Olsen banden? Det tror jeg faktisk er et ret udemærket bud, det er fandme kultur! Så kunne vi se den mens vi spiser? Tænker det er en god plan. Vi køber bare olsen banden ser rødt på youtube. Vi kan købe nogle grønne tuborg til.

Okay. Så det lidt større spørgsmål. Hvornår fortæller jeg at jeg flytter? Tja... Det er egentlig sjovt at det er blevet sådan et ømtåleligt emne i lyset af at jeg sådan set har tænkt at flytte i noget tid. Det er ikke som sådan fordi jeg har travlt med at skulle sige det ift. flyttetidspunkt, men det bliver også bare tiltagende omstændigt ikke at sige det. Er der nogen god grund til ikke at fortælle det i dag? Ikke andet end at det føles belejligt at udsætte.

Vi kan måske også lige starte med at beslutte, hvordan jeg gerne vil sige det. Jeg tænker oplagt bare jeg kan sige at Iris har spurgt om jeg vil flytte ind i hendes lejlighed fra september og at jeg har sagt ja til det. Det føles som det rigtige tidspunkt for os at flytte sammen. Vi har det rigtigt dejligt og i kraft af det har vi også begge to brug for at mærke hvordan det er at bo sammen. Jeg tror også det passer ret fint ift. at jeg ikke har haft lige så meget energi til at være social i Sannyas det sidste års tid, som da jeg flyttede ind, hvilket I nok også har kunnet mærke. Så selvom det er svært at give slip på det her sted føles det også rigtigt at der sker et skift nu her.

Det ser fint ud tænker jeg. Har jeg mod på at sige det i aften? Det ved jeg ikke rigtigt. Lad os se på det. Nu kan vi lige få gjort klar først. Lad os bare lave balluga bollo.


Vi kunne også oplagt lige tjekke ind ift. hvordan vi har det og de tiltag vi satte i søen i starten af ugen. Hmm... Jeg har det nok hverken værre eller bedre. Det var en rigtig dejlig dag i torsdags og jeg tænker det er helt rigtigt at man får det man giver og at jeg ikke kommer i mål med hverken Iris eller de andre ting jeg vil have tilbage på rette spor uden at gøre en ordentlig indsats. Jeg mødtes med Kasper og synes i det hele taget jeg har fået handlet på en del af de ting jeg havde sat mig for. Det har ikke nødvendigvis medført en højere grad af afklarethed, men det tæller stadig i den forstand at jeg faktisk har gjort en indsats.
Nu skal jeg ses med Iris i morgen igen og jeg synes godt jeg kan begynde at arbejde mere målrettet med, hvad der skal til for at gøre vores relation endnu bedre.
Som en sidste ting, så tror jeg altså det vil gøre et eller andet godt for migselv og for mig og Iris relation, hvis jeg får sagt det til kollektivet snart. Ellers er det lidt som om jeg egentlig ikke har lyst til at flytte sammen med Iris.
Måske skal vi i virkeligheden lige mærke efter igen. Har jeg stadig lyst til at flytte sammen med Iris? Det tror jeg. Det er super skræmmende, det er et kæmpe skift, der er mange bekymringer i ligningen, men alle andre muligheder ville jo virke helt forkerte. Og bare fordi det er skræmmende, betyder det ikke at det er forkert. Min tvivl fylder stadig meget og jeg kan godt tage mig selv i at føle det er noget jeg gør fordi jeg burde, mere end fordi jeg har lyst. Det er vel rigtigt nok at jeg føler jeg bør, men hvad fanden har jeg rent faktisk lyst til? Jeg har ikke lyst til at bo i kollektivet. Har jeg lyst til at bo alene? Måske, men ikke med tanken om at jeg bare gav op på Iris. Jeg har jo egentlig bare lyst til at have det som jeg havde det indtil for et halvt år siden. Og det handler jo sådan set mere om nogle helt andre livsomstændigheder end min bopæl. Men jeg tror at den bedste vej dertil starter med at jeg flytter sammen med Iris. Om den slutter med noget andet kan jeg ikke vide. 
Selvom ovenstående er en fin logisk betragtning, er det nok stadig en god ide at jeg prøver at bruge lidt mere tid og energi på at fokusere på den hverdag jeg GERNE vil skabe sammen med Iris. Og det tænker jeg oplagt at begynde på i morgen.

Så er det også i morgen, jeg melder mig ledig igen. Jeg behøver ikke nødvendigvis sætte alting igang fra dag 1, men jeg synes som minimum jeg bør lægge en plan i morgen for hvordan jeg vil takle de kommende mdr på den front. 

OK. Så recap af ting jeg vil følge op på:
- I morgen sætter jeg mig og skriver lidt ift. hvordan jeg bedst kan gøre noget positivt for min og Iris relation.
- I morgen lægger jeg også en videre plan for hvornår jeg sætter mig med diverse arbejdsting og får meldt mig ledig.
- Scripting bliver EFTER ovenstående og hvis jeg vurdere det er en dårlig ide ift. Iris, så gemmer vi det til tirsdag, hvorfra jeg kommer til at have mere tid.
- Få lavet alf.


27-04-26
Kom til at scripte lidt først, men no harm done. Lad os kigge lidt ind i planerne. Jeg sagde ikke noget i går. Tror torsdag ifm fixe faxe er et fint tidspunkt, hvor toppen er samlet igen.

Jeg bør ikke scripte mere før i morgen. Der er et par andre ting, jeg bør fokusere på i dag. Navnligt Iris og at begynde at sige arbejde/erhvervspraktik igen. Så lad os bare komme igang.

Lad os starte med Iris. Min gejst ift. Iris er gået lidt op og ned gennem de snart 2 år vi har kendt hinanden. Det er ret normalt med følelser og uanset hvem jeg var sammen med er det forventeligt at den slags sker. Oven i det vil mine egne omstændigheder uundgåeligt også påvirke mine relationer mere generelt. Så som jeg tidligere har været inde på tænker jeg ikke vi skal tolke det aktuelle dip i mine følelser som noget større på nuværende tidspunkt, men mere et opmærksomhedspunkt jeg kan arbejde med. Det mere relevante spørgsmål er: "Hvad kan jeg gøre for at mine følelser for Iris er der, hvor jeg gerne vil have dem?" Lad os starte med at brainstorme lidt:
- Undgå de mest distraherende hjerneaktiviteter op til at vi ser hinanden
- Undgå onani op til at vi skal være intime
- Sørge for selv at komme med en god energi og initiativ til ting jeg gerne vil lave sammen med Iris
- Finde ting i Iris liv der faktisk interesserer mig og spørge aktivt ind til dem
- Sørge for at være glad og have god energi generelt
- Have gjort mig nogle tanker om hvad jeg glæder mig til og synes kunne være fedt ved at bo sammen med hende
- Have lavet nogle ting, der er mere spændende at fortælle Iris om.
- Have højere grad af fokus på de ting jeg værdsætter ved Iris end de ting der gør mig mere i tvivl

De første 2 er mere generelle og ikke noget jeg kan ændre så meget på ift. i dag. De andre kunne jeg godt gå lidt mere i detaljer med. 

Det er meget oplagt at starte med hvad jeg har lyst til at vi laver sammen i dag. Vi tager ud og klatrer i dag. Hvad har jeg mere lyst til at der skal ske i dag? Jeg ved det faktisk ikke rigtigt. Vejret er mellem. Der er måske ikke så meget at sige til at det er svært at finde den store gejst frem, når jeg ikke engang kan finde noget jeg selv har lyst til ud over at sidde alene med min computer. Nå... men hvis jeg ikke kan komme på noget andet jeg vil i dag, så kan vi jo bare finde noget mad og måske en film/serie for nu. Næste gang vi skal ses synes jeg dog godt, jeg kunne prøve at tænke over det i lidt bedre tid og finde noget jeg godt kunne tænke mig at prøve sammen med Iris. Jeg kunne f.eks. spørge om ikke vi skal prøve Go-monkey på et tidspunkt? Og finde et tidspunkt at se Hail Marry.

Jeg kunne egentlig godt tænke mig at vide lidt mere om hvordan Iris dagligdag foregår mere praktisk. Både på hendes arbejde med social sundhed, men også hvordan det typisk foregår ift. hendes studie og processen der. Under forudsætning af at hun ikke har mere lyst til at tale om noget andet.

Glæde og god energi generelt er lettere sagt end gjort her og nu. Jeg tror det bedste jeg kan gøre på den korte bane er at prøve at fake det, forstået på den måde at hvis jeg styrer mit fokus på en god måde så smitter det også af på mit faktiske humør og energi.

Hvad glæder jeg mig til ved at flytte sammen med Iris? 
- Jeg glæder mig til at sidde på terassen sammen i solen og nyde roen og noget koldt at drikke sammen.
- Jeg glæder mig til at kunne sove sammen oftere.
- Jeg glæder mig til at have mere indflydelse på hvordan tingene foregår i hjemmet.
- Jeg glæder mig til at der er mere ro omkring mig.
- Jeg glæder mig til at kunne spille en masse musik for Iris
- Jeg glæder mig til at invitere venner over sammen

Tænker det er fint for nu. Sørg for at sige de her ting højt. Både for Iris og for dig selv. Fokus kommer ikke automatisk. Sørg også for at få sagt flere ting højt som de værdsætter ved Iris. Også selvom det er åbenlyst. Det er altid rart at høre.

Hvad kan jeg lave af spændende ting at fortælle Iris om? Tja... jeg skal til at finde et godt praktiksted. Jeg når nok ikke så meget inden vi skal ses, men jeg tænker det kunne være et godt sted at starte.

Højere grad af fokus på de ting jeg værdsætter ved Iris relativt til de ting, der gør mig usikker. Jeg tænker der er rigtig mange ting at tage fat i her, men måske bare nogle få pointers til i dag? 
- Jeg værdsætter at Iris er helt fantastisk til at vise affektion med sin fysik. Måden hun krammer min arm, nusser mig og søger mig er rigtig dejligt.
- Jeg værdsætter Iris kæmpe empatiske side og alt hendes omsorg
- Jeg værdsætter at Iris ikke hænger sig i bagateller og at hun accepterer mig som jeg er.
- Jeg værdsætter at Iris har en flot krop, der er dejlig at røre ved og nogle dejlige bløde bryster som hun godt kan lide at jeg kærtegner.
- Jeg værdsætter at Iris har lyst til at flytte sammen med mig
- Jeg værdsætter at Iris godt kan lide at klatre, sove længe, se film/serier, høre om hvad der interesserer mig og at hun kan med mine venner/familie og omvendt.
- Jeg værdsætter at Iris har en skøn familie.
- Jeg værdsætter at Iris er så accepterende rent sexuelt.

Så er der det med at kigge på andre flotte piger. Det har været en stor udfordring fra starten af og det kommer nok til at fylde mere her til sommer i takt med at folk har mindre tøj på. Jeg tror godt jeg kan arbejde med nogle ting, der kan gøre Iris mere tiltrækkende for mig. Men det vil næppe fjerne trangen til at kigge efter andre. Det er der jo nok i virkeligheden ikke noget der vil. Så spørgsmålet er hvordan jeg kan kigge uden at det medfører mindre begejstring for Iris? Hmm... statistisk set vil langt de fleste af dem jeg kigger på mangle en lang række kvaliteter, som hvis jeg kendte til dem ville gøre dem væsentligt mindre atraktive. Så en teknik kunne være at prøve at fokusere på hvad der formentligt er galt med vedkommende. Jeg tror det er et område jeg bør arbejde ret meget med den kommende tid, for selvom det er svært at ændre på er det også noget der kan fylde ret meget.

Okay. Fine tanker. Tror ikke der er plads til meget mere i hovedet på én gang, så lad os vende tilbage og samle pointerne og tage et billede inden vi mødes med Iris senere. Så kan vi lige tage noget mad nu og få kigget på de andre ting.

Okay. Arbejdssituation. Lad os gøre det relativt kort for nu. Det handler jo egentlig bare om at skal lægge en plan for hvornår jeg vil kigge på ting, ikke at jeg skal kigge på det hele nu. Jeg kan godt gå ind og melde mig ledig. Derefter er der en række ting, der giver mening at kigge på i løbet af ugen
- Melde mig ledig
- Opdatere linked-in
- Opdatere joblog med ansøgninger
- Brainstorme over potentielt oplagte steder til erhvervspraktik.

Der er 2 mdr til sommerferien starter. Hvis jeg skal i erhvervspraktik skal det slutte inden d. 1. juli tænker jeg. Så med det i mente giver det ret god mening at gå mere helhjertet ind i nu. Hvis ikke jeg finder noget inden for den næste måned så kommer det nok til at passe ret fint med at jeg bare er på dagpenge til sommerferien slutter. Så jeg synes egentlig det giver mening at vi ikke bare brainstormer, men også fuldt ud tager teten og finder ud af hvad der er af muligheder. Hvis det skal komme ordentligt i gang er der nok et par ting der skal være opfyldt:
- Det skal ske inden jeg får en masse andet i hovedet med bl.a. scripting
- Jeg skal være i et godt mood og relativt udhvilet og veloplagt. 
- Jeg skal ikke være alt for distraheret af andre ting.
En idé kunne være at tage min computer med over til Iris med det formål at få kigget på det inden jeg tager hjem og se om den luftforandring kan et eller andet. Enten ved Iris eller ved Frederikke. Jeg tænker i hvert fald at i morgen kunne være et ret godt tidspunkt at komme igang. Lad os satse på det. Hvis jeg er god kan jeg igangsætte alle de ting jeg skal på én gang i morgen, så det eneste jeg behøver resten af ugen er at følge op på diverse beskeder.

Okay. Rigtig fint. Lad os lige få alfet nu, så vi kan nå det inden vi smutter og så komme afsted.



- Jeg kunne f.eks. spørge om ikke vi skal prøve Go-monkey på et tidspunkt? Og finde et tidspunkt at se Hail Marry.
- Snak om hun har gode ideer til at søge erhvervspraktik
- spørg mere specifikt til hvordan dagligdagen foregår på hendes arbejde og studie
- Fake god energi og humør, så kommer det ægte.
- Sig det højt, når Iris gør dig glad
- Fokuser på de ting du værdsætter ved Iris


28-04-26
Synes egentlig generelt ovenstående gik ret fint. Det var ikke nødvendigvis en revolution, men bare det at møde op og prøve at fake god energi og humør for at fremprovokere det virkede bare rigtig godt. Så lad os satse videre på det fremover. Nu går der over en uge før jeg skal ses med Iris igen og jeg har i det hele taget ret god tid til projekter, den kommende uge. Jeg har jo egentlig planlagt at kigge på mulig erhvervspraktisk lige nu. Er jeg motiveret for det? Ikke sådan rigtigt... Meh... 


29-04-26
Iris har spurgt om vi skal sidde sammen i eftermiddag og jeg tænker det er en oplagt mulighed for at komme igang med jobting.

Okay. Jeg er hermed meldt ledig. Lad os brainstorme lidt. Jeg tænker ikke at jeg kommer til at bruge kræfter på at søge "rigtige" jobs medmindre der faktisk er noget der giver mening at søge. I stedet tænker jeg bare jeg skal række ud og skrive til steder der potentielt kunne have relavans, særligt ift. erhvervspraktik. Så i første omgang handler det nok bare om at lave en god liste af sådanne relevante steder eller personer jeg kunne kontakte for at få inspiration og så tage den derfra. Jeg kan også oplagt lige se hvad jeg har skrevet ned fra sidst jeg havde online møde med jobcentret.

# todo
- "søg" 1 job
- søg om udbetaling af dagpenge fra marts.
- lav liste over personer/steder jeg bør kontakte
- find noter fra sidste møde



Hmm... Lad os lige hoppe i bad en gang og så overveje om vi skal sige i dag at vi flytter. 

30-04-26
Så fik jeg det sagt. Det føltes stadig mærkeligt, men tror det var godt jeg fik det gjort.