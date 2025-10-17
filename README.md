# Assist-sovellus / Thierry Kaoneka
Kurssiprojektini on sovellus nimeltään Assist. Assist on perus palvelunmyynti palvelu, eli käyttäjä voivat myydä itse tehtyjä palveluja tai tuotteita:

* Käyttäjä voi luoda tunnuksen sekä kirjautua siihen sisään ja ulos
* Käyttäjä voi julkaista myytävän palvelun (esim. asunnon siivous tai tpaidan painotus) tai tuotteita (esim. itse tehtyjä vaatteita), sekä muokata ja poistaa niitä
* Käyttäjä voi etsiä palveluita sekä haun kautta että sovelluksen omien kategoreiten kautta
* Käyttäjä voi viestitellä myyjän kanssa
* Myyjä voi pistää tarjouksen omaan palveluun halutessa
* Käyttäjät voi myös julkaista tavallisia tekstijulkaisuja info-tilaisuuksia varten
* Käyttäjä voi tykätä ja tallentaa palveluita sekä jättää arvioinnin ostaessa palvelun
* Sovelluksen käyttäjät voi luoda käyttäjätunnuksen sekä muokata oman käyttäjäsivun tiedot (esim. profiiilikuva ja bio)
* Käyttäjä voi seurata myyjiä 
* Koska sovellus on suhteellisen ameteurinen, sovelluksessa ei aio olla maksutapoja, mahdollisuutta lisätä esim. IBAN-tunnuksen myyjänä, vahvan tunnistautumisen tai muuta tarvittavia piirteitä tai henkilötietoja kauppa-sovelluksissa

Välipalautus 2 (21.09.2025)
Sovellus toimii palautuksen vaatimuksien mukaisesti, mutta on bugeja:

* Käyttäjä voi luoda tunnuksen, sekä kirjautua sisään ja ulos
* Käyttäjä ei voi kirjautua sisään väärillä tunnuksilla tai luoda tilin vaatimuksien ulkopuolella
* Käyttäjä voi luoda, muokata ja poistaa tietokohteita eli tuotteita
* Käyttäjä näkee muiden luomat tuotteet
* Käyttäjä pystyy hakemaan tuotteita hakusanalla

* Tuotteen muokkaamisella ja poistamisella on bugi. Nämä sovelluksen reitit eivät tarkista jos tuotetta muokkaava/poistava on omistaja
* Sovelluksessa on valmiiksi laitettu käyttäjäsivu ja pikkukuva piirteet, jotka eivät vielä toimi
* Sovelluksessa ei ole vikailmoituksia esim. kun kirjautumisessa on virhe
* Tuotteen muokkaus sivulta ei pääse pois ellei täytät kaikki laatikot, vaikka et haluakkaan muokata tuotetta

Välipalautus 3 (5.10.2025)
Sovellus toimi palautuksen vaatimuksien mukaisesti:
* Käyttäjä pystyy katsomaan käyttäjäsivuja, missä näkyy eri tilastoja; kuinka monta tuotetta, tykkäystä ja arviointia käyttäjä on tehnyt (sekä arviointien KA)
* Käyttäjä voi valita useamman luokan tuote-tietokohteelle
* Käyttäjä pystyy lähettämään toisin käyttäjän tietokohteeseen lisätietoa (eli arvioinnit), sekä viestitellä myyjän kanssa
* Sovellus tarkistaa käyttäjän CSRF-tokenia, jolloin hän voi (tai ei voi) lisätä, muokata tai poistaa tietokohteita kuten tarkoitettu

  Sovelluksen bugit:
* Poistaessa tuotteen, käyttäjä ei voi selailla omia tekemiä tietokohteita enään (tämä johtuu bugista forum-koodissa)
* Käyttäjä ei saa virheilmoitusta kun tekee jokin virhe kirjautumisessa/rekistöröinnissä, vaikka on lisätty flash-piirre
* Jokin viestiketjun sisällöt eivät lataannu kunnolla
* Sovelluksen pikku- ja profiilikuva piirteet eivät vieläkään toimi

Saat sovelluksen toimimaan näin:
1. Kloonaa repositorion
2. Avaa Bash ja kirjoita seuraavat komennot:
- **cd Assist-sovellus-main**
- **python3 -m venv venv**
- **source venv/bin/activate**
- **pip install flask**
- **sqlite3 database.db < assist.sql**
- **flask run**