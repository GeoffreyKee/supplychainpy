import unittest
from unittest import TestCase
from decimal import Decimal
from supplybipy import model_inventory
import os


def print(selected):
    pass


class TestBuildModel(TestCase):
    _yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    _yearly_demand2 = {'jan': 75}
    _t = {}
    _inventory_summary = {'average_order': type(0.00), 'economic_order_quantity': type(0.00),
                          'reorder_level': type(0.00)}

    def test_model_orders_type(self):
        summary = model_inventory.analyse_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        self.assertIs(type(summary), type(self._t))

    def test_model_orders_length(self):
        with self.assertRaises(expected_exception=ValueError):
            summary = model_inventory.analyse_orders(self._yearly_demand2, 'RX983-90', 3, 50.99, 400, 1.28)

    def test_model_orders_content(self):
        summary = model_inventory.analyse_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        self.assertEqual(int(summary.get("average_order")), int(50))
        self.assertEqual(int(summary.get("standard_deviation")), int(25))
        #finish with all members

    def test_standard_deviation_row_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400)
        # act

        # assert
        self.assertEquals(len(d), 16)

    def test_file_path_extension_row(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/tel.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        with self.assertRaises(expected_exception=Exception):
            d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400, file_type="text")

    def test_file_path_extension_col(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        with self.assertRaises(expected_exception=Exception):
            d = model_inventory.analyse_orders_from_file_col(abs_file_path, 1.28, 400, file_type="text")


    def test_standard_deviation_col_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="text")
        # act
        # assert
        self.assertEquals(len(d), 11)

    def test_standard_deviation_col_count_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/data_col.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="csv")
        # act
        # assert
        self.assertEquals(len(d), 11)

    def test_standard_deviation_row_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400)

        for row in d:
            std = row.get('standard_deviation')
        # assert
        self.assertEqual(Decimal(std), 25)

    def test_standard_deviation_col_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="text")
        # act
        # assert
        print(d.get('standard_deviation'))
        self.assertEquals(Decimal(d.get('standard_deviation')), 25)

    def test_analyse_orders_from_file_row_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, z_value=Decimal(1.28),
                                                         reorder_cost=Decimal(400), file_type="csv")
        for row in d:
            if row['sku'] == 'KR202-209':
                std = row.get('standard_deviation')
        # assert
        self.assertEqual(Decimal(std), 976)


if __name__ == '__main__':
    unittest.main()
