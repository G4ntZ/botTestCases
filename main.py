# -*- coding: utf-8 -*-
import requests
import re
import csv
import time

class SourceDataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file, delimiter=";")
            data = []
            for element in reader:
                data.append(element)
        return data

def login(user, passw):
    url = 'https://testrail.afphabitat.net/testrail/index.php?/auth/login/'
    data = {'name': f'{user}',
            'password': f'{passw}',
            'rememberme': '1'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=data, headers=headers)
    cookies = r.request.headers['Cookie']
    return cookies

def getTestCases(jira, cookies):
    idCases = []
    c = {'Cookie': f'{cookies}'}
    url = f'https://testrail.afphabitat.net/testrail//index.php?/ext/jira/render_panel&jv=7.12.3&ae=sdk&av=1&issue={jira}&panel=references&login=button&frame=tr-frame-panel-references'
    r = requests.get(url, auth=('prov_zt', 'd3liverance'), cookies=c)
    cases = re.findall('<div class="grid-column text-ppp" style="width: 65px">\n.*</div>', r.text)
    for case in cases:
        tmp = case.replace('<div class="grid-column text-ppp" style="width: 65px">', '')
        tmp = tmp.replace('\n				', '')
        tmp = tmp.replace('			</div>','')
        idCases.append(tmp)
    return idCases

def getStringTestCases(cases):
    s_cases = ""
    for case in cases:
        s_cases = s_cases + str(case) + ", "
    return s_cases[:-2]

def generateReport(jiras, cookies):
    csv_out = open('Estadisitca.csv', 'w')
    fieldnames = ['jira', 'cantidadTestCases', 'testCases']
    writer = csv.DictWriter(csv_out, fieldnames=fieldnames, lineterminator='\n', delimiter=';')
    writer.writeheader()
    for jira in jiras:
        j = jira['jira']
        cases = getTestCases(j, cookies)
        t_cases = len(cases)
        s_cases = getStringTestCases(cases)
        row = {'jira': f'{j}', 'cantidadTestCases': f'{t_cases}', 'testCases': f'{s_cases}'}
        writer.writerow(row)
        time.sleep(0.1)

if __name__ == '__main__':
    std = SourceDataReader('jiras.csv')
    jiras = std.read()
    cookies = login('prov_zt', 'd3liverance')
    generateReport(jiras, cookies)