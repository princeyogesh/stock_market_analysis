import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
# from PyQt5.QtCore import pyqtslot
from PyQt5.QtCore import QSize
from PyQt5 import QtGui

company = "TSLA"


class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'stock market'
        self.left = 500
        self.top = 300
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("stock2.jpg"))
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel(self)
        pixmap = QPixmap('stock5.jpg')
        label.setPixmap(pixmap)

        self.dropdown = QComboBox(self)  ## we have to make drop down in order to select company
        self.dropdown.addItems(["TSLA", "MSFT", "NVDA", "CSCO", "NFLX"])
        self.dropdown.move(20, 50)
        self.dropdown.show()
        self.dropdown.setStyleSheet("background-color: blue;color: white")
        comapny = self.dropdown.currentText()

        button = QPushButton('Show text', self)
        button.move(0, 80)
        button.clicked.connect(self.sel_comp)
        button.setStyleSheet("background-color: red;color: white")



        button = QPushButton('weekly', self)
        button.setToolTip('Weekly Analysis')
        button.move(100, 50)
        button.resize(100, 40)
        button.clicked.connect(self.on_click)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('monthly', self)
        button.setToolTip('Monthly Analysis')
        button.move(100, 100)
        button.resize(100, 40)
        button.clicked.connect(self.on_click2)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('daily', self)
        button.setToolTip('Daily analysis')
        button.move(100, 150)
        button.resize(100, 40)
        button.clicked.connect(self.on_click3)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('bolingerband', self)
        button.setToolTip('Bolinger_Bads_ info')
        button.move(100, 200)
        button.resize(100, 40)
        button.clicked.connect(self.on_click4)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('$ to Rupee', self)
        button.setToolTip('Currency conversion')
        button.move(350, 150)
        button.resize(100, 40)
        button.clicked.connect(self.on_click5)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('bitcoin in US$', self)
        button.setToolTip('Cryptocurrency Info')
        button.move(350, 100)
        button.resize(100, 40)
        button.clicked.connect(self.on_click6)
        button.setStyleSheet("background-color: brown;color: white")

        button = QPushButton('bitcoin in INR', self)
        button.setToolTip('Cryptocurrencies in INR')
        button.move(350, 50)
        button.resize(100, 40)
        button.clicked.connect(self.on_click7)
        button.setStyleSheet("background-color: brown;color: white")

        self.show()

    @pyqtSlot()
    def on_click(self):
        print(company)
        plot_weekly()


    def on_click2(self):
        plot_monthly()

    def on_click3(self):
        plot_daily()

    def on_click4(self):
        bolinger_bands()

    def on_click5(self):
        currency_xchange()

    def on_click6(self):
        bitcoin_value_US()

    def on_click7(self):
        bitcoin_value_IND()

    def sel_comp(self):
        global company
        company = self.dropdown.currentText()
        print(self.dropdown.currentText())

    print(company)

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
from pandas import ExcelWriter
import matplotlib.pyplot as plt

ts = TimeSeries(key="X8HJ480KMWF82SML", output_format="pandas")
ti = TechIndicators(key='X8HJ480KMWF82SML', output_format='pandas')
crc = CryptoCurrencies(key="X8HJ480KMWF82SML", retries=5, output_format="pandas")
fe = ForeignExchange(key="X8HJ480KMWF82SML", output_format="json")


def export_data_to_excell():  # to be done properly some errors
    writer = ExcelWriter("data.xlsx")
    data, metadata = get_monthly(symbol="TSLA")
    data.to_excel(writer, "Sheet1")
    writer.save()


# to get data from alphavantage
def daily():
    data, meta_data = ts.get_daily(symbol="TSLA", outputsize="compact")
    print(data)


def monthly():
    data, meta_data = ts.get_monthly(symbol="TSLA")
    print(data)  # prints from 8 years


def weekly():
    data, meta_data = ts.get_weekly(symbol="TSLA")
    print(data)


def plotintraday():
    sel_type = select_which_type_you_want_to_plot()
    data, meta_data = ts.get_intraday(symbol="TSLA", interval="1min", outputsize="full")
    data[sel_type].plot()
    print(data)
    plt.title('Intraday Times Series for the TSLA stock (1 min)')
    plt.show()


def plot_daily():
    sel_type = select_which_type_you_want_to_plot()
    data, meta_data = ts.get_daily(symbol=company, outputsize="full")
    data[sel_type].plot()
    print(type(data))
    print(data)
    plt.title("DAILY TIMESEREIS FOR "+company+" STOCK ")
    plt.ylabel("stock rate")
    plt.xlabel("time period")
    plt.show()


def plot_monthly():
    sel_type = select_which_type_you_want_to_plot()
    data, meta_data = ts.get_monthly(symbol=company)
    data[sel_type].plot()
    print(data)
    plt.title("monthly TIMESEREIS FOR "+company+ " STOCK ")
    plt.ylabel("stock rate")
    # plt.xscale = 100
    plt.xlabel("time period")
    plt.show()


def plot_weekly():
    sel_type = select_which_type_you_want_to_plot()
    data, meta_data = ts.get_weekly(symbol=company)
    data[sel_type].plot()
    print(data)
    plt.title("WEEKLY TIMESEREIS FOR "+company+" STOCK ")
    plt.ylabel("stock rate")
    plt.xlabel("time period")
    plt.show()


def bolinger_bands():
    #   ti = TechIndicators(key='X8HJ480KMWF82SML', output_format='pandas')
    data, meta_data = ti.get_bbands(symbol=company, interval='60min', time_period=60)
    data.plot()
    plt.title('BBbands indicator for ' +company+  ' stock (60 min)')
    plt.show()


def bitcoin_value_US():
    data, metadata = crc.get_digital_currency_daily(symbol="BTC", market="INR")
    print(data)
    data["1b. open (USD)"].plot()
    plt.title("BITCOIN VALUES wrt US dollars")
    plt.show()


def bitcoin_value_IND():
    data, metadata = crc.get_digital_currency_daily(symbol="BTC", market="INR")
    print(data)
    data["1a. open (INR)"].plot()
    plt.title("BITCOIN VALUES wrt indian rupee")
    plt.show()


def currency_xchange():
    rate = fe.get_currency_exchange_rate("USD", "INR")
    print(rate)


def select_which_type_you_want_to_plot():
    sel_type = "4. close"

    select_col = input("enter one of these 1.open,2.close, 3.high, 4. low")
    if (select_col == "open"):
        sel_type = "1. open"
    elif (select_col == "close"):
        sel_type = "4. close"
    elif (select_col == "low"):
        sel_type = "3. low"
    elif (select_col == "high"):
        sel_type = "2. high"

    return sel_type


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




