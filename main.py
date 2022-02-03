import datetime
import pandas as pd

csvfile = pd.read_csv('owid-covid-data r.csv', sep=';', decimal = ',')
csvfile['date'] = pd.to_datetime(csvfile['date'])

#1.Wyznaczyć wartości:  Łącznej liczby zgonów COVID w podanym kraju oraz łącznej liczby przypadków na jednego mieszkańca. Funkcja ma mieć możliwość opcjonalnego przyjęcia parametrów określających przedział dat dla których wartości są liczone.
def newCasesPerInhabitatWithTime(location, day1: datetime = None, day2: datetime = None):
    if day1 is None and day2 is None:
        newDeaths = csvfile[csvfile['location'] == location].groupby('location').new_deaths.sum()
        newCases = csvfile[csvfile['location'] == location].groupby('location').new_cases.sum()
        pop = csvfile[csvfile['location'] == location].groupby('location').population.max()
    else:
        newDeaths = csvfile[((csvfile['date']) >= day1) & ((csvfile['date']) <= day2) & (csvfile['location'] == location)].groupby('location').new_deaths.sum()
        newCases = csvfile[((csvfile['date']) >= day1) & ((csvfile['date']) <= day2) & (csvfile['location'] == location)].groupby('location').new_cases.sum()
        pop = csvfile[((csvfile['date']) >= day1) & ((csvfile['date']) <= day2) & (csvfile['location'] == location)].groupby('location').population.max()

    newCasesPerInh = newCases.divide(pop)
    result = pd.concat([newDeaths, newCasesPerInh], axis=1)
    return result
print("\n1. Laczna liczba zgonow COVID w podabym kraju oraz laczna liczba przypadkow na jednego mieszkanca w podanym okresie czasu")
print(newCasesPerInhabitatWithTime(location = 'Poland'))

#2.Wyznaczyć wartości: Liczby osób zaszczepionych danego dnia oraz liczby osób zaszczepionych pełnie w podanym dniu
def numberOfPeopleVaccined(day: datetime) -> (float, float):

    newVaccinations = csvfile[(csvfile['date']) == day].new_vaccinations.sum(axis = 'index') #people_vaccinated
    fullyVaccinated = csvfile[(csvfile['date']) == day].people_fully_vaccinated.sum(axis = 'index')

    return newVaccinations, fullyVaccinated

newVaccinations, fullyVaccinated = numberOfPeopleVaccined('2021-11-23')
print('\n\n2.1. Liczba osob zaszczepionych w podanym dniu: ', newVaccinations)
print('2.2. Liczba osob zaszczepionych pelnie w podanym dniu: ', fullyVaccinated)