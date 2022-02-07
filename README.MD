# VOLTANS ASSEMBLE! (Market Dispatch System)

Here to handle your EnergyMarket Dispatch needs!
# Running the Application
## Start App
Make sure Python3 is installed
`python3 -V`

Install requirements via pip
`pip3 install -r requirements.txt`

In the real world, we would need an email server set up, too. This implementation leverages G-Mail's API, but `python3 run_email_server()` would set up an endpoint to hit. (using `#send_email()` instead of `#send_gmail()` in the email dispatch). This would run in its own terminal.

Start Dispatch Server in another terminal.
`python3 run_servers.py`

In another terminal, you can now send `curl` commands to the Dispatch Server (connect via port `DISPATCH_PORT`). Here's 2 example commands you can modify for your own implementation; first command is a closed-ended Dispatch (has an `end_time`), and second command has an open-ended Dispatch (no `end_time`).
**1.**
`curl --http0.9 -H 'Content-type: application/json' --data '{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04", "program_id":1, "event_type_id":"1"}' http://localhost:8080/ -v`
**2.**
`curl --http0.9 -H 'Content-type: application/json' --data '{"start_time":"08/27/2019 21:04", "program_id":1, "event_type_id":"1"}' http://localhost:8080/ -v` 

## Additional Notes
Some command-line operations in the program will only work on a Mac or Linux OS (I got it working on Windows using Git Bash). These won't break the program, but you may see some odd output in the console.
For the sake of streamlining a simple flow, I used pseudo-implementations of a full-fledged SMS and Email system. They both will send one notification to a test user for each Dispatch. (if you'd like your phone to be part of the tests, change value of `TWILIO_RECIPIENT_DEFAULT` to your own number). To view e-mails, sign onto G-mail using the values for these fields:

 - `USAIN_EMAIL`
 - `USAIN_PWD` <-- Check e-mail for the password. It's stored in what would be some 3rd party secret store in the real world.

# System Design

**View `doc/system_design.pdf` for visual reference**

## Isolated Responsibilities
For resilience, and extensibility, keeping responsibilities focused and delineated between components is important. The most _fragile_ component in this project is Dispatch Server, since it communicates with all of the other components in the system. However, in this system, failure of the Dispatch Server would not disrupt data (stored in mongo) or break dispatch endpoints (e.g. our email server). Horizontal scaling to add more instances per-project-component would help scale with performance.

## Loggers
In this implementation, one `Logger` instance records behavior across all system components as `SERVER_LOGGER`. However, we instantiate a new `Logger` instance for each Dispatch, and its transaction log, that comes through the system. In the real world, this may be an internal Message Queue (e.g. RabbitMQ) or some cloud log-hosting service (e.g. Amazon CloudWatch)

## MongoDB Backend
### Extensibility and No-SQL
One nice perk of using a No-SQL database is that we can extend the Dispatch data type to increasingly unique or complex structures without having to do considerable database maintenance or migrations. 

### Manual Reference (ID's)
One downside of using a No-SQL database is that we are responsible for keeping track of relationships between Collections in the DB. There do exist metadata tools to establish relationships between data (see Manual DB-Refs in Mongo). Given the data model in `doc/data_model.pdf`  I think this is okay, because we link a lot of Collections under one field: `dispatch_id`. Though additional configuration would be required, the data can be structured smartly to reduce the needs for that manual joining.
### Statement Sanitization
Real world, we should be handling problematic queries and sanitizing all db statements for any malicious scripts. However, this was skipped over for this project for timeliness.

## Code --> System Component

| Component | Code |
|-----------|------|
| Dispatch Server | `/server/dispatch_handler.py`|
| Mongo_DB Client | `/db/*`|
| SMS Server |`/server/text/*` |
| Email Server |`/server/e_mail/*` |
| Logger/Internal Message Queue | `/logger/*` |
| Runtime | `/run_servers.py` |

# Data Design
View **`doc/data_model.pdf`** for visual reference...

A dispatch behaves much like a notification, which informed the class structure, as well as potential extensions to functionality.

## Transaction Log
In a more established system, `logs/txn` could be likened to some cloud storage service (e.g. *AWS S3*). Dispatch data could become more complex than this, but given the current state of Transaction Logs (`~20 lines a log)`, the logic in `transaction_log#write_transaction_log()` could be placed in a Lambda Function. Especially with python, it can be difficult to handle multiple loggers at once.

##  User Group referenced only One-way
User Group was the only Collection where I decided to not have it refer to Documents from other Collections by their ID. This is under an assumption that indexing the User Collection by `group_id` would make performance similar to directly hopping from `User Group` -> `User` (this is all a hunch, so feel free to shoot this one down)

## Extensibility Considerations
In `doc/data_model.pdf`, there are 3 _abstract classes_ highlighted in pink to discuss functional extensibility.

 - **Transaction:** Future auditing should fall along some consistent data schema, such that we can expect consistency for this lower-level data concept. I am sure there are many other aspects of energy markets which place a high value on structured auditing.
 - **Event Rules:** As of now, we send dispatch notifications to users based on a set comparison of a User and Event Types' `user_group_id's`. These occur instantaneously upon receiving the Dispatch request. Adding predicates for a Dispatch Event to actually execute enables for scheduling dispatches, or even _Dispatch Rules_ which only trigger under certain conditions in the market. There exists SMS/E-mail services which support scheduled events, such as Twilio and G-Suite.
	 - e.g. `On June 12th, 2022, Execute Dispatch with dispatch_id= x`
	 - e.g. `Execute Dispatch with dispatch_id=x if solar_market <= x`


- **Dispatch Template:** With how I structure Dispatch Program, I wanted to allow for more customizable messaging (e.g. formatted message templates for a program)
 
# System Flow

View **`doc/system_flow.pdf`** for visual reference...

 - External-Facing Messaging Queue receives a dispatch request from an
   end user
   - The Dispatch Server receives the dispatch request:
	   - It processes a unique ID and transaction Timestamp for the Dispatch
	   - It sends the appropriate query requests to MongoDB
- MongoDB Performs the appropriate operations and returns results to the Dispatch Server
- The Dispatch Server then processes the Dispatch data to identify the Program, Event Type, and Users relevant to said dispatch
- Based on the Communication Codes queried from the Dispatch, the Dispatch Server starts requesting the appropriate endpoints to send notifications to the given user. In this implementation, those endpoints are the SMS and E-mail Servers (if you consider the Command Line as an end user, that makes a third).
	- You could imagine an internal Messaging Queue handling the communication between the various internal endpoints
	- This should then be extensible to any REST-digesting service or endpoint 






