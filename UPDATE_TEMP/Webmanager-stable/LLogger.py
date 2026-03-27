import time, os
import data_reader as dr
import datetime


def CreateLog(text="", severity=0, category="Uncategorised"):
    # Check if logging is allowed
    if str(dr.site_config_data["LoggingEnabled"]) != "1":
        return "Logging is disabled!"

    #Logging is turned on, do the actual logging
    #get date
    date = str(datetime.datetime.now())
    #separate time from date
    cur_time = date.split(" ")[1].split(".")[0]
    #reuse date, for storing only the date part
    #replace dashes with underscores, for consistency
    date = date.split(" ")[0].replace("-","_")
    #remove \ operators from text, so they wont break anything
    text = text.replace("\\", "")
    #category cant start with /
    if category[0] == "/" or category[0] == "\\":
        category = category[1:]
    #create the path, and also replace spaces with underscores
    LOGFOLDER = dr.site_config_data["LogFolder"]
    if not LOGFOLDER.endswith("/"):
        LOGFOLDER += "/"
    if category[-1] != "/":
        category += "/"
    path = f"{LOGFOLDER}{category}{date}.log".replace(" ", "_")


    #make sure there arent any file extensions
    if ".." in path:
        return "Path cant contain double dots"

    #make sure every folder and subfolder exists
    pathsplit = path.split("/")[:-1]
    current_check_path = ""
    for p in pathsplit:
        current_check_path += p + "/"
        if not os.path.exists(current_check_path):
            os.mkdir(current_check_path)

    if not os.path.exists(path):
        open(path, "x")
    f = open(path, "a")
    severitytxt = ""
    match str(severity):
        case "0":
            severitytxt = "MESSAGE"
        case "1":
            severitytxt = "WARNING"
        case "2":
            severitytxt = "ERROR"
    f.write(f"{cur_time} [{severitytxt}] {text}\n")
    
    if str(dr.site_config_data["LogPrint"]) == "1":
        print(f"{cur_time} [{severitytxt}] {text}")

    return f"{cur_time} [{severitytxt}] {text}"