⭐️ = Refactoring ideas, if there is time

# **Wave 1**

## Create Customer model with attributes

- [X] cust_id primary key
- [X] name of the customer
- [X] postal code of the customer (STRING)
- [X] phone number of the customer (STRING)
- [X] registered_at datetime of when the customer was added to the system (DATETIME)
- [X] videos_checked_out_count

## Create Video model with attributes

- [X] video_id primary key
- [X] title of the video (STRING)
- [X] release date datetime of when the video was released (DATETIME)
- [X] total inventory of how many copies are owned by the video store
- [X] available_inventory




## GET /customers

- [X] successful response has status 200  
- [X] successful response has this body: 

            [
        {
            "id": 1,
            "name": "Shelley Rocha",
            "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
            "postal_code": "24309",
            "phone": "(322) 510-8695",
            "videos_checked_out_count": 0
        },
        {
            "id": 2,
            "name": "Curran Stout",
            "registered_at": "Wed, 16 Apr 2014 21:40:20 -0700",
            "postal_code": "94267",
            "phone": "(908) 949-6758",
            "videos_checked_out_count": 0
        }
        ]

- [X] should return an empty array and a status 200 if there are no customers




## GET /customers/<id>

- [X] route has 1 required argument: id 
- [X] successful response has status 200  
- [X] successful response has this body: 

        {
            "id": 2,
            "name": "Curran Stout",
            "registered_at": "Wed, 16 Apr 2014 21:40:20 -0700",
            "postal_code": "94267",
            "phone": "(908) 949-6758",
            "videos_checked_out_count": 0
        }

- [X] returns detailed errors and a status 404: Not Found if this customer does not exist.



## POST /customers

- [X] required request body parameters are:

        {
            "name": "Curran Stout",
            "postal_code": "94267",
            "phone": "(908) 949-6758"
        }

- [ ] deal with registered_at datetime thing here. must have this format, meaning you're gonna have to figure out what to do with tz:

        "Wed, 16 Apr 2014 21:40:20 -0700"

- [X] successful response has status 201  
- [X] successful response has this body: 

        {
        "id": 10034
        }

- [X] if any of the required fields are missing from request, should get response with 400 and response body with some indication of what went wrong, such as { "details": "Invalid data"}
- [ ] ⭐️ provide a more detailed response body for error handling, such as {"title must be provided and it must be a string","total_inventory must be provided and it must be a number"}



## PUT /videos/<id>

- [X] route has 1 required argument: id 
- [X] required request body parameters are:

        {
            "name": "Curran Stout",
            "postal_code": "94267",
            "phone": "(908) 949-6758"
        }

- [X] successful response has status 200  
- [X] successful response has this body: 

        {
            "id": 2,
            "name": "Curran Stout",
            "registered_at": "Wed, 16 Apr 2014 21:40:20 -0700",
            "postal_code": "94267",
            "phone": "(908) 949-6758",
            "videos_checked_out_count": 0
        }

- [X] returns detailed errors and a status 404: Not Found if this customer does not exist.
- [X] if any of the required fields are missing from request, should get response with 400 and response body with some indication of what went wrong, such as { "details": "Invalid data"}
- [ ] ⭐️ provide a more detailed response body for error handling, such as {"title must be provided and it must be a string","total_inventory must be provided and it must be a number"}




## DELETE /customers/<id>

- [X] route has 1 required argument: id 
- [X] successful response has status 200  
- [X] successful response has this body: 

        {
        "id": 2
        }

- [X] returns detailed errors and a status 404: Not Found if this customer does not exist.

---

## GET /videos

- [X] successful response has status 200  
- [X] successful response has this body: 

        [
        {
            "id": 1,
            "title": "Blacksmith Of The Banished",
            "release_date": "1979-01-18",
            "total_inventory": 10,
            "available_inventory": 9
        },
        {
            "id": 2,
            "title": "Savior Of The Curse",
            "release_date": "2010-11-05",
            "total_inventory": 11,
            "available_inventory": 1
        }
        ]

- [X] should return an empty array and a status 200 if there are no videos



## GET /videos/<id>

- [X] route has 1 required argument: id 
- [X] successful response has status 200  
- [X] successful response has this body: 

        {
        "id": 1,
        "title": "Blacksmith Of The Banished",
        "release_date": "1979-01-18",
        "total_inventory": 10,
**❗️ The README says to include this key-value pair, but doing so will cause the Postman Tests to fail**
        "available_inventory": 9
        }

- [X] returns detailed errors and a status 404: Not Found if this video does not exist.




## POST /videos

- [X] required request body parameters are:

        {
        "title": "Blacksmith Of The Banished",
        "release_date": "1979-01-18",
        "total_inventory": 10
        }

- [X] successful response has status 201  
- [X] successful response has this body: 

        {
        "id": 10034
        }

- [X] if any of the required fields are missing from request, should get response with 400 and response body with some indication of what went wrong, such as { "details": "Invalid data"}
- [ ] ⭐️ provide a more detailed response body for error handling, such as {"title must be provided and it must be a string","total_inventory must be provided and it must be a number"}



## PUT /videos/<id>

- [X] route has 1 required argument: id 
- [X] required request body parameters are:

        {
        "title": "Blacksmith Of The Banished",
        "release_date": "1979-01-18",
        "total_inventory": 10
        }

- [X] successful response has status 200  
- [X] successful response has this body: 

        {
        "id": 1,
        "title": "Blacksmith Of The Banished",
        "release_date": "1979-01-18",
        "total_inventory": 10,
**❗️ The README says to include this key-value pair, but doing so will cause the Postman Tests to fail**
        "available_inventory": 9
        }

- [X] returns detailed errors and a status 404: Not Found if this video does not exist.
- [X] if any of the required fields are missing from request, should get response with 400 and response body with some indication of what went wrong, such as { "details": "Invalid data"}
- [ ] ⭐️ provide a more detailed response body for error handling, such as {"title must be provided and it must be a string","total_inventory must be provided and it must be a number"}




## DELETE /videos/<id>

- [X] route has 1 required argument: id 
- [X] successful response has status 200  
- [X] successful response has this body: 

        {
        "id": 2
        }

- [X] returns detailed errors and a status 404: Not Found if this video does not exist.