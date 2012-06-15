# -*- coding: utf-8 -*-

import sqlite3, os
#name = "Bush"

# Create table

initQuery = """CREATE TABLE Names (
id INTEGER PRIMARY KEY, 
file_Name VARCHAR(50),
last_Name VARCHAR(50) default null,
first_and_Last_Name VARCHAR(50) default null,
entire_Name VARCHAR(50),
nickname VARCHAR(50) default null, 
extra VARCHAR(50) default null,
title VARCHAR(50) default null
)"""


data = (
	('afghanistan.png', 'Afghanistans', 'null', 'Afghanistan',  'null',  'null',  'null'),
	('bulgarien.png',  'Bulgariens',  'null', 'Bulgarien',  'null',  'null', 'null'),
	('burma.png', 'Burma', 'Burmas', '',  'null',  'null',  'null'),
	('danmark.jpg',  'Konungariket Danmark',  'Danmarks', 'Danmark',  'Konungarikets Danmark',  'Konungariket Danmarks',  'null'),
	('george_bush.jpg','Bush','George Bush','George W Bush','Dubya','Miserable Failure', 'President Bush'),
	('bill_clinton.jpg','Clinton','Bill Clinton','William J Clinton','Bill J Clinton','William Jefferson Clinton', 'President Clinton'),
	('gordon_brown','Brown','Gordon Brown','J Gordon Brown','The Right Honorable Gordon Brown','James Gordon Brown', 'Premiärminister Brown'),
	('hillary_clinton.jpg', 'Rodham Clinton','Hillary Clinton','Hillary Rodham Clinton','Hillary Diane Rodham Clinton','Hillary D Rodham Clinton', 'Senator Clinton'),
	('england.jpg',  'null',  'null', 'England',  'Englands',  'null',  'null'),
	('etiopien.gif',  'null',  'null', 'Etiopien',  'Etiopiens',  'null',  'null'),
	('fatah.jpg',  'null',  'null', 'Fatah',  'null',  'null',  'null'),
	('finland.png',  'null',  'null', 'Finland',  'Finlands',  'null',  'null'),
	('FN.jpg',  'null',  'null', 'FN', 'Förenta Nationerna',  'FNs',  'Förenta Nationernas'),
	('fp.gif',  'null',  'null', 'Folkpartiet',  'Folkpartiets',  'FP',  'FPs'),
	('frankrike.gif',  'Franska Republiken',  'Frankrikes', 'Frankrike',  'Franska Republikens',  'Republiken Frankrike',  'Republiken Frankrikes'),
	('christer_fuglesang.jpg', 'Fuglesang', 'Christer Fuglesang', 'A Christer Fuglesang', 'Arne Christer Fuglesang', 'Rymdfararen Christer Fuglesang', 'Docent Fuglesang'),
	('goteborg.gif',  'Götets',  'Göteborgs', 'Göteborg', 'Götet', 'Västkustens Pärla',  'Västkustens Pärlas'),
	('hamas.jpg',  'null',  'null', 'Hamas',  'null',  'null',  'null'),
	('hizbollah.png',  'null',  'null', 'Hizbollah',  'Hizbollahs',  'null',  'null'),
	('saddam_hussein', 'Hussein', 'Saddam Hussein', 'Saddam Hussein Abd al-Majid al-Tikriti', 'Saddam', 'null', 'President Hussein'),
	('iran.jpg',  'null',  'null', 'Iran', 'Irans',  'null',  'null'),
	('israel.png',  'null',  'null', 'Israel', 'Israels',  'null',  'null'),
	('italien.gif',  'null',  'null', 'Italien',  'Italiens',  'null',  'null'),
	('irak.png',  'Republiken Irak',  'Iraks', 'Irak',  'Republiken Iraks',  'Republikens Irak',  'null'),
	('japan.gif',  'Kejsardömet Japans',  'Japans', 'Japan',  'Kejsardömet Japan',  'Kejsardömets Japan',  'null'),
	('carin_jamtin.jpg', 'Jämtin', 'Carin Jämtin', 'Carin Jämtin',  'null',  'null', 'Oppositionsborgarråd Jämtin'),
	('kd.gif',  'null',  'Kristdemokraterna', 'Kristdemokraterna',  'KD',  'KDs',  'null'),
	('kina.gif',  'Kina',  'Kinas', 'Folkrepubliken Kina',  'Folkrepublikens Kina',  'Folkrepubliken Kinas',  'null'),
	('henrik_larsson.jpg', 'Larsson', 'Henrik Larsson', 'E Henrik Larsson', 'Henke', 'Edvard Henrik Larsson',  'null'),
	('carolina_kluft.jpg', 'Klüft', 'Carolina Klüft', 'Carolina E Klüft', 'Carolina Evelyn Klüft', 'Friidrottaren Klüft',  'null'),
	('lars_leijonborg.jpg', 'Leijonborg', 'Lars Leijonborg', 'Lars E A Leijonborg', 'Lars Erik Ansgar Leijonborg', 'Folkpartisten Leijonborg', 'Partiledare Leijonborg'),
	('libanon.png',  'null',  'Libanons', 'Libanon',  'null',  'null',  'null'),
	('malmo.jpg',  'null',  'Malmös', 'Malmö',  'null',  'null',  'null'),
	('maud_olofsson.jpg', 'Olofsson', 'Maud E Olofsson', 'Maud Elizabeth Olofsson', 'Centerpartisten Olofsson', 'null','Partiledare Olofsson'),
	('john_mccain.jpg','McCain','John McCain','John S McCain','John Sidney McCain III','John S McCain III', 'Senator McCain'),
	('mp.jpg',  'Miljöpartiet De Grönas', 'Miljöpartiet De Gröna', 'Miljöpartiet',  'Miljöpartiets',  'Miljöpartiets De Gröna',  'null'),
	('nepal.png',  'Konungariket Nepal',  'Nepals', 'Nepal',  'Konungarikets Nepal',  'Konungarikets Nepal',  'null'),
	('nordkorea.png',  'null',  'Nordkoreas', 'Nordkorea',  'null',  'null',  'null'),
	('norge.gif',  'Konungariket Norge',  'Norges', 'Norge',  'Konungariket Norges',  'Konungarikets Norge',  'null'),
	('barack_obama.jpg','Obama','Barack Obama','Barack H Obama','Barack Hussein Obama Jr','Barack Hussein Obama', 'Senator Obama'),
	('ehud_olmert.jpg', 'Olmert', 'Ehud Olmert',  'null',  'null',  'null', 'Premiärminister Olmert'),
	('christian_olsson.jpg', 'Olsson', 'Christian Olsson', 'John Christian Bert Olsson', 'John Christian Olsson', 'Idrottaren Olsson',  'null'),
	('os.png',  'null',  'Olympiska Spelens', 'OS', 'Olympiska Spelen',  'null',  'null'),
	('pakistan.gif',  'null',  'null', 'Pakistan',  'Pakistans',  'null',  'null'),
	('paven.jpg','Benedictus','Benedictus XVI','Joseph Ratzinger','Joseph Alois Ratzinger','Påven', 'Påve Benedictus XVI'),
	('goran_persson.jpg','Persson','Göran Persson','H Göran Persson','Hans Göran Persson',  'null', 'Stadsminister Persson'),
	('vladimir_putin.jpg','Putin','Vladimir Putin','Vladimir V Putin','Vladimir Vladimirovich Putin','Premiärminister Putin', 'President Putin'),
	('anja_parson', 'Pärson', 'Anja Pärson', 'Anja Sofia Tess Pärson',  'null', 'Skidåkaren Anja Pärson',  'null'),
	('fredrik_reinfeldt.jpg','Reinfeldt','Fredrik ReinFeldt','J Fredrik Reinfeldt','John Fredrik Reinfeldt','Statsminister Reinfeldt', 'Statsministern'),
	('condoleezza_rice.jpg','Rice','Condoleezza Rice',  'null',  'null','Statssekreterare Condoleezza Rice', 'Statssekreterare Rice'),
	('ryssland.gif',  'null',  'null', 'Ryssland',  'Rysslands',  'Ryska Republiken',  'null'),
	('nicolas_sarkozy.jpg','Sarkozy','Nicolas Sarkozy', 'Nicolas P S Sarközy', 'Nicolas Paul Stéphane Sarközy de Nagy-Bocsa', 'Nicolas Sarközy', 'President Sarkozy'),
	('ariel_sharon.jpg', 'Sharon', 'Ariel Sharon',  'null', 'Arik', 'Ariel Scheinermann', 'Premiärminister Sharon'),
	('spanien.gif',  'Konungariket Spanien',  'Spaniens', 'Spanien',  'Konungariket Spaniens',  'null',  'null'),
	('socialdemokraterna.jpg',  'Socialdemokraternas',  'null', 'Socialdemokraterna',  'null', 'Sossarna',  'null'),
	('sudan.gif',  'null',  'null', 'Sudan',  'Sudans',  'null',  'null'),
	('sverige.png',  'Sveriges',  'Konungariket Sverige', 'Sverige',  'Konungariket Sveriges',  'Konungarikets Sverige',  'Sweden'),
	('turkiet.png',  'null',  'null', 'Turkiet',  'null',  'null',  'null'),
	('tyskland.gif',  'null',  'null' ,'Tyskland',  'null',  'null',  'null'),
	('ukraina.jpg',  'null',  'Ukrainas', 'Ukraina',  'null',  'null',  'null'),
	('umea.jpg',  'null',  'null', 'Umeå',  'null',  'null',  'null'),
	('usa.gif',  'null',  'USAs', 'USA', 'Amerikas Förenta Stater',  'Amerikas Förenta Staters',  'null'),
	('vitryssland.png',  'null',  'null', 'Vitryssland',  'Vitrysslands',  'null',  'null'),
	('maria_wetterstrand.jpg', 'Wetterstrand', 'Maria Wetterstrand', 'I Maria Wetterstrand', 'Ingrid Maria Wetterstrand',  'null', 'Riksdagsledamot Wetterstrand'),
	('zlatan.jpg', 'Ibrahimovic', 'Zlatan Ibrahimovic',  'null', 'Ibra', 'Zlatan',  'null' ),
	('drottningen.jpg','Silvia','Drottning Silvia', 'Silvia Sommerlath', 'Silvia Bernadotte', 'Svenska Drottningen', 'Drottningen'),
	('kronprinsessan.jpg','Viktoria','Prinsessan Viktoria', 'Kronprinsessan Viktoria',  'null',  'null', 'Kronprinsessan'),
	('kungen.jpg','Kung Carl Gustaf','Carl XVI Gustaf', 'Carl Gustaf Folke Hubertus', 'Carl Gustaf Folke Hubertus Bernadotte', 'Kung Carl XVI Gustaf', 'Kungen'),
	('prins_Carl_Philip.jpg','Prins Carl Philip','Carl Philip Edmund Bertil', 'Carl Philip Edmund Bertil Bernadotte', 'Prince Carl Philip Edmund Bertil Bernadotte', 'Motorprinsen', 'Prinsen'),
	('prins_gustaf_adolf.jpg','Prins Gustaf Adolf','Gustaf Adolf Bernadotte', 'Gustav Adolf Oscar Fredrik Arthur Edmund', 'Gustav Adolf Oscar Fredrik Arthur Edmund Bernadotte', 'Kungens Pappa',  'null'),
	('prinsessan_madeleine.jpg','Prinsessan Madeleine', 'Madeleine Thérèse Amelie Josephine',  'null', 'Madde', 'Prinsessan Madeleine Thérèse Amelie Josephine', 'Prinsessan'),
	('prinsessan_sibylla.jpg','Prinsessan Sibylla', 'Prinsessan Sibylla av Saxe-Coburg och Gotha',  'null',  'null',  'null',  'null')
	)


def name_ident(name):
    """Takes a name and matches it against any one of several aliases in a table, returns a filename"""
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_Name from Names WHERE last_Name =? OR first_and_Last_Name =?  OR entire_Name =? OR nickname = ? OR extra =? OR title=?', (name,name,name,name,name,name) )
    for row in cursor:
#        return ["proper_nouns/" + row[0]]
        return [row[0]]
    return ["NAME_NOT_FOUND"]

if __name__ == "__main__":
    if os.path.exists('names.db'):
        os.remove('names.db')
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute(initQuery)
    conn.commit()
    for t in data:
    	cursor.execute('INSERT INTO names VALUES (null,?,?,?,?,?,?,?)',t)
    		
    conn.commit()
