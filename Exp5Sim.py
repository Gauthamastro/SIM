import numpy as np
import pandas as pd


def calculateAQ(BI, ID):
    if BI >= ID:
        return ID
    else:
        return BI


def calculateEI(BI, AQ):
    return BI - AQ


def calculateLS(ID, AQ):
    return ID - AQ


def calculateBI(RQ, PI):
    return RQ + PI


def calculateED(alpha, ID, ED):
    return int((alpha * ID) + ((1 - alpha) * ED))


class supplychain_sim:

    def __init__(self):
        self.RQ = 0
        self.PI = 1
        self.BI = 2
        self.ID = 3
        self.ED = 4
        self.AQ = 5
        self.EI = 6
        self.OOQ = 7
        self.OQ = 8
        self.LS = 9
        self.DEL_LEAD_TIME = 10
        self.storage_retailer = np.zeros((30, 11))
        self.storage_wholesaler = np.zeros((30, 11))
        self.storage_distributor = np.zeros((30, 11))
        self.storage_factory = np.zeros((30, 11))
        self.week_counter = 0
        self.order_lead_time = 0
        self.alpha = 0.25
        self.unit_holding_cost_retailer = 5
        self.unit_holding_cost_wholesaler = 4
        self.unit_holding_cost_distributor = 3
        self.unit_holding_cost_factory = 1
        self.unit_bo_cost_retailer = 10
        self.unit_bo_cost_wholesaler = 8
        self.unit_bo_cost_distributor = 6
        self.unit_bo_cost_factory = 2
        self.period_start = 4
        self.period_stop = 22

    def reset(self, demand, leadTime):
        if len(demand) != 30:
            appendArray = [0]
            for i in range(29 - len(demand)):
                appendArray.append(0)
            demand = np.append(demand, appendArray)
        if len(leadTime) != 30:
            appendArray_ = [0]
            for i in range(29 - len(leadTime)):
                appendArray_.append(0)
            leadTime = np.append(leadTime, appendArray_)

        # ORDER_LEAD_TIME
        self.storage_retailer[:, self.DEL_LEAD_TIME] = leadTime
        self.storage_wholesaler[:, self.DEL_LEAD_TIME] = leadTime
        self.storage_distributor[:, self.DEL_LEAD_TIME] = leadTime
        self.storage_factory[:, self.DEL_LEAD_TIME] = leadTime

        # ID
        self.storage_retailer[:, self.ID] = demand

        # For 1st Week
        # Factory
        # RQ
        self.storage_factory[0, self.RQ] = 0
        # PI
        self.storage_factory[0, self.PI] = 285
        # BI
        self.storage_factory[0, self.BI] = calculateBI(self.storage_factory[0, self.RQ],
                                                       self.storage_factory[0, self.PI])
        # ID
        self.storage_factory[0, self.ID] = 0
        # ED
        self.storage_factory[0, self.ED] = self.storage_factory[0, self.ID]
        # AQ
        self.storage_factory[0, self.AQ] = calculateAQ(self.storage_factory[0, self.BI],
                                                       self.storage_factory[0, self.ID])
        # EI
        self.storage_factory[0, self.EI] = calculateEI(self.storage_factory[0, self.BI],
                                                       self.storage_factory[0, self.AQ])
        # OOQ
        self.storage_factory[0, self.OOQ] = 0

        # LS
        self.storage_factory[0, self.LS] = calculateLS(self.storage_factory[0, self.ID],
                                                       self.storage_factory[0, self.AQ])

        # Distributor
        # RQ
        self.storage_distributor[0, self.RQ] = 0
        # PI
        self.storage_distributor[0, self.PI] = 285
        # BI
        self.storage_distributor[0, self.BI] = calculateBI(self.storage_distributor[0, self.RQ],
                                                           self.storage_distributor[0, self.PI])
        # ID
        self.storage_distributor[0, self.ID] = 0
        # ED
        self.storage_distributor[0, self.ED] = self.storage_distributor[0, self.ID]
        # AQ
        self.storage_distributor[0, self.AQ] = calculateAQ(self.storage_distributor[0, self.BI],
                                                           self.storage_distributor[0, self.ID])
        # EI
        self.storage_distributor[0, self.EI] = calculateEI(self.storage_distributor[0, self.BI],
                                                           self.storage_distributor[0, self.AQ])
        # OOQ
        self.storage_distributor[0, self.OOQ] = 0

        # LS
        self.storage_distributor[0, self.LS] = calculateLS(self.storage_distributor[0, self.ID],
                                                           self.storage_distributor[0, self.AQ])

        # Wholesaler
        # RQ
        self.storage_wholesaler[0, self.RQ] = 0
        # PI
        self.storage_wholesaler[0, self.PI] = 285
        # BI
        self.storage_wholesaler[0, self.BI] = calculateBI(self.storage_wholesaler[0, self.RQ],
                                                          self.storage_wholesaler[0, self.PI])
        # ID
        self.storage_wholesaler[0, self.ID] = 0
        # ED
        self.storage_wholesaler[0, self.ED] = self.storage_wholesaler[0, self.ID]
        # AQ
        self.storage_wholesaler[0, self.AQ] = calculateAQ(self.storage_wholesaler[0, self.BI],
                                                          self.storage_wholesaler[0, self.ID])
        # EI
        self.storage_wholesaler[0, self.EI] = calculateEI(self.storage_wholesaler[0, self.BI],
                                                          self.storage_wholesaler[0, self.AQ])
        # OOQ
        self.storage_wholesaler[0, self.OOQ] = 0

        # LS
        self.storage_wholesaler[0, self.LS] = calculateLS(self.storage_wholesaler[0, self.ID],
                                                          self.storage_wholesaler[0, self.AQ])
        # Retailer
        # RQ
        self.storage_retailer[0, self.RQ] = 0
        # PI
        self.storage_retailer[0, self.PI] = 285
        # BI
        self.storage_retailer[0, self.BI] = calculateBI(self.storage_retailer[0, self.RQ],
                                                        self.storage_retailer[0, self.PI])
        # ID
        # ID is already set
        # ED
        self.storage_retailer[0, self.ED] = self.storage_retailer[0, self.ID]
        # AQ
        self.storage_retailer[0, self.AQ] = calculateAQ(self.storage_retailer[0, self.BI],
                                                        self.storage_retailer[0, self.ID])
        # EI
        self.storage_retailer[0, self.EI] = calculateEI(self.storage_retailer[0, self.BI],
                                                        self.storage_retailer[0, self.AQ])
        # OOQ
        self.storage_retailer[0, self.OOQ] = 0

        # LS
        self.storage_retailer[0, self.LS] = calculateLS(self.storage_retailer[0, self.ID],
                                                        self.storage_retailer[0, self.AQ])
        return self.storage_retailer, self.storage_wholesaler, self.storage_distributor, self.storage_factory

    def step_one_week(self, predictions):
        self.week_counter += 1
        assert (len(predictions) == 4)

        # Factory
        # OQ
        self.storage_factory[self.week_counter - 1, self.OQ] = predictions[3]
        # RQ of factory for future weeks
        self.storage_factory[
            self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] = \
            self.storage_factory[
                self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] + \
            self.storage_factory[self.week_counter - 1, self.OQ]

        # OOQ for future weeks (if any)
        for i in range(0, int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), 1):
            self.storage_factory[self.week_counter + i, self.OOQ] = self.storage_factory[
                                                                        self.week_counter + i, self.OOQ] + \
                                                                    self.storage_factory[self.week_counter - 1, self.OQ]
        # ID
        self.storage_factory[self.week_counter + self.order_lead_time, self.ID] = predictions[2]
        # PI
        self.storage_factory[self.week_counter, self.PI] = self.storage_factory[self.week_counter - 1, self.EI]
        # ED
        self.storage_factory[self.week_counter, self.ED] = calculateED(self.alpha,
                                                                       self.storage_factory[
                                                                           self.week_counter, self.ID],
                                                                       self.storage_factory[
                                                                           self.week_counter - 1, self.ED])
        # BI
        self.storage_factory[self.week_counter, self.BI] = calculateBI(self.storage_factory[self.week_counter, self.RQ],
                                                                       self.storage_factory[self.week_counter, self.PI])
        # AQ
        self.storage_factory[self.week_counter, self.AQ] = calculateAQ(self.storage_factory[self.week_counter, self.BI],
                                                                       self.storage_factory[self.week_counter, self.ID])

        # RQ for Distributor for future weeks
        self.storage_distributor[
            self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] = \
            self.storage_distributor[
                self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] + \
            self.storage_factory[
                self.week_counter, self.AQ]
        # EI
        self.storage_factory[self.week_counter, self.EI] = calculateEI(self.storage_factory[self.week_counter, self.BI],
                                                                       self.storage_factory[self.week_counter, self.AQ])
        # LS
        self.storage_factory[self.week_counter, self.LS] = calculateLS(self.storage_factory[self.week_counter, self.ID],
                                                                       self.storage_factory[self.week_counter, self.AQ])

        # Distributor
        # OQ
        self.storage_distributor[self.week_counter - 1, self.OQ] = predictions[2]

        # OOQ for future weeks (if any)
        for i in range(0, int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), 1):
            self.storage_distributor[self.week_counter + i, self.OOQ] = self.storage_distributor[
                                                                            self.week_counter + i, self.OOQ] + \
                                                                        self.storage_distributor[
                                                                            self.week_counter - 1, self.OQ]
        # ID
        self.storage_distributor[self.week_counter + self.order_lead_time, self.ID] = predictions[1]
        # PI
        self.storage_distributor[self.week_counter, self.PI] = self.storage_distributor[self.week_counter - 1, self.EI]
        # ED
        self.storage_distributor[self.week_counter, self.ED] = calculateED(self.alpha,
                                                                           self.storage_distributor[
                                                                               self.week_counter, self.ID],
                                                                           self.storage_distributor[
                                                                               self.week_counter - 1, self.ED])
        # BI
        self.storage_distributor[self.week_counter, self.BI] = calculateBI(
            self.storage_distributor[self.week_counter, self.RQ],
            self.storage_distributor[self.week_counter, self.PI])
        # AQ
        self.storage_distributor[self.week_counter, self.AQ] = calculateAQ(
            self.storage_distributor[self.week_counter, self.BI],
            self.storage_distributor[self.week_counter, self.ID])

        # RQ for Wholesaler for future weeks
        self.storage_wholesaler[
            self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] = \
            self.storage_wholesaler[
                self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] + \
            self.storage_distributor[
                self.week_counter, self.AQ]
        # EI
        self.storage_distributor[self.week_counter, self.EI] = calculateEI(
            self.storage_distributor[self.week_counter, self.BI],
            self.storage_distributor[self.week_counter, self.AQ])
        # LS
        self.storage_distributor[self.week_counter, self.LS] = calculateLS(
            self.storage_distributor[self.week_counter, self.ID],
            self.storage_distributor[self.week_counter, self.AQ])

        # Wholesaler
        # OQ
        self.storage_wholesaler[self.week_counter - 1, self.OQ] = predictions[1]

        # OOQ for future weeks (if any)
        for i in range(0, int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), 1):
            self.storage_wholesaler[self.week_counter + i, self.OOQ] = self.storage_wholesaler[
                                                                           self.week_counter + i, self.OOQ] + \
                                                                       self.storage_wholesaler[
                                                                           self.week_counter - 1, self.OQ]
        # ID
        self.storage_wholesaler[self.week_counter + self.order_lead_time, self.ID] = predictions[0]
        # PI
        self.storage_wholesaler[self.week_counter, self.PI] = self.storage_wholesaler[self.week_counter - 1, self.EI]
        # ED
        self.storage_wholesaler[self.week_counter, self.ED] = calculateED(self.alpha,
                                                                          self.storage_wholesaler[
                                                                              self.week_counter, self.ID],
                                                                          self.storage_wholesaler[
                                                                              self.week_counter - 1, self.ED])
        # BI
        self.storage_wholesaler[self.week_counter, self.BI] = calculateBI(
            self.storage_wholesaler[self.week_counter, self.RQ],
            self.storage_wholesaler[self.week_counter, self.PI])
        # AQ
        self.storage_wholesaler[self.week_counter, self.AQ] = calculateAQ(
            self.storage_wholesaler[self.week_counter, self.BI],
            self.storage_wholesaler[self.week_counter, self.ID])

        # RQ for Retailer for future weeks
        self.storage_retailer[
            self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] = \
            self.storage_retailer[
                self.week_counter + int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), self.RQ] + \
            self.storage_wholesaler[
                self.week_counter, self.AQ]
        # EI
        self.storage_wholesaler[self.week_counter, self.EI] = calculateEI(
            self.storage_wholesaler[self.week_counter, self.BI],
            self.storage_wholesaler[self.week_counter, self.AQ])
        # LS
        self.storage_wholesaler[self.week_counter, self.LS] = calculateLS(
            self.storage_wholesaler[self.week_counter, self.ID],
            self.storage_wholesaler[self.week_counter, self.AQ])

        # Retailer
        # OQ
        self.storage_retailer[self.week_counter - 1, self.OQ] = predictions[0]

        # OOQ for future weeks (if any)
        for i in range(0, int(self.storage_retailer[self.week_counter - 1, self.DEL_LEAD_TIME]), 1):
            self.storage_retailer[self.week_counter + i, self.OOQ] = self.storage_retailer[
                                                                         self.week_counter + i, self.OOQ] + \
                                                                     self.storage_retailer[
                                                                         self.week_counter - 1, self.OQ]
        # ID
        # Already defined while initialization
        # PI
        self.storage_retailer[self.week_counter, self.PI] = self.storage_retailer[self.week_counter - 1, self.EI]
        # ED
        self.storage_retailer[self.week_counter, self.ED] = calculateED(
            self.alpha,
            self.storage_retailer[self.week_counter, self.ID],
            self.storage_retailer[self.week_counter - 1, self.ED])
        # BI
        self.storage_retailer[self.week_counter, self.BI] = calculateBI(
            self.storage_retailer[self.week_counter, self.RQ],
            self.storage_retailer[self.week_counter, self.PI])
        # AQ
        self.storage_retailer[self.week_counter, self.AQ] = calculateAQ(
            self.storage_retailer[self.week_counter, self.BI],
            self.storage_retailer[self.week_counter, self.ID])
        # LS
        self.storage_retailer[self.week_counter, self.LS] = calculateLS(
            self.storage_retailer[self.week_counter, self.ID],
            self.storage_retailer[self.week_counter, self.AQ])
        # EI
        self.storage_retailer[self.week_counter, self.EI] = calculateEI(
            self.storage_retailer[self.week_counter, self.BI],
            self.storage_retailer[self.week_counter, self.AQ])


