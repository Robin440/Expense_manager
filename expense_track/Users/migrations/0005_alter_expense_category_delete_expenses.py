# Generated by Django 5.0.1 on 2024-01-25 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_expense_category_expenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Users.category'),
        ),
        migrations.DeleteModel(
            name='Expenses',
        ),
    ]