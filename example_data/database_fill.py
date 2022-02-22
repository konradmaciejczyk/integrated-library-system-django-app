#Konrad Maciejczyk, 2021-2022
#Note: To use this script run in terminal: python3 manage.py shell < ./example_data/database_fill.py
from accounts.models import Citizenship, IDType, Occupation, User
from user_side.models import Status, Client
from worker_side.models import Author, Condition, Availability, Director, Publisher, Screenwriter, Book, Movie, SoundRecording
from django.db import connection
from datetime import date

def fill_accounts(citizenships=True, id_types=True, occupations=True, genders=True, *args, **kwargs):
    """Procedure for inserting data rows into SQL accounts table. 
    Parameters:
    citizenship=True, id_types=true, occupations=True, genders=True
    Returns:
    None"""

    citizenships_data = (('Afghan'), ('Albanian'), ('Algerian'), ('American'), ('Andorran'), ('Angolan'), ('Anguillan'), ('Argentine'), ('Armenian'), ('Australian'), ('Austrian'), ('Azerbaijani'), ('Bahamian'), ('Bahraini'), ('Bangladeshi'), ('Barbadian'), ('Belarusian'), ('Belgian'), ('Belizean'), ('Beninese'), ('Bermudian'), ('Bhutanese'), ('Bolivian'), ('Botswanan'), ('Brazilian'), ('British'), ('British Virgin Islander'), ('Bruneian'), ('Bulgarian'), ('Burkinan'), ('Burmese'), ('Burundian'), ('Cambodian'), ('Cameroonian'), ('Canadian'), ('Cape Verdean'), ('Cayman Islander'), ('Central African'), ('Chadian'), ('Chilean'), ('Chinese'), ('Citizen of Antigua and Barbuda'), ('Citizen of Bosnia and Herzegovina'), ('Citizen of Guinea-Bissau'), ('Citizen of Kiribati'), ('Citizen of Seychelles'), ('Citizen of the Dominican Republic'), ('Citizen of Vanuatu '), ('Colombian'), ('Comoran'), ('Congolese (Congo)'), ('Congolese (DRC)'), ('Cook Islander'), ('Costa Rican'), ('Croatian'), ('Cuban'), ('Cymraes'), ('Cymro'), ('Cypriot'), ('Czech'), ('Danish'), ('Djiboutian'), ('Dominican'), ('Dutch'), ('East Timorese'), ('Ecuadorean'), ('Egyptian'), ('Emirati'), ('English'), ('Equatorial Guinean'), ('Eritrean'), ('Estonian'), ('Ethiopian'), ('Faroese'), ('Fijian'), ('Filipino'), ('Finnish'), ('French'), ('Gabonese'), ('Gambian'), ('Georgian'), ('German'), ('Ghanaian'), ('Gibraltarian'), ('Greek'), ('Greenlandic'), ('Grenadian'), ('Guamanian'), ('Guatemalan'), ('Guinean'), ('Guyanese'), ('Haitian'), ('Honduran'), ('Hong Konger'), ('Hungarian'), ('Icelandic'), ('Indian'), ('Indonesian'), ('Iranian'), ('Iraqi'), ('Irish'), ('Israeli'), ('Italian'), ('Ivorian'), ('Jamaican'), ('Japanese'), ('Jordanian'), ('Kazakh'), ('Kenyan'), ('Kittitian'), ('Kosovan'), ('Kuwaiti'), ('Kyrgyz'), ('Lao'), ('Latvian'), ('Lebanese'), ('Liberian'), ('Libyan'), ('Liechtenstein citizen'), ('Lithuanian'), ('Luxembourger'), ('Macanese'), ('Macedonian'), ('Malagasy'), ('Malawian'), ('Malaysian'), ('Maldivian'), ('Malian'), ('Maltese'), ('Marshallese'), ('Martiniquais'), ('Mauritanian'), ('Mauritian'), ('Mexican'), ('Micronesian'), ('Moldovan'), ('Monegasque'), ('Mongolian'), ('Montenegrin'), ('Montserratian'), ('Moroccan'), ('Mosotho'), ('Mozambican'), ('Namibian'), ('Nauruan'), ('Nepalese'), ('New Zealander'), ('Nicaraguan'), ('Nigerian'), ('Nigerien'), ('Niuean'), ('North Korean'), ('Northern Irish'), ('Norwegian'), ('Omani'), ('Pakistani'), ('Palauan'), ('Palestinian'), ('Panamanian'), ('Papua New Guinean'), ('Paraguayan'), ('Peruvian'), ('Pitcairn Islander'), ('Polish'), ('Portuguese'), ('Prydeinig'), ('Puerto Rican'), ('Qatari'), ('Romanian'), ('Russian'), ('Rwandan'), ('Salvadorean'), ('Sammarinese'), ('Samoan'), ('Sao Tomean'), ('Saudi Arabian'), ('Scottish'), ('Senegalese'), ('Serbian'), ('Sierra Leonean'), ('Singaporean'), ('Slovak'), ('Slovenian'), ('Solomon Islander'), ('Somali'), ('South African'), ('South Korean'), ('South Sudanese'), ('Spanish'), ('Sri Lankan'), ('St Helenian'), ('St Lucian'), ('Stateless'), ('Sudanese'), ('Surinamese'), ('Swazi'), ('Swedish'), ('Swiss'), ('Syrian'), ('Taiwanese'), ('Tajik'), ('Tanzanian'), ('Thai'), ('Togolese'), ('Tongan'), ('Trinidadian'), ('Tristanian'), ('Tunisian'), ('Turkish'), ('Turkmen'), ('Turks and Caicos Islander'), ('Tuvaluan'), ('Ugandan'), ('Ukrainian'), ('Uruguayan'), ('Uzbek'), ('Vatican citizen'), ('Venezuelan'), ('Vietnamese'), ('Vincentian'), ('Wallisian'), ('Welsh'), ('Yemeni'), ('Zambian'), ('Zimbabwean'), ("Not selected"))
    id_types_data = (('ID Card'), ('Passport'))
    occupations_data = (('Student'), ('Academic teacher'), ('Other'))

    if citizenships:
        print(f'Starting to enter data rows into accounts_citizenship table.')
        for citizenship in citizenships_data:
            buff = Citizenship(name=citizenship)
            buff.save()
        print(f'{len(citizenships_data)} row(s) has been inserted into accounts_citizenship table.\n')

    if id_types:
        print(f'Starting to enter data rows into accounts_id_type table.')
        for id_type in id_types_data:
            buff = IDType(name=id_type)
            buff.save()
        print(f'{len(id_types_data)} row(s) has been inserted into accounts_id_type table.\n')

    if occupations:
        print(f'Starting to enter data rows into acounts_occupation table.')
        for occupation in occupations_data:
            buff = Occupation(name=occupation)
            buff.save()
        print(f'{len(occupations_data)} row(s) has been inserted into accounts_occupation table.\n')

