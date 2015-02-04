import sys,getopt
import csv
import uuid

def transform_data(filename, level, header=False):
    output = [['id', 'amount', 'admin', 'cofog', 'geocode']] if header else []
    
    with open(filename) as input_file:
        for row in csv.DictReader(input_file):
            if len(str(row['Cofog1'])) == 1:
                cofog1 = '0'+str(row['Cofog1'])
            else:
                cofog1 = str(row['Cofog1'])

            cofog2 = '.'.join([cofog1, str(row['Cofog2'])])
            cofog = '.'.join([cofog2, str(row['Cofog3'])])
                
            output_row = [uuid.uuid4().hex,
                          row.get('Amount', row.get('amount', '')).strip(),
                          row.get('Title', row.get('title', '')).strip(),
                          cofog.strip(),
                          level.strip()]
            output.append(output_row)

    return output

def write_rows(filename, output):
    with open(filename, 'a') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output)

def parse_commandline():
    '''
    Parse command line variables
    -i input-file (can also be args)
    -o output-file
    -h header
    -l level
    '''

    # Read command line args (-i, -o, -m and -l are allowed)
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:hl:")
 
    # Store parse results in argument dictionary
    arguments = {'header': False,
                 'output': 'output.csv'}

    for option, argument in myopts:
        if option == '-i':
            arguments['input'] = argument
        elif option == '-o':
            arguments['output'] = argument
        elif option == '-h':
            arguments['header'] = True
        elif option == '-l':
            arguments['level'] = argument
        else:
            # Do nothing if unrecognized
            pass

    return arguments

if __name__ == "__main__":
    # Get all the important arguments
    args = parse_commandline()

    # Read and transform the data
    output_rows = transform_data(args['input'], args['level'],
                                 header=args['header'])
        
    # Write the data to a new file (default file name: 'output.csv')
    write_rows(args['output'], output_rows)
