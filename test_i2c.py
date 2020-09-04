from machine import I2C,Pin

i2c = I2C(scl=Pin(14), sda=Pin(2), freq=1000 * 100) #SCL=GPIO14, SDA=GPIO2
device_id = 66
print(i2c.scan())

i=0
while True:
    try:
        if i2c.writeto(device_id,bytearray('abc')):
            print(i,i2c.readfrom(device_id,2))
            i+=1
        if i>9:
            break
    except:
        pass