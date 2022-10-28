
test_dict = { 
    
    'G1':["Teksupport_OTB: Adriatique, Brian Cid", "Watergate Nacht with Butch Anja Schneider La Fleur Jimi Jules &more",
    "Backdrop with Dax J (Monnom Black), Dr. Joseph & Simon.", "Jan Beuving & Patrick Nederkoorn - Leuker Kunnen We Het Niet Maken",
    "Rated R - Classic R&B/Future Jams with DJ Rob Pursey & Andy P"],

    'G2':["P!nk - Strikes back", "Pink - Beautiful Trauma World Tour", " The Magnificent European Tour of 7Б", "7B - A Russian Sensation @Paris",
    "Adriaan de Roover - SoundCloud", "Oaktree - Voor Damiaan Concert at Amsterdam Central", "P!NK | St. Louis, Missouri"],

    'G3':["Arsenal F.C. vs Manchester United", "Arsenal vs Tottenham Hotspurs", "Arsenal - Melvin (Live - Antwerp - April 2014)",
    "Arsenal Concerts Tour, next Setlist 2022 - Concerty"],

    'G4':["Aaron Copland's The Empire Strikes Back on 21/10/2019", "Aaron Goldberg and his Uncoventional words of Wisdom",
    "Adam F says Hallelujah", "Adam Faith - The Reverend who couldnt stay faithful"],

    'P1':["Alex the Astronaut & Stella Donnelly - Adelaide, SA", "Julien Baker at The Burl", "SWING pres. Sam Paganini & Zøe",
    "Dinosaur Jr Unoffical After Party", "Ed Sheeran at CenturyLink Field!"],

    'P2':["Backdrop with Dax J (Monnom Black), Dr. Joseph & Simon.", "Rated R - Classic R&B/Future Jams with DJ Rob Pursey & Andy P",
    "Kendrick Lamar, SZA & Schoolboy Q - Ridgefield, WA", "Murth Mossel & Roué Verveer", "Daniël Arends"],

    'P3':["Foreigner / Whitesnake & Jason Bonham's Led Zep Evening", "Trevor Noah - Forum, København - fredag 8. juni", 
    "Jenna & Barbara Bush: Sisters First Tour", "Hommage à Pink Floyd chez Cécile et Ramone!", "Szorgalmas és Rest lány - RS9 Vallai Kert",
    "Keys n Krates: Europe Cura Album Tour", "Christian Löffler und Ensemble"],

    'L1':["Düsseldorf", "Morcheeba", "Cirque Du Soleil", "Mount Kimbie at The Velvet | May 19", "Fresku TheaterCollege", 
    "Los Temerarios en Visalia, CA", "Punnany Massif TavaCity Túr ’18", "Florida Georgia Line"],

    'L2':["Queen & Adam Lambert | Barclaycard Arena Hamburg", "O´Funkillo en Santander", "Mount Kimbie at The Velvet | May 19",
    "Maroon 5 Concert at Bankers Life Fieldhouse in Indianapolis, IN", "Tank and the Bangas w/ Maggie Koerner at Scoot Inn on Sat 4/7!"],

    'L3':["SOLD OUT: Billie Eilish at Heaven - London", "Max Nek Renga - Roma", "FISH! // JATE Klub, Szeged"],

    'L4':["Teksupport_OTB: Adriatique, Brian Cid", "Budapest Bár - Itt van a város turné Szombathely", "Barcelona vs Villarreal"],

    'L5':["Billy Joel in Tampa (Feb 9)", "Dash Café: Europe's Kitchen Table. Part of Eutopia", "SKID ROW ✦ Live at Druso BG",
    "Chris Young, Kane Brown, Morgan Evans - La Crosse, WI", "Kamasi Washington in Paradiso"],

    'L6':["DAFT PUNK Tribute Show @LA DAME Club / Ven 9 Fév. 2018", "Pablo López - Santa Libertad Tour",
    "DIDDY & TREY SONGZ ALL STAR WEEKEND @ BELASCO w/ Special Guests", "Fatoumata Diawara // Philharmonie Luxembourg"],

    'O1':["Steely Dan & The Doobie Brothers at Ascend Amphitheater", "Partido Valencia CF - FC Barcelona", 
    "Dubfire / Johnny Trika (Live) / Shades of Blk", "The Wave Pictures | Leamington", "The Dandy Warhols - Brooklyn, NY",
    "Broken Brass Ensemble"],

    'O2':["PNB Rock - Catch These Vibes Tour", "TOTO live in Zagreb", "OASIS Fans Reunion - ROMA", "Steven Curtis Chapman SOLO - Allen, TX",
    "CYNT w. Horse Meat Disco", "TEDE / PL | Chapeau Rouge, Praha Tourrrne"],

    'O3':["TEDE / PL | Chapeau Rouge, Praha Tourrrne", "WePlay 28.02 TikTokKiss // Magda Aliena & EFFE", "Shakey Graves with Jose Gonzalez & The Brite Lites",
    "Sanction x Trouve Grooves w/ Amine Edge & Dance", "Dillon Francis at Bootshaus pres. by Loonyland"],

    'O4':["Phlake i Roskilde Kongrescenter", "The Doors Pub", "Butcher Babies", "Agar Agar & Saint DX", "The Head & The Heart",
    "Reverend Horton Heat - O2 Academy Islington", "Venom Inc & Suffocation"],

    'O5':["Clowns Celebrate Love w/ Matchmaker Sasha Silberberg", "SHINE Green Velvet, Layton Giordani & Eclair Fifi",
    "Petit Biscuit | Variety Playhouse", "Insane Clown Posse and Attila at Funk 'n Waffles"],

    'M1':["First Aid Kit | Listening Party", "Royale Saturdays: Lost Frequencies | 2.24.18", "The Dire Straits Experience",
    "SHINE Green Velvet, Layton Giordani & Eclair Fifi", "Yellow Claw - SA 28.04. - Prater DOME Vienna"],

    'M2':["Peja/Slums Attack 03/03/18 Malbork, Dolek Klub", "Modern Life Is War • Cro-Mags • PARIS • 22 Juin 2018", "Metalmania - Metalica Show",
    "Stick To Your Guns & Being As An Ocean – Brisbane Lic AA", "Berlin And The Beat/ Sa, 24.3./ Spindler&Klatt"],

    'M3':["Clara Luzia 'When I Take To The Streets Tour 2018'", "Future Ritual II", "Interment * I Am Destruction * Gruesome Fate",
    "Halestorm + In This Moment w/ New Years Day, Stitched Up Heart", "The Little Mix Experience"],

    'M4':["Lack Of Afro - Full Band at The Parish", "Sum 41: Does This Look Infected 15th Anniversary Tour at Brooklyn Bowl Las Vegas",
    "G-Eazy - Live at Radio City", "Shortcut Europe: Exploring Cultural Spaces", "The Gin & Rum Festival", "Trace Adkins: How Did We Get Here Tour",
    "Opening Night with Diana Ross", "Full Noise - After Party at Whammy Backroom", "Drake Party At VICE - Tuesday"],

    'M5':["The Pink Floyd Sound - Climb Towards The Light + DVD presentatie", "Kamasi Washington in Paard", "Kiss The Tempo with Seff, Tim Baresko & Ben Jones",
    "Jo Koy: Break The Mold Tour - Sold Out", "Eddie Izzard: Believe Me Tour"],

    'M6':["TOKiMONSTA at Kingdom", "Heidi Piiroinen: Ohikuljetut – Erään kerjäläisperheen tarina", "Fight Night Present: Mall Grab's Nonstop Feeling Tour",
    "Eddie Izzard LIVE in Delaware", "Lyle Lovett And His Large Band at ACL Live", "FISH", "Kid Rock at Bi-Mart Willamette Country Music Festival",
    "San Diego, California Full Day Experiential Workshop"],

    'D1':["Dying Fetus and Thy Art Is Murder at The Crofoot Ballroom 3/20", "Kiss All Hipsters | Vintage Fangs | Melkweg A'dam | Sat Jan 13",
    "Peja/Slums Attack 03/03/18 Malbork, Dolek Klub", "Gorillaz live a Lucca • 12 luglio", "Lytos en Barcelona - 7:11 tour",
    "Royale Saturdays: Lost Frequencies | 2.24.18", "Paramore Pre & After Party - 50% Off Drinks Before 8pm",
    "Ania Dąbrowska - The Best Of, Klub Stodoła, 15.04.2018", "Boosie Badazz with Webbie & Yung Bleu March 23 at The Cotillion"]

}
