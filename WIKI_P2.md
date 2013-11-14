Part 2
==

Let's change the fts/tests.py like:

    from django.test import LiveServerTestCase, TestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from datetime import datetime as dt
    from polls.models import Poll, Choice
    from django.utils import timezone

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
            self.assertIn('Date published:', body.text)  # This need change

            # She types in an interesting question for the Poll
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys("What wrong with you?")

            # She sets the date and time of publication - it'll be a new year's
            # poll!
            dtn = dt.now()
            pub_date = '%s-%s-%s' % (dtn.date().year, dtn.date().month, dtn.date().day)
            pub_time = '%s:%s:%s' % (dtn.time().hour, dtn.time().minute, dtn.time().second)
            date_field = self.browser.find_element_by_name('pub_date_0')
            date_field.send_keys(pub_date)
            time_field = self.browser.find_element_by_name('pub_date_1')
            time_field.send_keys(pub_time)

            # She sees she can enter choices for the Poll.  She adds three
            choice_1 = self.browser.find_element_by_name('choice_set-0-choice_text')  # Need change
            choice_1.send_keys('Very awesome')
            choice_2 = self.browser.find_element_by_name('choice_set-1-choice_text')  # Need change
            choice_2.send_keys('Quite awesome')
            choice_3 = self.browser.find_element_by_name('choice_set-2-choice_text')  # Need change
            choice_3.send_keys('Moderately awesome')

            # Gertrude clicks the save button
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()
            # She is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link
            new_poll_links = self.browser.find_elements_by_link_text(
                    "What wrong with you?"
            )
            self.assertEquals(len(new_poll_links), 1)

            # Satisfied, she goes back to sleep
        def test_verbose_name_for_pub_date(self):
            for field in Poll._meta.fields:
                if field.name == 'pub_date':
                    self.assertEquals(field.verbose_name, 'Date published')

        def test_poll_objects_are_named_after_their_question(self):
            p = Poll()
            p.question = 'How is babby formed?'
            self.assertEquals(str(p), 'How is babby formed?')

    class ChoiceModelTest(TestCase):

        def test_creating_some_choices_for_a_poll(self):
            # start by creating a new Poll object
            poll = Poll()
            poll.question="What's up?"
            poll.pub_date = timezone.now()
            poll.save()

            # now create a Choice object
            choice = Choice()

            # link it with our Poll
            choice.poll = poll

            # give it some text
            choice.choice_text = "doin' fine..."  # Need change

            # and let's say it's had some votes
            choice.votes = 3

            # save it
            choice.save()

            # try retrieving it from the database, using the poll object's reverse
            # lookup
            poll_choices = poll.choice_set.all()
            self.assertEquals(poll_choices.count(), 1)

            # finally, check its attributes have been saved
            choice_from_db = poll_choices[0]
            self.assertEquals(choice_from_db, choice)
            self.assertEquals(choice_from_db.choice_text, "doin' fine...")  # Need change
            self.assertEquals(choice_from_db.votes, 3)


And then, let's run it.

     python manage.py test fts
    Creating test database for alias 'default'...
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 41.155s

    OK
    Destroying test database for alias 'default'...

Attention
==
Somewhere need change.

OK, Edit polls/models.py like:

    from django.db import models
    from django.utils import timezone
    import datetime

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

        def __str__(self):
            return self.question
    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):
            return self.choice_text

And edit polls/tests.py

    from django.test import TestCase
    from django.utils import timezone
    from polls.models import Poll, Choice

    class PollModelTest(TestCase):
        def test_creating_a_new_poll_and_saving_it_to_the_database(self):
            # start by creating a new Poll object with its "question" set
            poll = Poll()
            poll.question = "What's up?"
            poll.pub_date = timezone.now()

            # check we can save it to the database
            poll.save()

            # now check we can find it in the database again
            all_polls_in_database = Poll.objects.all()
            self.assertEquals(len(all_polls_in_database), 1)
            only_poll_in_database = all_polls_in_database[0]
            self.assertEquals(only_poll_in_database, poll)

            # and check that it's saved its two attributes: question and pub_date
            self.assertEquals(only_poll_in_database.question, "What's up?")
            self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)

        def test_choice_defaults(self):
            choice = Choice()
            self.assertEquals(choice.votes, 0)

OK, let's run it

    $ python manage.py test polls
    Creating test database for alias 'default'...
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK
    Destroying test database for alias 'default'...
