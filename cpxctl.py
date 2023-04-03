#!/usr/bin/env python3

import requests
import argparse
import urllib
from urllib.parse import urljoin
import json
from tabulate import tabulate
from prettytable import PrettyTable
import statistics
import threading
import time

BASE_URL = 'http://localhost:8000'
SERVER_URL = 'http://localhost:8000/servers'

server_list = requests.get(SERVER_URL).json()

# gather all available data, and additionally add status and ip as an item
# sort the list of dictionary according to the service and assign it a key which is the service name
def sort():
  all_server_stats = []
  for ip in server_list:
    new_url = urljoin(BASE_URL, ip)
    response = requests.get(new_url).json()

    # add ip and status as a dict item
    response["ip"] = ip
    if int(response["cpu"].strip('%')) > 80 and int(response["memory"].strip('%')) > 80:
      response["status"] = 'Unhealthy'
    else:
      response["status"] = 'Healthy'
  
  # group all dict in a list
    total = all_server_stats.append(response)

  group_service = {}
  for svc in all_server_stats:
    name = svc['service']
    if name in group_service:
      group_service[name].append(svc)
    else:
      group_service[name] = [svc]
  
  return(group_service)

# outputs the stats for all servers
def get_all():
  get_all_output = PrettyTable()
  get_all_output.field_names = ["IP", "Service", "CPU", "Memory", "Status"]
  for key, value in sort().items():
    for x in value:
      get_all_output.add_row([x["ip"], x["service"], x["cpu"], x["memory"], x["status"]])

  print(get_all_output)

# output the average cpu and memory of all service
def avg():
  avg = {}
  for key, value in sort().items():
    total_cpu = []
    total_memory = []

    # grab all cpu and memory values
    for cpu in value:
      total_cpu.append(cpu["cpu"])
    for memory in value:
      total_memory.append(memory["memory"])

    # remove % sign
    total_cpu_int = [int(x.strip('%')) for x in total_cpu]
    total_mem_int = [int(x.strip('%')) for x in total_memory]

    avg_cpu = statistics.mean(total_cpu_int)
    avg_mem = statistics.mean(total_mem_int)

    avg[key] = {'cpu': f'{round(avg_cpu, 2)}%', 'memory': f'{round(avg_mem, 2)}%'}

  avg_output = PrettyTable()
  avg_output.field_names = ["Service", "CPU", "Memory"]

  for i, j in avg.items():
    avg_output.add_row([i, j["cpu"], j["memory"]])
  
  print(avg_output)


def get_service(name, watch):
  get_svc_output = PrettyTable()
  get_svc_output.field_names = ["IP", "Service", "CPU", "Memory", "Status"]
  for key, value in sort().items():
    if key == name:
      for a in value:
        get_svc_output.add_row([a["ip"], a["service"], a["cpu"], a["memory"], a["status"]])
  print(get_svc_output)
  threading.Timer(watch, get_service(name,watch)).start()


def main():
  # set up the command line arguments
  parser = argparse.ArgumentParser()
 
  parser.add_argument('get', type=str, help='The action to perform on the API')
  parser.add_argument('--all', action="store_true", help='Get metrics for all servers')
  parser.add_argument('--avg', action="store_true", help='Get the average of CPU and Memory for all services')
  parser.add_argument('--service', type=str, help='Retrieve information for a given Service')
  parser.add_argument('--watch', type=int, help='Retrieve info for a given Service every X seconds')
  
  # parse the arguments
  args = parser.parse_args()
  if args.get == 'get':
    if args.all:
      get_all()
  
    elif args.avg:
      avg()
  
    elif args.service:
      get_service(args.service, args.watch)

if __name__ == '__main__':
  main()