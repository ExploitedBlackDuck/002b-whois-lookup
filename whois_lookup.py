import logging
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError, ASNRegistryError, HTTPLookupError, WhoisLookupError

# Configure logging
logging.basicConfig(filename='whois_lookup.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

sourcefile = 'input.txt'  # file with IP address
outfile = 'results.csv'  # file to write the IP addresses

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
