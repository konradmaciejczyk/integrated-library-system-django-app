#Konrad Maciejczyk, 2021-2022
#Note: To use this script run in terminal: python3 manage.py shell < ./example_data/database_fill.py
from accounts.models import Citizenship, Gender, IDType, Occupation

citizenships = (('Afghan'), ('Albanian'), ('Algerian'), ('American'), ('Andorran'), ('Angolan'), ('Anguillan'), ('Argentine'), ('Armenian'), ('Australian'), ('Austrian'), ('Azerbaijani'), ('Bahamian'), ('Bahraini'), ('Bangladeshi'), ('Barbadian'), ('Belarusian'), ('Belgian'), ('Belizean'), ('Beninese'), ('Bermudian'), ('Bhutanese'), ('Bolivian'), ('Botswanan'), ('Brazilian'), ('British'), ('British Virgin Islander'), ('Bruneian'), ('Bulgarian'), ('Burkinan'), ('Burmese'), ('Burundian'), ('Cambodian'), ('Cameroonian'), ('Canadian'), ('Cape Verdean'), ('Cayman Islander'), ('Central African'), ('Chadian'), ('Chilean'), ('Chinese'), ('Citizen of Antigua and Barbuda'), ('Citizen of Bosnia and Herzegovina'), ('Citizen of Guinea-Bissau'), ('Citizen of Kiribati'), ('Citizen of Seychelles'), ('Citizen of the Dominican Republic'), ('Citizen of Vanuatu '), ('Colombian'), ('Comoran'), ('Congolese (Congo)'), ('Congolese (DRC)'), ('Cook Islander'), ('Costa Rican'), ('Croatian'), ('Cuban'), ('Cymraes'), ('Cymro'), ('Cypriot'), ('Czech'), ('Danish'), ('Djiboutian'), ('Dominican'), ('Dutch'), ('East Timorese'), ('Ecuadorean'), ('Egyptian'), ('Emirati'), ('English'), ('Equatorial Guinean'), ('Eritrean'), ('Estonian'), ('Ethiopian'), ('Faroese'), ('Fijian'), ('Filipino'), ('Finnish'), ('French'), ('Gabonese'), ('Gambian'), ('Georgian'), ('German'), ('Ghanaian'), ('Gibraltarian'), ('Greek'), ('Greenlandic'), ('Grenadian'), ('Guamanian'), ('Guatemalan'), ('Guinean'), ('Guyanese'), ('Haitian'), ('Honduran'), ('Hong Konger'), ('Hungarian'), ('Icelandic'), ('Indian'), ('Indonesian'), ('Iranian'), ('Iraqi'), ('Irish'), ('Israeli'), ('Italian'), ('Ivorian'), ('Jamaican'), ('Japanese'), ('Jordanian'), ('Kazakh'), ('Kenyan'), ('Kittitian'), ('Kosovan'), ('Kuwaiti'), ('Kyrgyz'), ('Lao'), ('Latvian'), ('Lebanese'), ('Liberian'), ('Libyan'), ('Liechtenstein citizen'), ('Lithuanian'), ('Luxembourger'), ('Macanese'), ('Macedonian'), ('Malagasy'), ('Malawian'), ('Malaysian'), ('Maldivian'), ('Malian'), ('Maltese'), ('Marshallese'), ('Martiniquais'), ('Mauritanian'), ('Mauritian'), ('Mexican'), ('Micronesian'), ('Moldovan'), ('Monegasque'), ('Mongolian'), ('Montenegrin'), ('Montserratian'), ('Moroccan'), ('Mosotho'), ('Mozambican'), ('Namibian'), ('Nauruan'), ('Nepalese'), ('New Zealander'), ('Nicaraguan'), ('Nigerian'), ('Nigerien'), ('Niuean'), ('North Korean'), ('Northern Irish'), ('Norwegian'), ('Omani'), ('Pakistani'), ('Palauan'), ('Palestinian'), ('Panamanian'), ('Papua New Guinean'), ('Paraguayan'), ('Peruvian'), ('Pitcairn Islander'), ('Polish'), ('Portuguese'), ('Prydeinig'), ('Puerto Rican'), ('Qatari'), ('Romanian'), ('Russian'), ('Rwandan'), ('Salvadorean'), ('Sammarinese'), ('Samoan'), ('Sao Tomean'), ('Saudi Arabian'), ('Scottish'), ('Senegalese'), ('Serbian'), ('Sierra Leonean'), ('Singaporean'), ('Slovak'), ('Slovenian'), ('Solomon Islander'), ('Somali'), ('South African'), ('South Korean'), ('South Sudanese'), ('Spanish'), ('Sri Lankan'), ('St Helenian'), ('St Lucian'), ('Stateless'), ('Sudanese'), ('Surinamese'), ('Swazi'), ('Swedish'), ('Swiss'), ('Syrian'), ('Taiwanese'), ('Tajik'), ('Tanzanian'), ('Thai'), ('Togolese'), ('Tongan'), ('Trinidadian'), ('Tristanian'), ('Tunisian'), ('Turkish'), ('Turkmen'), ('Turks and Caicos Islander'), ('Tuvaluan'), ('Ugandan'), ('Ukrainian'), ('Uruguayan'), ('Uzbek'), ('Vatican citizen'), ('Venezuelan'), ('Vietnamese'), ('Vincentian'), ('Wallisian'), ('Welsh'), ('Yemeni'), ('Zambian'), ('Zimbabwean'), ("Not selected"))

genders = (('Male'), ("Female"), ("Diverse"), ("Not selected"))

id_types = (('ID Card'), ('Passport'), ("Not selected"))

occupations = (('Student'), ('Academic teacher'), ('Other'), ("Not selected"))

print("Starting to enter data rows into Citizenship table.")
for citizenship in citizenships:
    buff = Citizenship(name=citizenship)
    buff.save()
print("Entering data into Citizenship table completed.\n")

print("Starting to enter data rows into Gender table.")
for gender in genders:
    buff = Gender(name=gender)
    buff.save()
print("Entering data into Gender table completed.\n")

print("Starting to enter data rows into IDDocumentType table.")
for id_type in id_types:
    buff = IDType(name=id_type)
    buff.save()
print("Entering data into IDDocumentType table completed.\n")

print("Starting to enter data rows into Occupation table.")
for occupation in occupations:
    buff = Occupation(name=occupation)
    buff.save()
print("Entering data into Occupation table completed.")