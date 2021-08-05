import click
import sqlite3

conn=sqlite3.connect('data.db')
csr=conn.cursor()

def create_table():
	csr.execute('CREATE TABLE IF NOT EXISTS usersdata(firstname TEXT,lastname TEXT,email TEXT,phonenumber TEXT)')

def add_data(firstname,lastname,email,phonenumber):
	csr.execute('INSERT INTO usersdata(firstname ,lastname ,email ,phonenumber) VALUES (?,?,?,?)',(firstname,lastname,email,phonenumber))
	conn.commit()

def view_all_users():
	csr.execute('SELECT * FROM usersdata')
	data=csr.fetchall()
	return data

def get_single_user(firstname):
	csr.execute('SELECT * FROM usersdata WHERE firstname="{}"'.format(firstname))
	data=csr.fetchall()
	return data

def edit_single_user(firstname,new_name):
	csr.execute('UPDATE usersdata SET firstname ="{}" WHERE firstname="{}"'.format(new_name,firstname))
	conn.commit()
	data=csr.fetchall()
	return data

@click.group()
@click.version_option(version='0.01',prog_name='registrio')
def main():
	""" Registrio : A simple registration CLI  """
	pass

@main.command()
@click.option('--firstname','-fn',prompt=True)
@click.option('--lastname','-ln',prompt=True)
@click.option('--email','-em',prompt=True)
@click.option('--phonenumber','-ph',prompt=True)
def add_user(firstname,lastname,email,phonenumber):
	from terminaltables import AsciiTable

	user_data=[['User Data','Value'],['Firstname:',firstname],['Lastname:',lastname],['Email:',email],['Phone Number:',phonenumber]]
	create_table()
	add_data(firstname,lastname,email,phonenumber)
	table1=AsciiTable(user_data)

	click.echo(table1.table)
	click.secho('Saved Input To DataBase',fg='blue')

@main.command()
@click.option('--firstname','-fn')
def search_user(firstname):
	from terminaltables import AsciiTable

	click.secho('Searching For:: {}'.format(firstname),fg='yellow')
	result=get_single_user(firstname)
	table1=AsciiTable(result)
	click.echo(table1.table)

@main.command()
def show_table():
	from terminaltables import AsciiTable

	result=view_all_users()
	new_result=['Firstname','Lastname','Email','Phonenumber']
	click.secho('{}'.format(new_result),bg='blue')
	table1=AsciiTable(result)
	click.echo(table1.table)

@main.command()
@click.option('--firstname','-fn')
@click.option('--newname','-nn')
def edit_user(firstname,newname):
	from terminaltables import AsciiTable

	click.secho('Editting :: {} and Updating to {}'.format(firstname,newname),fg='yellow')
	result=get_single_user(firstname)
	table1=AsciiTable(result)
	click.echo(table1.table)
	edit_single_user(firstname,newname)
	click.secho('Showing Updated Data',fg='yellow')
	
	new_result = ['Firstname','Lastname','Email','Phonenumber']
	click.secho('{}'.format(new_result),bg='blue')
	new_result=get_single_user(newname)
	table2=AsciiTable(new_result)
	click.echo(table2.table)

if __name__ == '__main__':
	main()