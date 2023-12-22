
@echo off
cmd /k "cd /d C:\Users\Admin\Desktop\venv\Scripts & activate & cd /d    C:\Users\Admin\Desktop\helloworld & python manage.py runserver"

call workon venv & cd path/to/Python/proj & python -m script.py