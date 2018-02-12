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

Designing the Models
--------------------

My previous attempt at building *ConfirmationWebsite* used an Action model which was connected to an activity but it
was a little confused as to what it was. It had a ``type`` field with choices as to which page it was but I'm not sure
how multiple choice and true false questions would fit in. Perhaps the ``text`` field could contain the question while
a separate ``Choice`` model would connect to possible responses.

Here I will try to list the sorts of pages described in the planning document and the data that each one will need. That
may help me come up with a more clear model design.

Cover Page
**********

The cover page will need to display an overview of the activity and a list of pages for the activity. It has to know
which activity it belongs to and which user is accessing it at the moment. Control buttons allow the user to Begin (or
continue) the activity, or return to the Welcome Page. The Cover Page is much like a welcome page for the individual
activities.

Essay Page
**********

The esay page will allow the user to write out his or her answer to a question. It must display the question and contain
a place to store the answer. It must know to which activity is belongs. It displays Previous and Next buttons at the
bottom but the previous button is deactivated for the first page and the next button is deactivated until they have
completed the current page. This function for the previous and next buttons is the same for all the following pages.

Multiple Choice Page
********************

The multiple choice page displays the question and several possible answers with radio buttons from which the user is to
select one choice. It is connected to an activity but will have to search for the choices that pertain to the current
question on its own.  Previous and next buttons function as described above.

True/False Page
***************

The true/false page is a multiple choice page with only two choices: True, and False. The page arranges to have the
True choice always come first. It is connected to an activity but will only need to know whether the correct response is
True or False. Previous and next buttons function as described above.

Discussion Page
***************

The discussion page displays the current question plus all of the responses that have been given so far in the order in
which they were given. An "Add Comment" button is available for the user to add to the discussion. An Edit link appears
next to each comment made by the current user. Previous and next buttons function as described above.

Model Design
------------

The above suggests that it may be useful to expand the Activity model to include the information needed for the Cover
Page and create a Page model to connect to the Activity. The Page model could contain a choice field indicating what
sort of page it is and could be the one various other models connect to:  such as a Choice model, an Essay model and
a Discussion model.

This still doesn't feel right though. I need to think about it some more.

Imagining Template Creation
---------------------------

Perhaps if I imagine myself creating the templates, all of the CUD (Create, Update, Delete) templates, I will get a
better idea of what features are needed in the models. I will have a go again at all of the various page types:

Cover Page
**********

Displaying the Cover Page
+++++++++++++++++++++++++

At the top there will be some kind of information box that tells the user what the activity is about and tries to give
him or her some motivation for completing it.

Beneath that is a list of the various pages of the activity. The ones that are not currently open to the user are grayed
out, the ones already completed have a check mark next to them and can be clicked so that they can see and possibly edit
their responses. (Only essay answers can be edited.) The next one in line to be completed and, possibly, open discussion
pages are active links to go to those pages.  Beneath all of that is a button that says either "Begin" or "Continue"
depending on whether the user has previously begun this activity.

To display the cover page I will need:

*   The activity name (from the Activity model)
*   A list of the activity's pages (gathered from the Page model)
*   A list of the pages in this activity that the user has completed (gathered from the Response model)

Creating the Information on the Cover Page
++++++++++++++++++++++++++++++++++++++++++

Part of this is done by the administrator, or possibly by staff members, when an activity is created. Creating an
activity will involve creating the various kinds of pages for that activity.

The rest of it is done as the user completes pages of the activities. A record is kept referencing the user, the
activity and the page just completed.  Also, for at least some of the pages, a record is made of the user's answer. This
could be an essay, a discussion post, a multiple choice or a true/false answer. It seems best to try to combine all of
them into one with different types of answer slots available.

Here is a list of what I think I will need in this Response model:

*   The activity
*   The page
*   The user (who could be the AnonymousUser)
*   A large text field to hold essay and discussion responses
*   A small text field to hold Multiple Choice or True/False answers
*   A boolean field to indicate whether their answer was correct (for multiple choice and true/false pages)
*   A time/date stamp for discussion responses to keep them in order

This is also suggesting pages that are only available to the administrator and to the staff members (adult
facilitators). I will design them separately when I finish the candidate pages.

Updating the Information on the Cover Page
++++++++++++++++++++++++++++++++++++++++++

This will be updated either when the administrator/staff members update the contents or structure of the activities or
when a user updates his or her responses.

Deleting the Information on the Cover Page
++++++++++++++++++++++++++++++++++++++++++

This will be deleted when an activity itself is deleted. But what should I do if the activity has already been used? Can
I make activities invisible but keep them intact in the database? I will have to think about this. It seems like a good
idea to archive previous contents of the website for each group and only "delete" it when a new group starts. It would
also be good not to have to reproduce all of the activities and pages for subsequent groups. I will have to think about
how to do this. Perhaps it could involve putting the activities into groups and displaying only the current set, or
sets, of activities. Maybe I would have to have groups of groups, one for each Confirmation class. This raises a lot of
questions but I want to focus on the candidate version of the site for now.

Essay Page
**********

Displaying the Essay Page
+++++++++++++++++++++++++

The page will have the name of the activity, the page number (or some better name for it than that) and the question to
be answered or the statement to be commented upon. There will be a text area available for the answer, with the
insertion point already in it, and a submit button underneath. The Previous and Next buttons will show and be activated
if the user can go backward or forward. Upon clicking the Submit button the candidate is shown a non-editable version of
their response with an Edit button at the bottom of it.

To display the Essay Page I will need:

*   the Activity
*   the page number (Part 1, Part 2, etc.?)
*   a list of this user's responses to the parts of this activity.

Creating the Information on the Essay Page
++++++++++++++++++++++++++++++++++++++++++

The question or statement to spur the written response will be supplied by the administrator or staff member when the
activity is created or edited to include the page.

The user's response will be created when he or she clicks the Submit button.

Updating the Information on the Essay Page
++++++++++++++++++++++++++++++++++++++++++

The question or statement will be updated through the Activity update process.

A user can update his or her response by returning to the page. If he or she deletes the response completely that
that response is removed from the database and he or she no longer gets credit for it. The actions of the Previous
and Next buttons are modified accordingly. I'll have to think about whether he or she can get to later pages already
completed.

Deleting the Information on the Essay Page
++++++++++++++++++++++++++++++++++++++++++

During the development of the activity the page can be deleted through the Activity update process or the Activity
delete process. If there are already responses to that page they would be orphaned and so perhaps it would be better
simply to make the page inactive instead of deleting it completely.

A candidate can delete his or her response by clicking on the Edit button on the non-editable version of the Essay Page
and then selecting Delete. The non-editable version of the Essay Page shows the same information as before but their
response is placed under the question or statement instead of in an editing box. There is an Edit button at the bottom
of the page along with the Previous and Next buttons.

What I Learned from Thinking about the Essay Page
+++++++++++++++++++++++++++++++++++++++++++++++++

I learned that each response page will have to have another, non-editable version also with Previous and Next buttons
but also an Edit button to take the user to an editable version of the page.

Multiple Choice Page
********************

Displaying the Multiple Choice Page
+++++++++++++++++++++++++++++++++++

Entry
^^^^^

The version of the Multiple Choice Page that allows candidates to enter information will display the Activity Name, the
page or step number, the question being asked and the possible choices for answers, as many of them as there are. The
choices will be labeled with capital letters and each one will have a radio button associated with it. None of the radio
buttons are selected when they first enter the page. There is a Submit button underneath the choices and Previous and
Next buttons activated as appropriate. the Submit button is grayed out and inactive until the user selects one of the
choices. After the user clicks Submit, the Display version of the page appears.

Display
^^^^^^^

The Review form of the page displays the Activity Name, the page or step number, the question being asked and the
possible choices for answers with the user's selection highlighted in some manner (color, weight, style of font?). Some
questions may display the correct answer along with the user's answer and tell them whether they are right or wrong.
There may be an explanation of the correct answer included which may also explain why the others were incorrect. If an
answer is given the user will not be allowed to edit their answer. Otherwise, an Edit button will be on the page which
does give the user that ability. Previous and Next buttons appear as usual.

It seems that I have not yet written down any plans for the Activity model or the Page model. I think I am ready to do
this now.

Here are my current thoughts about the Activity model:

*   an integer index number for use in ordering the list of activities
*   the activity name
*   the slug for the activity
*   overview text for the activity
*   publish date for the activity (date on which it begins to appear on the website)
*   closing date for the activity (date on which it ceases to appear on the website)

Here are my current thoughts about the Page model (which used to be called the Action model - perhaps a good name):

*   the associated activity
*   an integer for use in ordering the list of actions
*   the type of action: essay, multiple choice, true/false, discussion, opinion poll
*   a text field to hold the question, statement or discussion point
*   an image field connecting to an image to be displayed on the page
*   a boolean to indicate whether the action is to be timed
*   an optional text field giving an explanation of the correct answer for those that have correct answers
*   a boolean indicating whether an answer is given after a user's response which tells whether the user can change it.
*   a boolean to indicate whether this page is currently active (so used pages can be made inactive instead of deleted?)
*   a boolean for True/False questions that have a definite answer (as opposed to poll questions)
*   a boolean to tell whether the discussion is public or anonymous

There will also have to be a Choice model to contain the possible multiple choice answers:

*   the action or question with which this choice is associated
*   a field to order the list of choices (either starting as, or converted to, a letter)
*   a text field containing the text of the choice
*   a boolean field indicating whether this answer is the correct one

