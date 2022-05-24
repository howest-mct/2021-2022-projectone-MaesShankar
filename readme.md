# Project One - Alco-CarLock

My project this year is an alcohol lock for in the car. It is a safety for people who drink and drive to much. I'm going to let the driver blow in to the sensor and see if he drank to much. If so, the car won't start for at least 3h. You have to identify yourself with a badge to see who wants to drive and it can' be manipulated by someone else. The temperature will be measured while the driver blows, that is not necessary but I'm going to use the data to see if there is a connection between alcohol usage and the temperature. There will be a dc motor to test and show the result of my project but it is the meaning to implement it in to a car. 

If u are an extern person you can look at the Ip adress on the device, make sure you're connected to the same network and lookup the ip address in your browser.



## Sparringspartner
Kato Borms
## Inhoud
### Starting with Fritzing
I'm going to start with my fritzing scheme, I made a scheme on paper to see if I connected something wrong, now it is easier to digitalise. I wrote down the types
of my sensors and other components so I can look them up in fritzing. I am waiting for approval.
Got approval with following changes:
- Forgot pullup with DS18B20
- 2 connections got lost at mcp3008
- MQ3 component is not drawn well
- Bit cleaner

### Doing my database in the meantime
In the meantime I made a ERD scheme for my database. The tables are made, now just fill them up with dummy data. I opened an excel to list the dummy data easily and filled it in my tables. While I tried to dump my file to show it to my teachers I saw that I got an error. So I read the error and it seemed like the version of my dump.exe file was less recent then my server version so I changed the path to a newer version of the dump.exe that I downloaded online.
### Website with connection to database
I made a small boilerplate where I'm going to send my history tabel, I'm trying to make connection but there is a problem with my endpoint.
It got fixed, now I managed to get my history on the web and I got live data from my temperature sensor.
## Instructables
Plaats zeker een link naar de Instructables zodat het project kan nagebouwd worden!



# Voor mezelf om te onthouden:
Zoals je kan zien is er geen "vaste" structuur voor zo'n document. Je bepaalt zelf hoe je het bestand via markdown structureert. Zorg ervoor dat het document minimaal op volgende vragen een antwoord biedt.

- Wat is de structuur van het project?
- Wat moet er gebeuren met de database? Hoe krijgt de persoon dit up and running?
- Moeten er settings worden veranderd in de backend code voor de database? 
- Runt de back- en front-end code direct? Of moeten er nog commando's worden ingegeven?
- Zijn er poorten die extra aandacht vereisen in de back- en/of front-end code?
Op github vind je verschillende voorbeelden hoe je een readme.md bestand kan structureren.
- [Voorbeeld 1](https://github.com/othneildrew/Best-README-Template)
- [Voorbeeld 2](https://github.com/tsungtwu/flask-example/blob/master/README.md)
- [Voorbeeld 3](https://github.com/twbs/bootstrap/blob/main/README.md)
- [Voorbeeld 4](https://www.makeareadme.com/)
