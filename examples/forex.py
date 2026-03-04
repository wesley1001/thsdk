from thsdk import THS
import time


with THS() as ths:
    response = ths.forex_list()
    print("基本汇率:")
    print(response.df)
    time.sleep(1)
