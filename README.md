# How to install and run the code

1. Have Python 3 installed
2. Create a virtual environment
3. Have MySQL installed, perferably v8 which what I used.
4. Create a `.env` file at the root directory. Copy contents from `.env.example` and modify any values for database user, password, host, name if needed
5. Have Postman installed in order test the API endpoints
6. On your root folder of this project enter this command: 

   `pip install -r requirements.txt`

   At this point, Flask along with other packages should be installed. 
7. To run the Flask application run the following command:

   `flask --app app.py run`

   This will also create the tables specfied at `models.py`
8. As a convenience, I've included `script.py`, which will prepopulate some sample data onto those tables. To run this, open a seperate terminal on the root location of this project and run `python3 script.py`
9. Have Postman installed to begin testing the API endpoints, if you hadn't done so already

# Authentication

You first need to be authenticated in order to test the other requests. Use one of the user credentials from `script.py` and include in the body at the `POST /v1/login` request, like below example
```
{
    "email": "user1@example.com",
    "password": "password1"
}
```

Once you successfully login, you will see an access token in the response. You will need this as the Bearer token for the other API requests

# Save User Subscription
Head to `POST /v1/user/subscription`, and make sure you include the bearer token from the login request for authorization.

On the body of the request, you need to include the `sector_id`, `source_id`, and `subcategory_id`, like in the below example
```
{
    "sector_id": 2,
    "source_id": 3,
    "subcategory_id": 1
}
```
If you include an ID that doesn't exist for any of those fields you will see an error.

Upon successfully saving the user subscription, it'll return the subscription information

# Get User Subscription
Head to `GET /v1/user/subscription` and make sure you include the bearer token from the login request for authorization.

Upon successfully request, it'll return the subscription information

# Unsubscribe
Head to `DELETE /v1/user/subscription` and make sure you include the bearer token from the login request for authorization.

Upon successfully request, it'll soft delete the record

# Design Decisions

For this task I have used Flask, along with MySQL for the backend. In terms of database schema, I have a few tables for the following components: `user`, `sector`, `source`, and `subcategory`. To manage the user subscription I've created a `user_subscription` table, which contains the `user_id`, `sector_id`, `source_id`, and `subcategory_id` to as foriegn keys to the aformentioned tables.

In terms of database schema, there were some considerations I made. First for `user_subscription`, I've made `user_id` a unique key as the requirement said that there will be one active subscription. The tradeoff here is that this will not account for if there is a request in the future to allow multiple subscriptions. This would make for a good arguement to not make the `user_id` as a unique key, to allow multiple records of a `user_id`. However I've decided to keep it simple and make `user_id` as unique, as I felt it would add some complexity on the API to mark other user subscriptions as inactive, and keeping only one that is created/updated as active. And if were a request in the future to allow multiple user subscriptions, then we can simply remove the unique key constraint on the `user_id`.

Another consideration that could have been made is what type of sector/subcategory combo (or something similar) would be considered valid. If there was such a case, this would needed by refined together with engineers and product managers to determine how and which fields and combos are valid. If that were the case, there could have another table to manage the valid combos, and validate by that table when a user creates/updates their subscription. I would also make the arguement that subcategory doesn't necessary have to be tied to a sector, it could apply for multiple sectors, so that was part of my thinking of not making an additonal table for managing those combos, and with my current database schema, it allows for such flexiblity

Another design pattern I used here was soft deletes, with all of the tables. The trade-off here is regarding extra database space used instead of actually deleting the record on the database. However, there is an arguement to keeping the data for historical data, for example when a user unsubscribed, or when a user, sector, source or subcategory was made inactive. Another arguement is creating a logging table for some or all of the tables where we wanted historical data. For example, `user_subscription_history` could have been created to keep track whenever a user saved/unsubscribed. This would give a whole bunch of information, but would require much more space on the database to be stored.

A final consideration was regarding whether to create seperate POST and PUT endpoints for when a user created new subscription or updated a subscription respectively. However, I've used one endpoint for POST to handle all saving (inserts and updates) becuase a lot of the validation is similar and with the inclusion of soft deletes which meant that a user re-subscription would require an update and not insert query.