Updating the Information on the Multiple Choice Page
++++++++++++++++++++++++++++++++++++++++++++++++++++

The questions and choices can be updated by the administrator or staff members through the Activity update process.

If a candidate wants to update their response they may do so only on those responses where answers have not already
been given.

Deleting the Information on the Multiple Choice Page
++++++++++++++++++++++++++++++++++++++++++++++++++++

The questions and choices can be deleted by the administrator or staff members through th Activity update process
during development or may be made inactive through the Activity update process.

The user is only permitted to delete their response on questions that do not give an answer. (poll questions?)

True/False Page
***************

Displaying the True/False Page
++++++++++++++++++++++++++++++

Entry
^^^^^

The page that allows candidates to respond to True/False questions will display the activity name, the current page,
part or action number, the statement to which they are to respond and radio buttons for their selection of either True
or False. True will always appear on top. Underneath this area will be a Submit button and the Previous and Next buttons
which operate in the usual way.

Display
^^^^^^^

The display page shows the activity name, the current page, part or action number, the statement to which the user
responded and the response given, either True or False. The correct answer and an optional explanation may also appear.
If the answer does not appear, there is an Edit button that allows them to change their response. The Previous and Next
buttons work as usual.

If there needs to be a separate model for True/False questions here is an idea for it:

*   the activity
*   the page, part or action number
*   the statement text
*   a boolean with the correct answer

Updating the Information on the True/False Page
+++++++++++++++++++++++++++++++++++++++++++++++

The statements and correct answer can be updated by the administrator and possibly one or more staff members in the
Activity editing process.

A candidate may be able to change their answer if the answer was not already given.

Deleting the Information on the True/False Page
+++++++++++++++++++++++++++++++++++++++++++++++

A true/false question can be deleted by the administrator or staff members through th Activity update process during
development or may be made inactive through the Activity update process if the page already has responses.

The user is only permitted to delete their response on questions that do not give an answer. (poll questions?)

Discussion Page
***************

Displaying the Discussion Page
++++++++++++++++++++++++++++++

Entry
^^^^^

When a candidate comes to the discussion page he or she sees the Activity name, the page or action number and the
question or statement forming the discussion point. Underneath that, in the order in which they were added, comes the
entries that were made to the discussion so far. Each one may or may not have the name of the contributor depending on
the nature of the discussion, open or anonymous. If the discussion is open (or public) any responses this user
contributed have an edit link next to them. At the bottom is an "Add Comment" button if they want to add to the
discussion. When he or she clicks it a text box appears on the page for entering the comment. The same box appears,
filled, if they click the Edit link next to an earlier comment he or she made. Previous and Next buttons appear as
usual.

Currently I am thinking the discussion comments can be handled by the Response model but I may have to rethink that. I
keep thinking about what I've read about the design of Django apps: that they should do one thing and do it well. Does
this suggest that I have separate apps for each kind of page? Will this change the Page model giving it a link to
whatever model in a different app is needed. I will have to consider this possibility. One advantage is that these apps
may be reusable in other programs that involve various kinds of quizzes. Like the trivia app in Christmas2017, or the
polls app in the Django tutorial. Hmm...

Display
^^^^^^^

There is no separate Display version of this page since everything is displayed and entered on the same page described
above.

Updating the Information on the Discussion Page
+++++++++++++++++++++++++++++++++++++++++++++++

The administrator or a staff member can edit the discussion question or statement during the creation or editing of an
activity. Or later if it seems prudent. An administrator or staff member can also remove inappropriate comments made by
candidates or hide the whole page if that becomes necessary.

Deleting the Information on the Discussion Page
+++++++++++++++++++++++++++++++++++++++++++++++

An administrator or staff member can delete a discussion page before it is published or make it invisible once it has
already begun.

Poll Pages
**********

Actually there are several poll pages, one for each page type except perhaps for the discussion page. Thus the
creation, updating and deleting of poll information will be the same as for the corresponding page type. I just may
have to come up with a boolean flag indicating whether the item is a poll or not.

Thinking about the Design
-------------------------

Okay, should I use several apps or try to do it all with the activity app? As noted above, having several apps keeps to
the idea of having an app do just one thing and do it well and may simplify some things about the model design too. I'm
thinking that the Page model is too complicated with ten different fields, some of them being used only for particular
versions of a page. Although, come to think of it, it's only the boolean for True/False questions indicating the correct
answer, that

On the other hand, it isn't clear to me how the page model would connect to the models in the various apps. Perhaps they
would connect to the page model.

It seems the purpose of the page model is to give me a way to list the various actions for an activity and keep track
of things for the Previous and Next buttons. I don't see how this could easily be done without having one place to go to
list them all and present them all.

Model Design
------------

So here is a start to the model design using just one activity app:

.. csv-table:: **Activity Model**
    :header: Field, Type, Attributes, Comments
    :widths: auto

    index, PositiveSmallIntegerField, unique=True
    name, CharField, max_length=40
    slug, SlugField, max_length=15; unique=True; db_index=True?, docs say "Implies setting Field.db_index to True"
    overview, CharField, max_length=512
    publish_date, DateField,,date on which it begins to appear
    closing_date, DateField,,date on which it ceases to appear
    visible, BooleanField, default=False, default is false so that it will not appear until publish_date

|

.. _page_model:

.. csv-table:: **Page Model**
    :header: Field, Type, Attributes, Comments
    :widths: auto

    activity, ForeignKey, Activity; on_delete=models.CASCADE
    index, PositiveSmallIntegerField,, unique with activity
    page_type, CharField, max_length=20; choices=Instructions; Essay; MultiChoice; True/False; Discussion
    text, CharField, max_length=512, for the question; statement or discussion point
    image, ForeignKey, Image; on_delete=models.CASCADE; blank=True, keyed to the image, if any, to display on the page
    explanation, CharField, max_length=512; blank=True, optional explanation for correct answer
    opinion, BooleanField, default=False, indicates whether MultiChoice or True/False questions have a correct answer
    reveal_answer, BooleanField, blank=True, indicates whether an answer is given after the user responds
    visible, BooleanField, default=True, indicates whether the page will be visible
    tf_answer, BooleanField, blank=True, indicates the correct answer to a True/False question
    open, BooleanField, default=True, indicates whether a discussion or poll is open or anonymous

activity and index are unique together.

Note: I did not include the timed BooleanField I had considered before for keeping track of how long it takes the user
to complete a page. I wondered whether I really have much cause to do that. I also wondered if a different use might be
a good idea: to limit the time a user can spend on certain pages, but I don't know how to implement that.

I added the Instruction page_type later. :ref:`See below.<instruction_page_idea>`

.. csv-table:: **Response Model**
    :header: Field, Type, Attributes, Comments
    :widths: auto

    user, ForeignKey, User; on_delete=models.CASCADE, could be the AnonymousUser
    activity, ForeignKey, Activity; on_delete=models.CASCADE
    page, ForeignKey, Page; on_delete=models.CASCADE
    time_stamp, DateTimeField, auto_now_add=True, date/time stamp for when the response was created
    last_edited, DateTimeField, auto_now=True, date/time stamp for the last edit
    essay, TextField, blank=True, contains responses to essay and discussion pages
    multi_choice, CharField, max_length=1; blank=True, the user's response to multi-choice questions
    true_false, BooleanField, blank=True, the user's response to true/false questions
    correct, BooleanField, blank=True, whether the user's response was correct

user, activity and page are unique together

.. csv-table:: **Choice Model**
    :header: Field, Type, Attributes, Comments
    :widths: auto

    page, ForeignKey, Page; on_delete=models.CASCADE
    index, PositiveSmallIntegerField,
    text, CharField, max_length=256
    correct, BooleanField, blank=True, indicates this choice is correct (if has_correct is True in Page model).

page and index are unique together

No more than one choice of a set may be marked as correct.

.. csv-table:: **Image Model**
    :header: Field, Type, Attributes, Comments
    :widths: auto

    filename, CharField, max_length=30, the filename as it appears in the page_images folder in the static directory
    category, CharField, max_length=20, the category that can be used to create tabbed pages of similar images

Adjusting the Database to the new Models
----------------------------------------

Here is the plan:

*   use the admin to erase all entries except for the User model
*   do a makemigrations
*   do a migrate

That didn't work. Since I had already created the models, the admin program would not let me into the existing Activity
model to change anything. I had to do it as follows:

*   do a makemigrations and fill in the ``closing_date`` and ``publish_date`` fields with ``timezone.now``
*   do a migrate
*   the admin app can now be used to remove existing information if you so desire, or add new model contents

This is how it was done on my home computer. Once I add new information to the database I will have to transfer
to my other computers as follows. First, on the computer that is most current:

*   use dumpdata auth.user, activity > <date>user_activity.json to create a fixture on the most current computer
*   add that fixture to git and do a commit
*   do a git push

Then, on the computer being transferred to:

*   do a git pull
*   do a makemigrations filling in ``closing_date`` and ``publish_date`` with ``timezone.now`` as above
*   do a migrate
*   do a loaddata <date>user_activity.json to read the information into the database

.. _url_plan:

The URL Patterns
----------------

Here are the URL Patterns I developed while :ref:`putting the pages together<building_pages>`. I used my previous work
on confirmation17 as a starter.

