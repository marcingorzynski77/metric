import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.tsa.stattools import adfuller


def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"

def test(cell):
    wb = xw.Book.caller()
    wb.sheets[0].range(cell).value = "Hello test!"

def corr2(sheet,range):
    wb = xw.Book.caller()
    shares = wb.sheets[sheet]
    df = shares.range(range).options(pd.DataFrame, index=False).value
    active = xw.sheets.active
    active.range('A3').value = df.corr()

def most_volatile(sheet, range, sec, period, output):
    wb = xw.Book.caller()
    shares = wb.sheets[sheet]
    df = shares.range(range).options(pd.DataFrame, index=False).value
    df['dailychange%'] = (df[sec]-df[sec].shift(1))/df[sec].shift(1)*100
    dfv = df['dailychange%'].rolling(period, win_type ='triang').sum() 
    maxIndex = dfv.idxmax(axis = 1, skipna = True)
    toDate = df.iloc[maxIndex,0]
    fromDate = df.iloc[maxIndex-period,0]
    active = xw.sheets.active
    active.range(output).value = 'Most volatile ' + str(period)+'d period is from: ' + fromDate.strftime("%d-%b-%Y") + ' to: '+ toDate.strftime("%d-%b-%Y")

def ks(sheet1, input1, sheet2, input2):
    wb = xw.Book.caller()
    sh1 = wb.sheets[sheet1]
    sh2 = wb.sheets[sheet2]
    df3 = sh1.range(input1).options(pd.DataFrame, index=False).value
    df6 = sh2.range(input2).options(pd.DataFrame, index=False).value

    df3_value = df3['value']
    df6_value = df6['value']

    sorted_returns3 = np.sort(df3['value'], axis = 0)
    scaled_returns3 = (sorted_returns3 - sorted_returns3.mean())/sorted_returns3.std()

    sorted_returns6 = np.sort(df6['value'], axis = 0)
    scaled_returns6 = (sorted_returns6 - sorted_returns6.mean())/sorted_returns6.std()

    fig = plt.figure(figsize=(6,3))
    plt.hist([sorted_returns3, sorted_returns6], label=['3m','6m'])
    plt.xlabel('bins')
    plt.ylabel('counts')
    plt.legend(loc = 'best')
    ax = plt.gca()

    res = stats.ks_2samp(sorted_returns3, sorted_returns6)
    active = xw.sheets.active
    active.range('A3').value = res

    sht = xw.sheets.active
    sht.pictures.add(fig, name='MyPlot', update=True)

def df(sheet1, input1, sheet2, input2):
    wb = xw.Book.caller()
    sh1 = wb.sheets[sheet1]
    sh2 = wb.sheets[sheet2]
    df3 = sh1.range(input1).options(pd.DataFrame, index=False).value
    df6 = sh2.range(input2).options(pd.DataFrame, index=False).value

    df3_value = df3['value']
    df6_value = df6['value']

    adf3_test = adfuller(df3_value)
    adf6_test = adfuller(df6_value)

    active = xw.sheets.active
    active.range('A3').value = "3m ADF=" + str(adf3_test[0])
    active.range('A4').value = "3m p-value=" + str(adf3_test[1])
    active.range('B3').value = "6m ADF=" + str(adf6_test[0])
    active.range('B4').value = "6m p-value=" + str(adf6_test[1])

def make_categorical(df, col_name):
    df.loc[:, col_name] = pd.Categorical(df[col_name])

def mem_mib(df):
    print("{0:.2f} MiB".format(
        df.memory_usage().sum() / (1024 * 1024)
    ))

