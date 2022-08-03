Hashtag-Search 
==============
This project is a Flask Web Application that supports login and register validation with a sql alchemy database. Then, with Selenium is going to search a hashtag that the user wants, and it is going to show the hashtags that are recommended for the user's use.

For the use of this application the next modules should be installed: 
- Flask 
- flask_sqlalchemy 
- flask_WTForms 
- SQLalchemy 
- flask_login 
- flask_session 
- selenium 

For the database use, there are several characteristics that need to be known, therefore, if anyone wants to use this project, has to request the database information in order to use it. The main idea behind this project was to use Web Scrapping with Selenium in order to access instagram's individual hashtag pages and scrape the hashtags that are most used to ones that the user searches.

In order for Selenium to work, the latest Chrome WebDriver must be download and installed in your PC. Inside the recommendedBot.py file, the chrome driver path should me updated for the path inside the user's computer.
