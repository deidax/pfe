from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from CrawlerApp.models import Crawler
from CrawlerApp.serializers import CrawlerSerializer

from uuid import uuid4
from urllib.parse import urlparse
from scrapyd_api import ScrapydAPI
import pymongo
import json
from django.conf import settings
import os
import time
import urllib

# connect scrapyd service
SCRAPYD_SERVER = 'http://localhost:6800'
# mongodb
MONGODB_CLIENT = "mongodb://localhost:27017/"
MONGO_DB = 'avito'
PRODUCTS_COL = 'products'
AVITO_CRAWLER_COL = 'avito_crawler'
scrapyd = ScrapydAPI(SCRAPYD_SERVER)

@csrf_exempt
def crawlerManagerApi(request, id=0):
    if request.method == 'GET':
        crawler_data = Crawler.objects.all()
        crawler_serializer = CrawlerSerializer(crawler_data, many=True)
        return JsonResponse(crawler_serializer.data, safe=False)
    elif request.method == 'POST':
        crawler_args_data = JSONParser().parse(request)
        crawler_args_serializer = CrawlerSerializer(data=crawler_args_data)
        if crawler_args_serializer.is_valid():
            crawler_args_serializer.save()
            return JsonResponse({"message":"Crawler saved successfully", "code":200}, safe=False)
        return JsonResponse({"message":"Failed to create crawler", "code":422}, safe=False)
    elif request.method =='DELETE':
        crawler = Crawler.objects.get(crawlerId=id)
        crawler.delete()
        return JsonResponse({"message":"Crawler deleted successfully", "code":200}, safe=False)
    # elif request.method == 'PUT':
    #     department_data = JSONParser().parse(request)
    #     department = Departement.objects.get(DepartementId=department_data['DepartementId'])
    #     department_serializer=DepartementSerializer(department,data=department_data)
    #     if department_serializer.is_valid():
    #         department_serializer.save()
    #         return JsonResponse("Updated successfully", safe=False)
    #     return JsonResponse("Fialed to update", safe=False)

@csrf_exempt
def crawlerApi(request, id):
    if request.method == 'GET':
        crawler_data = Crawler.objects.get(crawlerId=id)
        carwler_serializer=CrawlerSerializer(crawler_data)
        start_url = carwler_serializer.data['start_url']
        options = carwler_serializer.data['options']
        if not start_url:
            return JsonResponse({'error': 'Missing  start url', 'code': 422})
        
        domain = urlparse(start_url).netloc # parse the start url and extract the domain
        crawler_unique_id = str(uuid4()) # create a unique ID. 
        settings = {
            'unique_id': crawler_unique_id, #  crawler unique ID for each record for scrapyd DB
        }

        # schedule a new crawling task from scrapyd. 
        task = scrapyd.schedule('default', 'productspider', 
            settings=settings, url=start_url, options=options, domain=domain)

        crawler_data.task_id = task
        crawler_data.save(update_fields=['task_id'])

        return JsonResponse(
            {
             'task_id': task,
             'unique_id': crawler_unique_id,
             'crawler_id': carwler_serializer.data['crawlerId'],
             'crawler_name': carwler_serializer.data['name'],
             'crawler_start_url': carwler_serializer.data['start_url'],
             'crawler_data_options': carwler_serializer.data['options'],
             'status': 'started',
             'code': 200
            }
        )
        
@csrf_exempt
def cancelCrawlerProcessApi(request):
    if request.method == 'POST':
        crawler_in_process = JSONParser().parse(request)
        state_of_canceled_process = None

        for _ in range(3):
            state_of_canceled_process = scrapyd.cancel(crawler_in_process['project'], crawler_in_process['job'])

        return JsonResponse({
            'message': 'Process Canceled',
            'state_of_canceled_process': state_of_canceled_process
        })

@csrf_exempt
def getScrapydListJobsApi(request):
    if request.method == 'POST':
        running_project = JSONParser().parse(request)
        scrapyd_list_jobs = []

        scrapyd_list_jobs = scrapyd.list_jobs(running_project['project'])

        return JsonResponse(scrapyd_list_jobs)

@csrf_exempt
def crawlerDetailsManagerApi(request):
    client = pymongo.MongoClient(MONGODB_CLIENT)
    mongodb = client[MONGO_DB]
    avito_crawler_collection = mongodb[AVITO_CRAWLER_COL]
    if request.method == 'GET':
        avito_crawler_data = avito_crawler_collection.find_one()
        client.close()
        if avito_crawler_data:
            avito_crawler_data.pop('_id')
            return JsonResponse(avito_crawler_data)
        
        return JsonResponse({"message": "No crawler process is found. App started for the first time."})


@csrf_exempt
def readLogFileApi(request):
    if request.method == 'POST':

        logfile = 'logs/default/productspider/'+request.POST.get('task_id')+'.log'

        logfile_path = os.path.join(settings.SCRAPY_DIR, logfile)
        logfile = open(logfile_path, "r")

        loglines = logFollow(logfile)

        # iterate over the generator
        for line in loglines:
            # print(line)
            return JsonResponse(line, safe=False)


        return JsonResponse({"message": "No logs found. App started for the first time."})



def logFollow(logFile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    logFile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = logFile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line


@csrf_exempt
def getProductsData(request):
    client = pymongo.MongoClient(MONGODB_CLIENT)
    mongodb = client[MONGO_DB]
    products_collection = mongodb[PRODUCTS_COL]
    if request.method == 'GET':
        products_data = list(products_collection.find({},{"_id":0}))
        client.close()
        if products_data:
            return JsonResponse(products_data, safe=False)
        
        return JsonResponse({"message": "No product collection is found. App started for the first time."})

@csrf_exempt
def dropProductsData(request):
    client = pymongo.MongoClient(MONGODB_CLIENT)
    mongodb = client[MONGO_DB]
    products_collection = mongodb[PRODUCTS_COL]
    if request.method == 'GET':
        products_collection.drop()
        client.close()
        return JsonResponse({'message': 'Products data dropped successfully'})
        


