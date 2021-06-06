from datetime import datetime

from setuptools._vendor import more_itertools


class Apriori:
    def __init__(self, transactions, min_support, min_confidence, len_max):
        self.transactions = transactions
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.len_max = len_max
        self.sum_tran = len(transactions)
        self.list_frequent_itemsets = []
        self.l_conf = []
        self.temp = []
        self.l_support = []

    def time(self, s1, s2):
        s1, s2 = str(s1), str(s2)
        hour1 = int(s1[0:2])
        hour2 = int(s2[0:2])
        min1 = int(s1[3:5])
        min2 = int(s2[3:5])
        second1 = int(s1[6:8])
        second2 = int(s2[6:8])
        return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2 - second1)

    #toileanh
    def init_itemsets(self):
        itemsets = set()
        for i in self.transactions:
            for item in i:
                itemsets.add(item)
        results = []
        for i in list(itemsets):
            results.append([i])
        return results

    def create_new_candidate(self, itemsets):
        len_itemset = len(itemsets[0]) + 1
        items = set()
        for i in itemsets:
            for item in i:
                items.add(item)
        items = list(items)
        sinhtohop = more_itertools.distinct_combinations(items, len_itemset)
        candidate_itemsets = []
        for i in sinhtohop:
            candidate_itemsets.append(list(i))
        return candidate_itemsets


    def frequent_itemset(self, candidate_itemsets):
        frequent_itemsets = []
        for i in candidate_itemsets:
            if self.support_itemset(i) >= self.min_support:
                frequent_itemsets.append(i)
        return frequent_itemsets

    def create_frequent_itemsets(self):
        if (self.len_max < 1):
            print("Số item trong Frequent set phải lớn hơn 1 :) ")
        else:
            time1 = datetime.now().time()
            frequent_itemset = []
            itemset = self.init_itemsets()
            frequent_itemsets = self.frequent_itemset(itemset)
            for i in range(self.len_max - 1):
                new_candidates = self.create_new_candidate(
                    frequent_itemsets)
                frequent_itemsets = self.frequent_itemset(
                    new_candidates)
                if (len(frequent_itemsets) == 0):
                    print("Độ dài tối đa của  : %d" % (i + 1))
                    time2 = datetime.now().time()
                    print("Thời gian supported_itemsets len %d: " % (i + 2), self.time(time1, time2))
                    return frequent_itemset
                    break
                else:
                    frequent_itemset.append(frequent_itemsets)
                    time2 = datetime.now().time()
                    print("Time supported_itemsets len %d: " % (i + 2), self.time(time1, time2))
            return frequent_itemset

    def create_frequent_itemset_max(self):
        itemset = self.init_itemsets()
        frequent_itemsets = self.frequent_itemset(itemset)
        print("Len new_item 1 :", len(itemset))
        print("new_items 1: ", itemset)
        print("Len supported_itemset 1: ", len(frequent_itemsets))
        print("frequent_itemset 1: ", frequent_itemsets)
        i = 0
        while (True):
            new_candidates = self.create_new_candidate(frequent_itemsets)
            frequent_itemsets = self.frequent_itemset(new_candidates)
            if len(frequent_itemsets) > 0:
                print(
                    "================================================================================================")
                print("Len new_item %d :" % (i + 2), len(new_candidates))
                print("new_items %d : " % (i + 2), new_candidates)
                print("Len supported_itemset %d : " % (i + 2), len(frequent_itemsets))
                print("frequent_itemset %d : " % (i + 2), frequent_itemsets)
                i += 1
            else:
                return i + 1, frequent_itemsets

    def support_itemset(self, itemset):
        dem = 0
        for i in self.transactions:
            if all(itemm in i for itemm in itemset):
                dem += 1
        return dem / self.sum_tran

    def confident_itemset(self, X, Y):
        XY = []
        XY.extend(X)
        XY.extend(Y)
        return round(float(self.support_itemset(XY) / self.support_itemset(X)), 3)

    def confident_supported_itemset(self, left, right):
        self.rules(left, right)
        if len(left) == 1:
            pass
        else:
            for i in more_itertools.distinct_combinations(left, 1):
                x, y = left.copy(), right.copy()
                y.append(list(i)[0])
                x.remove(list(i)[0])
                if self.confident_itemset(x, y) >= self.min_confidence:
                    self.confident_supported_itemset(x, y)

    def rules(self, left, right):
        if len(right) > 0:
            for i in self.temp:
                if all(itemm in i for itemm in left) and len(left) == len(i):
                    return
            self.list_frequent_itemsets.append([left, right])
            self.l_conf.append(self.confident_itemset(left, right))
            c = []
            c.extend(left)
            c.extend(right)
            self.l_support.append(self.support_itemset(c))
            self.temp.append(left)

    def gen_rules(self, frequent_itemsets):
        for itemset in frequent_itemsets:
            self.temp = []
            left = itemset.copy()
            right = []
            self.confident_supported_itemset(left, right)
        return self.list_frequent_itemsets, self.l_support, self.l_conf
