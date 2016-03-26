#!/usr/bin/python

import json
import urllib
import urllib2
import time
import csv

ACCESS_TOKEN = 'ACCESS CODE'
 
base_url = 'https://api.nike.com'
url = '/me/sport/activities/FUELBAND?access_token=%s&experienceType=FUELBAND' % ACCESS_TOKEN
headers = {'appid':'fuelband', 'Accept':'application/json'} # weird required headers, blah.
current_month = None
emotion = ''
note = ''

outputFile = open('fuelband.csv', 'w')

while url:
 
	req = urllib2.Request('%s%s' % (base_url, url), None, headers)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
 
	if resp.get('data'):
 
		for activity in resp.get('data'):
 
			# 2013-05-26T14:48:42Z
			start_time = time.strptime(activity.get('startTime'), '%Y-%m-%dT%H:%M:%SZ')
			date = time.strftime('%a %m/%d/%y', start_time)
 
			month = time.strftime('%B', start_time)
			if month != current_month:
				current_month = month
				#print ''
				#file.write('\n')
				outputWriter = csv.writer(outputFile)
				outputWriter.writerow([current_month,'distance', 'fuel', 'calories', 'steps', 'duration', 'emotion', 'note'])
				#print '--', current_month, '--'
				#file.write('--' + current_month + '--\n')
				#file.write('\n')
			
			# distance calculation
			metrics = activity.get('metricSummary')
			kilom = metrics.get('distance')
			distance = '%.2f' % round(kilom, 2)
			
			if kilom == 0:
				kilom = 1
			
			# remove milliseconds
			duration = metrics.get('duration').partition('.')[0]

			calories = metrics.get('calories')
			fuel = metrics.get('fuel')
			steps = metrics.get('steps')

			for tag in activity.get('tags'):
				if tag.get('tagType') == "EMOTION":
					emotion = tag.get('tagValue').replace('_','-').title()
				if (tag.get('tagType') == "NOTE") and (tag.get('tagValue') != "NOTE"):
					note = tag.get('tagValue')


			if activity.get('activityType') == "ALL_DAY":
                                outputWriter.writerow([date, distance, fuel, calories, steps, duration, emotion, note])
                                emotion = ''
                                note = ''
				
	# pagination
	url = None
	if resp.get('paging') and resp.get('paging').get('next'):
		url = resp.get('paging').get('next') 

outputFile.close()
