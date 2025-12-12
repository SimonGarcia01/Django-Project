from django.db import models

# Create your models here.
from django.shortcuts import render
import json

def general_reports_view(request):
    # ... tu lógica original ...
    faculty_distribution = {
        "Ingeniería": 42,
        "Ciencias Económicas": 30,
        "Derecho": 18
    }
    return render(request, "reportsAndStats/reports.html", {
        "faculty_distribution": faculty_distribution,
        "faculty_json": json.dumps(faculty_distribution)
    })
