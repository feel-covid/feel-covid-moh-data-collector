import requests


def moh_request():
    url = 'https://datadashboardapi.health.gov.il/api/queries/_batch'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Host': 'datadashboardapi.health.gov.il',
        'Origin': 'https://datadashboard.health.gov.il',
        'Referer': 'https://datadashboard.health.gov.il',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Sit3e': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    }

    body = """
        {
            "requests": [
                {
                    "id": "0",
                    "queryName": "lastUpdate",
                    "single": true,
                    "parameters": {}
                },
                {
                    "id": "1",
                    "queryName": "infectedPerDate",
                    "single":false,
                    "parameters":{}
                },
                {
                    "id": "2",
                    "queryName": "updatedPatientsOverallStatus",
                    "single": false,
                    "parameters": {}
                },
                {
                    "id": "3",
                    "queryName": "sickPatientPerLocation",
                    "single": false,
                    "parameters": {}
                },
                {
                    "id": "4",
                    "queryName": "patientsPerDate",
                    "single": false,
                    "parameters": {}
                },
                {
                    "id": "5",
                    "queryName": "deadPatientsPerDate",
                    "single": false,
                    "parameters": {}
                },
                {
                    "id": "6",
                    "queryName": "testResultsPerDate",
                    "single": false,
                    "parameters": {}
                },
                {
                  "id": "7",
                  "queryName": "vaccinated",
                  "single": false,
                  "parameters": {}
                }
            ]
        }
    """

    response = requests.post(url, headers=headers, data=body).json()

    return response
