
#!/usr/bin/env python3
import os
import time
import binascii
import codecs

def swap_order(d, wsz=16, gsz=2 ):
    return "".join(["".join([m[i:i+gsz] for i in range(wsz-gsz,-gsz,-gsz)]) for m in [d[i:i+wsz] for i in range(0,len(d),wsz)]])

expected_genesis_hash = "00000009c4e61bee0e8d6236f847bb1dd23f4c61ca5240b74852184c9bf98c30"
blockheader1 = "020000005bf0e2f283edac06ea087a9324dc9bd865c79b175658849bd83900000000000085246da7e6e530d276d5f8e0d4222cb8938f7af0e9d6678ec08ff133812f4b7251e8e35cec16471af51dd61c"
expected_hash1 = "00000000623c9e9d39c1fb7ab7290b3014b6348d10c54aa6ab6fc408385dfaa6"

def read_fpga_temprature():

    #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
    # open port and then read from dedicated register
    fd = os.open("/dev/xdma0_user", os.O_RDWR)
    temp = os.pread(fd,32,0x0000 + 0x200)[::-1] # read temerature out from temperature register
    temp_reg = int.from_bytes(temp, "big")  
    t = ((int(temp_reg)/65536.0)/0.00198421639) - 273.15
    # print("--------------------------------------")
    print ("Temperature : {} Celsius".format(t))
    # print("--------------------------------------")
    os.close(fd)

# Read FPGA MAX Temprature
def read_fpga_maxtemprature():

    #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
    # open port and then read from dedicated register
    fd = os.open("/dev/xdma0_user", os.O_RDWR)
    temp = os.pread(fd,32,0x0000 + 0x280)[::-1] # read maxtemerature out from temperature register
    temp_reg = int.from_bytes(temp, "big")  
    t = ((int(temp_reg)/65536.0)/0.00198421639) - 273.15
    # print("--------------------------------------")
    print ("Temperature Max: {} Celsius".format(t))
    # print("--------------------------------------")
    os.close(fd)

# Read vccint voltage
def read_fpga_VCCINT():
    #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
    # open port and then read from dedicated register
    fd = os.open("/dev/xdma0_user", os.O_RDWR)
    vint_temp = os.pread(fd,32,0x0000 + 0x204)[::-1] # read voltage out from vccint register
    volt_int = int.from_bytes(vint_temp, "big")  
    vint = ((volt_int) * 3.0)/65536.0
    # print("--------------------------------------")
    print ("VCCINT : {0:.04f} V".format(vint))
    # print("--------------------------------------")
    os.close(fd)

# # Read max vccint voltage
# def read_fpga_maxVCCINT():
#     #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
#     # open port and then read from dedicated register
#     fd = os.open("/dev/xdma0_user", os.O_RDWR)
#     vint_temp = os.pread(fd,32,0x0000 + 0x284)[::-1] # read max voltage out from vccint register
#     volt_int = int.from_bytes(vint_temp, "big") 
#     print(volt_int) 
#     vint = ((volt_int) * 3.0)/65536.0
#     print("--------------------------------------")
#     print ("VCCINT max: {0:.04f} V".format(vint))
#     print("--------------------------------------")
#     os.close(fd)

# Read vccaux , read fpga auxillary volatges
def read_fpga_VCCAUX():
    #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
    # open port and then read from dedicated register
    fd = os.open("/dev/xdma0_user", os.O_RDWR)
    vaux_temp = os.pread(fd,32,0x0000 + 0x208)[::-1] # read voltage out from vccaux register
    volt_int = int.from_bytes(vaux_temp, "big")  
    vint = ((volt_int) * 3.0)/65536.0
    # print("--------------------------------------")
    print ("VCCAUX : {0:.04f} V".format(vint))
    # print("--------------------------------------")
    os.close(fd)

def read_fpga_VCCBRAM():
    #XADC IP is connected to xdma pcie IP via axi4-lite interface on base-addr 0x40000000
    # open port and then read from dedicated register
    fd = os.open("/dev/xdma0_user", os.O_RDWR)
    vbram_temp = os.pread(fd,32,0x0000 + 0x218)[::-1] # read voltage out from vccbram register
    volt_int = int.from_bytes(vbram_temp, "big")  
    vint = ((volt_int) * 3.0)/65536.0
    # print("--------------------------------------")
    print ("VCCBRAM : {0:.04f} V".format(vint))
    # print("--------------------------------------")
    os.close(fd)

def hash_genesis_block():

    blockheader = ("02000000" +
        "a4051e368bfa0191e6c747507dd0fdb03da1a0a54ed14829810b97c6ac070000" +
        "e932b0f6b8da85ccc464d9d5066d01d904fb05ae8d1ddad7095b9148e3f08ba6" +
        "bcfb6459" +
        "f0ff0f1e" + 
        "3682bb08")
    print("txdata:%s" %blockheader)
    blockheader_bin = binascii.unhexlify(swap_order(blockheader))
    tx_data = blockheader_bin

    # Open files
    fd_h2c = os.open("/dev/xdma/card0/h2c0", os.O_WRONLY)
    fd_c2h = os.open("/dev/xdma/card0/c2h0", os.O_RDONLY)

    start_time = time.time()
    # Send to FPGA 
    os.pwrite(fd_h2c, tx_data, 0)

    # Receive from FPGA 
    rx_data = os.pread(fd_c2h, 32, 0)
    end_time = time.time()
    delay = end_time -start_time
    blockheder_rx = codecs.encode(rx_data,'hex').decode('ascii')
    print("rxdata:%s" %swap_order(blockheder_rx)[0:64])
    print("Time elapsed:%f microsec" %(delay*1000000))
    os.close(fd_h2c)
    os.close(fd_c2h)

##############################################    
def main():
    
    hash_genesis_block()
    read_fpga_temprature()
    read_fpga_maxtemprature()
    read_fpga_VCCINT()
    read_fpga_VCCAUX()
    read_fpga_VCCBRAM()
##############################################    

if __name__ == '__main__':
    main()
