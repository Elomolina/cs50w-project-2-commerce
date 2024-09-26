# Second project for CS50's web programming with python and javascript course 👻
## Description
In this project the task is to design an eBay-like e-commerce auction site. 
..* The user is able to upload a listing .and put a starting price to it. 
..* Users that made the listings are able to close the bid.
..* Other users are able to bid on the listing only if the biding price is higher than the starting price.
..* Users can add listings to their watchlist, add comments in a listing, see listings per categories, and see their own listings.
## How to use it
Download the code and install the requierements
```
pip install -r requierements.txt
```
Apply migrations 
```
python manage.py migrate
```
Run app 
```
python manage.py runserver 
```