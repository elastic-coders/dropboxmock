# Dropboxmock: how to mock dropbox

Dropboxmock is a simple library that allow you to mock dropbox library 
in your test.

## Usage

1) pip install https://github.com/elastic-coders/dropboxmock/archive/0.0.2.zip
or add https://github.com/elastic-coders/dropboxmock/archive/0.0.2.zip to your project requirements

2) decorate your test wiht @mock_dbx_session and/or mock_dbx_client (or the other depending on what you need to mock)

3) run your test!

If you can't drop something in dropbox tell me what, so I can solve it!

## Clone the repo
If you want to clone the repo and test it:
1) git clone https://github.com/elastic-coders/dropboxmock.git
2) pip install -r requirements
3) test with python manage.py test

