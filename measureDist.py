def calculateRefpower( rssi, measuredPower ):

    RSSI_ = abs(rssi)

    if (RSSI_ == 0):
        return -1
    
    ratio = RSSI_ / measuredPower
    if ( ratio < 1):
        return pow(ratio,8)


    return (0.69976 * pow(ratio, 7.7095 )+ 0.111)


# x = calculateAccuracy(-47,197)

# print(x)