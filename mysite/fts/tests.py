from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
from polls.models import Poll, Choice
from django.utils import timezone
from collections import namedtuple

PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question="How are you?",
    choices=[
        'Fine',
        'Good',
        'I am OK',
    ]
)
POLL2 = PollInfo(
    question="Which development language do you like?",
    choices=[
        'Python',
        'Java',
        'Ruby',
    ]
)

class PollsTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

#    def test_can_create_new_poll_via_admin_site(self):
#        # Gertrude opens her web browser, and goes to the admin page
#        self.browser.get(self.live_server_url + '/admin/')
#
#        # She sees the familiar 'Django administration' heading
#        body = self.browser.find_element_by_tag_name('body')
#        self.assertIn('Django administration', body.text)
#
#        # She types in her username and passwords and hits return
#        username_field = self.browser.find_element_by_name('username')
#        username_field.send_keys('ryan')
#
#        password_field = self.browser.find_element_by_name('password')
#        password_field.send_keys('123qwe')
#        password_field.send_keys(Keys.RETURN)
#
#        # her username and password are accepted, and she is taken to
#        # the Site Administration page
#        body = self.browser.find_element_by_tag_name('body')
#        self.assertIn('Site administration', body.text)
#
#        # She now sees a couple of hyperlink that says "Polls"
#        polls_links = self.browser.find_elements_by_link_text('Polls')
#        self.assertEquals(len(polls_links), 2)
#
#        # The second one looks more exciting, so she clicks it
#        polls_links[1].click()
#
#        # She is taken to the polls listing page, which shows she has
#        # no polls yet
#        body = self.browser.find_element_by_tag_name('body')
#        self.assertIn('0 polls', body.text)
#
#        # She sees a link to 'add' a new poll, so she clicks it
#        new_poll_link = self.browser.find_element_by_link_text('Add poll')
#        new_poll_link.click()
#
#        # She sees some input fields for "Question" and "Date published"
#        body = self.browser.find_element_by_tag_name('body')
#        self.assertIn('Question:', body.text)
#        self.assertIn('Date published:', body.text)  # This need change
#
#        # She types in an interesting question for the Poll
#        question_field = self.browser.find_element_by_name('question')
#        question_field.send_keys("What wrong with you?")
#
#        # She sets the date and time of publication - it'll be a new year's
#        # poll!
#        dtn = dt.now()
#        pub_date = '%s-%s-%s' % (dtn.date().year, dtn.date().month, dtn.date().day)
#        pub_time = '%s:%s:%s' % (dtn.time().hour, dtn.time().minute, dtn.time().second)
#        date_field = self.browser.find_element_by_name('pub_date_0')
#        date_field.send_keys(pub_date)
#        time_field = self.browser.find_element_by_name('pub_date_1')
#        time_field.send_keys(pub_time)
#
#        # She sees she can enter choices for the Poll.  She adds three
#        choice_1 = self.browser.find_element_by_name('choice_set-0-choice_text')  # Need change
#        choice_1.send_keys('Very awesome')
#        choice_2 = self.browser.find_element_by_name('choice_set-1-choice_text')  # Need change
#        choice_2.send_keys('Quite awesome')
#        choice_3 = self.browser.find_element_by_name('choice_set-2-choice_text')  # Need change
#        choice_3.send_keys('Moderately awesome')
#
#        # Gertrude clicks the save button
#        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
#        save_button.click()
#        # She is returned to the "Polls" listing, where she can see her
#        # new poll, listed as a clickable link
#        new_poll_links = self.browser.find_elements_by_link_text(
#                "What wrong with you?"
#        )
#        self.assertEquals(len(new_poll_links), 1)
#
#        # Satisfied, she goes back to sleep
#
    def _setup_polls_via_admin(self):
        #
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('ryan')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123qwe')
        password_field.send_keys(Keys.RETURN)

        # She has a number of polls to enter.  For each one, she:
        for poll_info in [POLL1, POLL2]:
            # Follows the link to the Polls app, and adds a new Poll
            self.browser.find_elements_by_link_text('Polls')[1].click()
            self.browser.find_element_by_link_text('Add poll').click()

            # Enters its name, and uses the 'today' and 'now' buttons to set
            # the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            self.browser.find_element_by_link_text('Today').click()
            self.browser.find_element_by_link_text('Now').click()

            # Sees she can enter choices for the Poll on this same page,
            # so she does
            for i, choice_text in enumerate(poll_info.choices):
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice_text' % i)
                choice_field.send_keys(choice_text)

            # Saves her new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(
                    poll_info.question
            )
            self.assertEquals(len(new_poll_links), 1)

            # She goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')

        # She logs out of the admin site
        self.browser.find_element_by_link_text('Log out').click()
    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        #self.fail('TODO')
        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('ryan')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123qwe')
        password_field.send_keys(Keys.RETURN)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Django administration')

        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        # 'How are you?'
#        first_poll_links = self.browser.find_elements_by_link_text(
#                "How are you?"
#        )
#        first_poll_links[0].click()
        first_poll_title = POLL1.question
        self.browser.find_element_by_link_text(first_poll_title).click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        body = self.browser.find_element_by_tag_name('body')
#        self.assertIn("no-one has voted on this poll yet", body.text)

#        self.fail('TODO')

        # He also sees a form, which offers him several choices.
        # He decided to select "very awesome"
#        select_choice_links = self.browser.find_elements_by_css_selector(
                #'input[type="checkbox"]'
#                'inline-related dynamic-choice_set'
#            )
        #for choice_link in select_choice_links:
        #    if self.assertEquals(choice_link, )
#        self.assertEquals(len(select_choice_links), 3)
                #print "OK"

        # He clicks 'submit'

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".

        # The page also says "1 votes"

        # Satisfied, he goes back to sleep

#    def test_verbose_name_for_pub_date(self):
#        for field in Poll._meta.fields:
#            if field.name == 'pub_date':
#                self.assertEquals(field.verbose_name, 'Date published')
#
#    def test_poll_objects_are_named_after_their_question(self):
#        p = Poll()
#        p.question = 'How is babby formed?'
#        self.assertEquals(str(p), 'How is babby formed?')
#
#class ChoiceModelTest(TestCase):
#
#    def test_creating_some_choices_for_a_poll(self):
#        # start by creating a new Poll object
#        poll = Poll()
#        poll.question="What's up?"
#        poll.pub_date = timezone.now()
#        poll.save()
#
#        # now create a Choice object
#        choice = Choice()
#
#        # link it with our Poll
#        choice.poll = poll
#
#        # give it some text
#        choice.choice_text = "doin' fine..."  # Need change
#
#        # and let's say it's had some votes
#        choice.votes = 3
#
#        # save it
#        choice.save()
#
#        # try retrieving it from the database, using the poll object's reverse
#        # lookup
#        poll_choices = poll.choice_set.all()
#        self.assertEquals(poll_choices.count(), 1)
#
#        # finally, check its attributes have been saved
#        choice_from_db = poll_choices[0]
#        self.assertEquals(choice_from_db, choice)
#        self.assertEquals(choice_from_db.choice_text, "doin' fine...")  # Need change
#        self.assertEquals(choice_from_db.votes, 3)
