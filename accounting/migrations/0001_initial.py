# Generated by Django 2.1.4 on 2019-04-02 04:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('asset', 'Asset'), ('liability', 'Liability'), (
                    'equity', 'Equity'), ('income', 'Income'), ('cost-of-sales', 'Cost of Sales')], max_length=32)),
                ('description', models.TextField()),
                ('bank_account', models.BooleanField(default=False)),
                ('bank_account_number', models.CharField(
                    blank=True, max_length=32, null=True)),
                ('control_account', models.BooleanField(default=False)),
                ('balance_sheet_category', models.CharField(choices=[('current-assets', 'Current Assets'), ('non-current-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), (
                    'long-term-liabilites', 'Long Term Liabilites'), ('expense', 'Expense'), ('current-assets', 'Current Assets'), ('not-included', 'Not Included')], default='current-assets', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccountingSettings',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('start_of_financial_year', models.DateField()),
                ('default_accounting_period', models.PositiveSmallIntegerField(
                    choices=[(0, 'Annually'), (1, 'Monthly'), (2, 'Weekly')], default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adjustment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_created', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('category', models.IntegerField(choices=[(0, 'Land'), (1, 'Buildings'), (2, 'Vehicles'), (
                    3, 'LeaseHold Improvements'), (4, 'Furniture and Fixtures'), (5, 'Equipment')])),
                ('initial_value', models.DecimalField(
                    decimal_places=2, max_digits=9)),
                ('depreciation_period', models.IntegerField()),
                ('init_date', models.DateField()),
                ('depreciation_method', models.IntegerField(choices=[
                 (0, 'Straight Line'), (1, 'Sum of years digits'), (2, 'Double Declining balance')])),
                ('salvage_value', models.DecimalField(
                    decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Bookkeeper',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('can_create_journals', models.BooleanField(
                    blank=True, default=False)),
                ('can_create_orders_and_invoices',
                 models.BooleanField(blank=True, default=False)),
                ('can_record_expenses', models.BooleanField(
                    blank=True, default=False)),
                ('can_record_assets', models.BooleanField(
                    blank=True, default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyConversionLine',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate', models.DecimalField(
                    decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyConversionTable',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('category', models.PositiveSmallIntegerField(choices=[(0, 'Advertising'), (1, 'Bank Service Charges'), (2, 'Equipment Rental'), (3, 'Dues and Subscriptions'), (4, 'Telephone'), (
                    5, 'Vehicles'), (6, 'Travel and Expenses'), (7, 'Rent'), (8, 'Payroll Taxes'), (9, 'Insurance'), (10, 'Office Expenses'), (11, 'Carriage Outwards'), (12, 'Other')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('reference', models.CharField(
                    blank=True, default='', max_length=32)),
                ('date', models.DateField()),
                ('billable', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterestBearingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('asset', 'Asset'), ('liability', 'Liability'), (
                    'equity', 'Equity'), ('income', 'Income'), ('cost-of-sales', 'Cost of Sales')], max_length=32)),
                ('description', models.TextField()),
                ('bank_account', models.BooleanField(default=False)),
                ('bank_account_number', models.CharField(
                    blank=True, max_length=32, null=True)),
                ('control_account', models.BooleanField(default=False)),
                ('balance_sheet_category', models.CharField(choices=[('current-assets', 'Current Assets'), ('non-current-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), (
                    'long-term-liabilites', 'Long Term Liabilites'), ('expense', 'Expense'), ('current-assets', 'Current Assets'), ('not-included', 'Not Included')], default='current-assets', max_length=16)),
                ('interest_rate', models.DecimalField(
                    decimal_places=2, default=0.0, max_digits=6)),
                ('interest_interval', models.IntegerField(
                    choices=[(0, 'monthly'), (1, 'annually')], default=1)),
                ('interest_method', models.IntegerField(
                    choices=[(0, 'Simple')], default=0)),
                ('date_account_opened', models.DateField(
                    default=datetime.date.today)),
                ('last_interest_earned_date',
                 models.DateField(blank=True, null=True)),
                ('parent_account', models.ForeignKey(blank=True, null=True,
                                                     on_delete=django.db.models.deletion.SET_NULL, to='accounting.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('draft', models.BooleanField(default=True)),
                ('memo', models.TextField()),
                ('posted_to_ledger', models.BooleanField(default=False)),
                ('adjusted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=1, null=True,
                                                 on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('journal', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Journal')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Credit')),
                ('debit', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Debit')),
                ('entry', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.JournalEntry')),
                ('ledger', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Ledger')),
            ],
        ),
        migrations.CreateModel(
            name='RecurringExpense',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('category', models.PositiveSmallIntegerField(choices=[(0, 'Advertising'), (1, 'Bank Service Charges'), (2, 'Equipment Rental'), (3, 'Dues and Subscriptions'), (4, 'Telephone'), (
                    5, 'Vehicles'), (6, 'Travel and Expenses'), (7, 'Rent'), (8, 'Payroll Taxes'), (9, 'Insurance'), (10, 'Office Expenses'), (11, 'Carriage Outwards'), (12, 'Other')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('reference', models.CharField(
                    blank=True, default='', max_length=32)),
                ('cycle', models.IntegerField(choices=[(1, 'Daily'), (7, 'Weekly'), (14, 'Bi- Monthly'), (
                    30, 'Monthly'), (90, 'Quarterly'), (182, 'Bi-Annually'), (365, 'Annually')], default=30)),
                ('expiration_date', models.DateField(null=True)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('last_created_date', models.DateField(blank=True, null=True)),
                ('debit_account', models.ForeignKey(limit_choices_to=models.Q(type='asset'),
                                                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Account')),
                ('entry', models.ForeignKey(blank=True, null=True,
                                            on_delete=django.db.models.deletion.SET_NULL, to='accounting.JournalEntry')),
                ('recorded_by', models.ForeignKey(default=1, null=True,
                                                  on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('rate', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkBook',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
    ]