.. csv-table:: **URL Patterns**
    :header: URL, Page(s) Addressed, Views/Redirects, Notes
    :widths: auto

    /, , RedirectView to user.login
    user/, , RedirectView to user.login
    user/login/, login.html, auth_views.LoginView
    user/logout/, registration/logout.html, auth_views.LogoutView
    activity/, , RedirectView to /activity/welcome/
    activity/welcome/, welcome.html, WelcomeView
    activity/<slug>/summary/, summary.html, SummaryView
    activity/<slug>/n/, <page-type>.html, PageView, PageView selects the final view depending on the page-type


Adding Groups
-------------

I decided to leave the current acitivities: "Noah: The REAL Story" and "God? Are you there?" and begin working on pages
to display them and create, edit and delete them. I decided to add two or three phony users to the User model so that it
will now contain:

*   Jim as the superuser/administrator
*   Sylvia as the Supervisor/administrator, password: svd12345
*   Fred as a Team member, password frf12345
*   Diego as a Candidate, password: dfd12345
*   Susan as a Candidate, password: sfs12345

Before I do this I will have to re-study using Django groups.

Planning the Groups
*******************

According to https://docs.djangoproject.com/en/2.0/topics/auth/default/ beyond just permissions, I can use groups to
categorize users and develop code myself that gives them access to various parts of the site. With this in mind I'm
thinking of the following new groups:

*   Candidate, which gives access to the published activities and allows them to enter and edit their own answers
*   Team, which allows access to that,  to pages displaying their candidates' progress and to activity development pages
*   Supervisor, which allows access to all that and allows the setting of publish and closing dates
*   Administrator, the superusers, who have access to everything

Creating the Groups
*******************

As an experiment I used the admin to add the groups as follows:

*   Candidate: no permissions for anything, test later to see if that prevents them from adding responses
*   Team: no permissions for anything, test later to see if they can access things through the website if not the admin
*   Supervisor: no permissions but I gave Sylvia staff status when I created her User information
*   Administrator: no permissions but I put myself into the Administrator group

In order to fully experiment with these groups I will have to create some actual pages to interact with and see if the
right people can do the right things. Now, however all I can do is check to see if the right people can login and, once
they do, whether they have access to the admin site.

.. csv-table:: **Test for Access to admin App**
    :header: User, Expected Access, Actual Access, Notes
    :widths: auto

    Jim, Yes, Yes, Has access to Groups
    Sylvia, Yes, Yes, Cannot access Groups
    Fred, No, No, Invited him to login under a different account
    Susan, No, No, Invited her to login under a different account
    Diego, No, No, Invited him to login under a different account

.. Note::

    When trying to copy my new users to the rectory computer I first had to add the groups through the admin program in the
    order listed above:  Candidate, Team, Supervisor, Administrator. Then the loaddata worked.

.. _building_pages:

The Tedious Work of Adding Pages
--------------------------------

Plan for the Initial Pages
**************************

Starting with the page for creating activities would be just too complicated so I have decided to create them via the
admin app for now. If I work on the Welcome page that will require using the admin app to fake some user responses too.
Then, one by one, I can create the display version of each page, followed by the entry version of each page.

.. _instruction_page_idea:

In thinking about all this I may have discovered the need for another page. Some pages simply give instructions to
do something and then come back when finished. I will have to add that page type to the Page model then do another
makemigrations and migrate. That seems best to do before actually adding any pages.

I just added: ``('IN', 'Instructions'),`` to the choice field in the Page model. I added it to the Page Model table
:ref:`above<page_model>` too just for completeness. I did the ``makemigrations`` and the ``migrate`` and added the
migrations file to git without incident.

Here is a plan for testing the initial pages:

*   Add an Instruction page to the Noah activity
*   Design and implement a URL pattern for a page summarizing an activity
*   Modify the Welcome page so that the list of activity names becomes a list of links to the summary page.
*   Build a summary.html page and test the Noah link.
*   Build an instruction.html page, get it looking good, and see that you get to it from the summary page link
*   Build a congrats.html page, get it looking good.
*   Sign in as Susan and "complete" the first Noah Activity page. See that you get to the congrats page.
*   Sign in as Diego and go to the Noah activity. Do not complete the activity.
*   Add an Essay page to the Noah activity.
*   Modify the Welcome page so that the number of pages for each activity is visible.
*   Modify the Welcome page so that the number of pages the current user has completed is visible.
*   Check this for Susan and Diego.
*   Build an essay.html page, get it looking good, see that you get to it from the Next button for Susan but not Diego.
*   Check to see that the Previous button brings Susan back to the essay page but without the "Finished" button

That should be more than enough to do for now!

Adding an Instruction page to the Noah activity
***********************************************

I had forgotten to register the new models in the activity app's admin.py program but, after doing so, and refreshing
``localhost:8000/admin/`` a couple of times, they all appeared.

In the admin app I was able to add the instruction page without difficulty.

Putting Links on the Welcome Page
*********************************

Each Welcome Page link should link the user to an activity's summary page which will be at:

``<activity-slug>/summary/``

but that reminds me that I have not yet included a plan for the url patterns. I will create it so that it appears
:ref:`before this section<url_plan>`.

Things Discovered
*****************

Actually, the welcome page needs to link to a page that summarizes the activity and the pages it has available. Also,
the welcome page is supposed to report on such things as how many pages an activity has and how many the user has
completed. This seems to call for a table with the headings:

Activities, Pages Available, Pages Completed, Finished?

or some such thing.

I will have to do some more study on Django's ORM to figure out how to best do this.

In working on the summary page I decided to add a ``title`` field to the Page model. The title will appear as the link
to that page on the summary page.

Welcome Page Revisited
**********************

The Welcome Page is supposed to :ref:`display the user's progress<progress_display>`. That seems more difficult to
implement than I thought it would be.

The idea was that, while listing the available activities, the template would also list the current user's status on
each of the activities, that is, whether they can Start that activity, or if they are a certain percentage of the way
through that activity, or if they have completed that activity. (Another possibility is that the activity doesn't have
any pages for it yet and is NOT ready to be accessed.)

To access and count the current user's responses to all of the pages of the activity currently being listed was a bit
too much to handle with template logic so I put it into the WelcomeView::

    def get(self, request):
        activities = Activity.objects.all()
        user_stats = {}
        for activity in activities:
            pages = Page.objects.filter(activity=activity)
            page_count = len(pages)
            completed = len(Response.objects.filter(user=request.user, activity=activity))
            if page_count != 0:
                user_stats[activity.slug] = completed/page_count * 100
            else:
                user_stats[activity.slug] = -1

        return render(request, self.template_name, {'activities':activities, 'stats':user_stats})

It creates a dictionary which it sends in the context named stats. The keys in the dictionary are the corresponding
activities slugs, the values are the percentage the current user has completed or -1 if there are no pages to the
acivity yet.

It took me quite a while to figure out how to access this information in the welcome.html template because the construct
I thought would work: ``stats.activity.slug`` to pick out stats[activity.slug] did not work. Finally I got this to
work::

    <table class="u-full-width">
        {% for activity in activities %}
            <tr>
                <td>
                    <a class="no-underline" href="/activity/{{ activity.slug }}/summary/">
                        {{ activity.index }}. {{ activity }}
                    </a>
                </td>
                <td>
                    {% for key, value in stats.items %}
                        {% if key == activity.slug %}
                            {{ value }}
                        {% endif %}
                    {% endfor %}
                </td>
            </tr>
        {% endfor %}
    </table>

but this seems to violate the Django ideal of keeping logic out of templates as much as possible. They do suggest using
a custom template tag for things like this so I will study up on it.

.. index:: custom template tags

.. _custom_template_tags:

Custom Template Tags
++++++++++++++++++++

Whoa! The material at https://docs.djangoproject.com/en/2.0/ref/templates/api/ seems way beyond my abilities. I searched
for Custom Template Tags and got https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/ . This seems to be
written a bit more in my language.

Outline of Learnings:

*   the custom template tags should be in the app in which they are to be used
*   they should be contained in a ``templatetags`` directory within that app
*   the ``templatetags`` directory should be a python package so include a blank __init__.py file
*   the development server will have to be restarted after adding the ``templatetags`` module
*   if my custom template tags are in ``activity_extras`` templates using them need a {% load activity_extras %} tag
*   my tag library will need a module-level variable named ``register``, an instance of ``template.Library()``

I just tried it and... IT WORKED!!! And it wasn't all that difficult. Here is the entire ``activity_extras.py`` file::

    from django import template
    from ..models import Activity, Page, Response

    register = template.Library()

    @register.simple_tag
    def activity_stats(stats, slug):
        return stats[slug]

That allowed me to simplify the pertinent line in welcome.html to ``{% activity_stats stats activity.slug %}`` and it
replaced the five line for-loop I was using before.

I think I'll keep the calculation of the stats in the view or else I would have to add a rather large list of arguments:
user, activity, page, response. This seems simpler.

As it turns out, I didn't really need to use a custom template tag here.
(:ref:`See below<no_need_for_custom_template_tag>`.)

Visibility of Activities
++++++++++++++++++++++++

There was also supposed to be a check as to whether the activity was to be published yet and/or if it was marked as
visible. My current version of the Welcome page doesn't check for such things. I will consider here how to go about
doing that.


Improving the User's Activity Status Information
++++++++++++++++++++++++++++++++++++++++++++++++

Both the information supplied and the appearance need to be improved.

The information was best supplied by the view. I included the "Ready to Start", "xx.x% Completed", "Finished" and "Not
Yet Ready" messages in the ``stats`` dictionary supplied by the ``WelcomeView``.

For now I am opting for the sea-green color ``#2eb873`` for all of the text in the TOPICS box. The link text is further
modified by the ``link-list`` class which makes it bold face. The file skeleton.css supplies an aqua-blue color when
the mouse hovers over the link.

