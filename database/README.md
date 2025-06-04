# /database

This directory contains the files for creating and managing the database.

### Helpful Tips

*[Thank you Ahmet for the notes!](https://plain-stick-ac9.notion.site/SQL-Server-Basics-43ebfae960de4f89a1aa244dcecb0702)*  

You can use `sqlcmd` to connect to the database.  
This can be installed using `brew install sqlcmd`.  

To connect to the database use:  
`sqlcmd -S [host],[port] -U [user] -P [password] -d [dbname]`

To run a script add the `-i [filename.sql]` argument.

To execute a command once connected, end it with `GO`, as you would with a `;` normally.

It was difficult to understand where tables where being created, this is easier in a tool such as DBeaver.
