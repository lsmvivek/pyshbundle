import re
import numpy
import julian
import datetime

def read_tn13(file_path):
    data_dict = {}
    
    with open(file_path, 'rt') as file:
        lines = file.readlines()
        for line in lines:

            # Extract data using regex
            pattern = re.compile(r'^GRCOF2\s+(\d+)\s+(\d+)\s+([-+]?\d*\.\d+e[-+]?\d+)\s+([-+]?\d*\.\d+e[-+]?\d+)\s+([-+]?\d*\.\d+e[-+]?\d+)\s+([-+]?\d*\.\d+e[-+]?\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)')
            match = pattern.match(line)
            
            if match:
                degree = int(match.group(1))
                order = int(match.group(2))
                Clm = float(match.group(3))
                Slm = float(match.group(4))
                Clm_sdev = numpy.longdouble(match.group(5))
                Slm_sdev = numpy.longdouble(match.group(6))
                epoch_begin = match.group(7)
                epoch_end = match.group(8)

                # Use epoch start as key but in yyyy-mm-dd format
                epoch_key=datetime.datetime.strptime(epoch_begin, '%Y%m%d.%H%M%S').strftime('%Y-%m')
                data_dict[epoch_key, degree, order] = {
                    'degree': degree,
                    'order': order,
                    'Clm': Clm,
                    'Slm': Slm,
                    'Clm_sdev': Clm_sdev,
                    'Slm_sdev': Slm_sdev,
                    'epoch_begin': epoch_begin,
                    'epoch_end': epoch_end,
                }
    # Print a sample of the data to check if it's parsed correctly
    # for key in sorted(data_dict.keys())[:5]:  # print first 5 entries
    #     print(f"{key}: {data_dict[key]}")
    return data_dict
