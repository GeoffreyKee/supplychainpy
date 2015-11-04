from decimal import Decimal
from supplybipy import analyse_orders
from unittest import TestCase


class TestAnalyseOrders(TestCase):
    def test_is_average(self):
        # act
        data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                    'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

        d = analyse_orders.OrdersUncertainDemand(data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = d.get_average_orders
        # assert
        self.assertEqual(Decimal(a), 50)

    def test_order_constraint(self):
        # arrange
        orders_placed = [2, 2, 2]  # less than five orders are specified
        # act
        # assert
        with self.assertRaises(TypeError):
            analyse_orders.OrdersUncertainDemand(orders_placed, 'Rx493-90', 4)

    def test_standard_deviation(self):
        # arrange
        data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                    'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

        # act
        d = analyse_orders.OrdersUncertainDemand(data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = d.standard_deviation
        # assert
        self.assertEqual(a, 25)


# put the tests here. if this is called as main then the tests will run


if __name__ == '__main__':
    unittest.main()
