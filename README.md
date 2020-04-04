[![Build Status](https://travis-ci.com/div0ky/firestone_api.svg?branch=stable)](https://travis-ci.com/div0ky/firestone_api)

# Firestone Idle Bot - Website

This project started off as simply an API to interface with a bot I created... but has evolved into a full-fledged web app regarding the same.

## Installation



### Prerequisites

```
Werkzeug==1.0.0
SQLAlchemy==1.3.15
Markdown==3.2.1
Bootstrap_Flask==1.2.0
WTForms==2.2.1
requests==2.23.0
Flask_Login==0.5.0
Flask_Migrate==2.5.3
Flask==1.1.1
pytest==5.4.1
Flask_Moment==0.9.0
Flask_SQLAlchemy==2.4.1
alembic==1.4.2
Flask_WTF==0.14.3
```
These can be installed by running `pip install -r requirements.txt` with the project folder as your current working directory.

### Installing

Clone the repository:

`git clone https://github.com/div0ky/firestone_api.git`

Install the requirements:

`pip install -r requirements.txt`

Launch the Flask server:

`flask run`

## Running the tests

I need to build out more tests as there are newer functions I haven't written testing for. To run the tests that exist us **PyTesT** by simply running `py.test` and it'll grab the `test_things.py` and run the tests.


## Deployment

I don't personally use Docker (thought I'm considering it) so you'll need to setup a Python app on your web-server of choice. If you don't know how to setup a Flask app on a web server that's beyond the scope of this README.

## Built With

* Flask
* Bootstrap
* SASS


## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/div0ky/firestone_api/tags). 

## Authors

* **Aaron J. Spurlock** - *Initial work* - [div0ky](https://github.com/div0ky)

## License

This project is licensed under the GNUv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
@miguelgrinberg for helping me get started with Flask
