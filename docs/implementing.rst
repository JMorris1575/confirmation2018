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

* :ref:`Get logging in and logging out to work<authentication>`
    * Create the activity app (Done during first attempt at working on login.)
    * Create the Welcome Page (Done during first attempt at working on login.)
* :ref:`Create the Activity Model<activity_model>`
* Use admin to add some fake activities
* Get the Welcome page to display the activities
* Create the Page Model
* Use admin to add some fake pages of various types
* Create a Table of Contents or Activity Summary Page (Called the :ref:`Cover<cover_page>` page before.)
* Create individual page types in html
    * Essay
    * Multiple Choice
    * True/False
    * Discussion

Implementing the Candidate Portion
----------------------------------

Logging In
**********

Getting to the login page
+++++++++++++++++++++++++

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
++++++++++

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
+++++++++++

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

Great! Now I have to change it all.

.. index:: conf-secrets.json

First I did a ``git rm --cached conf-secrets.json`` to remove the file from the git repository without deleting it from
my computer. Unfortunately, when I deleted and recreated the github repository and did a push to it, the previous
commits, which included conf-secrets.json, all showed up.

To fix the problem I had to delete the repository on github and then recreate it, delete the .git folder in
the local confirmation2018 project folder, wait for the ``Invalid VCS root mapping`` event to pop up in PyCharm. Follow
the Configure link to delete the git root reference (or whatever it was) then go back and re-enable version control
integration. Finally I had to add the CORRECT files to git. Just to be safe I added
``confirmation/config/settings/conf-secrets.json`` to the .gitignore file.

While I'm thinking about it I will also get into team viewer to remove the file from git on my rectory computer. I don't
know what will happen when I try to do a git pull. Perhaps I should delete the whole project on the Rectory computer and
clone it again from github.

But now I should be ready to work on the website on my Home Computer.

.. _authentication:

Starting Over with Authentication
---------------------------------

Trying to use the methods that previously worked under Django 1.11 (and earlier) just isn't working now so I'm going to
start all over again. I could either try to follow the methods outlined in the Django documentation or try to use one of
the tutorial websites I saved the other night. Since I'm using Django 2.0, which is brand new, I suspect it may be
wiser to use the Django documentation.

Version 2.0 has removed a number of things that were present before -- at least one of which I was using: ``app_name``
being part of ``include()`` has been deprecated and removed. That may explain some of the problems I've been having. I
will see what happens when I try to use the authentication system as I THINK it was explained in the documents.

Redirection
***********

First I will check to see whether just entering the root url (locally:  ``localhost:8000`` will redirect me to
``localhost:8000/user/login/``.

This path did it::

    path('', RedirectView.as_view(url='user/login/')),

Now I will check to see whether, when I enter ``localhost:8000/user/`` or ``localhost:8000/user`` it also redirects me
to ``localhost:8000/user/login/``.

This path, in ``user/urls.py`` did it::

    path('', RedirectView.as_view(url='/user/login/')),

Logging In
**********

Now I will change the 'login' path to call the LoginView class as follows::

    path('login/', auth_views.LoginView.as_view(), name='login'),

At first it gave me a crazy ``AttributeError: 'SessionStore' object has no attribute '_session_cache'``. It was also,
however, warning me that I had 14 unapplied migrations which I didn't notice. With a lucky guess I did a
``python manage.py migrate`` and logging in seemed to be working until I tried to add the LoginRequiredMixin to
``activity/views.WelcomeView`` as follows::

    from django.shortcuts import render
    from django.views import View
    from django.contrib.auth.mixins import LoginRequiredMixin

    # Create your views here.

    class WelcomeView(LoginRequiredMixin, View):
        template_name = 'activity/welcome.html'

        def get(self, request):
            return render(request, self.template_name)

        def post(self, request):
            print('request.user = ', request.user)
            return render(request, self.template_name)

The extra print statement helped me discover that the user was still AnonymousUser so I tried to enter the admin app but
could not do so. Remembering that I had changed ``conf-secrets.json`` to indicate the correct database ``conf18`` I
remembered that I hadn't set a superuser so I did a ``python manage.py createsuperuser`` with my usual input and then
I could get into the admin app and logging in worked and reported that ``Jim`` was the ``request.user``.

Logging Out
***********

With this in the user/urls.py file::

    path('logout/', auth_views.logout, {'template_name': 'registration/login.html'}, name='logout'),

clicking on the Logout link that is currently on my stubbed-in Welcome page sent me back to ``/user/login`` with
``?next=/activity/welcome/`` but would not allow me to log in. I changed it to::

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

and it still didn't work.

.. index:: Problem Solutions; logging in

Logging In Revisited
********************

It seems I'm only really logging in when I do it through the admin app. Any time I've logged out and get to my own
login page, it doesn't really log me in. To experiment I will remove the LoginRequiredMixin from the WelcomeView.

Sure enough, it's still listing me as AnonymousUser. Maybe there's something I need to do in my own login view? Check
the documentation again...

Ah! I finally discovered the problem at
https://docs.djangoproject.com/en/2.0/topics/auth/default/#django.contrib.auth.views.LoginView In my ``login.html`` file
I had this line::

    <form method="post" action="{% url 'welcome' %}">

instead of::

    <form method="post" action="{% url 'login' %}">

so the user was never going back to the post method of LoginView to actually get logged in. Now I can try using
``loginrequired()`` around the view calls in the urls.py files and it worked fine!

Logging Out Revisited
*********************

I'd like the Logout page to include an easy way to log back in. First I will create a registration/logout.html file
that has a Log Back In link.

It worked after I changed ``users/urls.py`` to include the following::

    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

I thought I would not have had to do that if I had called my file logged_out.html but, when I tried that, it still
brought me to the admin app's login page instead of my own. Perhaps there is a conflict between namespaces or something
but I will just leave it alone for now.

Using skeleton.css
------------------

I copied both the ``templates`` directory and the ``static`` directory from confirmation2017. The ``templates``
directory contains ``base.html`` with all the css file information and the ``static`` directory contains the ``site``
directory with an ``images`` directory containing the Holy Spirit image and the three css files: ``custom.css``,
``normalize.css`` and ``skeleton.css``. Checking the confirmation2017 version of ``dev.py`` I found it the same as
I am using here so now I have to adjust my templates.

Updating the html pages
***********************

To use the css I had to update the existing html pages:  login.html, logout.html and welcome.html. I followed the way I
did it in christmas17 by having a separate header and footer file. It was a bit of an education since I had to remind
myself of such things as using {{ block.super }} to actually get the benefits I was looking for -- such as getting part
of the title from the parent page and part from the current page.

The login.html Page
*******************

I want the login form to appear in a nice rounded box, like the trivia questions in christmas17, so I will try adding a
"shadowed" class to the form itself and update custom.css to include::

    .shadowed {
        border-width: 2px;
        border-style: solid;
        border-color: black;
        border-radius: 10px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.8);
        padding: 10px;
    }

