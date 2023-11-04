import sys
import argparse
import logging

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to decrypt DTMF encoded string
def decrypt_multitap_code(encoded_string):
    """
    Decrypts the DTMF encoded string.
    
    Parameters:
    encoded_string (str): The DTMF encoded string.

    Returns:
    str: The decoded string.
    """
    code_dict = {
        '2': 'A', '22': 'B', '222': 'C', '3': 'D', '33': 'E', '333': 'F',
        '4': 'G', '44': 'H', '444': 'I', '5': 'J', '55': 'K', '555': 'L',
        '6': 'M', '66': 'N', '666': 'O', '7': 'P', '77': 'Q', '777': 'R', '7777': 'S',
        '8': 'T', '88': 'U', '888': 'V', '9': 'W', '99': 'X', '999': 'Y', '9999': 'Z'
    }

    decoded_string = ""
    current_digit = None
    count = 0

    for digit in encoded_string.split(' '):
        if current_digit is None or current_digit != digit:
            if current_digit is not None:
                decoded_string += code_dict[current_digit][(count - 1) % len(code_dict[current_digit])]
            current_digit = digit
            count = 1
        else:
            count += 1

    decoded_string += code_dict[current_digit][(count - 1) % len(code_dict[current_digit])]
    return decoded_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', type=str, help='(File containing DTMF tones in 77 666 7777 7 2 222 33 666 66 ..... format)')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as file:
            encoded_string = file.read().strip()

        decoded_string = decrypt_multitap_code(encoded_string)
        print("Decoded String:", decoded_string)

    except FileNotFoundError:
        logging.error('File not found')
        print("Error: File not found. Please provide a valid input file.")

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        print("An error occurred. Please check the input file and try again.")
