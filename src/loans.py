from collections import namedtuple, Counter, defaultdict
from datetime import datetime
from decimal import Decimal

fields = ('MSISDN', 'Network', 'Date', 'Product', 'Amount')


class LoanRecord(namedtuple('LoanRecord_', fields)):
    @classmethod
    def parse(cls, row):
        """
        Parse data values to namedtuple fields. Namedtuple chosen as structure is immutable,
        and provides a performance and memory benefit over dict.
        Mapping to namedtuple ensures that row is only loaded to memory when required. It is then processed to ensure
        that values are compatible for aggregating.
        This class also enables possibility of future persistence.

        Input list is expected in order (MSISDN,Network,Date,Product,Amount).

        The method will skip over an incorrectly formatted row and print out the data element it had a problem with.

        :param list row: Single row of values
        :return: Returns type LoanRecord of namedtuple
        :rtype: LoanRecord
        """
        try:
            row = list(row)
            # Parse date to month and year
            row[2] = datetime.strptime(row[2], "%d-%b-%Y").strftime('%b-%Y')
            row[4] = Decimal(row[4])
            return cls(*row)
        except ValueError as e:
            print("[WARN]: %s" % e)
            return False


class Loans(object):
    """
    Aggregator object for loans.
    """

    def __init__(self, iterable):
        self._loans = iterable
        self._counter = Counter()

    def __iter__(self):
        """
        Map data to LoanRecord namedtuple.
        """
        for row in map(LoanRecord.parse, self._loans):
            if row:
                self._counter[row.MSISDN] += 1
                yield row
            else:
                continue

    def add_loans(self, iterable):
        """
        Adds ability to keep process running and add multiple data inputs.

        :param iterable iterable: Any iterable data structure.
        """
        self._loans.extend(iterable)

    @property
    def counter(self):
        """
        Number of times an msisdn has occurs.

        :return: Counter with msisdn as key.
        :rtype: collections.Counter
        """
        if self._counter is False:
            for row in self:
                continue
        return self._counter

    @property
    def msisdn(self):
        """
        MSISDN values which have been processed.

        :return: msisdn values.
        :rtype: list
        """
        return self._counter.keys()

    @property
    def aggregated(self):
        """
        Aggregate loans by (Network, Product, Month).
        Method can make use of multiprocessing in the future to increase performance by adding a map to Pool
        in the loop of self.

        :return: Iterable result of aggregation.
        :rtype: list
        """
        result = []
        aggregated = defaultdict(list)
        for row in self:
            # Hashes the aggregation into dictionary
            # Adds amount to list of values with same key
            keys = (row.Network, row.Product, row.Date)
            aggregated[keys].append(row.Amount)
        for key, values in aggregated.items():
            result.append(list(key) + [sum(values), len(values)])
        return result
