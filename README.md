# KayKam
#### Video Demo: <https://youtu.be/irIfgsYGfj4>
#### DESCRIPTION:
***CONTENT***:

Hello World! I'm Kian Fotovat and my brother (Kamran Fotovat)
and I are the developers of this project. I'm writing it from Shiraz a city in Iran.

Our project is a web application about Barcelona
Football club and provides some intersting facilities for users.

It includes a home page, a quize page, a news page
a shop page and profile management and .... .

You can open and read our daily news about Barcelona and
Also in the profile tab, you can open a virtual bank
Account and manage it, for example charge it virtually and change
the card number or password.

After that you can use your virtual credit card and 
go to shop page and add anything you want to your cart.
(Our shop contains several sport items only related to barca)
Also in profile tap, you can change your user's information
Such as first/last name and .... .

Now let's talk about our advanced login/register and logout 
system. We tried to handle all kind of errors on it so with each
Wrong input value you will encounter an error. In register page
we ask you to enter your first/last name and username and a password
so you can relogin whenever you want!

In login page you have to enter your username and password so we can 
Confirm it's you!

Also we have provided a logout button in profile so you can switch between your accounts!

There is also a simple quize, which includes 5 questions and when you answered them it returns you a rating out of 5.
Of course It's content is about barca informations and history.

***CODE***:

Let's talk about coding of our project!

The framework of our project is set with flask.
We also used these programming languages ( html, css, python, JavaScript)
in our code. 

In our flask app, you can see templates file which includes 
about 40 html files. Also there is static file which includes
Css files and JavaScript files of our flask app.

We used JS files for our advanced quize and also css files all over the code!

There is two applications there that one of them is our main application.py and the 
next is a tool.py that returns a function which forces users
to login to their account before anything else!

in application.py we placed all routes and functions to control our html pages.

We took care of our database need with SQLite. 
We used it several times in register/login/logout, 
 Shop and user's cart and even user's personal information.
We record them all with SQLite in our barca.db file.

In our barca.db, we have users, credit, products, and cart tables that each of them keep diffrent datas for our web app.
for example, in users we store the first/last name, username, and password. in credit, we store the card number and password for related to each credit card that the user creates! in products we store the information for each product such as price, name and its id. and then finally in cart we keep the information for each product that the user adds to his/her cart, such as number, total price, their titles and ... .

In our application we used several libraries such as 

- Flask

- flask_session

- cs50

In the project file(KayKam) I added a requirements.txt so you can add the libraries needed for the web app.

That was our project! 

I hope you try it and enjoy it!