default_demand = [82, 73, 92, 85, 90, 74, 83, 79, 85, 83, 91, 57, 72, 87, 77, 69, 74, 91, 84, 67, 101, 82, 72, 83, 97]
delivery_lead_time = [2, 0, 2, 4, 4, 4, 0, 2, 4, 1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 1, 1, 4, 2, 2]


def generateDemand(mean, std):
    demand = np.random.normal(mean, std, 25).tolist()
    return np.round(demand)


def generateDeliveryLeadTime(mean, std):
    demand = np.random.normal(mean, std, 25)
    return np.maximum(np.round(demand), np.zeros_like(demand)).tolist()


# default_demand = generateDemand(mean=100, std=15)
# delivery_lead_time = generateDeliveryLeadTime(mean=2, std=1)

sim = supplychain_sim()
state = sim.reset(default_demand, delivery_lead_time)

retailer = pd.read_excel('DATA1.xlsx', sheet_name='Retailer')
wholesaler = pd.read_excel('DATA1.xlsx', sheet_name='Wholesaler')
dist = pd.read_excel('DATA1.xlsx', sheet_name='Distributor')
fact = pd.read_excel('DATA1.xlsx', sheet_name='Factory')

pred = np.hstack((retailer['Unnamed: 9'].values[2:len(retailer['Unnamed: 9'].values) - 6].reshape(25, 1),
                  wholesaler['Unnamed: 9'].values[2:len(wholesaler['Unnamed: 9'].values) - 4].reshape(25, 1),
                  dist['Unnamed: 9'].values[2:len(dist['Unnamed: 9'].values) - 4].reshape(25, 1),
                  fact['Unnamed: 9'].values[2:len(fact['Unnamed: 9'].values) - 4].reshape(25, 1)))
for prediction in pred:
    sim.step_one_week(prediction)

print(["RQ", "PI", "BI", "ID", "ED", "AQ", "EI", "OOQ", "OQ", "LS", "LEAD_TIME"])

print(sim.storage_factory)
