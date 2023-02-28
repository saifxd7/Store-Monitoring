import csv
from datetime import datetime, timedelta
from io import StringIO

import pytz
from celery import shared_task
from django.core.files.base import ContentFile
from main.models import Report, Store, StoreReport, StoreStatus


@shared_task
def generate_report_async(report_id):

    # get the report object by report_id
    report = Report.objects.get(report_id=report_id)
    print(report)

    # generate store reports data
    store_reports = []
    stores = Store.objects.all()
    print(stores)

    # generate CSV data
    csv_data = StringIO()
    writer = csv.writer(csv_data)

    writer.writerow(
        [
            "store_id",
            "uptime_last_hour(in minutes)",
            "uptime_last_day(in hours)",
            "update_last_week(in hours)",
            "downtime_last_hour(in minutes)",
            "downtime_last_day(in hours)",
            "downtime_last_week(in hours)",
        ]
    )

    for store in stores:
        print(store)

        store_tz = pytz.timezone(store.timezone_str)
        print(store_tz)

        # Get the current time
        now = datetime.now(tz=store_tz)
        print(now)

        # Retrieve the store status data for the last hour
        one_hour_ago = now - timedelta(hours=1)
        store_status_last_hour = StoreStatus.objects.filter(
            store=store, timestamp_utc__gte=one_hour_ago
        ).values_list("timestamp_utc", "status")
        print(store_status_last_hour)

        # Calculate the uptime and downtime for the last hour
        uptime_last_hour = store_status_last_hour.filter(
            status="active").count()
        downtime_last_hour = store_status_last_hour.filter(
            status="inactive").count()

        print(uptime_last_hour, downtime_last_hour)

        # Calculate uptime and downtime for the last day
        one_day_ago = now - timedelta(days=1)

        store_status_last_day = StoreStatus.objects.filter(
            store=store, timestamp_utc__gte=one_day_ago
        ).values_list("timestamp_utc", "status")
        print(store_status_last_day)

        uptime_last_day = store_status_last_day.filter(status="active").count()
        downtime_last_day = store_status_last_day.filter(
            status="inactive").count()
        print(uptime_last_day, downtime_last_day)

        # Calculate uptime and downtime for the last week
        one_week_ago = now - timedelta(weeks=1)
        store_status_last_week = StoreStatus.objects.filter(
            store=store, timestamp_utc__gte=one_week_ago
        ).values_list("timestamp_utc", "status")
        print(store_status_last_week)

        uptime_last_week = store_status_last_week.filter(
            status="active").count()
        downtime_last_week = store_status_last_week.filter(
            status="inactive").count()
        print(uptime_last_week, downtime_last_week)

        # append the generated data to store_reports list
        store_reports.append(
            {
                "store": store,
                "uptime_last_hour": uptime_last_hour,
                "uptime_last_day": uptime_last_day,
                "uptime_last_week": uptime_last_week,
                "downtime_last_hour": downtime_last_hour,
                "downtime_last_day": downtime_last_day,
                "downtime_last_week": downtime_last_week,
            }
        )

        writer.writerow(
            [
                str(store.store_id),
                uptime_last_hour,
                uptime_last_day,
                uptime_last_week,
                downtime_last_hour,
                downtime_last_day,
                downtime_last_week,
            ]
        )

    print(store_reports)

    # update the report object with the generated data
    report.status = "Completed"
    report.created_at = datetime.now()
    print("report completed")

    for store_report_data in store_reports:
        StoreReport.objects.create(
            store=store_report_data["store"],
            report=report,
            uptime_last_hour=store_report_data["uptime_last_hour"],
            uptime_last_day=store_report_data["uptime_last_day"],
            uptime_last_week=store_report_data["uptime_last_week"],
            downtime_last_hour=store_report_data["downtime_last_hour"],
            downtime_last_day=store_report_data["downtime_last_day"],
            downtime_last_week=store_report_data["downtime_last_week"],
        )

    csv_file = ContentFile(csv_data.getvalue().encode("utf-8"))
    print("created csv file: ", csv_file)

    # save report object with csv file
    report.csv_file.save(f"{report_id}.csv", csv_file)
    report.save()
    print("Report Generated")
