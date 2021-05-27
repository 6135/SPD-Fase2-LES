setup:
		python3 -m venv ~/.dia-aberto-new/
		#source ~/.dia-aberto-new/bin/activate
install:
		pip3 install --upgrade pip
		pip3 install -r requirements.txt
		
prep:
		python manage.py makemigrations atividades
		python manage.py makemigrations colaboradores
		python manage.py makemigrations configuracao
		python manage.py makemigrations coordenadores
		python manage.py makemigrations inscricoes
		python manage.py makemigrations notificacoes
		python manage.py makemigrations auth
		python manage.py makemigrations utilizadores
		python3 manage.py migrate
		python3 manage.py create_groups
		python3 manage.py create_admin test_user
		mysql spdfase2 -u root < inserir_dados_bd.sql
run: 
		python3 manage.py runserver 0.0.0.0:8000
init: install
deploy: prep
all: init deploy