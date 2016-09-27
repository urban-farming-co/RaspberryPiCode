import time
import Adafruit_TCS34725
import smbus


def save(r,g,b, l):
    r1="#%0.2X"%r
    g1="#%0.2X"%g
    b1="#%0.2X"%b
    c = r1+g1[-2:]+b1[-2:]
    print(c)
    f = open("color.txt","w")
    f.write(str(c))
    f.close()
    
    print('Luminosity: {0} lux'.format(l))
    f = open("lux.txt", "w")
    f.write(str(l))
    f.close()

# Create a TCS34725 instance with default integration time (2.4ms) and gain (4x).
tcs = Adafruit_TCS34725.TCS34725()

tcs.set_integration_time(Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_24MS)
# Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
tcs.set_interrupt(False)

# Read the R, G, B, C color data.

def getRGB():
	return tcs.get_raw_data()

def getLux():
        r, g, b, c = tcs.get_raw_data()
        return Adafruit_TCS34725.calculate_lux(r, g, b)  

def capt():
        tcs.enable()
        tcs.set_interrupt(False)
        r,g,b,c = getRGB()

        l = getLux() 
	save(r,g,b, l)
        tcs.disable()
        tcs.set_interrupt(True)

r, g, b, c = tcs.get_raw_data()
# Calculate color temperature using utility functions.  You might also want to
# check out the colormath library for much more complete/accurate color functions.
color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

# Calculate lux with another utility function.
lux = Adafruit_TCS34725.calculate_lux(r, g, b)

# Print out the values.
print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))

# Print out color temperature.
if color_temp is None:
    print('Too dark to determine color temperature!')
else:
    print('Color Temperature: {0} K'.format(color_temp))

# Print out the lux.
print('Luminosity: {0} lux'.format(lux))

# Enable interrupts and put the chip back to low power sleep/disabled.
tcs.set_interrupt(True)
tcs.disable()

capt()
