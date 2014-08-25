from BeautifulSoup import BeautifulSoup

def parse_html(html):
	"""
	Parse the HTML output of Banner's "Summary Class List", returning
	a tuple with a dictionary of class information (class name, etc.)
	and a dictionary of student information keyed on student ID.
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

	students = {}
	for row in tables['Summary Class List'].findAll('tr'):
		columns = row.findAll('td')
		if len(columns) == 1:
			continue

		(num, name, stuid, status, degree, credit_hours, grade, email) = columns

		name = columns[1].text
		student_id = int(columns[2].text)
		email = columns[7].find('a')['href'].split(':')[1]

		students[student_id] = (name, email)

	return (course_info, students)
