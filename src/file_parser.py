import csv


class CSVReader:
    """
    Interface to allow for different methods of inputting data to the system
    """

    def __init__(self, strategy=None, args={}):
        """
        Initialise a chosen strategy.

        :param object strategy: Chosen concrete strategy class.
        :param dict args: Optional arguments if concrete strategy requires parameters.
        """
        self._length = None
        self.action = None
        if strategy:
            self.action = strategy(args)

    def __iter__(self):
        """
        Iterable object to load one row into memory at a time. Abstracts where the file is coming from.
        """
        if self.action:
            self._length = 0
            for row in self.action.__iter__():
                self._length += 1
                yield row
        else:
            raise UnboundLocalError('No strategy class supplied to CSVReader')

    def __len__(self):
        """
        Calculates the number of rows in CSV.
        This method can be used to split up the file for multiprocessing.

        :return: Number of rows in CSV
        :rtype: int
        """
        if self._length is None:
            for row in self:
                continue
        return self._length

    @property
    def number_read(self):
        """
        Track how many entries have been read.
        This method can be used to split up the file for multiprocessing.

        :return: Number of rows processed
        :rtype: int
        """
        return self._length


class CSVReaderFileSystem:
    """
    Concrete class to read CSV from file system
    """

    def __init__(self, args):
        self.path = args.get('path', 'data/Loans.csv')

    def __iter__(self):
        with open(self.path, 'r') as file:
            file.readline()
            csv_reader = csv.reader(file, quotechar="'")
            for row in csv_reader:
                yield row


class CSVReaderAPI:
    """
    Concrete class to read CSV from API
    This class has been added to prove scalability
    """

    def __init__(self, args):
        raise NotImplementedError('CSV reading from API not yet implemented')

    def __iter__(self):
        raise NotImplementedError('CSV reading from API not yet implemented')


class CSVReaderStream:
    """
    Concrete class to read CSV from data stream
    This class has been added to prove scalability
    """

    def __init__(self, args):
        raise NotImplementedError('CSV reader from data stream not yet implemented')

    def __iter__(self, args):
        raise NotImplementedError('CSV reader from data stream not yet implemented')


class CSVWriter:
    """
    Interface to output loan specific CSV files
    """

    @classmethod
    def output_csv(cls, header, rows, path='Output.csv'):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
