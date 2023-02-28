import csv
import random

from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from main.models import Report
from main.tasks import generate_report_async
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
@csrf_exempt
def trigger_report(request):
    try:
        # create a new report id
        report_id = f"report-{random.randint(100000, 999999)}"
        Report.objects.create(report_id=report_id)

        # initiate the report generation in background
        generate_report_async.delay(report_id)

        return Response({"report_id": report_id}, status=status.HTTP_200_OK)
    except Exception as err:
        Response({"message": err.__str__()},
                 status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'report_id',
            in_=openapi.IN_QUERY,
            description='ID of the report',
            type=openapi.TYPE_STRING
        ),
    ]
)
@api_view(["GET"])
def get_report(request):
    try:

        # check if the report is generated and ready to be served
        report_id = request.query_params.get("report_id")
        report = Report.objects.filter(report_id=report_id).first()

        if not report:
            # report not found, return 404
            return Response(status=status.HTTP_404_NOT_FOUND)

        if report.status == "Running":
            # report is still generating, return "Running" status
            return Response({"status": "Running"}, status=status.HTTP_200_OK)

        elif report.status == "Completed":

            # Handle the case where the report does not have a CSV file
            if not report.csv_file:
                return Response(
                    {"message": "Report does not have a CSV file"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:

                # Generate the response with the CSV file
                response = FileResponse(report.csv_file)

                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{report.report_id}.csv"'
                return response
    except Exception as err:
        Response({"message": err.__str__()},
                 status=status.HTTP_400_BAD_REQUEST)
