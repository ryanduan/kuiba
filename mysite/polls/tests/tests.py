from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Poll, Choice
from polls.forms import PollVoteForm

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

class HomePageViewTest(TestCase):

    def test_root_url_shows_all_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

        polls_in_context = response.context['polls']
        self.assertEquals(list(polls_in_context), [poll1, poll2])

        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)

        poll1_url = reverse('polls.views.poll', args=[poll1.id,])
        self.assertIn(poll1_url, response.content)
        poll2_url = reverse('polls.views.poll', args=[poll2.id, ])
        self.assertIn(poll2_url, response.content)

class SinglePollViewTest(TestCase):

    def test_page_shows_poll_title_and_no_votes_message(self):
        # set up two polls, to check the right one is displayed
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/poll/%d/' % (poll2.id, ))

        # check we've used the poll template
        self.assertTemplateUsed(response, 'poll.html')

        # check we've passed the right poll into the context
        self.assertEquals(response.context['poll'], poll2)

        # check the poll's question appears on the page
        self.assertIn(poll2.question, response.content)

        # check our 'no votes yet' message appears
        self.assertIn('No-one has voted on this poll yet', response.content)

    def test_page_shows_choices_using_form(self):
        # set up a poll with choices
        poll1 = Poll(question='time', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice="PM", votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice="Gardener's", votes=0)
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll1.id, ))

        # check we've passed in a form of the right type
        self.assertTrue(isinstance(response.context['form'], PollVoteForm))

        # and check the form is being used in the template,
        # by checking for the choice text
        #self.assertIn(choice1.choice, response.content)
        #self.assertIn(choice2.choice, response.content)
        self.assertIn(choice1.choice, response.content.replace('&#39;', "'"))
        self.assertIn(choice2.choice, response.content.replace('&#39;', "'"))


class PollsVoteFormTest(TestCase):

    def test_form_renders_poll_choices_as_radio_inputs(self):
        # set up a poll with a couple of choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
        choice2.save()

        # set up another poll to make sure we only see the right choices
        poll2 = Poll(question='time', pub_date=timezone.now())
        poll2.save()
        choice3 = Choice(poll=poll2, choice='PM', votes=0)
        choice3.save()

        # build a voting form for poll1
        form = PollVoteForm(poll=poll1)

        # check it has a single field called 'vote', which has right choices:
        self.assertEquals(form.fields.keys(), ['vote'])

        # choices are tuples in the format (choice_number, choice):
        self.assertEquals(form.fields['vote'].choices, [
            (choice1.id, choice1.choice),
            (choice2.id, choice2.choice),
        ])

        # check it uses radio inputs to render
        #self.assertIn('input type="radio"', form.as_p())
        self.assertIn('type="radio"', form.as_p())  # Something between input and type