### Backgroud:
* You are a professional and you use a notion database to manage your netwok contacts. This database contains  name, email, skills, 
current location, current company and the last day you contacted you talked to this person.

As any CMR teaches us, is not important to have a huge list of contact, but have personal relationship with them, and the hardest part
is not to build this list, but maintain the relationship active over the time.

Sometimes, I lack in maintaing the relationship active, so, I created a script that automatically contact people and invite them over for a coffee.


### Network Notion Manager
Fetch the data from a notion database used to store contacts and/or progressional network details, and 
runs daily jobs to send an automatic email with people where last iteration was more than 40 days ago. 

### Notion Database structure



### System Requirements
* Sendiblue.com account and SMTP configuration (you are able to send up to 100 daily emails for free)
* Dotenv ```pip3 install python-dotenv```
* Pytz ```pip3 install pytz```
* Notion client ```pip3 install notion-client```
* SSL (version >=1.0.1)

### Notion backgroun 

Database ID: You'll find the Database ID in the url. Suppose this is the example url: https://www.notion.so/workspace/XXX?v=YYY&p=ZZZ then XXX is the database ID, YYY is the view ID and ZZZ is the page ID.

### TODO:
* Add in notion main tag about the automation language (italian/english), and upon that value, 
send the email in italian, or, english. 
* Automaticamente fetchare SOLO (dalla response, dal filtro, quelli che hanno contact date > 40 giorni)
* Diminuire disponibilita' nel calendario networking (fare un giorno a settimana, basta) => NON Il weekend; Un friday, fare un bel friday.