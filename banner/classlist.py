from BeautifulSoup import BeautifulSoup


class Student:
	def __init__(self, student_id, name, email, level):
		self.id = student_id
		(self.surname, self.forenames) = name.split(', ')
		self.email = email
		self.level = level

	def email_prefix(self):
		return self.email.split('@')[0]

	def name(self):
		return ' '.join([ self.forenames, self.surname ])

	def __str__(self):
		return '%s (%d)' % (self.name(), self.id)

	def __repr__(self):
		return "{ %d: '%s' '%s', '%s' }" % (
			self.id, self.forenames, self.surname, self.email)


def parse_html(html):
	"""
	Parse the HTML output of Banner's "Summary Class List", returning
	a tuple with a dictionary of class information (class name, etc.)
	and a list of Student objects.

	Example usage:
	(course_info, students) = banner.classlist.parse_html(open(filename, 'r'))

	print('%s (CRN %d)' % (course_info['name'], course_info['crn']))
	print(course_info['duration'])
	print('')

	for s in sorted(students, key = lambda s: s.name):
		print('%9d %14s %-40s' % (s.id, s.email, s.name))
	"""

	soup = BeautifulSoup(html)

	raw_tables = soup.findAll('table', **{ 'class': 'datadisplaytable' })
	tables = dict([ (t.caption.text, t) for t in raw_tables ])

	course_info = dict(
		zip([ 'name', 'crn', 'duration', 'status' ],
			[ i.text for i in tables['Course Information'].findAll('tr') ]
		)
	)

	course_info['crn'] = int(course_info['crn'].split(':')[1])

	students = []
	for row in tables['Summary Class List'].findAll('tr'):
		columns = row.findAll('td')
		if len(columns) == 1:
			continue

		(num, name, stuid, status, level, credit_hours) = columns[:6]
		email = columns[-1]

		name = name.text
		student_id = int(stuid.text)
		level = level.text
		email = email.find('a')['href'].split(':')[1]

		students.append(Student(student_id, name, email, level))

	return (course_info, students)
