#!/usr/bin/env python3

#!/usr/bin/env python3

import re
import sys
import csv 
import operator

# syslog.log as input 
logfile = sys.argv[1]

error = {}
per_user = {}

try:
  with open(logfile, "r") as f:
    for line in f:
      # set error messages to be the keys of error{}, which values are their frequence in this file, respectively
      error_message = re.search(r"ERROR ([\w ']*) \(", line)
      if error_message:
        key = error_message.group(1)
        if key not in error.keys():
            error[key] =1
        else:
          error[key] +=1
        
      # set username to be the keys of the per_user{},        
      # which values are a dict having "INFO" and "ERROR" as keys and their frequence as values, respectively
      user_message = re.search(r"ticky: ([\w]*) [\w '\[\]#]* \(([\w.]+)\)", line)
      if user_message:
        entry = user_message.group(1)
        username = user_message.group(2)
        if username not in per_user.keys():
          per_user[username]=[0,0]
          if entry == "INFO":                    
            per_user[username][0]=1
          elif entry == "ERROR":
            per_user[username][1]=1
        elif entry == "INFO":
          per_user[username][0] +=1
        elif entry == "ERROR":
          per_user[username][1] +=1                            
    f.close()
except:
    print("Please check your inputfile.")
    
# sort the error{} according to the values
sorted_error= sorted(error.items(), key=operator.itemgetter(1), reverse=True)             
sorted_error[0] =("Error", "Count")  
# write the sorted_error to a csv file
with open("error_message.csv", "w") as f:
  writer =csv.writer(f)
  writer.writerows(sorted_error)

# sort the per_user{}, turn the list to a dict and extract the keys and values of this dict to three string lists.      
Username=["Username"]
INFO =["INFO"]
ERROR =["ERROR"]    
sorted_user= dict(sorted(per_user.items(), key=operator.itemgetter(0)))  
for key in sorted_user.keys():
  Username.append(key)
  INFO.append(sorted_user[key][0])
  ERROR.append(sorted_user[key][1])
user_rows=zip(Username, INFO, ERROR)
# write the string lists to a csv file
with open("user_statistics.csv", "w") as f:
  writer =csv.writer(f)
  writer.writerows(user_rows)

