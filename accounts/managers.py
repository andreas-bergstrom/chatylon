from django.contrib.auth.base_user import BaseUserManager
import django.contrib.auth.models as models
from django.db.models.expressions import RawSQL


class UserManager(models.UserManager):
    def get_user_list_for(self, me):
        """
        Returns a queryset with users and data form any existing threads between them and the current user
        todo: optimize annotations and/or remove raw sql
        """
        user_list = self.model.objects.exclude(pk=me.pk).filter(is_staff=False)

        # Add modified timestamp from thread
        user_list = user_list.annotate(thread_modified=RawSQL("""
            SELECT ct.modified
            FROM chat_thread_participants ctp
            INNER JOIN chat_thread ct ON ctp.thread_id = ct.id
            WHERE ctp.customuser_id = accounts_customuser.id AND ctp.thread_id IN 
                    (SELECT thread_id FROM chat_thread_participants WHERE customuser_id = %s)
        """, (me.pk,)))

        # Add body from last_message
        user_list = user_list.annotate(last_message_body=RawSQL("""
                    SELECT cm.body
                    FROM chat_thread_participants ctp
                    INNER JOIN chat_thread ct ON ctp.thread_id = ct.id
                    INNER JOIN chat_message cm ON ct.last_message_id = cm.id
                    WHERE ctp.customuser_id = accounts_customuser.id AND ctp.thread_id IN 
                            (SELECT thread_id FROM chat_thread_participants WHERE customuser_id = %s)
                """, (me.pk,)))

        # Add userid from last_message
        user_list = user_list.annotate(last_message_sender_id=RawSQL("""
                            SELECT cm.sender_id
                            FROM chat_thread_participants ctp
                            INNER JOIN chat_thread ct ON ctp.thread_id = ct.id
                            INNER JOIN chat_message cm ON ct.last_message_id = cm.id
                            WHERE ctp.customuser_id = accounts_customuser.id AND ctp.thread_id IN 
                                    (SELECT thread_id FROM chat_thread_participants WHERE customuser_id = %s)
                        """, (me.pk,)))

        return user_list
