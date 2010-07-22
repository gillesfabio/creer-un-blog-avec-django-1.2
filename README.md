Source code of my french tutorial: "Créer un blog avec Django 1.2"
==================================================================

Tutorial URL: http://gillesfabio.com/blog/2010/07/22/creer-un-blog-avec-django-1-2/

Grab the source:

    $ git clone git://github.com/gillesfabio/creer-un-blog-avec-django-1.2.git

Go in the project's folder:

    $ cd creer-un-blog-avec-django-1.2/website

Change some settings if you need and synchronize the database:

    $ python manage.py syncdb

Load the fixtures:

    $ python manage.py loaddata test_data
    
Run the server:

    $ python manage.py runserver
    
That's all.
