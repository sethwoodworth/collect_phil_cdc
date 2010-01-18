DROP TABLE IF EXISTS hires_status;
CREATE TABLE IF NOT EXISTS `hires_status` (
	id INTEGER NOT NULL, 
	status BOOLEAN, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS lores_status;
CREATE TABLE IF NOT EXISTS `lores_status` (
	id INTEGER NOT NULL, 
	status BOOLEAN, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS phil;
CREATE TABLE IF NOT EXISTS `phil` (
	id INTEGER NOT NULL, 
	`desc` TEXT, 
	categories TEXT, 
	credit TEXT, 
	links TEXT, 
	provider TEXT, 
	source TEXT, 
	url_to_hires_img TEXT, 
	url_to_lores_img TEXT, 
	url_to_thumb_img TEXT, 
	copyright TEXT, 
	creation TEXT, 
	access_time TIMESTAMP, 
	PRIMARY KEY (id)
);
INSERT INTO phil VALUES(1,'''<td><b>Data tape storage room</b><p>Data tape storage room, NCHS.</p></td>''','u''\n0 CDC Organization\n1 Locations\n2 CDC Buildings and Facilities\n0 MeSH\n1 Anthropology, Education, Sociology and Social Phenomena\n2 Social Sciences\n3 Government\n4 Government Agencies\n5 United States Dept. of Health and Human Services\n6 United States Public Health Service\n7 Centers for Disease Control and Prevention (U.S.)\n1 Health Care\n2 Health Care Economics and Organizations\n3 Organizations\n4 Government Agencies\n5 United States Dept. of Health and Human Services\n6 United States Public Health Service\n7 Centers for Disease Control and Prevention (U.S.)''','','','CDC','','http://phil.cdc.gov/phil_images/20031003/3/PHIL_1.tif','http://phil.cdc.gov/phil_images/20031003/3/PHIL_1_lores.jpg','http://phil.cdc.gov/phil_images/20031003/3/PHIL_1_thumb.jpg','''<td><b>None</b> - This image is in the public domain and thus free of any copyright restrictions. As a matter of courtesy we request that the content provider be credited and notified in any public or private usage of this image.</td>''',NULL,'2010-01-17 00:40:59.537985');
INSERT INTO phil VALUES(2,'''<td><b>Hantavirus field studies</b><p>CDC scientist collecting specimens from trapped rodents.</p></td>''','u''\n0 CDC Organization\n1 Roles\n2 CDC Health Personnel\n0 MeSH\n1 Anthropology, Education, Sociology and Social Phenomena\n2 Social Sciences\n3 Government\n4 Government Agencies\n5 United States Dept. of Health and Human Services\n6 United States Public Health Service\n7 Centers for Disease Control and Prevention (U.S.)\n1 Diseases\n2 Animal Diseases\n2 Virus Diseases\n3 RNA Virus Infections\n4 Bunyaviridae Infections\n5 Hantavirus Infections\n1 Geographic Locations\n2 Geographic Locations\n3 Americas\n4 North America\n5 United States\n6 Southwestern United States\n7 New Mexico\n1 Health Care\n2 Health Care Economics and Organizations\n3 Organizations\n4 Government Agencies\n5 United States Dept. of Health and Human Services\n6 United States Public Health Service\n7 Centers for Disease Control and Prevention (U.S.)\n1 Organisms\n2 Animals\n3 Chordata\n4 Vertebrates\n5 Mammals\n6 Rodentia''','','','CDC/ Cheryl Tryon','','http://phil.cdc.gov/PHIL_Images/02112002/00033/PHIL_2.tif','http://phil.cdc.gov/PHIL_Images/02112002/00033/PHIL_2_lores.jpg','http://phil.cdc.gov/PHIL_Images/02112002/00033/PHIL_2_thumb.jpg','''<td><b>None</b> - This image is in the public domain and thus free of any copyright restrictions. As a matter of courtesy we request that the content provider be credited and notified in any public or private usage of this image.</td>''','1993','2010-01-17 00:41:01.031667');
INSERT INTO phil VALUES(3,'''<td><b>Boy with smallpox.</b><p>Boy with smallpox.  Face.</p></td>''','u''\n0 CDC Organization\n0 MeSH\n1 Anatomy\n2 Integumentary System\n3 Skin\n1 Diseases\n2 Virus Diseases\n3 DNA Virus Infections\n4 Poxviridae Infections\n1 Organisms\n2 Viruses\n3 DNA Viruses\n3 Vertebrate Viruses\n4 DNA Viruses\n1 Persons\n2 Persons\n3 Age Groups\n4 Child''','','\'[(u''CDC Responds: Smallpox: What Every Clinician Should Know'', u''http://www.sph.unc.edu/about/webcasts/2001-12-13_smallpox/''), (u''CDC - National Immunization Program: Smallpox'', u''http://www.bt.cdc.gov/agent/smallpox/index.asp'')]\'','CDC','','http://phil.cdc.gov/PHIL_Images/02112002/00045/PHIL_3.tif','http://phil.cdc.gov/PHIL_Images/02112002/00045/PHIL_3_lores.jpg','http://phil.cdc.gov/PHIL_Images/02112002/00045/PHIL_3_thumb.jpg','''<td><b>None</b> - This image is in the public domain and thus free of any copyright restrictions. As a matter of courtesy we request that the content provider be credited and notified in any public or private usage of this image.</td>''',NULL,'2010-01-17 00:41:02.684013');
INSERT INTO phil VALUES(4,'''<td><b>Motor vehicle accident scene</b><p>Motor vehicle accident scene.</p></td>''','u''\n0 CDC Organization\n0 MeSH\n1 Geographic Locations\n2 Geographic Locations\n3 Americas\n4 North America\n5 United States\n6 Appalachian Region\n7 Georgia\n6 Southeastern United States\n7 Georgia\n1 Technology and Food and Beverages\n2 Technology, Industry, and Agriculture\n3 Transportation\n4 Motor Vehicles''','','','CDC/ James Gathany','','http://phil.cdc.gov/phil_images/20031003/2/PHIL_4.tif','http://phil.cdc.gov/phil_images/20031003/2/PHIL_4_lores.jpg','http://phil.cdc.gov/phil_images/20031003/2/PHIL_4_thumb.jpg','''<td><b>None</b> - This image is in the public domain and thus free of any copyright restrictions. As a matter of courtesy we request that the content provider be credited and notified in any public or private usage of this image.</td>''',NULL,'2010-01-17 00:41:04.051412');
DROP TABLE IF EXISTS thumb_status;
CREATE TABLE IF NOT EXISTS `thumb_status` (
	id INTEGER NOT NULL, 
	status BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO thumb_status VALUES(1,1);
INSERT INTO thumb_status VALUES(2,1);
INSERT INTO thumb_status VALUES(3,1);
INSERT INTO thumb_status VALUES(4,1);
