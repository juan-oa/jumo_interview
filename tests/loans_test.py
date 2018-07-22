from loans import Loans
from decimal import Decimal
import unittest


class TestLoan(unittest.TestCase):
    def setUp(self):
        self.data = [[27729554427, 'Network 1', '12-Mar-2016', 'Loan Product 1', 1000.00],
                     [27729554428, 'Network 1', '12-Mar-2016', 'Loan Product 1', 1000.00]]

    def test_aggregator_positive_00(self):
        # Test positive
        expected = [['Network 1', 'Loan Product 1', 'Mar-2016', Decimal('2000'), 2]]
        loans = Loans(self.data)
        result = loans.aggregated
        self.assertEqual(result, expected, 'Aggregation Failed')
        self.assertEqual(list(loans.msisdn), [27729554427, 27729554428], 'MSISDN does not match')
        self.assertEqual(dict(loans.counter), {27729554427: 1, 27729554428: 1}, 'Did not process all rows')

    def test_aggregator_parsing_01(self):
        # Test parsing of incorrect formatting
        expected = [['Network 1', 'Loan Product 1', 'Mar-2016', Decimal('2000'), 2]]
        loans = Loans(self.data)
        result = loans.aggregated
        self.data.append([27729554429, 'Network 1', 'Loan Product 1', '03/2016', Decimal('2000'), 2])
        self.assertEqual(result, expected, 'Aggregation with incorrect date failed')