Adding Links to the Summary Page
********************************

The summary page currently only shows a list of pages and no way to get to those pages.

Here is my sequence of implementation:

*   make the list into a table
*   make the page names into links
*   add the progress information
*   activate or deactivate the links according to the progress information
*   make it all look good

.. _no_need_for_custom_template_tag:

I discovered that, since the {% for %} template tag can read in a list of lists, as in {% for x,y in points %}, I can
use the WelcomeView and SummaryView to pack up a data list with tuples like (activity, msg) and (page, progress) and
send that list to the welcome.html and summary.html templates. Thus, I don't need to use a custom template tag as
:ref:`described above<custom_template_tags>`.

I decided to use buttons as a means to getting to the pages instead of using the page titles as links. I override
skeleton.css' ``.button`` class by changing the color and border color and also the ``.button:hover`` class to reverse
the colors when the mouse hovers over a button. I notice that when I return to the page after an error (since I don't
have the actual page views or urls or templates implemented yet) the colors revert to black until I do a refresh. I
don't know if this is a problem that will show up in production however so I choose not to try to do anything about it.

I realize that I'm not naming things well. Currently the list of pages is called "Acivities" and the list of activities
on the Welcome page is called "Topics." I think I will change the heading on the Welcome page to say "Activities" and
the heading on the summary page to say "Pages." Perhaps later I will come up with a better, more inviting and/or more
descriptive, heading than "Pages." (For now I'm going with "Things to Do."

Improving the Welcome Page Again
********************************

I wanted to have the Welcome page and the Summary page have a similar look and feel so I had to change from using
activity names as links to using buttons as links. It was a little simpler here since only the caption of the buttons
had to change, but I also had to change the WelcomeView to use a data list. I got it to working fairly quickly.

I think the Summary page needs a link or a button at the bottom to return to the welcome page. I will make it a link so
as not to make it too prominent.

As it turned out, using a button made it look better. It was easier to center a button than the text of the link and
there is enough of a separation between the table and the Return to Welcome Page button to make it seem right.

Implementing the Instruction Page
*********************************

Here I envision as the steps leading to implementing the Instruction Page:

*   create the url to reach any of the pages
*   create a PageView to select between pages
*   figure out how each page method can send the right values to it's pages (via the context dictionary)
*   create the instruction.html stub page - see that it displays
*   get the instructions to display
*   add a Start Activity button and see that it gets to the post method
*   see to it that the Start button's post method records the start time and returns to this instruction page (X)
*   add a Finished Activity button that appears after the Start Activity button is clicked (X)
*   see to it that Finished button's post method records finish time and marks activity as complete (X)
*   make returning to a completed and timed instruction page display the time it took (X)
*   make returning to a completed but untimed instruction page simply display a "Finished" message of some kind
*   make the Instruction page look good
*   add the Previous and Next buttons

Timing the Instruction Page
+++++++++++++++++++++++++++

I need to think through how timed pages are supposed to work. The timing needs to be started when the candidate first
enters the page. That means within the 'get' part of the view however much it goes against the grain. Then, since I
would like to avoid false measurements as much as possible, I would need to give careful instructions on leaving the
page and then re-entering it when finished. But that might seem to the candidates to deprive them of another look at the
instructions.

Another idea is to start with a "Start Timer" button which, when they click it, posts their starting time and returns
them to the same page which now displays a "Stop Timer" button. I would still have to give careful instructions. Perhaps
like the following::

    With the Start Timer button showing:

    This is a timed activity. Click the 'Start Timer' button below when you are ready to start.

    With the Stop Timer button showing:

    You can complete the activity with this instruction page showing or leave this page, or the whole website, while you
    finish it. The "Stop Timer" button will show whenever you come to this page until you click it. Click it when you
    have finished the instructions above.

On the other hand, this whole thing might be more trouble than it's worth. There are too many ways for it to go wrong
and little benefit to having the information anyway. I think I will not implement this feature.

Adding the Previous and Next Buttons
++++++++++++++++++++++++++++++++++++

Since these are to appear on every page it makes sense to implement them once, in a file called nav_buttons.html and
include them at the bottom of every page.

Also, it is probably easier, and more in keeping with Django philosophy, to determine the availability of the previous
and next buttons to a particular user in the model method rather than gumming up the template too much.

No, the model methods are good for determining whether previous or next pages are available, but determining whether a
particular user can view them or not is best left to the view. I will implement that after I get more pages.

Then again, I don't want the Next button appearing if the candidate can't actually get to that page. Hmm... I'll have to
re-think it again. (Is the current user available from the model? I think it is.)

Implementing the Essay Page
***************************

The steps I envision are as follows:

*   move the context formation into the body of the view
*   add what happens when an ES page comes to the get method
*   create the essay.html page stub and see that it displays
*   fill out the entry version of the essay.html page
*   add what happens when an ES page comes to the post method
*   check to see if the previous and next buttons are operating correctly
*   figure out how a candidate can edit his or her responses

.. index:: Problems; textarea input spaces

Fixing Problem with Extra Spaces in Input
+++++++++++++++++++++++++++++++++++++++++

The essay text entered through the ``<textarea>`` tag was picking up extra spaces. I could get them out of the database
entry by using ``essay=request.POST[essay].strip()`` in the post method of the PageView but they were creeping in again
when returning to the page. I discovered they were being picked up as the spaces between the ``<textarea>`` open and
close tags ``</textarea>``. When I got rid of those spaces by using::

    <form action="{% url 'page' activity.slug page.index %}" method="post">
        {% csrf_token %}
        {% with essay=response.essay %}
            <textarea class="u-full-width text-field" name="essay" autofocus>{{ essay }}</textarea>
            <input class="offset-by-four four columns button-primary" value="Submit" type="submit"/>
        {% endwith %}
    </form>

the extra spaces disappeared from the ``<textarea>`` when displayed with a pre-existing entry.

Rethinking the Essay Page
+++++++++++++++++++++++++

So far the entry version of the page and the edit version of the page look identical, and there is no delete version of
the page. I kind of like the idea of at least a similar look to the pages but the post method has to know if it is
supposed to create, or edit, or delete an entry. I suppose I could simply display the user's response in <p> tags,
then replace the Submit button with Edit and Delete buttons which bring the user to a new page in each case, or a
different version of the same page.

Could I, instead, just change the mode of the existing page, or change the results by adjusting the href of the buttons
(both in <a> tags)? Can I use <a> tag buttons in a <form> with its action already set? I think I need to study what I
did for the Christmas website.

Also, it might sometimes be nice for the users to see other people's responses after they have made their own response.
In that case, should they be allowed to edit their response?

I just realized that, as currently designed, the Response model is capable of handling a "discussion" because the same
user can make several entries for the same activity and page number. Thus I need to prevent users from changing their
responses to essay questions except in a very controlled way. Thus I have opted to display an uneditable version of
their essay response on the essay page after they have responded and give them an Edit button, or Edit and Delete
buttons to handle those operations. I think I will need new URLs for those circumstances perhaps::

    <activity-slug>/<page-index>/edit/
    <activity-slug>/<page-index>/delete/

Making a Shared page.html
*************************

It occurs to me that each page should have a simple way to get back to the summary page if they should so desire, or
maybe it should be a simple way to get back to the welcome page.

This looks more and more as if I need to implement a ``page.html`` that can be shared by all of the various kinds of
pages files. It should work like ``base.html`` works for all of the pages of the website but that works when the other
website pages "extend" ``base.html`` but since the activity pages already extend ``base.htm.`` through such things as
``base_activity.html`` can I put another file into the mix. (I just tried adding a line to ``base_activity.html``
thinking it would display on all of the activity pages, but it did not. Time for more study of how that {% extends %}
tag works.

Ah! It seems from reading https://docs.djangoproject.com/en/2.0/ref/templates/language/#template-inheritance that my
``base_activity.html`` may have needed to include a {% block content %}{% endblock %} pair to have anything display.

That didn't work either. What DID work was to include a new {% block page-content %} in ``base_activity.html`` and then
replace the {% block content %} tags in the acivity page html files with {% block page-content %}. Now to move what is
common to all activity page files to ``base_activity.html``.

Editing and Deleting Responses on the Essay Page
************************************************

Though this went fairly easily, I did notice I was repeating a lot of code in the views. I think I need to study how
mixins work again.

.. index:: Mixins

.. index:: Problems; catching the DoesNotExist error

Mixins
++++++

I didn't use mixins in christmas17 so I studied the material at
https://docs.djangoproject.com/en/2.0/topics/class-based-views/mixins/ instead. The material there seems to focus more
on using generic class based views for everything and I don't think I want to do that. It does have a
JSONResponseMixin example, however, that seems to just supply a couple of methods that can be used by my views.

*Django Unleashed* seemed to concur so I created the following mixin::

    class PageMixin:

        """
        This mixin gets single responses from the Response model depending on the user, activity and page
        """

        def get_response_info(self, user=None, activity_slug=None, page_index=None):
            activity = Activity.objects.get(slug=activity_slug)
            page = Page.objects.get(activity=activity, index=page_index)
            try:
                response = Response.objects.get(user=user, activity=activity, page=page)
            except Response.DoesNotExist:
                response = None
            return activity, page, response

I included the try/except block with some difficulty. I took me a while to find out where the DoesNotExist error was
coming from. I thought I had to import it but it turns out it is part of the model itself so what I've shown above is
all that is necessary.

Now each of my Page views contains this line::

    activity, page, response = self.get_response_info(request.user, activity_slug, page_index)

instead of the three lines required before.

Editing Essays
++++++++++++++

It was easy to edit the essays. I created an essay_edit.html page containing a form very much like the one on the
essay.html page. The post method of the PageEdit view does the actual work.

Deleting Essays
+++++++++++++++

This would not be too difficult either but it could cause problems if a candidate deletes earlier parts of an activity.
What should it do? Delete it and everything after it? That doesn't seem right.

I think responses should only be deleted as long as the user has not gone any further. That will involve hiding the
Delete button in those cases and also making sure they can't accomplish deleting by entering
``activity/<activity_slug>/<page_index>/delete/`` by hand either. That will take some thought.

Making sure the Delete button and Next button don't show up when they are not supposed to was rather easy. I just wrote
some model methods in the Response model called ``can_goto_next`` and ``can_delete``. What surprises me is that, within
these methods I could not refer to the current response's page's index simply by writing ``self.page.index`` until I
created a model method in the Page model called ``get_page_index``. I just happened upon that name, I will try to change
it to see if something else would work as well...

Never mind! I CAN use ``self.page.index`` it's just that PyCharm doesn't seem to recognize it, or any of the other field
names.

Implementing the Multiple-Choice Page
*************************************

This ought to be fairly easy both because I have recently done something like this in the trivia app in christmas17 and
because much of the groundwork, such as the ``navigation.html`` page, the PageMixin and the changes in the
``base_activity.html`` file, has already been set in place. Here is what I think I should do:

*   Check to make sure questions and choices have already been created
*   Modify PageView's ``get`` method to include 'MC' pages
*   Create a stub ``multi_choice.html`` page
*   Add the question to the page
*   Add the possible responses to the page
*   Modify PageView's ``post`` method to include 'MC' pages
*   Make sure a user's responses are being recorded correctly
*   If an answer is to be given right away, make sure it is
*   If there is an explanation for the answer make sure it displays properly
*   Make sure an answer is NOT given when it is not supposed to be
*   Make sure Edit and Delete buttons appear only when the answer is not given
*   Create the Edit page
*   Make sure the Edit page works
*   Create the Delete page
*   Make sure the Delete page works

For testing purposes I just added a second multiple choice question -- this one not giving an explanation. I will have
to remember to create another fixture file to transfer the data.

Error Messages
++++++++++++++

I used what I did in the trivia acivity in christmas17 to try to get a box to appear around the error message and the
choices when the user did not select any choice but I couldn't get it to appear around anything more than just the error
message. I don't know why. Maybe something will occur to me overnight. Meanwhile I am just having the error message and
choices appear in red bold-face type. I still don't like the spacing of the error message however. (It looks better if
I put it in <p></p> tags.)

Recording the Response
++++++++++++++++++++++

When I do make a response it seems to record correctly but, currently, it just displays the same question and choices as
if giving the user another chance at it. I need to modify the ``get`` method in the 'MC' portion of the PageView, or
perhaps just the template. It's too late in the evening to think too clearly about it.

Displaying the User's Multiple Choice Response
++++++++++++++++++++++++++++++++++++++++++++++

There are two fields in the Page model that determine the appearance of the multi-choice page when a response has been
giveen:

*   A) ``page.reveal_answer`` - a boolean flag set to True if the answer is to be revealed
*   B) ``page.explanation`` - a character field with an explanation for the answer

