import ata

def identify_cf_card():
    # Open the IDE interface
    with ata.ATAInterface() as interface:
        # Select the appropriate drive (e.g., primary master - 0, primary slave - 1, etc.)
        drive = interface.get_drive(0, 0)  # Update with your specific drive configuration
        
        # Send the IDENTIFY command
        identify_data = drive.identify()
        
        # Process the response
        if identify_data:
            # Extract information from Word 0
            word0 = identify_data[0]
            word0_value = word0.value
            
            # Decode Word 0 value into English
            decoding_table = {
                0x0040: "Fixed disk or removable media",
                0x0080: "Heads can load/unload",
                0x0100: "LBA not supported",
                0x0200: "DMA not supported",
                0x0400: "IORDY not supported",
                0x0800: "LBA48 not supported",
                0x2000: "Advanced Power Management not supported",
                0x4000: "Removable Media not supported",
                0x8000: "ATA/ATAPI-7 not supported",
            }
            
            decoded_word0 = []
            for bit_position, description in decoding_table.items():
                if word0_value & bit_position:
                    decoded_word0.append(description)
            
            # Print the extracted information
            print("Manufacturer:", identify_data.get_manufacturer())
            print("Model:", identify_data.get_model())
            print("Serial Number:", identify_data.get_serial_number())
            print("Word 0 Value:", hex(word0_value))
            print("Word 0 Decoded:")
            for description in decoded_word0:
                print("-", description)
        else:
            print("No response from the CF card.")

# Call the function to identify the CF card
identify_cf_card()
