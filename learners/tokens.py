from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, staff_id, timestamp):
        return (
            six.text_type(staff_id) + six.text_type(timestamp)
        )

account_activation_token = AccountActivationTokenGenerator()