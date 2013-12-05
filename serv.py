import os

os.system('python manage.py migrate')
os.system(os.path.join('python manage.py loaddata fixtures','champions.xml'))
os.system(os.path.join('python manage.py loaddata fixtures','matchups.xml'))
os.system(os.path.join('python manage.py loaddata fixtures','synergies.xml'))

os.system('python manage.py runserver')
