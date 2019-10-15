# Picoevb_Keccak256hash_Pcie_ipi
Keccak256 hash on picoevb fpga pcie board with xilinx artix7 FPGA

Keccak256 hash algo is implemented on artix7 fpga using xdma pcie ip, using axi-stream interface.

Upload *.mcs file to FPGA using Vivado.

Download and install XDMA Drivers
https://github.com/RHSResearchLLC/XilinxAR65444

Do a cold shutdown, then start system, as PCIe is enumerated during BIOS boot-up.

run the code with following command:
python3 keccak256hash_pcie.py

Here is the link where you can buy this fpga
https://picoevb.com/
