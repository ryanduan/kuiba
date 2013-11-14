
Download and install Python-3.3.2

    wget http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz
    tar zxvf Python-3.3.2.tgz
    cd Python-3.3.2
    ./configure
    make
    make install

Install git & git-flow

    sudo apt-get install git
    sudo apt-get install git-flow

Install pip

    sudo apt-get install python-pip

Install virtualenv

        sudo apt-get install virtualenv (or pip install virtualenv)

Make virtualenv for TDD

    virtualenv --no-site-packages tddenv
    source tddenv/bin/activate
    pip install django==1.5.2
    pip install selenium
    pip install mock

Use git-flow

    mkdir kuiba
    git flow init

You can create a new repo on you github name kuiba, then add remote to you local

    git remote add origin git@github.com:ryanduan/kuiba.git

I use ssh.

You can visit [gitflow](https://github.com/nvie/gitflow) to know git-flow

And then, use travis-ci

    vim .travis.yml

Input:

    language: python
    python:
      - "2.7"
      - "3.3"
    env:
      - DJANGO_VERSION=1.5.2
    # command to install dependencies
    install:
      - "pip install ."
      - pip install -q Django==$DJANGO_VERSION
      - python setup.py -q install
    # command to run tests
    script: nosetests

OK, let's creating a django project named "mysite"

    django-admin.py startproject mysite

Fine, let's create an app

    cd mysite
    python manage.py startapp fts

Edit mysite/settings.py add the app and datebase, and open the admin

Edit mysite/urls.py like mime

Now, edit the fts/tests.py, delete the example test case and replace it with mime

    from django.test import LiveServerTestCase
    from selenium import webdriver

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # She sees the familiar 'Django administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # TODO: use the admin site to create a Poll
            self.fail('finish this test')

OK, lets run the test

    (tddenv)ryan@Ryan:~/tdd/kuiba/mysite$ python manage.py test fts
    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/ryan/tdd/kuiba/mysite/fts/tests.py", line 22, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test')
    AssertionError: finish this test

    ----------------------------------------------------------------------
    Ran 1 test in 13.181s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

OK, let's sync db and create superuser

    $ python manage.py syncdb
    Creating tables ...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_groups
    Creating table auth_user_user_permissions
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (leave blank to use 'ryan'):(default: ryan)
    Email address: a@b.com
    Password:(your password)
    Password (again):
    Superuser created successfully.
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)

And then, if you run the django server you can login the admin, then let's test it.

You need change the fts/tests.py like mime.

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # She sees the familiar 'Django administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # She types in her username and passwords and hits return
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('admin')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('adm1n')
            password_field.send_keys(Keys.RETURN)

            # her username and password are accepted, and she is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Site administration', body.text)

            # She now sees a couple of hyperlink that says "Polls"
            polls_links = self.browser.find_elements_by_link_text('Polls')
            self.assertEquals(len(polls_links), 2)

            # TODO: Gertrude uses the admin site to create a new Poll
            self.fail('todo: finish tests')

Then, let's run it:

    $ python manage.py test fts
    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/ryan/tdd/kuiba/mysite/fts/tests.py", line 33, in test_can_create_new_poll_via_admin_site
        self.assertIn('Site administration', body.text)
    AssertionError: 'Site administration' not found in u'Django administration\nPlease enter the correct username and password for a staff account. Note that both fields may be case-sensitive.\nUsername:\nPassword:\n '

    ----------------------------------------------------------------------
    Ran 1 test in 10.901s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Oh, failed, the username and password wrong. Why? Because it's test db, no username
and password like the production db.

OK, no problem, let's create a test fixture

    mkdir fts/fixtures
    python manage.py dumpdata auth.User --indent=2 > fts/fixtures/admin_user.json

And add the codes in you fts/tests.py after the class PollsTest(...) before the def setUp(...)

    fixtures = ['admin_user.json']

Then, let's run it again and again

    $ python manage.py test fts
    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/ryan/tdd/kuiba/mysite/fts/tests.py", line 38, in test_can_create_new_poll_via_admin_site
        self.assertEquals(len(polls_links), 2)
    AssertionError: 0 != 2

    ----------------------------------------------------------------------
    Ran 1 test in 15.711s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

I think you can login. OK, let's commit our code now.

    git status (to see which files have changed)
    git diff (review the detail)
    git add -A (add all of the files)
    git commit -m 'Part 1 running test can login'
    git checkout master
    git merge develop
    git push (default push origin branch to github)