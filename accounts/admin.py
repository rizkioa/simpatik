from accounts.models import Account
from accounts.account_admin import AccountAdmin

from django.contrib import admin


# Register your models here.

admin.site.register(Account, AccountAdmin)