*   If A is True and B is not empty, the user's answer displays with a correct or incorrect message with the explanation
*   if A is True and B is empty, the user's answer displays with a correct or incorrect message
*   If A is False, the user's answer is displayed with Edit and Delete buttons that allow for each action

To create and test this requires another change to the information in the database so that I have all three
possibilities represented.

.. index:: Problems; database migration

Database Changes
++++++++++++++++

In the process of getting the Edit function of the third type of page to work I had to change the field type of
the multi_choice field in the Response model to PositiveSmallIntegerField. After doing the ``makemigrations`` the
``migrate`` did not work complaining about how "" was an improper thing to be putting into an integer field. I had to
use the admin to delete ALL of my existing responses in the database to get ``migrate`` to work.

Later I tried that on my office computer and coldn't get into Responses in the admin program. It complained something
about "column activity_page.discussion_type does not exist..." I will try to do loaddata from the most recent fixture...

That didn't work either, and with a similar error message. Something seems to be wrong with the discussion_type field on
this computer. Let's see if I can get into the other models in the admin...

Activity: Yes
Choice: Yes (but it only has one set of choices)
Image: Yes
Page: No: "column activity_page.discussion_type does not exist"

Perhaps I need to use PGAdmin to see what's going on...

Once I finally got into PgAdmin4 I could see there was no discussion_type field in the activity_page table. Perhaps I
forgot to include one of the migrations in git...

Nope, it's there, ``0017_auto_20180201_1636.py`` from when I was at home last Thursday.

Perhaps I need to delete the whole database on this machine and then recreate it with ``migrate`` and ``loaddata``.

That almost worked. The only problem was that I don't have an up-to-date datadump from the auth.user app. I'll have
to create one tonight on the rectory computer.

Time for a commit and push...



Editing and Deleting Multi-Choice Responses
+++++++++++++++++++++++++++++++++++++++++++

This wasn't too difficult, except for the problem outlined above. It mostly just follows what I did for editing and
deleting essay responses.

Implementing the True/False Page
********************************

Here are my initial thoughts as to what needs to be done:

*   Check the database with admin and come up with a better subtitle for the page
*   Modify PageView's ``get`` method to include 'TF' pages
*   Create a stub ``true-false.html`` page
*   Add the question to the page
*   Add the possible responses to the page
*   Modify PageView's ``post`` method to include 'TF' pages
*   Make sure a user's responses are being recorded correctly
*   If an answer is to be given right away, make sure it is
*   If there is an explanation for the answer make sure it displays properly
*   Make sure an answer is NOT given when it is not supposed to be
*   Make sure Edit and Delete buttons appear only when the answer is not given
*   Create the Edit page
*   Make sure the Edit page works
*   Create the Delete page
*   Make sure the Delete page works

The plan is almost identical to the plan for Multi-Choice pages so I think I'll probably be doing a lot of copying --
especially since the True/False page is really just a special case of the Multi-Choice page.

.. index:: Problems; image next to column of text

Getting the Heading to look Good
++++++++++++++++++++++++++++++++

Because the subtitle I came up with for the true/false page was short: "Faith in Noah," it displayed NEXT to the main
heading instead of below it. I checked and found that other pages with short subtitles were doing the same. It seems I
should be able to put a <div> tag around the heading and subheading and another one around the image and have them
display properly. We'll see...

It wasn't that difficult implement. I just had to think it through carefully. Defining the problem as I did above
helped too I think. Here is the ``base_activity.html`` file::

    {% block content %}
        <div class="container">
            <div class="offset-by-two eight columns activity-text shadowed">
                <div class="row separator">
                    <div class="u-pull-left">
                        <p class="heading">
                            {{ activity }}
                        </p>
                        <p class="sub-heading">
                            {{ page.title }}
                        </p>
                    </div>
                    <div class="page-image">
                        <img src="{% static 'images/illustrations/' %}{{ activity.image }}" width="150" />
                    </div>
                </div>
                <div class="page-text row">
                    <p class="u-full-width">
                        {{ page.text }}
                    </p>
                </div>
                {% block page-content %}
                {% endblock %}
            </div>
        </div>
    {% endblock %}

Filling Out the True/False Page
+++++++++++++++++++++++++++++++

This should not be that difficult. I will be like multi-choice.html except the choice <input> tag(s) will be replaced by
two "hardwired" <input> tags with True and False as their values.

Editing and Deleting a True/False Page
++++++++++++++++++++++++++++++++++++++

Since editing a True/False response simply means to toggle the response from True to False or vice versa, I just took
care of toggling the user's response in the get method of the 'TF' section of the PageEdit view.

Deleting the response followed the usual pattern of asking them if they wanted to delete it and then click the Delete
button. But I realized that if they DIDN'T want to delete it, I gave them no way out. I need to put a Cancel button on
all of the delete pages and maybe the edit pages too.

That sounds like a job for tomorrow when I'm rested.

Adding a Cancel Button to the Delete Pages
++++++++++++++++++++++++++++++++++++++++++

