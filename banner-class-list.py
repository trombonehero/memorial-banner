#!/usr/bin/env python

import argparse
from BeautifulSoup import BeautifulSoup

args = argparse.ArgumentParser()
args.add_argument('filenames', nargs = '+')

args = args.parse_args()

course_info = {}
students = {}

for filename in args.filenames:
	soup = BeautifulSoup(open(filename, 'r').read())

	raw_tables = soup.findAll('table', **{ 'class': 'datadisplaytable' })
	tables = dict([ (t.caption.text, t) for t in raw_tables ])

	if not course_info:
		course_info = dict(
			zip([ 'name', 'crn', 'duration', 'status' ],
				[ i.text for i in tables['Course Information'].findAll('tr') ]
			)
		)

		course_info['crn'] = int(course_info['crn'].split(':')[1])

	for row in tables['Summary Class List'].findAll('tr'):
		columns = row.findAll('td')
		if len(columns) == 1:
			continue

		(num, name, stuid, status, degree, credit_hours, grade, email) = columns

		name = columns[1].text
		student_id = int(columns[2].text)
		email = columns[7].find('a')['href'].split(':')[1]

		students[student_id] = (name, email)

print('%s (CRN %d)' % (course_info['name'], course_info['crn']))
print(course_info['duration'])
print('')

for (id, (name, email)) in students.items():
	print('%9d %14s %-40s' % (id, email, name))
