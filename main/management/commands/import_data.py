import csv
from datetime import datetime

from django.apps import apps
from django.core.management.base import BaseCommand
from main.models import Store, StoreHours, StoreStatus


class Command(BaseCommand):
    help = "Import data from CSV file to model"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        model_name = kwargs["model_name"]

        model = apps.get_model("main", model_name)

        with open(csv_file) as f:
            reader = csv.reader(f)
            fields = [
                f"{f.name}_id" if f.is_relation else f.name for f in model._meta.fields
            ]

            # skip header row
            next(reader)
            for row in reader:
                dictionary = {}
                if (
                    model_name == "StoreStatus" or model_name == "StoreHours"
                ) and "id" in fields:
                    for i, col in zip(range(1, len(fields)), row):
                        if "UTC" in col:
                            dictionary[fields[i]] = datetime.strptime(
                                col, "%Y-%m-%d %H:%M:%S.%f %Z"
                            ).strftime("%Y-%m-%d %H:%M:%S.%f %Z")
                        else:
                            dictionary[fields[i]] = col
                else:
                    for field, col in zip(fields, row):
                        dictionary[field] = col

                from django.db import connections

                # Disable foreign key constraints
                with connections["default"].constraint_checks_disabled():
                    print(dictionary)
                    model.objects.update_or_create(
                        **dictionary
                        # add more fields as necessary
                    )

        print("Completed")


# python manage.py import_data D:\loop\server\incoming_csv\store.csv Store
# python manage.py import_data D:\loop\server\incoming_csv\store_status.csv StoreStatus
# python manage.py import_data D:\loop\server\incoming_csv\store_hours.csv StoreHours
