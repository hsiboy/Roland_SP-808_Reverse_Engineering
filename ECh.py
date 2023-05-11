import ata

def identify_ata_device():
    # Open the ATA interface
    with ata.ATAInterface() as interface:
        # Iterate through all available drives
        for bus in interface.buses:
            for device in bus.devices:
                # Send the IDENTIFY command
                identify_data = device.identify()
                
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
                    print("Device:", device.name)
                    print("Manufacturer:", identify_data.get_manufacturer())
                    print("Model:", identify_data.get_model())
                    print("Serial Number:", identify_data.get_serial_number())
                    print("Word 0 Value:", hex(word0_value))
                    print("Word 0 Decoded:")
                    for description in decoded_word0:
                        print("-", description)
                    print("--------------------------------------")
                else:
                    print("No response from the device.")
                    print("--------------------------------------")

# Call the function to identify ATA/ATAPI devices
identify_ata_device()
