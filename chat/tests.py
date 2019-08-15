from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser


class ChatTestCase(TestCase):
    """
    Test the core functionality of the chat app.
    """
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@user1.se', first_name='user1_first',
                                                    last_name='user1_last', password='user1pass')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@user2.se', first_name='user2_first',
                                                    last_name='user2_last', password='user2pass')

    def test_redirect_on_unauthenticated(self):
        """
        An unauthenticated user should be redirected to the login page
        """
        c = Client()

        redirect_from_threads = c.get(reverse('chat:threads'), follow_redirects=True)
        redirect_from_message = c.get(reverse('chat:messages', args=[1]), follow_redirects=True)

        self.assertRedirects(redirect_from_threads, '/accounts/login/?next=/threads/')
        self.assertRedirects(redirect_from_message, '/accounts/login/?next=/threads/user/1')

    def test_login(self):
        """
        The login view should accept valid credentials and deny invalid credentials
        """
        c = Client()
        valid_credentials = {'username': 'user1', 'password': 'user1pass'}
        invalid_credentials = {'username': 'user1wrong', 'password': 'user1passwrong'}

        login_with_valid_credentials = c.post(reverse('login'), data=valid_credentials)
        login_with_invalid_credentials = c.post(reverse('login'), data=invalid_credentials)

        self.assertEqual(login_with_valid_credentials.status_code, 302)
        self.assertEqual(login_with_invalid_credentials.status_code, 200)

    def test_signup(self):
        """
        The signup view should accept a complete form and deny an incomplete form
        """
        c = Client()
        signup_credentials_complete = {
            'username': 'user3',
            'email': 'user3@user3.se',
            'first_name': 'user3first',
            'last_name': 'user3last',
            'password1': 'complexpass',
            'password2': 'complexpass'
        }

        signup_credentials_incomplete = {'username': 'user3'}

        valid_signup = c.post(reverse('signup'), data=signup_credentials_complete)
        invalid_signup = c.post(reverse('signup'), data=signup_credentials_incomplete)

        self.assertEqual(valid_signup.status_code, 302)
        self.assertEqual(invalid_signup.status_code, 200)

    def test_see_user_list(self):
        """
        A authenticated user should see other users in the user list, but not herself
        """
        c = Client()
        c.force_login(self.user1)

        user_list = c.get(reverse('chat:threads'))

        self.assertContains(user_list, '<strong>user2_first user2_last</strong>', 1)
        self.assertNotContains(user_list, '<strong>user1_first user1_last</strong>')

    def test_empty_message_thread(self):
        """
        If no thread yet exists between two users, a information alert should be visible
        """
        c = Client()
        c.force_login(self.user1)

        messages_with_user2 = c.get(reverse('chat:messages', args=[2]))

        self.assertContains(messages_with_user2, 'No messages in this conversation yet.', 1)

    def test_post_message(self):
        """
        A posted message should appear on the message page and update thread info in users list
        """
        c = Client()
        c.force_login(self.user1)
        message_payload = {'body': 'user1 to user2, over'}

        post_message = c.post(reverse('chat:messages', args=[2]), data=message_payload)
        posted_message_visible = c.get(reverse('chat:messages', args=[2]))
        users_list_updated = c.get(reverse('chat:threads'))

        self.assertEqual(post_message.status_code, 302)
        self.assertContains(posted_message_visible, 'user1 to user2, over', 1)
        self.assertContains(users_list_updated, 'You: user1 to user2, over - 0 minutes', 1)

    def test_404(self):
        """
        On 404-errors the custom 404 view should be used
        """
        c = Client()
        c.force_login(self.user1)

        should_not_be_found = c.get(reverse('chat:messages', args=[5000]))

        self.assertContains(should_not_be_found, 'Nothing here!', status_code=404)
