Part 2
==

Let's change the fts/tests.py like:

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from datetime import datetime as dt

    class PollsTest(LiveServerTestCase):
        fixtures = ['admin_user.json']

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
            username_field.send_keys('ryan')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('123qwe')
            password_field.send_keys(Keys.RETURN)

            # her username and password are accepted, and she is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Site administration', body.text)

            # She now sees a couple of hyperlink that says "Polls"
            polls_links = self.browser.find_elements_by_link_text('Polls')
            self.assertEquals(len(polls_links), 2)

            # The second one looks more exciting, so she clicks it
            polls_links[1].click()

            # She is taken to the polls listing page, which shows she has
            # no polls yet
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('0 polls', body.text)

            # She sees a link to 'add' a new poll, so she clicks it
            new_poll_link = self.browser.find_element_by_link_text('Add poll')
            new_poll_link.click()

            # She sees some input fields for "Question" and "Date published"
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Question:', body.text)
            self.assertIn('Pub date:', body.text)  # This need change

            # She types in an interesting question for the Poll
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys("How awesome is Test-Driven Development?")

            # She sets the date and time of publication - it'll be a new year's
            # poll!
            dtn = dt.now()
            pub_date = '%s-%s-%s' % (dtn.date().year, dtn.date().month, dtn.date().day)
            pub_time = '%s:%s:%s' % (dtn.time().hour, dtn.time().minute, dtn.time().second)
            date_field = self.browser.find_element_by_name('pub_date_0')
            date_field.send_keys(pub_date)
            time_field = self.browser.find_element_by_name('pub_date_1')
            time_field.send_keys(pub_time)

And then, let's run it.

    $ python manage.py test fts
    Creating test database for alias 'default'...
    .
    ----------------------------------------------------------------------
    Ran 1 test in 15.729s

    OK
    Destroying test database for alias 'default'...

And you can see it open firefox and create a new poll.

Attention
==
fts/tests.py:56 needs change. If you run it like tdd-django-tutorial.com/tutorial/2/
you can get an error.
