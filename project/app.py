from gino import Gino
import asyncio
db = Gino()


class University(db.Model):
	__tablename__ = 'universities'

	id = db.Column(db.Integer(), primary_key=True)
	university = db.Column(db.String)
	city = db.Column(db.String)


class Student(db.Model):
	__tablename__ = 'students'

	id = db.Column(db.Integer(), primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	age = db.Column(db.Integer())
	student_id = db.Column(db.String)
	university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))


user_choice = """
Enter:
- 'a' to add a new student 
- 'l' to list of students
- 'r' to delete a student
- 'd' to update a student 
- 'i' to get detail of one student
- 't' How many students study an university
- 'q' to quit


Your choice:"""

async def menu():
	await db.set_bind('postgresql://root:123@localhost/student')
	await db.gino.create_all()
	choice = input(user_choice)
	while choice!='q':
		if choice=='a':
			first_name = input('enter your first name\n')
			last_name = input('enter your last name\n')
			age = int(input('enter your age\n'))
			university_id = int(input('enter university_id\n'))
			student_id = input('enter student id\n')
			university_id = await University.get(university_id)
			new_student = await Student.create(
			first_name=first_name,
			last_name=last_name,
			age=age,
			student_id=student_id,
			university_id=university_id.id

		)	
		elif choice=='l':
			all_students = await db.all(Student.query)
			for i in all_students:
				print(f'first_name:{i.first_name}')
				print(f'last_name:{i.last_name}')
				print(f'age:{i.age}')
				print(f'student id:{i.student_id}')
				x = await University.get(i.university_id)
				print(f'university:{x.university}')
				print('\n')

		elif choice=='r':
			student_id = input('enter student_id\n')
			await Student.delete.where(Student.student_id == student_id).gino.status()
		elif choice=='d':
			student_id = input('enter student_id\n')
			key = input('enter key value\n')
			new_data = input('enter new data\n')
			all_students = await Student.query.gino.all()
			for student in all_students:
				if student.student_id==student_id:
					if key == 'first_name':
						await student.update(first_name=new_data).apply()
					elif key == 'last_name':
						await student.update(last_name=new_data).apply()
					elif key == 'age':
						await student.update(age=int(new_data)).apply()
					else:
						print('Unknown keyword key\n')
				else:
					print('Error student id\n')
		elif choice == 'i':
			student_id = input('enter student id\n')
			all_students = await Student.query.gino.all()
			for student in all_students:
				if student.student_id==student_id:
					print(f'first_name: {student.first_name}')
					print(f'last_name: {student.last_name}')
					print(f'age: {student.age}')
					print(f'student_id: {student.student_id}')
					x = await University.get(student.university_id)
					print(f'university: {x.university}')
		elif choice == 't':
			query = db.select([University])
			universities = await query.gino.load(University).all()
			for query_id in universities:
				count = await (db.select([db.func.count()]).where(Student.university_id==query_id.id).gino.scalar())
				print(f'{query_id.university} has {count} students')

		choice = input(user_choice)
	await db.pop_bind().close()

asyncio.get_event_loop().run_until_complete(menu())




	




