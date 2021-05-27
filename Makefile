#setup:
		#python3 -m venv ~/.dia-aberto-new/
		#source ~/.dia-aberto-new/bin/activate
install:
		pip3 install --upgrade pip
		pip3 install -r requirements.txt
format:
		black *
prep:
		python3 manage.py makemigrations
		python3 manage.py migrate
		python3 manage.py create_groups
		python3 manage.py create_admin test_user
		
test:
		python3 manage.py test


init: install format
deploy: prep test