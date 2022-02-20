#Konrad Maciejczyk, 2021-2022
#Note: To use this script run in terminal: python3 manage.py shell < ./example_data/database_fill.py
from accounts.models import Citizenship, IDType, Occupation
from user_side.models import Status
from worker_side.models import Author, Condition, Availability, Director, Publisher, Screenwriter

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
            print(id_type)
            buff = IDType(name=id_type)
            buff.save()
        print(f'{len(id_types_data)} row(s) has been inserted into accounts_id_type table.\n')

    if occupations:
        print(f'Starting to enter data rows into acounts_occupation table.')
        for occupation in occupations_data:
            buff = Occupation(name=occupation)
            buff.save()
        print(f'{len(occupations_data)} row(s) has been inserted into accounts_occupation table.\n')

def fill_worker_side(conditions=True, availabilities=True, authors=True, publishers=True, directors=True, screenwriters=True):
    """Procedure for inserting data rows into SQL worker_side tables. 
    Parameters:
    conditions=True, availabilities=True
    Returns:
    None"""

    conditions_data = (('Good'), ('Damaged'))
    availabilities_data = (('Available to borrow'), ('Library use only'), ('Not available'))
    authors_data = (("Terry Pratchett"), ("Adam Mickiewicz") , ("Henryk Sienkiewicz") , ("Stefan Żeromski"), ("Fyodor Dostoyevsky"), ("Stanisław Lem"))
    publishers_data = (("Prószyński i S-ka"), ("Wydawnictwo Literackie"), ("Wydawnictwo MG"))
    directors_data = (('Stanley Kubrik'), ("Christopher Nolan"), ("Denis Villeneuve"), ("Darren Aronofsky"), ("Guillermo del Toro"))
    screenwriters_data = (('Jonathan Nolan'), ('Micheal Herr'), ("Stanley Kubrik"), ("Vince Gilligan"), ("Frank Darabont"), ("Peter Gould"))

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

def fill_user_side():
    statuses_data = (('Placed'), ('Ready'), ("Fullfilled"))

    print(f'Starting to enter data rows into user_side_status table.')
    for status in statuses_data:
        buff = Status(name=status)
        buff.save()
    print(f'{len(statuses_data)} row(s) has been inserted into user_side_status table.\n')

def fill_whole_database():
    fill_accounts()
    fill_worker_side()
    fill_user_side()

if __name__ == '__main__':
    fill_accounts()
    fill_worker_side()
    fill_user_side()