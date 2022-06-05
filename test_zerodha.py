import datetime
from xlwt import Workbook
from time import sleep
from selenium import webdriver
import csv


def test_setup():
    global driver, sheet1, wb, data_count, file_name
    data_count = 20
    file_name = "data_set3.csv"
    driver = webdriver.Chrome("chrome drivr location")
    driver.get("https://kite.zerodha.com/")
    # driver.minimize_window()
    z_userid = "userid"
    z_pwd = "pw"
    z_pin = "pin"
    wb = Workbook()
    sheet1 = wb.add_sheet('sheet1')

    sleep(3)
    # Set username
    inputElement = driver.find_element_by_id("userid")
    inputElement.send_keys(z_userid)

    # Set password
    pwdElement = driver.find_element_by_id("password")
    pwdElement.send_keys(z_pwd)

    # Login
    inputElement.submit()

    # Set PIN (6 digit)
    sleep(3)
    pwdElement = driver.find_element_by_id("pin")
    pwdElement.send_keys(z_pin)
    pwdElement.submit()
    sleep(5)

    for x in range(1, data_count + 1):
        print("Data count no : " + str(x))
        get_price(driver, x)

    driver.close()


def get_price(driver, i):
    global ct, sym
    """
    Get the price from the driver obj
    """
    # Get prices
    elements = driver.find_elements_by_class_name("last-price")
    # Get symbols
    name_elements = driver.find_elements_by_class_name("nice-name")

    val = []
    sym = [7]
    val_check = []
    for ele in elements:
        # Iterate the prices
        if not "\n" in ele.get_attribute('innerHTML'):
            ct = datetime.datetime.now()
            val.append(ele.get_attribute('innerHTML'))
            sleep(1)
            val_check.append(ele.get_attribute('innerHTML'))
            print(val, "OLD VAL")
            print(val_check, "NEW VAL")
            with open('live_data.csv', 'a') as csv_file:
                csv_write = csv.writer(csv_file)
                csv_write.writerow(val_check)
    for ele in name_elements:
        # Iterate the Symbol
        stock_name = ele.get_attribute('innerHTML')
        sym.append(stock_name)
        # print(zip(val, sym))
    # Make list(tuples)
    res = list(zip(val, sym))
    print(res)
    # pdb.set_trace()

    if val == val_check:
        pass
    else:
        var = float(val[0]) - float(val_check[0])
        print(var, "DIFFERANCE VALUE")
        j = 0
        for x in range(len(val)):
            if j < len(val):
                sheet1.write(i, j, val[j])
                sheet1.write(i, len(sym) + 1, var)

                j = j + 1
        sheet1.write(i, len(sym), str(ct))
        if i < len(val):
            sheet1.write(i, j, val[j])
            i = len(sym) + 1


def test_write_excel_header():
    i = 0
    j = 0
    while sym != []:
        if i < len(sym):
            sheet1.write(0, i, sym[j])
            j = j + 1
        if i == len(sym):
            break
        i = i + 1
    sheet1.write(0, len(sym), "TIME")
    sheet1.write(0, len(sym) + 1, "Diff val")

    wb.save(file_name)
