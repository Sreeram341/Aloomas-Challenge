# Aloomas-Challenge

Extracting Data   Pull Data from Hubspot.  
Using their API and Python, build out logic to extract Engagement data from their endpoint.  

Organize this data and store it into a file structure that makes sense. 
Auth: https://developers.hubspot.com/docs/overview (see demo key)
Engagments API: https://developers.hubspot.com/docs/methods/engagements/engagements-overview   

Spin Up a relational db Instance, you can choose either: Postgres 9.4+ MySQL 5.6+ Oracle 11g+ SQL server(but please provide the docker image tag for it)   Create a table and Load the Data In (this can be done during reads as well)   

Reading Data Write a SQL Query that pulls the Engagements per Day broken down by type.  

You should expose both the counts per day and a rolling 2 week avg for each day.     

Bonus Points: present a rolling 2 week avg for each day.     

Present these results in a format that makes sense to view   
