import serial

def send_command(port, command):
    port.write(command)
    response = port.read(512)  # Adjust the read size based on your CF card's response size
    return response

def identify_cf_card(serial_port):
    # Open the serial port
    port = serial.Serial(serial_port, 9600, timeout=1)
    
    # Send the IDENTIFY command
    identify_command = b'\xEC\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    response = send_command(port, identify_command)
    
    # Process the response
    if response:
        # Extract information from Word 0
        word0 = response[54:56]  # Assuming Word 0 is located at offset 54-55
        word0_value = int.from_bytes(word0, byteorder='little')
        
        # Decode Word 0 value into English
        decoding_table = {
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
          
            # Add more decoding entries based on your CF card's specifications
        }
        decoded_word0 = decoding_table.get(word0_value, "Unknown")
        
        # Print the extracted information
        print("Manufacturer:", response[27:47].decode('utf-8').strip())
        print("Model:", response[23:27].decode('utf-8').strip())
        print("Serial Number:", response[10:20].decode('utf-8').strip())
        print("Word 0 Value:", hex(word0_value))
        print("Word 0 Decoded:", decoded_word0)
    else:
        print("No response from the CF card.")
    
    # Close the serial port
    port.close()

# Specify the serial port to which the CF card is connected
serial_port = '/dev/ttyUSB0'  # Update with your specific serial port

# Call the function to identify the CF card
identify_cf_card(serial_port)
