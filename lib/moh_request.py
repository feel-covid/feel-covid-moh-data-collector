import requests


def moh_request():
    url = 'https://datadashboardapi.health.gov.il/api/queries/_batch'

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Content-Type': 'application/json',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    body = '{"requests":[{"id":"0","queryName":"lastUpdate","single":true,"parameters":{}},{"id":"1","queryName":"infectedPerDate","single":false,"parameters":{}},{"id":"2","queryName":"updatedPatientsOverallStatus","single":false,"parameters":{}},{"id":"3","queryName":"sickPerDateTwoDays","single":false,"parameters":{}},{"id":"4","queryName":"sickPatientPerLocation","single":false,"parameters":{}},{"id":"5","queryName":"patientsPerDate","single":false,"parameters":{}},{"id":"6","queryName":"deadPatientsPerDate","single":false,"parameters":{}},{"id":"7","queryName":"recoveredPerDay","single":false,"parameters":{}},{"id":"8","queryName":"testResultsPerDate","single":false,"parameters":{}},{"id":"9","queryName":"infectedPerDate","single":false,"parameters":{}},{"id":"10","queryName":"patientsPerDate","single":false,"parameters":{}},{"id":"11","queryName":"doublingRate","single":false,"parameters":{}},{"id":"12","queryName":"infectedByAgeAndGenderPublic","single":false,"parameters":{"ageSections":[0,10,20,30,40,50,60,70,80,90]}},{"id":"13","queryName":"isolatedDoctorsAndNurses","single":true,"parameters":{}},{"id":"14","queryName":"testResultsPerDate","single":false,"parameters":{}},{"id":"15","queryName":"contagionDataPerCityPublic","single":false,"parameters":{}},{"id":"16","queryName":"hospitalStatus","single":false,"parameters":{}}]}'

    response = requests.post(url, headers=headers, data=body).json()

    return response
