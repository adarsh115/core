from accounting.models import (
    Account,
    Expense,
    Tax,
    AccountingSettings,
    Currency
)
import datetime


class AccountingModelCreator():
    def __init__(self, klass):
        self.cls = klass
    # changed opening balances from 100 to 0

    def create_all(self):
        self.create_accounts()
        self.create_expense()
        self.create_tax()
        self.create_currency()
        self.create_settings()


    def create_accounts(self):
        self.cls.account_c = Account.objects.create(
            name='Model Test Credit Account',
            balance=0,
            type='asset',
            description='Some description'
        )
        self.cls.account_d = Account.objects.create(
            name='Model Test Debit Account',
            balance=0,
            type='liability',
            description='Some description'
        )

    def create_expense(self):
        self.cls.expense = Expense.objects.create(
            date=datetime.date.today(),
            description='Test Description',
            category=0,
            amount=100,
            billable=False,
            debit_account=self.cls.account_d)

    def create_tax(self):
        if hasattr(self.cls, 'tax'):
            return self.cls.tax

        self.cls.tax = Tax.objects.create(
            name="tax",
            rate=15
        )

        return self.cls.tax

    def create_currency(self):
        self.cls.currency = Currency.objects.create(
            name='ZWD',
            symbol='P'
        )
        return self.cls.currency

    def create_settings(self):
        if not self.cls.currency:
            self.create_currency()
        if AccountingSettings.objects.all().count() == 0:
            self.cls.accounting_settings = AccountingSettings.objects.create(
                active_currency = self.cls.currency
            )
        else:
            self.cls.accounting_settings = AccountingSettings.objects.first()
            self.cls.accounting_settings.active_currency = self.cls.currency

        return self.cls.accounting_settings