*The HTML PocketGuide* (pp. 171-172) seems to indicate that the processing script gets both the ``name`` and the
``value`` of <input> tags of type submit.  So, if I include those in the form on my delete pages they should be
available for detection in my views. (I checked just to be sure, it does seem to need both of them to be set. If only
``value`` is set, nothing gets sent.

But it seems it may be useful to create a generic ``base_delete.html`` page that extends ``base_activity.html`` since
the delete pages are so much alike. I will look into this.

Yes, that is a good idea! It very much simplifies writing the individual delete pages.

Implementing the Discussion Page
********************************

Discussion pages allow a user to make more than one entry and display all of the entries from all of the users either
in forward or reverse order. I think the forward order will be best here.

When it comes to editing and deleting, each comment by the current user should be open for editing but not for deleting.
That, it seems to me, would break up the flow of the discussion. Perhaps edited comments should be prefixed with some
kind of indicator such as [Edited: <date>]

I can imagine discussions coming in three types:
*   Open discussions where each user's name displays next to his or her comment
*   Private(?) discussions where the user's name is recorded, editing works, but the name is not displayed
*   Secret discussions where the "AnonymousUser" is recorded as making all of the entries. Editing will not work.

For Private and Secret discussions the comments can be numbered for later reference. Perhaps that would be helpful for
Open discussions too. I suppose what I have here is a blog of sorts. Perhaps it merits its own app but, if so, I'm not
sure how I would integrate it into the page system I have already set up. I will have to think about this.

It also seems that some changes to the Page model are going to be necessary to indicate which kind of discussion we're
dealing with at any particular time.

As I think about it I suspect creating another app IS in order here. I've already done that in the ``comment`` app part
of the Christmas websites. The views of the app can still be called from the activity urls it seems to me but I can
look and see how it was done on the Christmas websites.

No, there was not a separate ``comment`` app on the Christmas websites, the comment capability was part of the ``gifts``
app. It was the ``question`` app that had the blog-like capabilities but one entered that through a link on the header
menu. Time for more study. Can one app's urls call another apps views? I don't see why not, they would just have to be
imported. Perhaps something like that was done in *Django Unleashed* for the website developed there.

Going to the book's GitHub repository ( https://github.com/jambonrose/DjangoUnleashed-1.8 ), I didn't see anywhere that
was done. I'll look in Django's own documentation.

Couldn't find much there, at least not that I want to deal with now (making an app reusable) but stackoverflow.com has
some questions about this indicating that it can be done
( https://stackoverflow.com/questions/47801621/unable-to-import-view-from-different-app ) and explaining how to get to
a namespace in a template ( https://stackoverflow.com/questions/26812980/django-template-url-from-another-app ). I'll
give it a try.

Creating a Discussion App
+++++++++++++++++++++++++

I created the ``discussion`` app with ``python manage.py startapp discussion`` and added all of the files it created
(including the ``__init__.py`` in ``migrations``) to git.

Plan for Implementing Discussion Pages
++++++++++++++++++++++++++++++++++++++

Here is the plan, though it may be modified by having a separate app:

*   Modify PageView's ``get`` method to include 'DS' pages, redirect to the corresponding discussion url
*   update url patterns at the site level to include the discussion urls
*   figure out and implement the url patters in the discussion app
*   Create a stub ``discussion.html`` page in the discussion app
*   Create a ``base_discussion.html`` page to be extended by ``discussion.html`` (plus private and secret versions?)
*   Add the question to the page
*   Add a form with a textview for the user to enter longish entries
*   Add a way to display the current state of the discussion
*   Modify PageView's ``post`` method to include 'DS' pages
*   Make sure a user's responses are being recorded correctly
*   Add an Edit link to the current user's comments
*   Create the Edit page
*   Make sure the Edit page works
*   Add an indicator to show an entry has been edited and when
*   Make it usable for private discussions (and come up with a better name: semi-confidential?)
*   Make is usable for secret discussions (and come up with a better name: confidential?)

I don't know that I will need separate templates for semi-confidential and confidential discussions so, at least for now
I will not try to implement them in ``disucssion.urls.py``.

Implementing discussion/views.py
++++++++++++++++++++++++++++++++

.. index:: Problems;unresolved reference in PyCharm

In creating ``discussion/views.py`` and trying to import the models from the activity app I wrote::

    from activity.models import Activity, Page, Response, Choice

but PyCharm underlined it in wavy red lines indicating it was an unresolved reference. It worked perfectly well,
however once I actually created a view which displayed my ``discussion.html`` stub. I fixed this by going to
File->Settings->Project<project name>->Project Structure and marking the ``confirmation`` directory as a source folder
by selecting it and then clicking the blue src folder above.

I thought of using a mixin for this view just like I did in the ``activity`` app, and it was working too! I copied the
PageMixin class from ``activity/views.py`` to a ``mixins.py`` file in ``config``. Then importing that file in
``discussion/views.py`` I could use it to create the DiscussionView. However, PageMixin was designed to return a
single response and I'm going to have several responses for each discussion question, and, as I'm planning it now, there
is only going to be one DiscussionView. I can get what I need within the view itself without violating the DRY
principle. (For now I'm leaving ``mixins.py`` in the ``config`` folder just in case I find it useful later.

.. index:: access to pages

Checking Whether Users Can Access Pages They Shouldn't
++++++++++++++++++++++++++++++++++++++++++++++++++++++

While working on the Discussion page I made a couple of entries for Fr. Jim Morris and then switched my identity to
Diego. Well, Diego hadn't completed any part of Noah: The Real Story but was immediately sent to the last page in the
list. This should not happen. I will check to see if it happens with other pages too...

It does! That probably means Diego can enter URLs ahead of where he is and get to those pages too. I will check...

Yep, he can!

To fix this I think I will have to change the get method of the PageView to include some kind of test and, if the test
fails sends the user back to the summary page for that activity.

Refactoring PageMixin
+++++++++++++++++++++++++

I had been testing the Discussion Page as Diego, who has made no responses yet. When I switched to myself I got an
error about Response.objects.get returning too many objects. This was because calls to DiscussionView come through
PageView in the activity app and PageView was presuming no more than one response to come from ``get_response_info``.

My solution is klunky, but it seems to be working for the Discussion page anyway. I will have to test entry, editing
and deleting on all of the different page types however since this change affects all of them.

Also, I used the option of creating the PageMixin in ``config/mixins.py`` so it can be used by all apps, currently
the activity app and the discussion app. Here is the PageMixin class::

    class PageMixin:

        """
        This mixin gets a response or QuerySet of responses with the corresponding activity and page
        from the user, activity_slug and page_index
        """

        def get_response_info(self, user=None, activity_slug=None, page_index=None):
            activity = Activity.objects.get(slug=activity_slug)
            page = Page.objects.get(activity=activity, index=page_index)
            responses = Response.objects.filter(user=user, activity=activity, page=page)
            single_response = None              # single_response = None for no responses and if there are more than one
            if len(responses) == 1:
                response = responses[0]
            context = {'activity':activity, 'page':page, 'response':single_response}
            return activity, page, responses, context

This required a different approach in the views. Here is what I did in the get method of PageView::

    class PageView(PageMixin, View):

        def get(self, request, activity_slug, page_index):
            activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
            if not page.allowed(request.user, activity_slug, page_index):
                return redirect('summary', activity_slug)
            if page.page_type == 'IN':
                self.template_name = 'activity/instructions.html'
            elif page.page_type == 'ES':
                self.template_name = 'activity/essay.html'
            elif page.page_type == 'MC':
                self.template_name = 'activity/multi-choice.html'
                choices = Choice.objects.filter(page=page)
                context['choices'] = choices
            elif page.page_type == 'TF':
                self.template_name = 'activity/true-false.html'
            elif page.page_type == 'DS':
                return redirect('discussion', activity_slug, page_index)
            return render(request, self.template_name, context)

Testing After the Refactor
++++++++++++++++++++++++++

I will sign in as Diego and try to do everything possible with each page. Here is a table of tests

.. csv-table:: **Create, Edit and Delete Tests for Each Page Type After Refactoring PageMixin**
    :header: Page, Display, Create, Review, Edit, Delete
    :widths: auto

    /noah/1/ 'IN', Yes, Yes, No (1), -, -
    /noah/2/ 'ES', No (2), Yes, Yes, No (3), Yes
    /noah/3/ 'MC' AE, Yes, Yes, Yes, -, -
    /noah/4/ 'MC' A, Yes, Yes, Yes, -, -
    /noah/5/ 'MC', Yes, Yes, No (4), Yes
    /noah/6/ 'TF' AE, Yes, Yes, No (5), -, -
    /noah/7/ 'TF', Yes, Yes, Yes, Yes, Yes
    /noah/8/ 'DS', No (6), Yes, Yes, No (7), -

Notes:

#.  Somehow, in PageMixin I used ``response = responses[0]`` instead of ``single_response = responses[0]``
    I think I'd like to use response throughout anyway.
#.  After completing page 1 Diego could not get to page 2. I think ``allowed`` must be returning False.
    It was. I was checking if the current page was completed not the previous page setting ``page=page_index-1`` did
    the trick.
#.  I neglected to modify the post method of PageEditView to expect four values back from ``get_response_info``
    I also had to get the value of ``response`` from the context: ``response = context['response']``
#.  I get back to the Review page but nothing is changed... because I had ``response.multi_coice`` at the crucial point
    where the value was to change instead of ``response.multi_choice = request.POST['choice']``.
#.  The explanation displays twice because I left an extra ``{{ page.explanation }}`` in ``true_false.html`` for
    debugging.
#.  Jim's answers do not display when Diego is logged in because ``get_response_info`` only returns the responses for
    the current user. I need to put ``context['responses'] = Response.objects.filter(activity=activity, page=page)``
    into it.
#.  I haven't implemented editing yet for discussion entries. That's up next.

Implementing the Edit Link for Discussion Entries
+++++++++++++++++++++++++++++++++++++++++++++++++

I can probably follow the style of the PageEditView here.

Implementing Semi-confidential Discussions
++++++++++++++++++++++++++++++++++++++++++

I think the view is already done but I have to change the way the template displays discussion entries depending on the
type of discussion. If it is an 'OP' discussion it should display the name, otherwise not. I made sure that the Edit
links will not show up for 'AN' discussions because if an Anonymous user does happen upon the site somehow, he or she
would be able to edit all of those entries!

Here is the pertinent part of ``base_discussion.html``::

    {% for response in responses %}
        <div class="row">
            {% if page.discussion_type == 'OP' %}
                <div class="three columns discussion-name">
                    {{ forloop.counter }}.
                        <div class="u-pull-right">
                            {{ response.user.first_name }} {{ response.user.last_name }}:
                        </div>
                </div>
                <div class="nine columns discussion-response">
                    {{ response.essay }}
                    {% if response.user == user %}
                        <a href="{% url 'discussion_edit' activity.slug page.index response.pk %}">
                            Edit
                        </a>
                    {% endif %}
                </div>
            {% else %}
                <div class="twelve columns discussion-response">
                    {{ forloop.counter }}. {{ response.essay }}
                    {% if page.discussion_type != 'AN' %}
                        {% if response.user == user %}
                            <a href="{% url 'discussion_edit' activity.slug page.index response.pk %}">
                                Edit
                            </a>
                        {% endif %}
                    {% endif %}
                </div>
            {% endif %}
        </div>

Now to see if it works.

To test it I will first change the type of "The Message of the Story" discussion to 'SA' and see if the names still
print...

They do not. Also, Edit links appear next to the appropriate entries.

Now to try 'AN' type discussions. I will have to make an entry to see how it gets recorded...

The discussion page does not show any Edit links. Good!  However, I cannot use the AnonymousUser to save the response
since it is not a User instance. I suppose that means I will have to create my own AnonymousUser. Maybe I will call it
'Unknown.'

I did that, giving it a password of 'unknown1234554321nwonknu' (notice the mirror reversal). I gave it a first name of
'Unknown' so it would display in the admin app but did not give it a LastName or an e-mail address.  I unchecked
'Active.' When I create things that list all the users I will have to find a way not to list Mr./Ms. Unknown.

Now it was able to accept and display my test entry and, in the admin, it displayed as being created by 'Unknown.' Yay!
I have deleted it and will go back to having "The Message of the Story" be an 'OP' discussion.

Plans
-----

*   Make it possible to have multiple, linked, help pages (with the menu selection opening to an index--help app?).
*   Implement Quizzes
*   Create and implement e-mail app
*   Start working on activity creation pages
*   At some point, deploy to webfaction

.. index:: Quizzes

Idea for Quizzes
----------------

The next thing up is to implement multiple-choice pages. (I started this section well before getting around to
implementing it.) It occurred to me, though, that it might be nice to be able to collect multiple-choice questions
into a single entity, called a quiz(?), instead of putting them into activities one by one. Then why not allow a mix of
questions: multiple-choice, essay, True/False, and maybe even implement matching type questions?

I think this could be done by creating another model called Quiz, and maybe learn how to get the admin to call the
plural "Quizzes." I would have to add an optional field to each page type to refer to the quiz it belongs to and then
put a quiz into the activity instead of the individual pages. I could also develop a new quiz.html page to display the
quizzes. I'm thinking it could display the questions and their answers as they proceed through the quiz and then, after
they submit the whole thing, I can give them instant results, and prevent them from changing their answers.

I first decided to delay the implementation of this feature until after the basic site is done, perhaps because I
couldn't figure out how the view would work, but now I think I have. The PageView, when it came to quiz questions, could
load up the list of questions and then CALL it's own ``get`` method with all the proper parameters instead of returning
a request right away. I may have to study exactly what is in a request to make it work properly since it wouldn't do to
keep calling the same page over and over again. I suspect I should do that first.

Studying the Request
********************

I can put a print statement into the PageView and then visit any page to see what is included in a request...

Well, that didn't work. Simply printing a request did not list, for instance, the .user component. What other components
might there be? I'll have to look into the Django documentation...

As I did, finding out that the request object contains a lot of information, and information that mostly can't be
changed besides, it also occurred to me that my plan of calling the ``get`` method from within the ``get`` method will
not work. It's not because a method can't recursively call itself, it can, the problem is that when the ``get`` method
determines, say, that the desired page is a multi-choice page it will do a ``return render`` and try to go back to the
calling method (itself) which, I suppose, could used the returned response to display the right page somehow but where
would it go after that? If the user submits the filled out form it will go to the ``post`` method and I don't see how it
would ever get back to the loop that was looping through the quiz questions.

That's the problem, it seems to me, how to get back to the loop that is counting through the quiz questions. Perhaps
there is something I can add to the url, like a %next% or some such thing.

.. index:: error pages

By the way, I found something about error handlers at https://docs.djangoproject.com/en/2.0/topics/http/urls/ that
might be of use when I'm trying to get my own error pages to display -- such as ``404.html``.

The same page spoke of Passing extra options to view functions (would it work for view classes?) that perhaps I can
figure out how to use. But not right now. Maybe I could implement quizzes something like the summary page. Upon clicking
the button in the Activity's summary page the user would get to a list of quiz questions which may or may not have to be
completed in order. Perhaps it could somehow send back to the summary page (with a model method?) how much the user has
completed so far.

In any case, perhaps I was right to delay the quiz feature until later. It is important, I think, to have something up
and running soon.

A Possible Help App
-------------------

But it would be good to make the help system more than one page. Here is a possible outline:

#.  Getting into the Confirmation Website
#.  The Welcome Page
#.  Activity Summary Pages
#.  Written Response Pages
#.  Multiple Choice Pages
#.  True/False Pages
#.  Discussion Pages

Starting the Help App
*********************

Should be easy: ``python manage.py startapp help``...

It was easy! Now to add it to the INSTALLED_APPS...

That was easy too! Now to add all the files to git. (By the way, the files ``startapp`` created are: __init.py__,
admin.py, apps.py, models.py, tests.py and views.py. There is no urls.py. I may need to read up on the latest approach
to urls which I noticed at https://docs.djangoproject.com/en/2.0/topics/http/urls/ was different than what I've been
doing.

I remembered to include the __init__.py file under the migrations folder in git too.

New Approach to urls.py?
************************

In the section on *Including other URLconfs*, the documentation mentioned above used this kind of location for the
urls::

    # In settings/urls/main.py

    # In foo/urls/blog.py

so I was wondering whether having a urls folder and an <appname>.py file inside it was now the recommended place to have
URLconfs. If so, why?

I didn't find anything in that part of the documentation so I thought I'd look at the current version of the tutorial
pages...

The first page of the tutorial had the usual scheme of having a urls.py file in the app directory so I will continue
with that practice for now. I should probably re-do the tutorial, however, to notice anything that has changed and, most
especially, to do the later parts.

Getting to the Views
********************

I need to create a help/urls.py file, give it some URLconfs and add a path in my config/urls.py file to get to it.

That worked fine, once I had the right syntax in my ``path()`` statements. I got it to work with new models in the help
app, and new templates in the help app.

.. index:: Problems: migrations again!

Weird Problem with Makemigrations
*********************************

But, while adding the new templates I accidentally created a file named ``true_false`` instead of ``true_false.html``
and tried to rename it. PyCharm did one of its refactor things and, somehow, my ``true_false`` field in the Response
model got changed to ``true_false.html`` not what I intended at all. Unfortunately, now when I try a ``makemigrations``
it asks if I've changed it and, whether I respond 'y' or 'N' it seems to make a migration file that can't be used by
``migrate``. I've tried deleting just those files but then the question comes up again. I have backed up all of the
files in the confirmation2018 project and I am going to delete ALL of the migrations files except for
``0001_initial.py`` in each app.

I checked with PgAdmin4 -- after updating it in a strange way that leaves it as a separate program on my Start Menu
instead of being listed under PostgreSQL10 as it was before (Home Computer) -- but the activity_response table had NOT
been changed. So this delete migration files trick might work. It will be like I have created all the models fresh...I
hope...

It didn't seem to work. I got "django.db.utils/ProgrammingError: relation "activity_choice" already exists" meaning, I
think, that the database already has a table for the Choice model. I will try to create a new database ``conf18-1`` to
see if I can use that...

O.K. That worked. Of course I had to change the DATABASE_NAME setting in conf_secrets.json. I will also have to run a
loaddata on my most recent fixture...

That didn't work because I had not created my four groups: Candidate, Team, Supervisor and Administrator. I have now
created them, in that order, and will try loaddata again...

It worked! Or at least it seemed to. I will have to check the users to see that they are in the right groups and have
the right permissions...

Yep! Everything seems to be set up properly. There are no entries in the help app, of course. I will have to recreate
those.

Synchronizing My Computers After the Migrations Problem
*******************************************************

Here are the steps I think I will need to follow:

*   Do a git pull
*   Use PgAdmin4 to create a new conf18-1 database
*   Adjust conf-secrets.json accordingly
*   Do a migrate (the proper migration files have been pulled in)
*   Create a superuser (yourself)
*   Create four groups: Candidate, Team, Supervisor and Administrator in that order
*   Load data from the latest fixture

.. _update_fields:

It worked fine on the Rectory Computer but I discovered that the help/views.py file needed to be updated to the current
field names.

Continuing With the help App
****************************

I added the category of 'usage' to the HelpCategory model (which needs something to tell it how to properly pluralize)
and added welcome, summary, written_response, multi_choice, true_false and discussion, in that order, to the HelpPage
model. The system can locate each help page from the index but I have yet to implement the ability to make Next and
Previous links or buttons or figure out a way the user can go back to the last page he or she visited (aside from using
the browser's Back button of course -- perhaps that is not a necessary feature.)

After some difficulty, and some additional entries in the HelpCategory model, I was able to get it all to work. Here are
some example files:

**help/urls.py**::

    from django.urls import path, include
    from django.views.generic import RedirectView
    from django.contrib.auth.decorators import login_required

    from .views import HelpView

    urlpatterns = [
        path('', RedirectView.as_view(url='help/index/')),
        path('<category_name>/', HelpView.as_view(), name='help_page'),
        path('<category_name>/<int:page_number>/', HelpView.as_view(), name='numbered_help_page'),
    ]

**help/views.py**::

    from django.shortcuts import render, redirect
    from django.views import View
    from .models import HelpCategory, HelpPage


    class HelpView(View):
        template_name = 'help/help.html'

        def get(self, request, category_name, page_number=None):
            category = HelpCategory.objects.get(name=category_name)
            if not page_number:
                context = {'page_file_name': 'help/' + category_name + '.html',
                           'category': category_name, 'previous': None, 'next': None}
            else:
                help_page = HelpPage.objects.get(category=category, page=page_number)
                page_count = len(HelpPage.objects.filter(category=category))
                page_number = help_page.page
                previous_page_num = page_number - 1
                if previous_page_num <= 0:
                    previous = None
                else:
                    previous = previous_page_num
                next_page_num = page_number + 1
                if next_page_num > page_count:
                    next_page = None
                else:
                    next_page = next_page_num
                context = {'page_file_name': 'help/' + help_page.page_name + '.html',
                           'category': category_name, 'previous': previous, 'next': next_page}
            return render(request, self.template_name, context)

**help/templates/help.html**::

    {% extends parent_template|default:"base.html" %}
    {% load static %}

    {% block content %}
        <div class="container">
            {% include page_file_name %}
            <div class="twelve columns">
                {% if previous %}
                    <a class="u-pull-left" href="{% url 'numbered_help_page' category previous %}">Previous</a>
                {% endif %}
                {% if next %}
                    <a class="u-pull-right" href="{% url 'numbered_help_page' category next %}">Next</a>
                {% endif %}
            </div>
        </div>
    {% endblock %}

**help/templates/index.html**::

    {% load static %}

    <div class="container">
        <h1>Help Index</h1>
        <h2>Here is a list of the help topics available:</h2>
        <ul>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 1 %}">The Welcome Page</a>
            </li>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 2 %}">The Acitivity Summary Page</a>
            </li>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 3 %}">Written Response Pages</a>
            </li>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 4 %}">Multiple Choice Pages</a>
            </li>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 5 %}">True/False Pages</a>
            </li>
            <li>
                <a href="{% url 'numbered_help_page' 'usage' 6 %}">Discussion Pages</a>
            </li>
        </ul>
    </div>

**help/templates/summary.html** (unfinished)::

    {% load static %}

        <h1>The Activity Summary Page</h1>

It seems like a crazy system to me: if a url is given with no page number it goes one place, with a page number it goes
another.

I don't know what will happen in testing, when I try to get into pages improperly. Hopefully the correct html error page
will eventually show up but I don't want to mess with that now.

I can fill out the various help page stubs as I get around to it but hopefully before putting it all online.

Changes to Help Models
**********************

I need to learn how to get the admin to properly pluralize the HelpCategory model to "Help categories." Also the
HelpPage model needs to be unique for category and page_number, which, by the way, reminds me that the field named
"page" should be called "page_number." First I will make the changes in the models, then do a makemigrations and
finally a migrate. I may end up having to change some things in help/views.py if PyCharm's refactoring doesn't
do it. Here goes nothing...

I discovered when I synced the Rectory computer that I hadn't updated help/views.py. (:ref:`See above<update_fields>`)

Plans
-----

Once I get an e-mail system I've got version 0.5 ready for deployment. I plan to present it to Sylvia first, and get her
ideas, then, after some fixes, open it up to the team members for their comments. Then it will be time to develop some
actual content. Maybe I will have an easier way to do that by that time. Finally, it will be time to present it to the
candidates and see what happens.

Building an E-mail System
-------------------------

Here are the steps I imagine myself taking:

#.  Study django documentation to figure out how to get "practice" e-mail on the local system
#.  Think about how you want to use the e-mail system
#.  Plan the pages you will want/need
#.  Work out a url scheme
#.  Create and implement an e-mail app

E-mail on the Local System
**************************

Things I learned:

*   https://docs.djangoproject.com/en/2.0/topics/email/ is the page with the e-mail information I want
*   the line ``from django.core.mail import send_mail`` will need to be in the views.py file (if I use it)
*   ``send_mail()`` is used to send the mail
*   ``subject``, ``message``, ``from_email`` and ``recipient_list`` are required parameters
*   there is also a ``send_mass_mail()`` option - both sending methods reveal all of the To: email addresses
*   ``mail_admins()`` might be useful for getting feedback from users - but I might not want to
*   bcc can only be done by creating **EmailMessage** instances directly
*   To send "e-mails" to stdout use ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``
*   That line is already present in my ``config/settings/dev.py`` file since it came from the Christmas website

Thinking About E-mail
*********************

I will want to send mass e-mails, such as the invitation e-mail when the system is finally on line. I will want to have
a system like I used for the Christmas website to use my own "template language" for such things as <name>, <username>
and <password>. I will want the option to send individual or small group e-mails.

In these things what I have in mind is exactly like the Chrismas website. Is there anything more? Would it be possible
to e-mail Team feedback on the site? Perhaps, but it makes more sense to have the comments visible there instead so that
everyone can see what everyone has said. (Names or no names? That is the question.)

I think I'll stick to the same plan I used for the Christmas website but improve the looks and the functionality of the
corresponding web pages.

Planning the E-mail Pages
*************************

Perhaps I could have the possibility of composing mass e-mails, complete with "template variables" right in the
application. That would require a model to keep the e-mails for later editing should I so desire. That would require
a name for the e-mail being saved too.

Actually, I think I've already done that in the Christmas website on the individual/sub-group e-mail page, though I
don't think it got saved nor could it handle variables. That sounds like I may only need one page both to compose the
e-mail and select the recipients - including a "select all" option.

I think I should be able to list all the candidates alphabetically in columns. Maybe have team members listed
separately.

URL Scheme
**********

If it all comes down to one page, the url scheme is easy: ``/email/`` gets you to the e-mail page, but only if you are
a Supervisor. I still haven't learned how to do that but I think it would be in the view.

Ceating and Implementing the E-mail App
---------------------------------------

The Menu Link
*************

Adding the menu link to the header should be easy, and this is where I should be able to learn how to restrict viewing
that link to Supervisors and Administrators.

Appearance of the Menu Link
+++++++++++++++++++++++++++

Adding the link was easy. Getting it to look right is another matter. I think my implementation of the dropdown menu
button may be interfering with the display of this E-mail link I am trying to add. I probably just need a better set
of css rules. Here is what I would like the header to look like with a possible div/css scheme to make it so::

    +-----------------------------------------------------------------------------------------------------------------+
    | container row                                                                                                   |
    |  +------------------+ +---------------------------------------------------------------------------------------+ |
    |  | two columns      | | ten columns                                                                           | |
    |  |                  | | +---------------------------------------------------------------------------------+   | |
    |  | (logo)           | | | banner                                                                          |   | |
    |  |                  | | |                                                                                 |   | |
    |  |                  | | +---------------------------------------------------------------------------------+   | |
    |  |                  | | +---------------------------------------------------------------------------------+   | |
    |  |                  | | | navigation                                                                      |   | |
    |  |                  | | | +--------------------------------+ +------------------------------------------+ |   | |
    |  |                  | | | | welcome                        | | menu                                     | |   | |
    |  |                  | | | +--------------------------------+ +------------------------------------------+ |   | |
    |  |                  | | +---------------------------------------------------------------------------------+   | |
    |  +------------------+ +---------------------------------------------------------------------------------------+ |
    +-----------------------------------------------------------------------------------------------------------------+

Applying Groups
+++++++++++++++

From what I've been able to learn so far, mostly from *Django Unleashed* **Chapter 20.3.2 Groups in the Shell**, here
is my current idea of how to deal with this:

In the views, create a context list variable called 'group_names' that contains all of the groups the request.user
belongs to. This can be found with something like the following::

    from django.contrib.auth.models import Group

    group_names = []
    for group in Group.objects.filter(user=request.user):
        group_names.append(group.name)

Include ``group_names`` in the context variable and then, in the templates access it with something like the following::

    {% if '<the necessary group name>' in group_names %}
        <display what they have access to>

I may end up using a Mixin or some global method to which all the views will have access instead of placing it in each
view, but I think this should work. I'll try it first for the E-mail link on the welcome page...

Well, that wasn't too hard to implement in the activity app. I ended up putting a ``get_group_names`` method into the
``PageMixin`` class in ``config/mixins.py`` which I have renamed from ``ResponseMixin``. I had Refactor/Rename change
the name in the documentation too so references to if above should all say ``PageMixin`` now.

Since neither the ``WelcomeView`` nor the ``SummaryView`` used ``PageMixin`` I had to include::

    group_names = PageMixin.get_group_names(self, request.user)

before adding it to the context.

I haven't checked out ALL the activity pages yet, like those for editing and deleting, but I suspect they will all work.

I still need to change the view in the help app...

The only glitch I ran into is that, since the help pages do not require authentication, when I logged out while on a
help page I got an error something like: Anonymous User is not Iterable (presumably because ``get_group_names`` tries
to filter the Groups for the AnonymousUser, though I didn't look carefully enough at the message to be sure.

I added the following to the HelpView class::

    if request.user.is_authenticated:
        group_names = PageMixin.get_group_names(self, request.user)
    else:
        group_names = None

and all seems well.

Now to create and develop the e-mail app, and later to change the looks of certain views for Team members and above.

Creating the e-mail App
***********************

