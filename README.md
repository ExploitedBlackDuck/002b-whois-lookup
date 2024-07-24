# Python Script Documentation: WHOIS Lookup Script

## Purpose
This script performs WHOIS lookups for a list of IP addresses provided in an input text file, retrieves relevant information such as country code, CIDR, and contact name, and writes the results to a CSV file. It also logs the process and any errors encountered during execution.

## Prerequisites
- Python installed on the system.
- `ipwhois` library installed (install using `pip install ipwhois`).
- An input file (`input.txt`) containing a list of IP addresses, each on a new line.

## Script Components

### Importing Modules
The script imports the necessary modules for logging and performing WHOIS lookups:
```python
import logging
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError, ASNRegistryError, HTTPLookupError, WhoisLookupError
```

### Logging Configuration
The script configures logging to write logs to `whois_lookup.log` with a specified format:
```python
logging.basicConfig(filename='whois_lookup.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
```

### File Paths
The script defines the file paths for the input and output files:
```python
sourcefile = 'input.txt'  # File with IP addresses
outfile = 'results.csv'  # File to write the results
```

### Reading Input and Writing Output
The script reads the IP addresses from the input file and writes the results to the output file:
```python
with open(sourcefile, 'r') as inputf:
    with open(outfile, 'a') as outputf:
        addresses = inputf.readlines()

        for i, address in enumerate(addresses):
            address = address.strip()
            print(f"Processing {i + 1}/{len(addresses)}: {address}")

            try:
                ipwhois = IPWhois(address)
                result = ipwhois.lookup_rdap()
                logging.info(f"Successfully retrieved WHOIS information for {address}")

                country = result.get("asn_country_code", "Unknown")
                cidr = result.get("asn_cidr", "Unknown")
                initObjKey = list(result['objects'].keys())[0]
                contact_name = result['objects'][initObjKey]['contact'].get('name', 'Unknown')

                output_line = f"{address},{country},{cidr},{contact_name}\n"
                outputf.write(output_line)
                print(f"Processed {address}: Country={country}, CIDR={cidr}, Contact={contact_name}")

            except (IPDefinedError, ASNRegistryError, HTTPLookupError, WhoisLookupError) as e:
                logging.error(f"Error retrieving WHOIS information for {address}: {e}")
                outputf.write(f"{address},Unknown\n")
                print(f"Could not resolve {address}")
            except Exception as e:
                logging.error(f"Unexpected error for {address}: {e}")
                outputf.write(f"{address},Unknown\n")
                print(f"Unexpected error for {address}")

print("Processing complete. Results written to", outfile)
```

### Exception Handling
The script handles specific exceptions related to WHOIS lookups and logs errors accordingly:
- `IPDefinedError`
- `ASNRegistryError`
- `HTTPLookupError`
- `WhoisLookupError`

It also handles any unexpected exceptions:
```python
except (IPDefinedError, ASNRegistryError, HTTPLookupError, WhoisLookupError) as e:
    logging.error(f"Error retrieving WHOIS information for {address}: {e}")
    outputf.write(f"{address},Unknown\n")
    print(f"Could not resolve {address}")
except Exception as e:
    logging.error(f"Unexpected error for {address}: {e}")
    outputf.write(f"{address},Unknown\n")
    print(f"Unexpected error for {address}")
```

### Completion Message
The script prints a completion message indicating that the processing is complete and the results are written to the output file:
```python
print("Processing complete. Results written to", outfile)
```

## Usage Instructions
1. Ensure you have Python and the `ipwhois` library installed.
   ```bash
   pip install ipwhois
   ```
2. Create an `input.txt` file with a list of IP addresses, each on a new line.
3. Save the script to a `.py` file, for example, `whois_lookup_script.py`.
4. Run the script:
   ```bash
   python whois_lookup_script.py
   ```
5. Check the `results.csv` file for the results and `whois_lookup.log` for logs.

## Example
**input.txt**
```
8.8.8.8
1.1.1.1
192.168.1.1
```

**Command**
```bash
python whois_lookup_script.py
```

**Output in results.csv**
```
8.8.8.8,US,8.8.8.0/24,GOOGLE
1.1.1.1,AU,1.1.1.0/24,CLOUDFLARE
192.168.1.1,Unknown
```

**Log file (whois_lookup.log)**
```
2023-07-24 12:34:56 [INFO] Successfully retrieved WHOIS information for 8.8.8.8
2023-07-24 12:34:57 [INFO] Successfully retrieved WHOIS information for 1.1.1.1
2023-07-24 12:34:58 [ERROR] Error retrieving WHOIS information for 192.168.1.1: IP defined error
```

---

This document outlines the purpose, functionality, and usage of the Python script for performing WHOIS lookups and logging the details.
