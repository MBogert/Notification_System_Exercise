# Notification System Exercise
A casual proof of concept exploring a handful of small technical components in a faux system.
 - NoSQL data-storage with MongoDB
 - SMS 3rd-party services (via Twilio)
 - SMTP E-mail Server (or Gmail API)
 - Consolidated logger system

Additionally below are an assortment of documents and discussion about system design. All statements made herein are from unlicensed professionals in computing :)

# Running the Application
Make sure Python3 is installed:
`python3 -V`

Install requirements via pip:
`pip3 install -r requirements.txt`

_In the real world, we would need an email server set up. This implementation leverages G-Mail's API, but `python3 run_email_server()` would set up an endpoint. (we'd use `#send_email()`, instead of `#send_gmail()`). This would have to run in its own terminal._

In a separate terminal window, start the program:
`python3 run_servers.py`

In another terminal, you can now send `curl` commands to the server (connect via port `DISPATCH_PORT`). Here's 2 example commands you can modify for your own implementation; first command is a closed-ended notification (has an `end_time`), and second command has an open-ended notification (no `end_time`).

**1.**
`curl --http0.9 -H 'Content-type: application/json' --data '{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04", "program_id":1, "event_type_id":"1"}' http://localhost:8080/ -v`

**2.**
`curl --http0.9 -H 'Content-type: application/json' --data '{"start_time":"08/27/2019 21:04", "program_id":1, "event_type_id":"1"}' http://localhost:8080/ -v` 

# System Design
**View `doc/system_design.pdf` for visual reference**

## Code --> System Component

| Component                     | Code |
|-------------------------------|------|
| Notification Server           | `/server/dispatch_handler.py`|
| Mongo_DB Client               | `/db/*`|
| SMS Server                    |`/server/text/*` |
| Email Server                  |`/server/e_mail/*` |
| Logger/Internal Message Queue | `/logger/*` |
| Runtime                       | `/run_servers.py` |

# Data Design
View **`doc/data_model.pdf`** for visual reference...

## Extensibility Considerations
In `doc/data_model.pdf`, there are 3 _abstract classes_ highlighted in pink to discuss functional extensibility.
 
# System Flow
View **`doc/system_flow.pdf`** for visual reference...

 - External-Facing Messaging Queue receives a notification request from an
   end user
   - The server receives the notification request:
	   - It processes a unique ID and transaction Timestamp for the notification
	   - It sends the appropriate query requests to MongoDB
- MongoDB Performs the appropriate operations and returns results to the server
- The server then processes the notification data to identify the Program, Event Type, and Users relevant to said dispatch
- Based on the Communication Codes queried from the notification, the server starts requesting the appropriate endpoints to send notifications to the given user. In this implementation, those endpoints are the SMS and E-mail Servers (if you consider the Command Line as an end user, that makes a third).
	- You could imagine an internal Messaging Queue handling the communication between the various internal endpoints
