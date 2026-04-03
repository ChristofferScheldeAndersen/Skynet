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