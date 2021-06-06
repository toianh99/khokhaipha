# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime

import apriori


import pandas as pd


def time(s1, s2):
    s1, s2 = str(s1), str(s2)
    hour1 = int(s1[0:2])
    hour2 = int(s2[0:2])
    min1 = int(s1[3:5])
    min2 = int(s2[3:5])
    second1 = int(s1[6:8])
    second2 = int(s2[6:8])
    return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2 - second1)

def read_transaction(file):  # tên file
    data = pd.read_excel(file, sheet_name="Test")
    transactions = []
    invoice_item = set()  # mã hóa đơn
    for i in range(len(data)):
        item = data['Description'][i]
        invoice_item.add(item)  # loại bỏ kí tự cách ở đầu và cuối tên mặt hàng
        if (i < len(data) - 1 and data['InvoiceNo'][i] != data['InvoiceNo'][i + 1]):
            transactions.append(list(invoice_item))
            invoice_item = set()
        if (i == len(data) - 1):
            transactions.append(list(invoice_item))  # thêm một transaction và tập transaction
    return transactions

if __name__ == '__main__':
    time1 = datetime.now().time()
    print("Thời gian bắt đầu ", time1)
    transactions=read_transaction('Book1.xlsx')
    print("Số giao dịch:", len(transactions))
    time2 = datetime.now().time()
    print("Thời gian bắt đầu thuật toán ", time2)
    min_support = 0.014
    min_confidence = 0.6
    apri = apriori.Apriori(transactions, min_support=min_support, min_confidence=min_confidence, len_max=3)
    frequent_itemsets = apri.create_frequent_itemsets()
    print("Đã tạo xong frequent_itemsets at: ", datetime.now().time())
    for j in range(len(frequent_itemsets)):
        time3 = datetime.now().time()
        apri.list_frequent_itemsets = []
        rules, l_support, l_conf = apri.gen_rules(frequent_itemsets[j])
        time4 = datetime.now().time()
        gen_rule = {'X': [],
                    'Y': [],
                    'Support': [],
                    'Confident': [],
                    }
        for i in range(len(rules)):
            gen_rule['X'].append(rules[i][0])
            gen_rule['Y'].append(rules[i][1])
            gen_rule['Support'].append(l_support[i])
            gen_rule['Confident'].append(l_conf[i])
            print("Rule:", rules[i][0], "===>", rules[i][1])
            print("Support: ", l_support[i])
            print("Confident: ", l_conf[i])
            print("-----------------------------------------------------------------------------------------")
        df = pd.DataFrame(gen_rule)
        filename = "C:/Users/Admin//" + "thuat_toan_" + str(datetime.now().date()) + "_" + str(min_support) + "_" + str(
            min_confidence) + ".xlsx"
        df.to_excel(filename)


