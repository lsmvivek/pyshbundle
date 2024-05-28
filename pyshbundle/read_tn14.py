import gzip
import re
import numpy
import julian

def read_tn14(file_path):
    data_dict = {}
    
    with open(file_path, 'rt') as file:
        lines = file.readlines()
        for line in lines:

            # Extract data using regex
            pattern = re.compile(
                r'(\d+\.\d+)\s+(\d+\.\d+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+|NaN)?\s+([-\d.eE+]+|NaN)?\s+([-\d.eE+]+|NaN)?\s+(\d+\.\d+)\s+(\d+\.\d+)')
            match = pattern.match(line)
            
            if match:
                mjd_start = float(match.group(1))
                year_frac_start = float(match.group(2))
                c20 = numpy.longdouble(match.group(3))
                c20_mean_diff = numpy.longdouble(match.group(4))
                c20_sigma = numpy.longdouble(match.group(5))
                c30 = match.group(6)
                c30_mean_diff = match.group(7)
                c30_sigma = match.group(8)
                mjd_end = float(match.group(9))
                year_frac_end = float(match.group(10))

                # Only add C30 if it exists (not)
                if c30.lower() != 'nan':
                    c30 = numpy.longdouble(c30)
                    c30_mean_diff = numpy.longdouble(c30_mean_diff)
                    c30_sigma = numpy.longdouble(c30_sigma)
                else:
                    c30 = None
                    c30_mean_diff = None
                    c30_sigma = None

                # Use mjd as key but in yyyy-mm-dd format
                mjd_key = julian.from_jd(mjd_start, fmt='mjd').date().strftime('%Y-%m')
                data_dict[mjd_key] = {
                    'year_frac_start': year_frac_start,
                    'mjd_start': mjd_start,
                    'c20': c20,
                    'c20_mean_diff': c20_mean_diff,
                    'c20_sigma': c20_sigma,
                    'c30': c30,
                    'c30_mean_diff': c30_mean_diff,
                    'c30_sigma': c30_sigma,
                    'mjd_end': mjd_end,
                    'year_frac_end': year_frac_end
                }
    # Print a sample of the data to check if it's parsed correctly
    # for key in sorted(data_dict.keys())[:5]:  # print first 5 entries
    #     print(f"{key}: {data_dict[key]}")
    return data_dict
