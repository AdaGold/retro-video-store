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
# form_data = {"name":  "nombre"}
# if not "name" and "postal_code" and "phone" in form_data:
#     print("booo")
'''
"Wed, 01 Jan 1958 00:00:00 GMT",
"Thu, 13 May 2021 19:27:47 GMT",
'''

# HoW do I  join it  with its
# instance of all the videos for that customer including (id, title, 
# release date, total inventory,available inventory)

#rentals = Rental.query.filter(Rental.customer_id==customer_id).all()

# what is the difference btw the lines below and line 11 on customer model?
# register_at = db.Column(db.DateTime, server_default=db.func.current_timestamp()) 