def fill_worker_side(conditions=True, availabilities=True, authors=True, publishers=True, directors=True, screenwriters=True, books=True, movies=True, sr=True):
    """Procedure for inserting data rows into SQL worker_side tables. 
    Parameters:
    conditions=True, availabilities=True
    Returns:
    None"""

    conditions_data = (('Good'), ('Damaged'))
    availabilities_data = (('Available to borrow'), ('Library use only'), ('Not available'))
    authors_data = (("Terry Pratchett"), ("Adam Mickiewicz") , ("Henryk Sienkiewicz") , ("Stefan Żeromski"), ("Fyodor Dostoyevsky"), ("Stanisław Lem"))
    publishers_data = (("Prószyński i S-ka"), ("Wydawnictwo Literackie"), ("Wydawnictwo MG"), ('Walker'))
    directors_data = (('Stanley Kubrik'), ("Christopher Nolan"), ("Denis Villeneuve"), ("Darren Aronofsky"), ("Guillermo del Toro"))
    screenwriters_data = (('Jonathan Nolan'), ('Micheal Herr'), ("Stanley Kubrik"), ("Vince Gilligan"), ("Frank Darabont"), ("Peter Gould"))
    books_data = (('0802755267', 'Solaris', 'Stanisław Lem - Solaris', 1970, 'pages: 216', 1, 2, 'Walker', 'books_covers/Solaris_1.jpg', 'Stanisław Lem'),
    ('9780575070530', 'Roadside Picnic', 'Arkadij, Boris Strugackij - Roadside Picnic', 1970, 'pages: 145', 1, 1, 'Gollancz', 'books_covers/Roadside_picnic_1.jpg', 'Arkadij Natanovič Strugackij, Boris Natanovič Strugackij'),
    ('9780399501487', 'Lord of the Flies', 'William Golding - Lord of the Flies', 1954, 'pages: 208', 1, 1, 'Perigee', 'books_covers/Lord_of_the_flies_1.jpg', 'William Golding'),
    ('9780425033807', 'Solaris', 'Stanisław Lem - Solaris', 1962, 'pages: 223', 1, 1, 'Berkley Publishing Corporation', 'books_covers/Solaris_2.jpg', 'Stanisław Lem'),
    ('9780380005840', 'The Futurological Congress', 'Stanisław Lem - The Futurological Congress', 1975, 'Original title: Kongres futurologiczny', 1, 1, 'Avon', 'books_covers/Kongres_1.jpg', 'Stanisław Lem'),
    ('9780380005840', 'The Futurological Congress', 'Stanisław Lem - The Futurological Congress', 1975, 'Original title: Kongres futurologiczny', 1, 1, 'Avon', 'books_covers/Kongres_1.jpg', 'Stanisław Lem'),
    ('9781520540290', 'Count of Monte Cristo', 'Alexandre Dumas - Count of Monte Cristo vol. 5, 1888 edition', 1888, 'pages: 231, 1888 edition with more than 80 original illustrations', 2, 1, None, 'books_covers/Monte_cristo_1.jpg', 'Alexandre Dumas'),
    ('0802755267', 'Solaris', 'Stanisław Lem - Solaris', 1970, 'pages: 216', 1, 1, 'Walker', 'books_covers/Solaris_4.jpg', 'Stanisław Lem'),
    ('9780380556656', 'Tales of Pirx the pilot', 'Stanisław Lem - Tales of Pirx the pilot', 1981, 'pages: 206', 1, 1, 'Avon', 'books_covers/Pirx_1.jpg', 'Stanisław Lem'),
    ('0025668552', 'Quo Vadis?', 'Henryk Sienkiewicz - Quo Vadis?', 1993, 'pages: 579, contributions: Kuniczak, W. S., 1930-', 1, 1, 'Macmillan', 'books_covers/quo_vadis_1.jpg', 'Henryk Sienkiewicz'),
    ('0684801221', 'The old man and the sea', 'Ernest Hemingway - The old man and the sea', 1995, 'pages: 127', 1, 1, 'Simon & Schuster', 'books_covers/old_man_1.jpg', 'Ernest Hemingway'),
    ('9780140009729', 'Nineteen Eighty-Four', 'George Orwell - Nineteen Eighty-Four (1984)', 1981, 'pages:  251', 1, 1, 'Penguin Books', 'books_covers/1984_1.jpg', 'George Orwell'),
    ('9788380690905', 'Kolor Magii', 'Terry Pratchett - Kolor Magii (ang. The Colour of Magic)', 1983, 'pages:  250, original title: The Colour of Magic, Disc World series', 1, 1, 'Prószyński Media', 'books_covers/kolor_magii_1.jpg', 'Terry Pratchett'),
    ('0061020648', 'Guards! Guards!', 'Terry Pratchett - Guards! Guards!', 2001, 'pages:  355, Disc World series', 1, 1, 'HarperTorch', 'books_covers/guards_1.jpg', 'Terry Pratchett'),
    ('9780451157041', 'Equal Rites', 'Terry Pratchett - Equal Rites', 1988, 'pages:  254, Disc World series', 1, 1, 'New American Library', 'books_covers/equal_rites_1.jpg', 'Terry Pratchett'),
    ('9780061020704', 'The Light Fantastic', 'Terry Pratchett - The Light Fantastic', 2000, 'pages:  241, Disc World series', 1, 1, 'HarperTorch', 'books_covers/light_1.jpg', 'Terry Pratchett'),
    ('9780061020667', 'Wyrd Sisters', 'Terry Pratchett - Wyrd Sisters', 2001, 'pages:  288, Disc World series', 1, 1, 'HarperTorch', 'books_covers/wyrd_sisters_1.jpg', 'Terry Pratchett'),
    ('0385299842', 'Truckers', 'Terry Pratchett - Truckers', 1989, 'Disc World series', 1, 1, 'Delacorte Press', 'books_covers/truckers_1.jpg', 'Terry Pratchett'),
    ('0575046368', 'Eric', 'Terry Pratchett - Eric', 1990, 'pages: 126, contributions: Kirby, Josh, Disc World series', 1, 1, 'Gollancz', 'books_covers/eric_1.jpg', 'Terry Pratchett'),
    ('0399128964', 'Dune', 'Frank Herbert - Dune', 1965, 'pages: 517, Dune series', 1, 1, 'Putnam', 'books_covers/dune_1.jpg', 'Frank Herbert'),
    ('9780342847334', 'Thus Spake Zarathustra', 'Friedrich Nietsche - Thus Spake Zarathustra - A Book for all and None', 2018, 'pages: 508', 1, 1, 'Franklin Classics', 'books_covers/zarathustra_1.jpg', 'Friedrich Nietsche'),
    ('9780140278736', 'Animal farm', 'George Orwell - Animal farm', 1987, 'pages: 95', 1, 1, 'Penguin in association with Martin Secker & Warburg Ltd.', 'books_covers/animal_farm_1.jpg', 'George Orwell'),
    ('9780553213515', 'The Time Machine', 'H. G. Wells - The Time Machine', 1984, 'pages: 128', 2, 2, 'Bantam Classics', 'books_covers/time_machine_1.jpg', 'H. G. Wells'),
    ('9780553103748', 'A brief history of time', 'Stephen Hawking - A brief history of time', 1996, 'pages: 248', 1, 1, 'Bantam Books', 'books_covers/brief_history_of_time_1.jpg', 'Stephen Hawking'),
    ('9781510766709', 'Crime and Punishment', 'Fyodor Dostoyevsky - Crime and Punishment', 2021, '200th Birthday Edition', 1, 1, 'Skyhorse Publishing Company', 'books_covers/crime_and_punishment_1.jpg', 'Fyodor Dostoyevsky'),
    ('9782724278484', 'Pet Sematary', 'Stephen King - Pet Sematary', 2019, 'pages: 465', 1, 1, 'Hodder & Stoughton', 'books_covers/pet_sementary_1.jpg', 'Stephen King'),
    ('0156837501', 'Solaris', 'Stanisław Lem - Solaris', 1987, 'pages: 204', 1, 1, 'Harcourt Brace Jovanovich', 'books_covers/Solaris_3.jpg', 'Stanisław Lem'),
    ('9781857988536', 'Ubik', 'Philip K. Dick - Ubik', 2000, 'pages: 224', 1, 1, 'Gollancz', 'books_covers/ubik_1.jpg', 'Philip K. Dick'),
    ('0090015304', '2001 - A space odyssey', 'Arthur C. Clarke - 2001', 1968, 'pages: 256', 1, 1, 'Arrow Books', 'books_covers/2001_1.jpg', 'Arthur C. Clarke'),
    ('0345336275', 'Foundation', 'Isaac Asimov - Foundation', 1983, 'pages: 285', 1, 1, 'Ballantine Books', 'books_covers/foundation_1.jpg', 'Isaac Asimov'),)
    movies_data = (('Stanley Kubrik', 'Stanley Kubrik', 'A Clockwork Orange', 'Stanley Kubrik - A Clockwork Orange', 1971, 'Based on Anthony Burgess book.', 1, 1, 'movies_covers/clockwork_orange_1.png'), 
    ('Stanley Kubrik', 'Stanley Kubrik', '2001: a space odyssey', 'Stanley Kubrik - 2001: a space odyssey', 1968, 'Based on Arthur C. Clarke book.', 1, 1, 'movies_covers/space_odyssey_1.jpg'),
    ('Andriej Tarkowski', 'Andriej Tarkowski, Fridrikh Gorenshtein', 'Solaris', 'Andriej Tarkowski - Solaris', 1972, 'Based on Stanisław Lem\'s book.', 1, 1, 'movies_covers/solaris_1.jpg'),
    ('Darren Aronofsky', 'Darren Aronofsky', 'Pi', 'Darren Aronofsky - Pi', 1997, 'length: 1h 24min', 1, 1, 'movies_covers/pi_1.jpg'),
    ('Orson Welles', 'Herman J. Mankiewicz, Orson Welles', 'Citizen Kane', 'Orson Welles - Citizen Kane', 1941, 'length: 1h 59min', 1, 2, 'movies_covers/citizen_kane_1.jpg'),
    ('Christopher Nolan', 'Christopher Nolan, Jonathan Nolan', 'Interstellar', 'Christopher Nolan - Interstellar', 2014, 'length: 2h 49min', 1, 1, 'movies_covers/interstellar_1.jpg'),
    ('Andriej Tarkowski', 'Andriej Tarkowski', 'Stalker', 'Andriej Tarkowski - Stalker', 1979, 'Based on Arkadij Natanovič Strugackij and Boris Natanovič Strugackij book - Roadside Picnic', 1, 1, 'movies_covers/stalker_1.jpg'),
    ('Masaki Kobayashi', 'Yôko Mizuki', 'Kwaidan', 'Masaki Kobayashi - Kwaidan', 1964, 'Based on Lafcadio Hearn novel, original title: Kaidan', 2, 2, 'movies_covers/kwaidan_1.jpg'),
    ('Alfred Hitchcock', 'Joseph Stefano', 'Psycho', 'Alfred Hitchcock - Psycho', 1960, 'Based on Robert Bloch novel', 1, 2, 'movies_covers/psycho_1.jpg'),
    ('Quentin Tarantino', 'Quentin Tarantino', 'Pulp Fiction', 'Quentin Tarantino - Pulp Fiction', 1994, 'length: 2h 34min', 1, 1, 'movies_covers/pulp_fiction_1.jpg'),
    ('Steven Spielberg', 'Steven Spielberg, Hal Barwood', 'Close Encounters of the Third Kind', 'Steven Spielberg - Close Encounters of the Third Kind', 1977, 'length: 2h 18min', 1, 1, 'movies_covers/close_1.jpg'),
    ('Martin Scorsese', 'Paul Schrader', 'Taxi Driver', 'Martin Scorsese - Taxi Driver', 1976, 'length: 1h 54min', 1, 1, 'movies_covers/taxi_1.jpg'),
    ('Martin Scorsese', 'Martin Scorsese', 'Goodfellas', 'Martin Scorsese - Goodfellas', 1990, 'length: 2h 26min', 1, 1, 'movies_covers/goodfellas_1.jpg'),
    ('Ethan Coen, Joel Coen', 'Ethan Coen, Joel Coen', 'No Country for Old Men', 'Coen brothers - No Country for Old Men', 2007, 'length: 2h 2min', 1, 1, 'movies_covers/no_country_1.jpg'),
    ('Hayao Miyazaki', 'Hayao Miyazaki', 'Spirited Away', 'Hayao Miyazaki - Spirited Away', 2001, 'length: 2h 5min, original title: Sen to Chihiro no kamikakushi', 1, 1, 'movies_covers/spirited_1.jpg'),)
    sr_data = (("Solaris", "Stanisław Lem", "Robert Więckiewicz, Magdalena Cielecka", "Stanisław Lem - Solaris", None, "Audioteka", "language: polish", 1, 1, "sound_recordings_covers/solaris_1.jpg"),
    ("Krzyżacy T. 1-2", "Henryk Sienkiewicz", "Zbigniew Wróbel", "Henryk Sienkiewicz - Krzyżacy T. 1-2", 2007, "Katowice: \"Aleksandia\"", "language: polish, seria: lektury dla leniwych", 1, 1, "sound_recordings_covers/krzyzacy_1.jpg"),
    ("2001: odyseja kosmiczna", "Arthur C. Clarke", "Krystyna Czubówna, Mirosław Zbrojewicz, Antoni Pawlicki", "Arthur C. Clarke - 2001: odyseja kosmiczna", None, "Audioteka", "language: polish", 1, 1, "sound_recordings_covers/2001_1.jpg"),
    ("Balladyna", "Juliusz Słowacki", "Mirella Rogoza-Biel, Konrad Biel", "Juliusz Słowacki - Balladyna", 2020, "Storybox.pl", "language: polish", 1, 1, "sound_recordings_covers/balladyna_1.jpg"),
    ("Robinson Crusoe", "Daniel Defoe", "Stanisław Biczysko", "Daniel Defoe - Robinson Crusoe", 2015, "Biblioteka Akustyczna", "language: polish", 1, 1, "sound_recordings_covers/crusoe_1.jpg"),) 

    if conditions:
        print(f'Starting to enter data rows into worker_side_condition table.')
        for condition in conditions_data:
            buff = Condition(name=condition)
            buff.save()
        print(f'{len(conditions_data)} row(s) has been inserted into worker_side_condtion table.\n')

    if availabilities:
        print(f'Starting to enter data rows into worker_side_availability table.')
        for availability in availabilities_data:
            buff = Availability(name=availability)
            buff.save()
        print(f'{len(availabilities_data)} row(s) has been inserted into worker_side_availability table.\n')

    if authors:
        print(f'Starting to enter data rows into worker_side_author table.')
        for author in authors_data:
            buff = Author(name=author)
            buff.save()
        print(f'{len(authors_data)} row(s) has been inserted into worker_side_author table.\n')

    if publishers:
        print(f'Starting to enter data rows into worker_side_publisher table.')
        for publisher in publishers_data:
            buff = Publisher(name=publisher)
            buff.save()
        print(f'{len(publishers_data)} row(s) has been inserted into worker_side_publisher table.\n')

    if directors:
        print(f'Starting to enter data rows into worker_side_director table.')
        for director in directors_data:
            buff = Director(name=director)
            buff.save()
        print(f'{len(directors_data)} row(s) has been inserted into worker_side_director table.\n')

    if screenwriters:
        print(f'Starting to enter data rows into worker_side_screenwriter table.')
        for screenwriter in screenwriters_data:
            buff = Screenwriter(name=screenwriter)
            buff.save()
        print(f'{len(screenwriters_data)} row(s) has been inserted into worker_side_screenwriter table.\n')

    if books:
        cursor = connection.cursor()
        print(f'Starting to enter data rows into worker_side_book')        
        for book in books_data:
            item = Book()
            item.isbn = book[0]
            item.title = book[1]
            item.full_title = book[2]
            item.pub_year = book[3]
            item.description = book[4]
            item.availability = Availability.objects.get(id=book[5])
            item.condition = Condition.objects.get(id=book[6])
            try:
                item.publisher = Publisher.objects.get(name=book[7])
            except:
                if book[7] != None:
                    publisher = Publisher.objects.create(name=book[7])
                    item.publisher = publisher
                else:
                    item.publisher = None
            item.save()
            if authors != None:
                authors = book[9].split(", ")
                for author in authors:
                    try:
                        aux = Author.objects.get(name=author)
                        item.author.add(aux)
                    except:
                        aux = Author.objects.create(name=author)
                        item.author.add(aux)

            query = "UPDATE worker_side_book SET cover='{}' WHERE id={}".format(book[8], item.id)
            cursor.execute(query)
        print(f'{len(books_data)} row(s) has been inserted into worker_side_book table.\n')

    if movies:
        cursor = connection.cursor()
        print(f'Starting to enter data rows into worker_side_movie')
        for movie in movies_data:
            item = Movie()
            item.title = movie[2]
            item.full_title = movie[3]
            item.pub_year = movie[4]
            item.description = movie[5]
            item.condition = Condition.objects.get(id = movie[7])
            item.availability = Availability.objects.get(id = movie[6])
            item.save()

            if movie[0] != None:
                directors = movie[0].split(", ")
                for director in directors:
                    try:
                        aux = Director.objects.get(name=director)
                        item.director.add(aux)
                    except:
                        aux = Director.objects.create(name=director)
                        item.director.add(aux)

            if movie[1] != None:
                screenwriters = movie[1].split(", ")
                for screenwriter in screenwriters:
                    try:
                        aux = Screenwriter.objects.get(name=screenwriter)
                        item.screenwriter.add(aux)
                    except:
                        aux = Screenwriter.objects.create(name=screenwriter)
                        item.screenwriter.add(aux)

            query = "UPDATE worker_side_movie SET cover='{}' WHERE id={}".format(movie[8], item.id)
            cursor.execute(query)
        print(f'{len(movies_data)} row(s) has been inserted into worker_side_movie table.\n')

    if sr:
        cursor = connection.cursor()
        print(f'Starting to enter data rows into worker_side_soundrecording')        
        for sr in sr_data:
            item = SoundRecording()
            item.title = sr[0]
            item.cast = sr[2]
            item.full_title = sr[3]
            item.pub_year = sr[4]
            item.description = sr[6]
            item.availability = Availability.objects.get(id=sr[7])
            item.condition = Condition.objects.get(id=sr[8])
            try:
                item.publisher = Publisher.objects.get(name=sr[7])
            except:
                if sr[5] != None:
                    publisher = Publisher.objects.create(name=sr[5])
                    item.publisher = publisher
                else:
                    item.publisher = None
            item.save()
            if authors != None:
                authors = sr[1].split(", ")
                for author in authors:
                    try:
                        aux = Author.objects.get(name=author)
                        item.author.add(aux)
                    except:
                        aux = Author.objects.create(name=author)
                        item.author.add(aux)

            query = "UPDATE worker_side_soundrecording SET cover='{}' WHERE id={}".format(sr[9], item.id)
            cursor.execute(query)
        print(f'{len(sr_data)} row(s) has been inserted into worker_side_soundrecording table.\n')

        


