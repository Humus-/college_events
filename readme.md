# Evento
### Installation
```sh
$ git clone https://github.com/dipkakwani/college_events.git
$ cd college_events
```
Create virtual environment and install the dependencies by:

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Last thing needed to run the application is [MySQL](https://dev.mysql.com/downloads/). 
Create a database named evento. And then run this command:

```sh
$ python run.py
```

### TODO
* Add front end templates.
* Add follow user feature.
* Add events model.
* Add event related views (host event, view event, join event, leave event etc).
* Enable social login.
* Send verification mail to complete registration.
* Add captcha to registration form.
* Consider the requirement of adding phone number to the users table from sqlalchemy_utils package
* Add the view lobby functionality and use appropriate algorithm to choose the lobbys to be displayed to different users
* Add the tags field to the lobby and event form
## License
----
GNU General Public License v3
