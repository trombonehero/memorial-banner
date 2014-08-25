#!/usr/bin/env python

import argparse
import banner.classlist

args = argparse.ArgumentParser()
args.add_argument('filenames', nargs = '+')

args = args.parse_args()

course_info = {}
students = {}

for filename in args.filenames:
	(info, stud) = banner.classlist.parse_html(open(filename, 'r'))

	if not course_info:
		course_info = info

	elif info != course_info:
		raise ValueError("files' course info does not match: %s vs %s" % (
				course_info, info
			))

	students.update(stud)

print('%s (CRN %d)' % (course_info['name'], course_info['crn']))
print(course_info['duration'])
print('')

for id in sorted(students):
	(name, email) = students[id]
	print('%9d %14s %-40s' % (id, email, name))
