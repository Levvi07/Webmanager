import time, os
import data_reader as dr


def CreateLog(category="Uncategorised", severity=0, text=""):
    # Check if logging is allowed
    if str(dr.config_data["LoggingEnabled"]) != "1":
        return "Logging is disabled!"

    #Logging is turned on, do the actual logging
    