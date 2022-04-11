import platform    # For getting the operating system name
import subprocess  # For executing a shell command

import mysql.connector as mysql

from django.http import HttpResponse, response
from django.shortcuts import render


def ping_checker():
    host = 'ec2-3-68-193-21.eu-central-1.compute.amazonaws.com'
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    ping_test = []
    for _ in range(4):
        command = f'ping {param} 1 {host}'
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8")
        ping_test.append(output)
    return ping_test


def index(request):
    result = ping_checker()
    database_status()
    status = f" SERVER STATUS: {HttpResponse.status_code}"
    return render(
        request=request,
        template_name="index.html",
        context={"result": result, "status": status, "db_status": database_status()}
    )


def database_status():
    # enter your server IP address/domain name
    HOST = "mysql-cheaptrip.carxec0yhyqa.eu-central-1.rds.amazonaws.com"
    # or "domain.com"
    # database name, if you want just to connect to MySQL server, leave it empty
    DATABASE = "djangodb"
    # this is the user you create
    USER = "admin"
    # user password
    PASSWORD = "XLm650DR"
    # connect to MySQL server
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    return f"Connected to MySQL DB version: {db_connection.get_server_info()}"
