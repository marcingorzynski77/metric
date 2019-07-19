import csv
import random
from time import time
from decimal import Decimal
from faker import Faker
from faker.providers import BaseProvider


RECORD_COUNT = 10000000
fake = Faker()

class TenorProvider(BaseProvider):
    def tenor(self):
        tenors = ['1D', '1W', '1M', '2M', '3M', '6M', '12M', '2Y', '3Y', '5Y', '10Y', '15Y','20Y','25Y','30Y']

        return random.choice(tenors)

class ClientProvider(BaseProvider):
    def client(self):
        clients = ['VW', 'HSBC', 'Barclays', 'Volvo', 'Google', 'Vodafone', 'EE', 'Tmobile', 'Great Nothern', '360']

        return random.choice(clients)

class RiskMeasureProvider(BaseProvider):
    def risk(self):
        risks = ['FxGamma', 'FxVega', 'FxDelta', 'IrDelta', 'IrVega', 'IrGamma']

        return random.choice(risks)

fake.add_provider(TenorProvider)
fake.add_provider(ClientProvider)
fake.add_provider(RiskMeasureProvider)


def create_csv_file():
    with open('./sensitivities_big4.csv', 'w', newline='') as csvfile:
        fieldnames = ['CLMS ID','PartyName','PartyLegalName','PartyType','Entity','MlcTrnKey','RiskMeasureType','Value','ValueCurrency','InstrumentTenor','RiskFactorName','ScenarioName','ProformaShiftValue','ProformaShiftType','UnderlyingTenor','FixingTenor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {
                    'CLMS ID': fake.random_int(min=1, max=RECORD_COUNT),
                    'PartyName': fake.client(),
                    'PartyLegalName': fake.client(),
                    'PartyType': 'Subsidiary',
                    'Entity': 'LBCM',
                    'MlcTrnKey': 'SU123434344343',
                    'RiskMeasureType': fake.risk(),
                    'Value': fake.random_int(min=1, max=RECORD_COUNT),
                    'ValueCurrency': 'GBP',
                    'InstrumentTenor': fake.tenor(),
                    'RiskFactorName': 'Intrest Rate SwapsIOS ' + fake.currency_code(),
                    'ScenarioName': 'FRASwapIOSCurve',
                    'ProformaShiftValue': float(Decimal(random.randrange(1, 100000))/10000000),
                    'ProformaShiftType': 'ABS',
                    'UnderlyingTenor': fake.tenor(),
                    'FixingTenor': 'Not Set'
                }
            )


if __name__ == '__main__':
    start = time()
    create_csv_file()
    elapsed = time() - start
    print('created csv file time: {}'.format(elapsed))
