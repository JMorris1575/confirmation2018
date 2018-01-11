Implementing the Website
========================

This document discusses the planning and programming details of implementing the website. Since I still don't really
know how to program in the testing, I will just do my "testing charts" to gradually implement the website.

Overall Plan
------------

Here are my thoughts as to the order in which to implement the website:

* Create the Candidate Activities and Pages
* Create the Administrator CRUD pages
* Create Special access for the Adult Facilitators

Plan for the Candidate Portion
------------------------------

Here are my initial plans for how to the Candidate portion of the Website working:

* Get logging in and logging out to work
* Create the activity app
* Create the Welcome Page
* Create the Activity Model
* Use admin to add some fake activities
* Get the Welcome page to display the activities
* Create the Page Model
* Use admin to add some fake pages of various types
* Create a Table of Contents or Activity Summary Page (Called the :ref:`Cover<cover_page>` page before.)
* Create individual page types
    * Essay
    * Multiple Choice
    * True/False
    * Discussion

Implementing the Candidate Portion
----------------------------------

Logging In
++++++++++

Getting to the login page
*************************

It seems I can largely copy what I did for the Christmas website except updating the approach to urls moving from
url patterns to url paths. The ``urls.py`` file in the ``config`` directory looks like this::

    """confirmation URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/2.0/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

I'm thinking there should be a line at the beginning of the urlpatterns list saying::

    path('/', include('user.urls')),

This would also require the import of ``include`` as follows::

    from django.urls import path, include

It would also, of course, require the creation of a ``user`` app and adding some url paths there. Here is a testing
chart:

.. csv-table::**Does a user come to the login page when first entering the site?**
    :header: Success?, Result, Action to be Taken
    :widths: auto

    No, still displays the success page, add the '' path
    No, name 'include' is not defined, add include to the django.urls import
    No, ModuleNotFoundError: No module named 'user', create the user app
    No, ModuleNotFoundError: No mocule named 'user.urls', create user.urls.py
    No, '...user\\urls.py' does not appear to have any patterns in it..., add the pattern :ref:`below.<login_url>`
    No, 'Page not found' looked for / and admin/ but the empty path didn't match, try '//'
    No, 'Page not found' looked for // and admin/ but the empty path didn't match try '' in config\urls.py
    No, NoReverseMatch at / 'dj-auth' is not a registered namespace, put 'user.apps.UserConfig' in INSTALLED_APPS
    No, same error, add app_name='user', namespace='dj-auth' to include statement in config\urls.py
    No, TypeError: include() got an unexpected keyword argument 'app_name', remove the app_name='user' argument
    No, ImproperlyConfigured: namespace in include without providing app_name not supported, copy second path from c17
    No, same problem, delete second path
    No, back to 'dj-auth' is not a registered namespace, study the docs!
    Yes, :ref:`this<login_final>` is what finally worked.

.. _login_url:

Here is the login url modified from christmas17::

    path('', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False)),

I also had to add::

    from django.urls import path
    from django.views.generic import RedirectView

for this part.

.. _login_final:

config\urls.py::

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('', include('user.urls')),
        path('user/', include('user.urls'), name='dj-auth'),
        path('admin/', admin.site.urls),
    ]

user\urls.py::

    from django.urls import path
    from django.contrib.auth import views as auth_views
    from django.views.generic import RedirectView

    urlpatterns = [
        path('', RedirectView.as_view(pattern_name='login', permanent=False)),
        path('login/', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),

    ]

Logging In
**********

I should be able to copy my former login.html page, from StBasilConfirmation, pretty much. First I will do it without
any css formatting.

.. csv-table::**Does the login page display instructions, a username box and a password box?**
    :header: Success?, Result, Action to be Taken
    :widths: auto

    No, just a "This will be my login page message.", add the three items as in StBasilConfirmation
    No, got 'dj-auth' is not a registered namespace, replace login.html's reference to 'dj-auth' with 'welcome'
    Yes, but it looks ugly and may or may not work

.. csv-table::**Does entering the superuser username and password display the welcome page?**
    :header: Success?, Result, Action to be Taken
    :widths: auto

    No, it goes to localhost:8000/activity/welcome/ but does not display anything, add a get method to WelcomeView
    No, still just displays a blank page - it's posting not getting, change the method to post
    Yes, after adding 'activity.apps.ActivityConfig' to the INSTALLED_APPS

.. csv-table::**Does it prevent me from getting to activity/welcome if I am not logged in?**
    :header: Success?, Result, Action to be Taken
    :widths: auto

    No, after creating 'get' method in WelcomeView, import 'login_required' and use it around url view calls
    No, got 'dj-auth' not registered namespace again, remove references to dj-auth from base.py
    No, goes back to login page but it doesn't allow me to log in,

Logging Out
***********

I will have to temporarily add a "Logout" button to welcome.html to test this since I have not yet created the
header.html page.

.. csv-table::**Does clicking the logout link log me out of the website?**
    :header: Success?, Result, Action to be Taken
    :widths: auto

Moving to the Home Computer
---------------------------

I got into a PyCharm project that had VCS enabled, in this case christmas17, and selected ``VCS->Git->Clone...``. Upon
entering the Git Repository URL, ``https//github.com/JMorris1575/confirmation2018``, PyCharm opened a new project on
this machine.

I also had to configure PyCharm to use the ``conf`` virtual environment and upgrade that environment to Django 2.0. That
turned out to be possible from within PyCharm under File->Settings...->Project Interpreter the outdated packages could
be updated by selecting them and then clicking on the blue up-arrow on the right hand side. I upgraded Django and, while
I was at it, upgraded psycopg2, sphinx and setuptools. The latter had to be done in a system command window using::

    pip install -U setuptools

    pip install -U sphinx

I'm not sure if upgrading sphinx automatically upgraded setuptools as there was some weirdness going on during the
process.

I had to create a database to use on this machine but I didn't have postgreSQL10 installed. Going through PostreSQL's
weird download process, I downloaded and installed PostgreSQL 10.1.

Information for Home Computer's Installation of PostgreSQL::

    Installation Directory: C:\Program Files\PostgreSQL\10
    Server Installation Directory: C:\Program Files\PostgreSQL\10
    Data Directory: C:\Program Files\PostgreSQL\10\data
    Database Port: 5433
    Database Superuser: postgres
    Operating System Account: NT AUTHORITY\NetworkService
    Database Service: postgresql-x64-10
    Command Line Tools Installation Directory: C:\Program Files\PostgreSQL\10
    pgAdmin4 Installation Directory: C:\Program Files\PostgreSQL\10\pgAdmin 4
    Stack Builder Installation Directory: C:\Program Files\PostgreSQL\10

Getting into pgAdmin4 I right clicked Login/Group Roles and added Jim, clicked 'Definition' and gave my "dylan selfie"
password. I made myself a superuser by clicking on the Permissions tab.

Finally, I did a ``python manage.py migrate`` and a ``python manage.py createsuperuser``, but, the latter failed since
it said there was already a username of Jim. In the admin app I found Username: Jim, First name: Fr. Jim, Last name:
Morris, Email address: FrJamesMorris@gmail.com. I did not enter any of that on this computer. Could it be in the
migration files? Nope. I couldn't find anything in the migration files. Checking the ``conf-secrets.json`` file I
discovered two things:

# it still refers to ``confdatabase`` rather than to ``conf18``
# IT WAS SAVED ON GITHUB!!!!!

Great! Now I have to change it all

so now I should be ready to
work on the website on my Home Computer.

Starting Over with Authentication
---------------------------------

Trying to use the methods that previously worked under Django 1.11 (and earlier) just isn't working now so I'm going to
start all over again. I could either try to follow the methods outlined in the Django documentation or try to use one of
the tutorial websites I saved the other night. Since I'm using Django 2.0, which is brand new, I suspect it may be
wiser to use the Django documentation.

