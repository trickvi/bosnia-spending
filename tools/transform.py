import sys,getopt
import csv

def get_mapping(filename):
    mapping = {}
    with open(filename) as mapping_file:
        for line in csv.DictReader(mapping_file):
            if line['Bosnian']:
                mapping[line['Code']] = line['Bosnian']

    return mapping

def transform_data(filename, mapping, level):
    output = [['title', 'amount', 'time',
               'cofog1.code', 'cofog1.label',
               'cofog2.code', 'cofog2.label',
               'cofog3.code', 'cofog3.label',
               'level']]
    
    with open(filename) as input_file:
        for row in csv.DictReader(input_file):
            if len(str(row['Cofog1'])) == 1:
                cofog1 = '0'+str(row['Cofog1'])
            else:
                cofog1 = str(row['Cofog1'])

            cofog2 = '.'.join([cofog1, str(row['Cofog2'])])
            cofog3 = '.'.join([cofog2, str(row['Cofog3'])])
                
            output_row = [row.get('Title', row['title']),
                          row.get('Amount', row['amount']),
                          row.get('Time', row['time']),
                          cofog1, mapping[cofog1],
                          cofog2, mapping[cofog2],
                          cofog3, mapping[cofog3],
                          level]
            output.append(output_row)

    return output

def write_rows(filename, output):
    with open(filename, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output)

def parse_commandline():
    '''
    Parse command line variables
    -i input-file (can also be args)
    -o output-file
    -m mapping-file
    -l level
    '''

    # Read command line args (-i, -o, -m and -l are allowed)
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:m:l:")
 
    # Store parse results in argument dictionary
    arguments = {}

    for option, argument in myopts:
        if option == '-i':
            arguments['input'] = argument
        elif option == '-o':
            arguments['output'] = argument
        elif option == '-m':
            arguments['mapping'] = argument
        elif option == '-l':
            arguments['level'] = argument
        else:
            # Do nothing if unrecognized
            pass

    return arguments

if __name__ == "__main__":
    # Get all the important arguments
    args = parse_commandline()

    # Get cofog mapping
    mapping = get_mapping(args['mapping'])

    # Get level
    level = args['level']

    # Read and transform the data
    output_rows = transform_data(args['input'], mapping, level)
        
    # Write the data to a new file (default file name: 'output.csv')
    write_rows(args.get('output', 'output.csv'), output_rows)
