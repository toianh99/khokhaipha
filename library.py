import pandas as pd
from efficient_apriori import apriori
from datetime import datetime


def time(s1, s2):
    s1, s2 = str(s1), str(s2)
    hour1 = int(s1[0:2])
    hour2 = int(s2[0:2])
    min1 = int(s1[3:5])
    min2 = int(s2[3:5])
    second1 = int(s1[6:8])
    second2 = int(s2[6:8])
    return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2 - second1)

def read_transaction(file):
    data = pd.read_excel(file, sheet_name="Test")
    transactions = []
    invoice_item = set()
    for i in range(len(data)):
        invoice_item.add(data['Description'][i])
        if (i < len(data) - 1 and data['InvoiceNo'][i] != data['InvoiceNo'][i + 1]):
            transactions.append(list(invoice_item))
            invoice_item = set()
        if (i == len(data) - 1):
            transactions.append(list(invoice_item))
    return transactions


time1 = datetime.now().time()
print("Thời gian bắt đầu lúc: ", time1)
transactions = read_transaction('Book1.xlsx')
print("Tổng giao dịch:", len(transactions))
time2 = datetime.now().time()
print("bắt đầu thuật toán ", time2)
len_rule = 4
min_support = 0.014
min_confidence = 0.6
itemsets, rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, max_length=len_rule)
print("tổng rules: ", len(rules))
list_rule = []

rules_rhs_2 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == 2, rules)
l_2 = list(rules_rhs_2)
sum_rules_2 = len(l_2)
list_rule.append(l_2)

rules_rhs_3 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == 3, rules)
l_3 = list(rules_rhs_3)
sum_rules_3 = len(l_3)
list_rule.append(l_3)
rules_rhs_4 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == len_rule, rules)
l_4 = list(rules_rhs_4)
sum_rules_4 = len(l_4)
list_rule.append(l_4)
for i in range(len(list_rule)):
    gen_rule = {'X': [],
                'Y': [],
                'Support': [],
                'Confident': [],
                }
    for rule in sorted(list_rule[i], key=lambda rule: rule.lhs):
        gen_rule['X'].append(list(rule.lhs))
        gen_rule['Y'].append(list(rule.rhs))
        gen_rule['Support'].append(rule.support)
        gen_rule['Confident'].append(rule.confidence)
    df = pd.DataFrame(gen_rule)
    filename = "" + "C:/Users/Admin//" + str(i + 2) + "_" + str(
        min_support) + "_" + str(min_confidence) + ".xlsx"
    df.to_excel(filename)