.. _activity_model:

.. index:: Problem Solutions; migrations

Create the Activity Model
-------------------------

I used pretty much the same Activity model as in confirmation2017. The only change I made was to use 'index' in place of
'number' to allow for the ordering of the activities the way I want them ordered.

Now I will do a ``python manage.py makemigrations`` and ``python manage.py migrate`` and use the admin app to create at
least one activity. Then I can improve the welcome page.

It didn't work at first, just told me there were no changes, because I had not registered the model in
``activity/admin.py``.

Hmm... it still didn't work afterward. What is going on?

Apparently the activity app needed to have a migrations folder with a blank ``__init__.py`` file in it. After I did that
``makemigrations`` and ``migrate`` worked as expected.

What happened to the migrations foler?  I don't know if I accidentally deleted it some time after it was created or if
it just didn't make it into the git clone.

Checking on github I see that there is no migrations folder under the acivity app, but there is one under the user app
even though it only contains the empty ``__init__.py`` file. I may have accidentally deleted it after startapp created
it. Just to be sure startapp does create it I will do a ``python manage.py startapp fakeapp`` and see if it comes with a
migrations folder...

Yep! The migrations folder is there! Hard telling what happened to the activity app's version -- unless I just didn't
include it in git. I will check with TeamViewer...

Yep, that was it! The rectory computer had a migrations folder in the activity app's directory but it's ``__init__.py``
file was not marked to be included in git. Funny I would miss that but include ``conf-secrets.json``.

Moving Back to the Rectory Computer
-----------------------------------

I could not do a ``git pull`` command because it refused to merge unrelated projects or some such thing. So I took the
whole Confirmation2018 folder and renamed it Confirmation2018Bak then cloned confirmation2018 from git hub. After I used
TeamViewer to copy ``conf-secrets.json`` and assured myself that the right database existed on this computer I attempted
a ``migrate`` but it could not find Django -- I wasn't in the conf virtual environment. In PyCharm's Settings module I
set the right environment and upgraded all the things needing upgrading (I had to close PyCharm again to upgrade
Sphinx).

When I tried the ``migrate`` command I got::

    django.db.utils.OperationalError: FATAL:  role "Jim" is not permitted to log in

so I tried to create a superuser by that name but got the same error message.

Back in PgAdmin4 (version 2.0 -- the version that I often have to start twice) I discovered that Jim did not have any
access rights. I had to click on Jim in Login/Group Roles then click what seems to be an edit button at the top of
the properties page. Then, on the Priveledges page, gave myself the proper access rights.

Finally, the ``migrate`` command worked.

Using TeamViewer I did a ``dumpdata > all-2018-01-12.json`` and copied it over to this computer. Upon doing
``loaddate all-2018-01-12.json`` it didn't work, as dumpdata of the whole thing usually hasn't worked. This is what did
work::

    On the home computer:
    python manage.py dumpdata auth.user activity > user-activity-2018-01-12.json

    On the rectory computer:
    python manage.py loaddata user-activity-2018-01-12.json

Doing ``runserver`` and checking out the local website everything seemed to be as I left it last night on the home
computer.

Cosmetic Fixes
--------------

I have noticed, at least on some computers, that the Holy Spirit image I'm using for a logo sometimes flashes full-size
before the website settles down. I think this may be caused because the image being used is quite large and is being
reduced to a much smaller size (width = two columns, or 1/6, of a 960 pixel container? = 160 pixels. Using Gimp to
create a HolySpiritLogo.png with width=160 pixels might help. It didn't seem to hurt, but I wasn't experiencing that
problem on this machine. Time will tell.

I would also like the website to have a "favicon" so I created a 32 x 32 pixel one in Gimp. Checking
*The HTML PocketGuide* I learned that it could be included either by having it at the root of my website (Boo!) or
using the following link in the header::

    <link rel="shortcut icon" href="{% static 'images/favicon.ico' %}" type="image/x-icon" />

After putting that into my ``base.html`` file the website now has a favicon!

Finally, I didn't like the color of the text on the welcome page so I changed it to #2eb873 by setting that in the
activity_text selector in custom.css. I'm not sure I like that one either but it's a start.