def get_sens_info(fileToExamine, toFilter):
    list_of_dataframes = []
    size = 100000
    total = 0
    df1 = pd.read_csv(fileToExamine, delimiter = ',', chunksize=size)
    instrumentTenorsAll = {}
    underlyingTenorsAll = {}
    riskMeasureTypeAll = {}
    partyNameAll = {}
    active = xw.sheets.active
    for chunk in df1:
        total = total + size
        columns_to_keep = ["ProformaShiftValue", "PartyName", "CLMS ID", "InstrumentTenor", "RiskMeasureType","UnderlyingTenor"]
        df_quick = chunk.filter(columns_to_keep)
        make_categorical(df_quick, "PartyName")
        make_categorical(df_quick, "InstrumentTenor")
        make_categorical(df_quick, "RiskMeasureType")
        make_categorical(df_quick, "UnderlyingTenor")

        instrumentTenors = pd.Categorical(df_quick["InstrumentTenor"])
        instrumentTenorsDict = dict(enumerate(instrumentTenors.categories))
        instrumentTenorsAll = {**instrumentTenorsAll, **instrumentTenorsDict}

        underlyingTenors = pd.Categorical(df_quick["UnderlyingTenor"])
        underlyingTenorsDict = dict(enumerate(underlyingTenors.categories))
        underlyingTenorsAll = {**underlyingTenorsAll, **underlyingTenorsDict}

        riskMeasureType = pd.Categorical(df_quick["RiskMeasureType"])
        riskMeasureTypeDict = dict(enumerate(riskMeasureType.categories))
        riskMeasureTypeAll = {**riskMeasureTypeAll, **riskMeasureTypeDict}

        partyName = pd.Categorical(df_quick["PartyName"])
        partyNameDict = dict(enumerate(partyName.categories))
        partyNameAll = {**partyNameAll, **partyNameDict}

        #filtered = df_quick.query('InstrumentTenor=="2M"')
        if toFilter:
            toFilter = toFilter.replace('^','"')
            #filtered = df_quick.loc[lambda x: (x.InstrumentTenor == '1M') | (x.InstrumentTenor == '2M')]
            filtered = df_quick.query(toFilter)
            list_of_dataframes.append(filtered)
            active.range('F3').value = total
        else:
            list_of_dataframes.append(df_quick)
            active.range('F3').value = total


    df_final = pd.concat(list_of_dataframes)
    active = xw.sheets.active
    #active.range('A2').value = toFilter
    active.range('A3').options(transpose=True).value = [ v for v in instrumentTenorsAll.values() ]
    active.range('B3').options(transpose=True).value = [ v for v in underlyingTenorsAll.values() ]
    active.range('C3').options(transpose=True).value = [ v for v in riskMeasureTypeAll.values() ]
    active.range('D3').options(transpose=True).value = [ v for v in partyNameAll.values() ]
    active.range('E3').value = df_final.shape[0]

def get_sens_data(fileToExamine, toFilter):
    list_of_dataframes = []
    size = 100000
    total = 0
    df1 = pd.read_csv(fileToExamine, delimiter = ',', chunksize=size)
    
    active = xw.sheets.active
    for chunk in df1:
        total = total + size
        columns_to_keep = ["ProformaShiftValue", "PartyName", "CLMS ID", "InstrumentTenor", "RiskMeasureType","UnderlyingTenor"]
        df_quick = chunk.filter(columns_to_keep)
        make_categorical(df_quick, "PartyName")
        make_categorical(df_quick, "InstrumentTenor")
        make_categorical(df_quick, "RiskMeasureType")
        make_categorical(df_quick, "UnderlyingTenor")

        #filtered = df_quick.query('InstrumentTenor=="2M"')
        if toFilter:
            toFilter = toFilter.replace('^','"')
            #filtered = df_quick.loc[lambda x: (x.InstrumentTenor == '1M') | (x.InstrumentTenor == '2M')]
            filtered = df_quick.query(toFilter)
            list_of_dataframes.append(filtered)
            active.range('B1').value = total
        else:
            list_of_dataframes.append(df_quick)
            active.range('B1').value = total


    df_final = pd.concat(list_of_dataframes)
    active = xw.sheets.active

    active.range('A3').value = df_final