def fill_user_side(statuses = True, clients = True, workers = True):
    """Procedure for inserting data rows into SQL user_side tables. 
    Parameters:
    conditions=True, availabilities=True
    Returns:
    None"""
    statuses_data = (('Placed'), ('Ready'), ("Fullfilled"))

    if statuses:
        print(f'Starting to enter data rows into user_side_status table.')
        for status in statuses_data:
            buff = Status(name=status)
            buff.save()
        print(f'{len(statuses_data)} row(s) has been inserted into user_side_status table.\n')

    if clients:
        print("Creating reader account")
        password = "alamakota"
        user = User()
        user.first_name = "Zuzanna"
        user.last_name = "Nowak"
        user.email = "zuzia@example.com"
        user.phone_num = "+48123456789"
        user.set_password(password)
        user.save()

        client = Client()
        client.user = user
        client.borrows_max = 10
        client.citizenship = Citizenship.objects.get(id=164)    
        client.occupation = Occupation.objects.get(id=2)
        client.corr_address = "ul. Poniatowskiego 24, m. 10, 40-020, Katowice, Polska"
        client.id_type = IDType.objects.get(id=1)
        client.id_number = "CHK 123456"
        client.date_of_birth = date(1997, 3, 12)
        client.save()
        print("Reader account created: email: {}, password: {}".format(user.email, password))

    if workers:
        print("Creating worker account")
        password = "akotmaale"
        user = User()
        user.first_name = "Alice"
        user.last_name = "Bowman"
        user.email = "alice@example.com"
        user.phone_num = "+1987654321"
        user.is_staff = True
        user.set_password(password)
        user.save()
        print("Worker account created: email: {}, password: {}".format(user.email, password))

def fill_whole_database():
    fill_accounts()
    fill_worker_side()
    fill_user_side()

if __name__ == '__main__':
    fill_accounts()
    fill_worker_side()
    fill_user_side()