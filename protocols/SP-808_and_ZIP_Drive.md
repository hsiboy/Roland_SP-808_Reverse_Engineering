# Technical Paper: Initialisation of Iomega Zip Drive by Roland SP-808

## Abstract:

This technical paper explores the initialization process of an Iomega Zip Drive by the Roland SP-808. The SP-808 communicates with the Zip drive using ATAPI commands, revealing unique interactions and potential manufacturer-specific extensions by Iomega. The paper aims to provide a comprehensive understanding of the commands issued during the initialization process.

## 1. Introduction:

The Roland SP-808 utilizes the ATAPI protocol to communicate with an Iomega Zip Drive for storage purposes. This paper delves into the initialization sequence, examining the commands issued by the SP-808 and noting any proprietary extensions introduced by Iomega.

## 2. Initialization Commands:

### 2.1 Software Reset:

The initialization process begins with a software reset (SRST) command, initiated by the SP-808 to reset the ATA interface.

```plaintext
[00:02:00 DEBUG D0 A0 5A] Software (SRST) Reset
```

### 2.2 IDENTIFY PACKET DEVICE:

Following the reset, the SP-808 issues the IDENTIFY PACKET DEVICE command to gather detailed information about the connected Zip drive.

```plaintext
[00:02:00 DEBUG D0 A1 --] IDENTIFY PACKET DEVICE
```

### 2.3 SET FEATURES:

A SET FEATURES command is utilized by the SP-808, employing manufacturer-specific extensions.

```plaintext
[00:02:00 DEBUG D0 EF --] SET FEATURES ID - drive: A0
[00:02:00 DEBUG D0 EF --] Subcomm: 03, params: 08 | 01 | 14 | eb
```

Manufacturer-specific extensions may include configuring features or settings specific to Iomega's implementation.

### 2.4 Request Sense and Unit Attention:

The SP-808 issues a REQUEST SENSE command to retrieve information about a reported Unit Attention condition.

```plaintext
[00:02:00 DEBUG D0 A0 03] REQUEST SENSE: key=06, asc=29, ascq=00
```

### 2.5 START/STOP UNIT:

A START/STOP UNIT command is issued, possibly to initialize or start the drive.

```plaintext
[00:02:00 DEBUG D0 A0 1B] START/STOP UNIT: LoEj: 0, start: 1, immed: 0
```

### 2.6 ATAPI INQUIRY:

The ATAPI INQUIRY command is used to obtain information about the connected Iomega Zip Drive.

```plaintext
[00:02:00 DEBUG D0 A0 12] ATAPI INQUIRY
```

### 2.7 MODE SENSE:

MODE SENSE commands are employed, possibly for retrieving information about specific modes supported by the drive.

```plaintext
[00:02:00 DEBUG D0 A0 5A] MODE SENSE (10)
[00:02:00 DEBUG D0 A0 5A] MODE SENSE PC=0, PageCode=2f, alloc_len=80
```

Manufacturer-specific extensions, such as Iomega's proprietary commands, may be present in the output.

### 2.8 READ Commands:

The SP-808 issues READ commands to read data from the Zip Drive, specifying the number of sectors and desired block size.

```plaintext
[00:05:52 TRACE D0 A0 A8] Packet: A8 00 00 00 00 21 00 00 00 09 00 00, DMA: 0
[00:05:52 DEBUG D0 A0 A8] READ (12), sector: 33, len: 9
```

## 3. Conclusion:

This technical paper outlines the initialization process of an Iomega Zip Drive by the Roland SP-808, detailing the specific ATAPI commands issued during the interaction. Noteworthy are manufacturer-specific extensions, potentially introduced by Iomega, emphasizing the importance of understanding unique implementations for successful integration.

## 4. Acknowledgments:

The authors would like to acknowledge the importance of documentation and communication standards in ensuring seamless interactions between devices.

---

Feel free to expand on each section with more details, explanations, or additional insights based on your specific knowledge of the interaction between the SP-808 and the Iomega Zip Drive.
