# Examples
from datetime import datetime
# now = datetime.now()
# print(now.strftime("%A"), now) 

# print(now.strftime("%A"), now) 

# print(now.strftime("%a, %d %b %Y %X %z"))

# # print(datetime.now()).strftime("%c") 
# time_day = (datetime.now()).strftime("%a, %d %b %Y %X %z")
# print(time_day)
time_day = (datetime.now()).strftime("%Y-%m-%d")
print(time_day) 
time_day = (datetime.now()).strftime("%a, %d %b %Y %X %z %Z")
print(time_day)
# form_data = {"name":  "Ari"}
# if not "name" and "postal_code" and "phone" in form_data:
#     print("nya")
'''
"Wed, 01 Jan 1958 00:00:00 GMT",
"Thu, 13 May 2021 19:27:47 GMT",
'''