from django.db import models


class Store(models.Model):
    store_id = models.IntegerField(primary_key=True, editable=False)
    timezone_str = models.CharField(max_length=50, default="America/Chicago")

    def __str__(self):
        return f"{self.store_id}"


class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=[("active", "active"), ("inactive", "inactive")]
    )
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"{self.store} - {self.timestamp_utc} ({self.status})"


class StoreHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day = models.IntegerField(
        choices=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ]
    )
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store} - {self.day} ({self.start_time_local} - {self.end_time_local})"


class Report(models.Model):
    report_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=255,
        default="Running",
        choices=[("RUNNING", "Running"), ("COMPLETED", "Completed")],
    )
    csv_file = models.FileField(upload_to="reports/", null=True, blank=True)

    def __str__(self):
        return self.report_id


class StoreReport(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="store_reports"
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    uptime_last_hour = models.IntegerField(default=0)
    uptime_last_day = models.IntegerField(default=0)
    uptime_last_week = models.IntegerField(default=0)
    downtime_last_hour = models.IntegerField(default=0)
    downtime_last_day = models.IntegerField(default=0)
    downtime_last_week = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.report} - {self.store}"
