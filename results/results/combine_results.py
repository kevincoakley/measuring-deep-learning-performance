
import csv, glob, os

csv_files = glob.glob("*.csv")
csv_files = sorted(csv_files)

for csv_file in csv_files:

    # Skip the combined CSV files
    if "combined" in csv_file:
        continue

    print(csv_file)
    csv_file_split = csv_file[:-4].split("-")
    
    model = csv_file_split[0]
    dataset = csv_file_split[1]
    cluster = csv_file_split[2]
    gpu = csv_file_split[3]
    framework = csv_file_split[4]
    environment = csv_file_split[5]
    run = csv_file_split[6]
    
    if len(csv_file_split) == 7:
       output_file = f"{model}-{dataset}-{cluster}-{gpu}-{framework}-{environment}-combined.csv"
    elif len(csv_file_split) == 8:
       addional = csv_file_split[6]
       run = csv_file_split[7]
       output_file = f"{model}-{dataset}-{cluster}-{gpu}-{framework}-{environment}-{addional}-combined.csv"

    if os.path.exists(output_file):
        write_header = False
    else:
        write_header = True

    rows = []
    csv_control_values = {}
    csv_seed_values = {}

    # Read the source CSV file
    with open(csv_file, newline='') as csv_read_data:
        csv_reader = csv.reader(csv_read_data, delimiter=',', quotechar='"')
        for row in csv_reader:
            # Get the header from the first row of the CSV
            if row[0] == "run_name":
                header = row
            # Read the control rows
            elif row[17] == "123456789" or row[16] == "123456789":
                # If the control value doesn't exist, add it to the dictionary
                if output_file not in csv_control_values:
                    csv_control_values[output_file] = row[len(row) - 1]
                else:
                    # If the control value doesn't matches the previous control value
                    # exit with an error
                    if csv_control_values[output_file] != row[len(row) - 1]:
                        print("ERROR: control value mismatch")
                        exit()
            else:
                # If the combined CSV file isn't in the dictionary, add it
                if output_file not in csv_seed_values:
                    csv_seed_values[output_file] = []
                # If the seed value doesn't exist in the dictionary, add it
                if row[11] not in csv_seed_values[output_file]:
                    csv_seed_values[output_file].append(row[10])
                    rows.append(row)
                # If the seed value already exists in the dictionary, exit with an error
                else:
                    print("ERROR: duplicate seed")
                    exit()

    with open(output_file, "a") as csv_write_data:

        csv_writer = csv.writer(csv_write_data)

        if write_header:
            csv_writer.writerow(header)

        csv_writer.writerows(rows)
