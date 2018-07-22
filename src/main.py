from file_parser import CSVReader, CSVWriter, CSVReaderFileSystem
from loans import Loans


def get_input_with_default(prompt, default='Loans.csv'):
    """
    Ask for user input in console and provide a default value if none is given.

    :param str prompt: Message to present to user
    :param str default: Default value if none is given by user
    :return: Returns input value or default
    :rtype: str
    """
    return input(prompt) or default


if __name__ == '__main__':
    retry = True
    while retry:
        try:
            # Read input from file
            input_path = get_input_with_default('Enter the path of loans file: ', 'data/Loans.csv')
            data = CSVReader(CSVReaderFileSystem, {'path': input_path})

            # Initialise aggregator object with data
            loans = Loans(data)

            # Output aggregation
            output_path = get_input_with_default('Save file as: ', 'Output.csv')
            header = ['Network', 'Product', 'Date', 'Currency', 'Count']
            CSVWriter.output_csv(header, loans.aggregated, output_path)

            # Processed successfully, save to exit
            retry = False
            print('Process Successful!')
        except FileNotFoundError as e:
            # File was not found, should retry a different path
            print('{WARN]: %s' % e)
            print('Please try a different path', end='\n\n')
            continue
        except NotImplementedError as e:
            # Safely handle CSVReading strategies to be implemented
            print('{ERROR]: %s' % e)
            raise SystemExit(0)
