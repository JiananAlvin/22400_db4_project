# NOTES:
# Connect pin 25 (A1) with pin 32 (the one to linearize)
# Set DAC_Vmax (should be 3.15 in all devices, but...)
# Set the desired ADC_MAX = 2^ADC_BIT_WIDTH-1 and the proper adc.width(ADC.WIDTH_10BIT)

import gc
from machine import Pin
from machine import ADC
from machine import DAC

import machine
import utime

ADC_DELAY = 10
DAC_DELAY = 5

ADC_PIN_NO = 32
DAC_PIN_NO = 25

NUM_SAMPLES = 50
ADC_MAX = 1023
DAC_MAX = 255

DAC_Vmax = 3.15
DAC_Vmin = 0.09 # Not used!

DAC_QUANTUM = DAC_Vmax / DAC_MAX

look_up_ADC = []

# Initialize ADC
adc = ADC(Pin(ADC_PIN_NO))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_10BIT) # was 10

# Initialize DAC
dac = DAC(Pin(DAC_PIN_NO), bits=8)

# Measure
adc_read = []
for i in range(0, DAC_MAX+1):
    print('Samples acquired: ' + str(i) + '/' + str(DAC_MAX))
    dac.write(i)
    utime.sleep_ms(ADC_DELAY)
    raw_read = []
    for i in range(1, NUM_SAMPLES+1):
        raw_read.append(adc.read())
        utime.sleep_ms(DAC_DELAY)
    adc_read.append(round(sum(raw_read)/NUM_SAMPLES))

# Print result
#print(adc_read)

adc_V_lookup = []

for i in range(0, ADC_MAX+1):
    gc.collect()
    gc.mem_free()
    print('Processing index ' + str(i))
    if adc_read.count(i) == 1:
        print('  1 to 1 match!')
        # There is a 1 to 1 match
        adc_V_lookup.append(DAC_QUANTUM * adc_read.index(i))
    elif adc_read.count(i) == 0:
        print('  No match!')
        # There is not a match, interpolating
        # Searching range indexes (min and max)
        range_min = -1
        i_min = i-1
        while(range_min==-1):
            if i_min < min(adc_read):
                range_min = adc_read.index(min(adc_read))
            elif i_min in adc_read:
                range_min = adc_read.index(i_min)
            else:
                i_min = i_min - 1

        range_max = -1
        i_max = i+1
        while(range_max==-1):
            if i_max > max(adc_read):
                range_max = adc_read.index(max(adc_read))
            elif i_max in adc_read:
                range_max = adc_read.index(i_max)
            else:
                i_max = i_max + 1
        print('  i_min: ' + str(i_min) +  ' range_min: ' + str(range_min) +  ' i_max: ' + str(i_max) +  ' range_max: ' + str(range_max))
        # Interpolation
        adc_V_lookup.append(DAC_QUANTUM * (range_min + ((range_max - range_min)/(i_max-i_min))*(i-i_min)))
    else:
        print('  Multiple matches!')
        # There are multiple matches, collapsing
        # Searching range indexes (min and max)
        tmp_range = []
        for j in range(0, DAC_MAX+1):
            if adc_read[j] == i:
                tmp_range.append(j)
        range_min = min(tmp_range)
        range_max = max(tmp_range)
        # Collapsing
        adc_V_lookup.append(DAC_QUANTUM * ((range_max - range_min)/2 + range_min))
    print('  adc_V :' + str(adc_V_lookup[i]) + ' V')

print('----------------------------------------------------')
print('----------------------------------------------------')
print(adc_V_lookup)
