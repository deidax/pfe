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

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

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
        if not start_url:
            return JsonResponse({'error': 'Missing  start url', 'code': 422})
        
        domain = urlparse(start_url).netloc # parse the start url and extract the domain
        crawler_unique_id = str(uuid4()) # create a unique ID. 
        settings = {
            'unique_id': crawler_unique_id, #  crawler unique ID for each record for DB
        }

        # schedule a new crawling task from scrapyd. 
        task = scrapyd.schedule('default', 'productspider', 
            settings=settings, url=start_url, domain=domain)

        crawler_data.task_id = task
        crawler_data.save(update_fields=['task_id'])

        return JsonResponse(
            {
             'task_id': task,
             'unique_id': crawler_unique_id,
             'crawler_id': carwler_serializer.data['crawlerId'],
             'crawler_name': carwler_serializer.data['name'],
             'crawler_start_url': carwler_serializer.data['start_url'],
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
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongodb = client["avito"]
    avito_crawler_collection = mongodb["avito_crawler"]
    if request.method == 'GET':
        avito_crawler_data = avito_crawler_collection.find_one()
        # client.close()
        avito_crawler_data.pop('_id')
        return JsonResponse(avito_crawler_data)

