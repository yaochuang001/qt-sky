# modbus连接plc
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md

master = mt.TcpMaster('192.168.3.11', 502)
master.set_timeout(2)

data1 = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=300,
                                 quantity_of_x=20)
data2 = master.execute(slave=1, function_code=md.READ_COILS, starting_address=8,
                             quantity_of_x=4)
data3 = master.execute(slave=1, function_code=md.READ_COILS, starting_address=8692,
                             quantity_of_x=10)
print("读取保持寄存器D300-D319对应的值：{}".format(str(data1)))
print("读取线圈Y10-Y13对应的值：{}".format(str(data2)))
print("读取线圈M500-M509对应的值：{}".format(str(data3)))
data4 = master.execute(slave=1, function_code=md.WRITE_SINGLE_COIL, starting_address=8192,
                       output_value=1)
data5 = master.execute(slave=1, function_code=md.WRITE_SINGLE_REGISTER, starting_address=0,
                       output_value=10)
