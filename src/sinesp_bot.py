import re
import sys
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException


def get_driver():
    opts = {
        'platformName': 'Android',
        'platformVersion': '8.0',
        'appPackage': 'br.gov.sinesp.cidadao.android',
        'appActivity': 'MainActivity',
        'deviceName': 'emulator-5554',
    }
    return webdriver.Remote('http://localhost:4723/wd/hub', opts)

def search_plate(plate):
    wd = get_driver()

    # Touch vehicle search image button
    botoes = wd.find_element_by_id('botoes')
    TouchAction(wd).tap(x=400, y=500).perform()

    # Fill form and search for vehicle by plate
    wd.find_element_by_id('txPlacaLetra').send_keys(plate[:3])
    wd.find_element_by_id('txPlacaNumero').send_keys(plate[3:])
    wd.find_element_by_id('imgBtnConsultar').click()

    try:
        message = wd.find_element_by_id('message')
    except NoSuchElementException:
        message = None

    message = message and message.text
    if message and message.lower() == 'Veículo não encontrado':
            data = {
                'city': None,
                'state': None,
                'brand': None,
                'model': None,
                'year': None,
                'color': None,
                'municipio_uf': None,
                'chassis': None,
                'date': None,
                'return_code': 1,
                'return_message': message,
                'status_code': None,
                'status_message': None,
            }
            return data

    consulta = None    
    start_time = int(time.time())
    while not consulta:
        end_time = int(time.time())
        if (end_time - start_time) > 30:
            print('Timeout')
            exit(1)

        try:
            consulta = wd.find_element_by_id('txDataHoraConsulta')
        except NoSuchElementException:
            pass

    try:
        situacao = wd.find_element_by_id('imgBtnSituacaoLegal')
    except NoSuchElementException:
        situacao = None

    marca_modelo = wd.find_element_by_id('txMarcaModelo').text
    munipicio_uf = wd.find_element_by_id('txMunicipioUF').text
    chassi = wd.find_element_by_id('txChassi').text
    data_hora = wd.find_element_by_id('txDataHoraConsulta').text

    city, state = munipicio_uf.split('/')
    brand_model, year, color = [x.strip() for x in marca_modelo.split('-')]
    brand = brand_model.split()[0]
    model = ' '.join(brand_model.split()[1:])
    chassis = '************' + chassi.split()[-1]
    date = data_hora.split()[-3] + ' ' + data_hora.split()[-1]
    status_code = 0 if situacao else 1
    status_message = 'Sem restrição' if situacao else 'Com restrição'

    data = {
        'city': city,
        'state': state,
        'brand': brand,
        'model': model,
        'year': year,
        'color': color,
        'municipio_uf': munipicio_uf,
        'chassis': chassis,
        'date': data_hora,
        'return_code': 0,
        'return_message': 'Sem erros.',
        'status_code': status_code,
        'status_message': status_message,
    }

    return data

if __name__ == '__main__':
    try:
        plate = ''.join(sys.argv[1].upper().split())
    except IndexError:
        print('Usage: sinesp_bot.py <plate as XYZ1234>')
        exit(1)

    results = search_plate(plate)

    import json
    print(json.dumps(results))
