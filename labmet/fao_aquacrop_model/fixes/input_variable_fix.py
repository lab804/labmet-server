def lux_to_n_N(lux):
    """Lux to n/N

    Computes the ratio between sunny
     and cloudy days

    :param lux: The measured amount of lumens
    :return: Lumens to cloudy/sunny ratio
    :rtype: float
    """
    if lux > 20000.0:
        return 1.0
    else:
        return float(lux)/20000.0


def soil_moisture_to_mm(percentage, awc):
    """Soil moisture to mm

    Converts the percentage soil moisture
    into mm, ie converts the percentage
    to the amount of water inside the
    awc(Available Water Content)

    :param percentage: Soil moisture percentage
    :param awc: Soil Water content

    :type percentage: int or float
    :type awc: float

    :return: Soil Moisture im mm
    :rtype: int or float
    """
    if percentage > 100:
        percentage = 100
    elif percentage < 0:
        percentage = 0
    return awc * percentage / 100
