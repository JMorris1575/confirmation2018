============================
Team Sections of the Website
============================

User Groups
-----------

There are four levels of users of the website:

*   Administrator
*   Supervisor
*   Team
*   Candidate

Candidates have access only to the Activity pages and Help pages.

Team members should be able to help with Activity creation by making comments on the creation pages but not to actually
edit them personally.

Team members should also have access to the work their candidates have completed. It may be sufficient to give them
access to the work of all candidates but to group the candidates under their respective team members.

Supervisors should be able to create content as well as do all of the things Team members can do.

Administrators, or superusers, have total access to everything on the website.

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

Here is what I think I need to do:

*   Use startapp email to create the e-mail app
*   Create the url paths both in config and in the email app
*   Create the EmailView
*   Create email.html
*   Practice sending e-mails to selected users (which could include all users)
*   Work on a means to implement substitutions within e-mail templates (both for subject lines and the message itself).
*   Test the substitutions
*   Create a model to save e-mail templates
*   Work on a means to create, edit and delete e-mail templates
*   Work on a means to select a template to send
*   Test the saved templates

I could not use ``email`` for the name of the app because it conflicts with an existing Python module. I will try
``e-mail`` instead.

Nope, it doesn't seem to be a valid app name. Probably because of the hyphen. I guess I can use what worked in the
Christmas website:  mail.

That worked. Now to add all the new files to git and put it into ``INSTALLED_APPS``.

URL Paths
*********

Here is the scheme:

.. csv-table:: **URLs for the mail app**
    :header: url path, view, notes
    :widths: auto

    /email/, , redirects to /email/send/
    /email/send/, EmailView, allows the sending of send e-mails to the whole group, subgroups or individuals
    /email/create/, EmailCreateView, allows the user to create an email to be saved
    /email/n/edit/, EmailEditView, allows the user to edit a saved email created above
    /email/n/delete/, EmailDeleteView, allows the user to delete a saved email

While creating the patterns above I happened to think about whether one Supervisor should be allowed to change an
e-mail template created by another. I decided that, yes, they should be able to. They need to work together on these
things.

Selecting Groups of Users
*************************

Adding Button Elements and Installing jquery
++++++++++++++++++++++++++++++++++++++++++++

I added some <button> elements to select all users, supervisors, team members and/or candidates. I installed jquery by
adding the lines::

    <script
          src="https://code.jquery.com/jquery-3.3.1.min.js"
          integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
          crossorigin="anonymous">
    </script>

to ``base.html`` after the css section.

I wrote a jquery script for the Select All button as follows::

    {% block head %}

        <script>
            $(document).ready(function() {
                $('#select_all').click(function() {
                    $(':checkbox').each(function() {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    }); // end checkbox each
                }); // end select_all click
            }); // end ready
        </script>

    {% endblock %}

And, in the html part of the code::

    <button class="u-pull-left five columns" id="select_all">Select All</button>

to be able to select that button.

When I tried it, it seemed to select all of the boxes well enough but it also submitted the form! Not what I wanted.
Using Firefox's Debugger console I eventually learned that <button> elements have a default type of 'submit' and that
was causing the problem. When I added ``type="button"`` that fixed the problem.

To add buttons for the individual groups I had to add a class to each
``<input ... type="checkbox" class="*group*"...>``. I tried to use ``id="*group*`` at first but that only returned one
element to my jquery code.

Here is the final version of the jquery code::

    {% block head %}

        <script>
            $(document).ready(function() {
                $('#select_all').click(function() {
                    $(':checkbox').each(function() {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    }); // end checkbox each
                }); // end select_all click
                $('#select_supervisors').click(function() {
                    $('.supervisor').each(function() {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    }); // end supervisor each
                }); // end select_supervisors click
                $('#select_team').click(function() {
                    $('.team').each(function() {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    }); // end team each
                }); // end select_team click
                $('#select_candidates').click(function() {
                    $('.candidate').each(function() {
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    }); // end candidate each
                }); // end select_candidates click
            }); // end ready
        </script>

    {% endblock %}

Two improvements:

*   The buttons should change their looks when they are "on" from when they are "off."
*   When some boxes of a group are checked already, they should be either all checked or all unchecked, not just toggled

It seems these could both be handled by learning how to get jquery to add a css class to the button's description. Then
I could use it to both change its appearance and determine whether all the boxes in a group are to be checked or
unchecked. Perhaps I will do that next.

Button Improvements
+++++++++++++++++++

I did manage my two improvements but I'm not happy with them yet. I did learn how to create a named function in
JavaScript and used it as shown below::

    function toggleSelected(button) {
        // toggles the 'selected' class in the given button, returns true if selected, false if not selected
        if ($(button).hasClass('selected')) {
            $(button).removeClass('selected');
            return false;
        } else {
            $(button).addClass('selected');
            return true;
        }; // end if
    }; // end toggleSelected

That required a change to each of the individual button codes as well. Here is the code for the supervisor button for
an example::

    $('#select_supervisors').click(function() {
        selected = toggleSelected(this);
        $('.supervisor').each(function() {
            $(this).prop('checked', selected); // sets the checkbox to status of button
        }); // end supervisor each
    }); // end select_supervisors click

But it is still awkward to use. If I click "Select All" and then click "Supervisors" nothing appears to happen because
the "Supervisors" button was "off" and then clicked to "on" so the supervisor checkboxes that were already checked did
not change their appearance. I think it would be better to turn on all of the sub-group buttons when "Select All" is
clicked, which shouldn't be too difficult. I'll have to decide what to do, if anything, to the "Select All" button when
a sub-group button is clicked.

Controlling the Buttons
+++++++++++++++++++++++

This should not be difficult since the variable ``selected`` is already available. Here is the code I ended up with::

    $('#select_all').click(function() {
        var selected = toggleSelected(this); // toggles 'selected' class and returns true if it is set
        $('.sub-group').each(function() {
            if (selected) {
                $(this).addClass('selected');
            } else {
                $(this).removeClass('selected');
            }
        });
        $(':checkbox').each(function() {
            $(this).prop('checked', selected); // sets the checkbox to status of button
        }); // end checkbox each
    }); // end select_all click

Now I need to finish the e-mail form by adding a ``<textarea>`` element.

Sizing Input Areas
++++++++++++++++++

This might be a good time to use the id of the textarea and ``<input type="text"...>`` tag...

Here is the current html code for the subject line and text area::

    <div class="row">
        <div class="nine columns small-font">
            <div>
                <label class="u-pull-left" for="subject">Subject:</label>
                <input class="u-full-width" type="text" id="subject" name="subject"></inputtextarea>
            </div>
            <div>
                <label for="message">Enter the text of the e-mail below:</label>
                <textarea type="text" class="u-full-width" id="message" name="message"></textarea>
            </div>
        </div>
        <div class="three columns border">
            <p class="small-font">
                The following tags in the subject line or message will be converted as shown:
            </p>
            <p class="small-font">
                [first] = first name<br>
                [last] = last name<br>
                [full] = full name<br>
                [user] = username<br>
                [pwrd] = password
            </p>
        </div>
    </div>

Translating Template Tags in E-mails
++++++++++++++++++++++++++++++++++++

Borrowing from the Christmas website and improving things a bit, here is the code I came up with for the view::

    def convert_tags(subject, message, user):
        """
        Converts the following tags in the message or subject line of an e-mail to their equivalent for the given user:
        [first] = first name
        [last] = last name
        [full] = full name
        [user] = username
        [pwrd] = password
        :param subject: string containing the subject line to be sent
        :param message: string containing the message to be sent
        :param user: User object containing data for the given user
        :return: a subject string and message string with all the tags filled in
        """
        user_info = {'[first]':user.first_name,
                     '[last]': user.last_name,
                     '[full]': user.get_full_name(),
                     '[user]': user.username,
                     '[pwrd]': get_secret(user.username.upper())}
        for tag in user_info.keys():
            subject = subject.replace(tag, user_info[tag])
            message = message.replace(tag, user_info[tag])

        return subject, message


    class EmailView(View):
        template_name = 'mail/send-mail.html'

        def get(self, request):
            if request.user.is_authenticated:
                group_names = PageMixin.get_group_names(self, request.user)
            else:
                group_names = None
            supervisors = Group.objects.get(name="Supervisor").user_set.all().order_by('last_name')
            team_members = Group.objects.get(name="Team").user_set.all().order_by('last_name')
            candidates = Group.objects.get(name="Candidate").user_set.all().order_by('last_name')
            context = {'group_names': group_names,
                       'supervisors': supervisors,
                       'team_members': team_members,
                       'candidates': candidates}
            return render(request, self.template_name, context)

        def post(self, request):
            recipients = request.POST.getlist('recipients')
            subject_template = request.POST['subject']
            message_template = request.POST['message']
            for recipient in recipients:
                member = User.objects.get(username=recipient)
                subject, message = convert_tags(subject_template, message_template, member)
                send_mail(subject, message, 'FrJamesMorris@gmail.com', [member.email], fail_silently=False,)

            return redirect('send_email')

Overview of Desired Team Interaction
------------------------------------

To enlist the aid of the team members in the creation of the activities, they should be able to see the activities that
are under development and make comments and suggestions about them, both appearance and content. I think only
Supervisors and Administrators should be able to change the content however. Perhaps only the one who is working on it,
though that would require a new field in the Activity Model as to who is developing the activity. If I do that, however,
I may be able to open up activity creation to any team member, though the final say as to whether and what should go to
Supervisors and Administrators. It would be great if I could do that but it will require a very simple and intuitive
page or set of pages for the development of activities, and an easy way of viewing how they will appear to the
candidates.

I suspect a lot of javascript will be needed to make it interactive and simple -- as I found when trying to develop
pages to add multiple choice questions to the trivia app in Christmas17.

Narrative Walk-through
**********************

Fr. Jim wants to add an activity to the Confirmation website and so logs in to the website and clicks the 'Development'
link that appears to Administrators, Supervisors and Team members. There he is taken to a list of activities currently
under development with the developer's name listed next to each one.

Seeing [somehow] that Sylvia has recently edited an activity she is working on, he decides to check it out and clicks
on the corresponding button.

He is taken to a page, similar to the Summary page, which lists the current parts of the activity, and provides buttons
for viewing each one. Some of the buttons are highlighted indicating that Fr. Jim has not viewed them since the last
edits were made by Sylvia. He clicks on one of them.

The current form of the candidate page appears with an extra section at the bottom containing comments team members have
made during the page's development. This comment section actually appears on all of the pages of this section, including
the Summary page. Jim views the page, makes some comments, and then goes back to the Activity Development page to start
the activity he came here to start.

There is an 'Add Activity' button there and he clicks it. He comes to a page that allows him to enter the pertinent
information about the activity, such as it's name, description, and icon image. Some information, such as that it will
be invisible until published, is filled in with default values. This page has a 'Publish' button visible only to
Supervisors and Administrators, and an 'Add Page' button visible only to the person (or persons?) developing the
activity.

Fr. Jim clicks the 'Add Page' button and comes to a generic page that allows him to do that. A combo box near the top
allows him to select the kind of page this will be and the selection he makes on that page determine the subsequent
choices he can make. As he enters data, the image of the page as it will appear to candidates develops on the screen.
Once he is happy with it, or just when he wants to quit, he can click the 'Save' button on the page.

Thus Jim builds up the activity, page by page and, when he is ready, can present it to the group with a 'Open for
Comments' button that appears on the summary page.

When all is ready a Supervisor or Administrator can set the dates for its appearance and Publish the activity to the
candidates.

Planning the Development App
****************************

It seems that this will require another app, perhaps called "development" that will provide a model for comments on
each developing activity as well as a model for the team member(s) responsible for its development. It can have its own
templates, which can probably borrow extensively from what is already available in the activity app, and views that will
manage what goes into and comes out of those templates.

Since the development app should only be available to team members and higher that may simplify the access control.
Perhaps it can all be done in the ``development`` views.

Here is what I think I will need to do:

*   Plan the URL scheme
*   Plan the Models
*   Create the app and include it in the settings
*   Create the models and register them in admin.py
*   Add a 'Development' link to the header menu visible only to Team members and above
*   Work on the Activity List Page (it should include ways to edit existing activities)
*   Work on the development summary page
*   Work on the creation page(s) for each page type

Planning the URL Scheme
+++++++++++++++++++++++

Here are my initial thoughts:

.. csv-table:: **Development App URL Scheme**
    :header: URL, View, name, notes
    :widths: auto

    develop/, RedirectView, , the base url for the app-redirects to develop/activities/
    develop/activities/, DevActivityListView, dev_activity_list, goes to the list of activities that can be edited
    develop/activities/<activity_slug>/summary/, DevSummaryView, dev_summary, goes to the development summary page
    develop/activities/<activity>/<page>/, DevActivityPageView, dev_activity_page, goes to the page development page

Planning the Models
+++++++++++++++++++

Right now I'm thinking of two models, one to hold comments on the developing activities, the other to contain working
information about who has publishing/editing rights over each of the developing activityies. The first should be easy,
just call it Comment or DevComment.

The other will probably change as I get more deeply into the creation of this part of the website. What shall I call it?
How about Developer? Fields in this model would connect to an Activity, a User, and something to indicate the rights
this user has over the activity. I will have to think more about this.

Perhaps one of the members of the group working on the activity can be called the Leader, and the others Partners. Or
perhaps I don't have to distinguish between leaders and partners since it is only Supervisors and Administrators who can
publish an activity. Leaders, if there are any, can click a button that will automatically notify Supervisors and
Administrators that an activity is ready for final review and publication. I think I could use some more narratives...

Additional Narrative Walk-throughs
++++++++++++++++++++++++++++++++++

Fred has an idea for an activity and goes to the Development part of the website and clicks on 'Add Activity.' He names
the activity, enters its description and selects an images from those available to use as its icon. He adds several
pages to the activity and receives feedback from other team members. When he is satisfied with the activity as a whole
he clicks on the 'Submit Activity to Supervisors' in hopes of getting it onto the website.

Sylvia likes Fred's activity and decides it will fit well with what she has planned for the April segment and sets the
publication date for the beginning of April and the ending date for the beginning of June.

Simon and Kathy want to work together on an activity and Simon goes to the Development part of the website and clicks on
'Add Activity.' He names Kathy as his partner and then leaves the website because something came up he had to tend to.

Later, Kathy wants to begin work on the activity and goes to the Development section of the website and sees, on the
Activity List page a new activity named 'Unnamed Activity' listed in a table next to Simon's name as the initiator and
the date that it was begun. She enters into that activity, gives it a name and a slug and starts work on the first page
of the activity when she is called away.

Later, Simon comes to the Development section of the website and finds the activity he started now has a name and has
been begun by Kathy. The website gives he and Kathy a way to communicate with one another before they open their work up
for comments from the whole group. He comments on Kathy's work and makes some changes to it and then adds some pages
himself.

When Kathy sees his pages she likes them but thinks they need to be in a different order. She comments accordingly and
makes those changes.

For the most part Simon likes the changes Kathy has made but had a particular reason for one part of the actvity being
in the position that it was. He explains that to Kathy and puts that page back into the proper place in the sequence.

Finally, both Simon and Kathy are satisfied with the activity and open it up to comments from the group. Some of the
feedback they get inspires new thoughts and they make some changes to the activity.

Once they are both ready, Kathy submits the activity to the supervisors.

Reflections on the Additional Walk-throughs
+++++++++++++++++++++++++++++++++++++++++++

I may need two models for comments, one for general comments and one for partner comments. Perhaps TeamComment and
PartnerComment can be the names of the models. There will have to be enough detail in both so that the Activity and
Page can be determined that the comment applies to and there will have to be some means of assuring that only
partners on this activity can see the current state of the activity and other partner's comments.

Once an activity is open for general comments, should I maintain two copies of it, one that was published for all the
team to see and one, the updated version, that only the partners can see? That sounds difficult, and perhaps a waste
of database space unless the extra copies are deleted when they are no longer needed.

I can see that "Developer" may not be the best name for the model to accompany activity development. It will have to
contain some information on what state the developing activity is currently in: visible to all or only to those working
on it. Should a "published" field be in this model or in the original Activity model?

I'm thinking a one to many field from this model to the users who are working on it is necessary but I'm having trouble
picturing how to do that. In multiple-choice questions there is a Choice model that indicates to which model it belongs.
I don't know how to do that with users. Do I need another Partner model with users and their roles and the activity they
are working on? That might work.

Initial Model Design
++++++++++++++++++++

So, so far it seems that I may need the following models in addition to the already existing Activity model:

*   Developer (a model to connect activities [or developing activities?] with those who are working on them)
*   PartnerComment (a model to contain comments partners make while developing an activity)
*   TeamComment (a model to contain comments the whole team makes after the new activity is opened for discussion)
*   DevelopingActivity (a model to keep track of the status of the developing activity)

Perhaps the following models will work:

.. csv-table:: **DevelopingActivity Model**
    :header: Field Name, Field Type, Attributes, Comments
    :widths: auto

    activity, ForeignKey, Activity; on_delete=models.CASCADE, the activity being worked on
    initiator, ForeignKey, User; on_delete=models.CASCADE, the team member initiating this activity
    status, CharField, max_length=15; choices=Developing; Reviewing; Publishing; Published, status of the activity

.. csv-table:: **Developer Model**
    :header: Field Name, Field Type, Attributes, Comments
    :widths: auto

    activity, ForeignKey, DevelopingActivity; on_delete=models.CASCADE, the developing activity
    partner, ForeignKey, User; on_delete=models.CASCADE, user partnering with the initiator of this activity
    full_partner, Boolean, default=False, indicates whether this user has full rights to edit, publish, etc.

|

.. csv-table:: **Comment**
    :header: Field Name, Field Type, Attributes, Comments
    :widths: auto

    activity, ForeignKey, DevelopingActivity; on_delete=models.CASCADE, the developing activity
    user, ForeignKey, User; on_delete=models.CASCADE, the user making the comment
    text, TextField, blank?; null?; either?, the text of the comment
    type, CharField, max_length=15; choices=General; Partner, type of comment for display

Building the Development App
****************************

``python manage.py startapp development`` should do the trick...

It did, now to add all the files it created to git...

That's done. Now to create a plan:

*   add the development app to INSTALLED_APPS in ``config/settings/base.py`` [X]
*   create urls in both ``config/urls.py`` and ``development/urls.py`` [X]
*   create the new models in development/models.py [X]
*   register the new models in the admin program [X]
*   makemigrations, migrate, add migrations to git [X]
*   create the activity list page
*   create the activity summary page
*   one by one, create the individual page types

Creating the Activity List Page
+++++++++++++++++++++++++++++++

Here is what I think I have to do:

*   create the ``development/base_development.html`` page stub [X]
*   create a ``development/activity_list.html`` page stub [X]
*   add a 'Development' menu item to the header visible only to Team and above [X]
*   fill out the ``activity_list.html`` page
*   make it look good

Filling Out the Activity List Page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two kinds of activities that need to be listed, maybe three:

#.  Published Activities
#.  Activities being Reviewed
#.  Activities being worked on but not yet to the point of being reviewed.

The first two categories should be visible to everybody while the last should only be visible to the team members
working on them, Administrators and Supervisors.

Each should be displayed in its own section and in a table indicating:

*   The activity name
*   The initiator
*   A list of partners
*   Perhaps a button to enter the activity development page for that activity (or the name can be the link?)

It seems that the view must send the DevelopingActivity entry and that model should have a ``get_partners`` method to
return a list of partners.

Before I can implement this I will have to fake a couple of entries for the already existing activities...

That was easy and I have got a good start on the ``activity_list.html`` page. I've decided it makes no sense to list the
activities in separate groups. Including a Status column should be sufficient.

To save space I was thinking to make the activity's name into the link to that activity's summary page but it would be
easier, I think, to use a small button for that. The button would only appear for developing activities for the
initiator and partners for that activity. I think a model method called 'is_developer' might work for this.

But what should be the text on the button? For some, clicking the button will only allow them to make comments on the
developing (or complete) activity. For the developers of that activity it allows them to edit it. Is there a word that
covers both possibilities, or should the text just be different in different cases: Review for non-developers, Edit for
developers? That seems easier to me. The above mentioned model method: ``is_developer`` should be all it takes to
distinquish.

I will also have to invent another css class called ``small-button`` to get the button to fit into the table and
override any button formatting by skeleton.css.

The ``small-button`` class wasn't needed since I ended up using links instead of buttons, they look as good and take up
less space.

Creating the Activity Summary Page
++++++++++++++++++++++++++++++++++

The links on the list page should lead to the summary page for that activity so I will add to ``development/urls.py``,
then create stubs for ``DevSummaryView`` and ``dev_summary.html``.

After some confusion about how to get to the summary view I finally just typed out the url in ``activity_list.html`` as
follows::

    <a href="/develop/{{ activity.activity.slug }}/">Review</a>

Now to actually get something useful on the page.

It seems that copying, or including, the ``acivity/summary.html`` page and then adding a means to comment on it is
something I can do, though I'm sure there will be a learning curve. My first step is to look at ``base.html`` to see
how to included other html files like ``header.html`` and ``footer.html``...

That seems simple enough, simply type {% include 'activity/summary.html` %}. But will it be complicated by the files
the summary page extends? I'm about to find out...

Yes, it does cause complications. I got the header and footer all over again, and the image doesn't show, probably
because DevelopingActivity does not have the image directly available. This is going to take some thought...

At first it seemed that creating core html pages for each of the pages would be the way to go but that was quickly
getting very complicated. Most notably, clicking on one of the navigation buttons would take me back to the activity
versions of the pages and I would have to keep getting back to the development version. Ugh!

Perhaps a better approach would be to add some kind of flag in the activity versions of the files to indicate whether
the developer options should be visible or not. Again, I'll have to think some about this...

I've opted, for now, to recreate the pages in the development app but make the changes necessary to keep the links
going to the right places. I just copy/pasted most of ``summary.html`` into ``dev_summary.html`` to see how it will
work.

Creating the Individual Page Building Page
++++++++++++++++++++++++++++++++++++++++++

Rethinking the Approach to Development
--------------------------------------

What I'm trying to do is too complicated, both from the programming point of view and from the user interface point of
view. Team members, and my testers among the candidates, should be able to make comments on the actual activity pages
as they will be displayed to the rest of the users. A comment box at the bottom, or perhaps a sidebar, should be all
that is needed. This will be visible only to those with the proper credentials. Perhaps, somewhere --
config/utilities.py maybe -- I can make an is_advisor routine to help with this.

By the way, if I am going to have candidate testers I will probably want to create a new group called Testers for that
purpose. I could include Team, Supervisors and Administrators in the Testers group.

Anyway, this would allow the development app to concentrate on creating the activities. But how would the builders be
able to see what they will look like in the final version? Will I have to recreate each of the activity pages? Can there
be a side-by-side approach, building the final form of the page as the developer fills in a form at the side? This could
still be complicated to program but I have suspected the development pages were going to be complicated from the start.

I think I will concentate first on my testers. The sooner I get something online the better!

Narrative Walk-through for a Tester
***********************************

Sally has been invited, and has agreed, to be one of the candidates testing the website before it is ready for anyone
else. She goes to the website using her special temporary identity as a Tester.

She sees the Welcome page as it appears to everyone else but also sees a box at the bottom for comments. This box may
already have a comment from Fr. Jim about what he is especially interested in knowing about the page -- its overall
appearance, color scheme, whether it is obvious what a person is supposed to do when they get to the page, etc. She
makes her comments in a text area by the side of the comment box and clicking on a button that says "Submit Comment."
It immediately appears in the comment box and includes an "Edit" link at the end of it along with any previous comments
she may have made.

If she clicks on the "Edit" link she goes to another page where she can edit or delete the comment. [OR that comment
appears in the editing box along with buttons that say "Submit Edited Comment", "Cancel", or "Delete Comment."]

So it is on all of the pages of the website, including the help pages.

Thoughts After Writing the Narrative Walk-through
*************************************************

I can focus my efforts on creating an html page to include in all of the website's pages. I can put the
``{% include %}`` tag into ``base.html``. Perhaps I can call it ``tester_comments.html``. If the ``{% include %}`` tag
appears AFTER the footer, it will help separate the comments from the rest of the page.

This would require each view to send a flag as to whether the user is a tester to be checked at the beginning of
``tester_comments.html``.

It would also require a Comment model in some app. I suppose I can keep it in the development app since that is what it
is for but I may need an improved means of determining which page each comment belongs to: activity pages?, help pages?,
what? I wonder if there is a URL field I can use for this purpose...

There IS such a thing as a ``models.URLField`` it is a subclass of CharField with a ``max_length`` that defaults to
200. Somehow, when a comment is added, the url of the page it is sent from would be saved in this field and then, when
comments are displayed, only comments from that url, which is probably in the request someplace, will be supplied. This
only has to be done for Testers.

I will experiment now to find out what information is in the request for the welcome page...

Yes, it is, and the best way to access it is through the ``.path_info`` attribute. I might have tried to use ``.path``
but the Django Documents warned that some webservers include a WSGIScriptAlias in the ``.path`` but strip that off of
the ``.path_info`` attribute. Using ``.path_info`` makes for a better transition from development servers to the final
deployment servers.

Thus it should be fairly easy to match comments to the pages they belong on regardless of what kind of page they are. I
will have to make the Tester section look sufficiently different from the rest of it to clearly indicate that it won't
belong on the final webpages as seen by the candidates.

Starting to Implement Tester Comments
-------------------------------------

I've decided to create a new app to hold the Comment model but I need to decide on some good names. First, the app name.

Brainsorming Names
******************

Here is some brainstorming on app names:

tester_comments, comments, tester, reviewers, suggestions, overseers, managers, commenters, opinions, advisors

I put "tester" into WordPerfect and checked for synonyms and finally came up with "consultants."

I think I like advisors (or advisor) the best of those. Should it be singular or plural?

Now for model names:

Comment, Advice, Suggestion, Remark

I think I like Remark of those choices.

Again, using WordPerfect, I came up with Critique for the model name.

Starting the App
****************

``python manage.py startapp consultants`` should do it...

It did, and I added all the files it created to git.

I forgot, at first, to register the new app in INCLUDED_APPS and with the admin program. I noticed when I tried to do a
``makemigrations`` and it reported "No changes detected."

Model Design
************

I suspect the model design can be much the same as for the Christmas website except it needs to include the URLField to
identify which page each critique goes with.

Here is the first attempt at a design:

.. csv-table:: **Critique Model Field Design**
    :header: Name, Type, Attributes, Comments
    :widths: auto

    url, URLField, max_length=100, the page to which this Critique applies
    user, ForeignKey, settings.AUTH_USER_MODEL; on_delete=models.CASCADE, the user making this statement
    text, TextField, none, the critique itself

I am going to need to include a date field to record the date the critique is first posted and use that to list the
critiques in order of that date.

Designing the html
******************

I've decided to call it ``critiqe_area.html`` and have it appear at the bottom of every page for testers only. I think
it might be a good idea to implement some sort of toggle so the testers can turn it off and see the website without the
area at the bottom of each page, but I haven't implemented that yet.

The ``{% include %}`` statement at the end of ``base.html`` make it very easy to add this section to each page. I simply
have to make sure the context includes::

    ...
    'critiques': get_critiques(request.path_info),
    'tester': is_tester(request.user)``
    ...

and the template takes care of the rest.

How to Get Back to the Same Page After Submitting a Comment
***********************************************************

That's my current problem. When a user clicks the Submit button to enter a comment, a post method somewhere will need
to know the page it comes from, to save in the Critique model, and to use to get back to the same page. This seems to
imply that something in the template should already know what the path is that got to it. I will try
``{{ request.path_info }}`` to see if it displays anything...

YES!!! It worked! That means I can send it to a view in the consultants app, save the comment, and redirect to the same
page. Wonderful! How do I send it? I think I will try an <input> tag with type="hidden".

That works beautifully. Now, it might be nice to be able to turn the critique section on and off...

Toggling the Visibility of the Critique Section
***********************************************

There are two things I don't currently know how to do:

#.  Set a variable for a particular user without using the database (perhaps sessions data?)
#.  Get back to the page that sent the message in the first place.

I wonder of javascript might be the solution to both problems. Does javascript have global variables that can be set
when a website is first entered and then left alone until a user changes it? Where would that be done? What I know about
javascript so far seems to indicate it is focused on only one page at a time. I will have to read more.

No, I don't think that is going to work. Of course, I haven't learned, yet, to keep my javascript code in a separate
file and maybe I could do it there, but the way I'm doing things now, every time the file containing my javascript code
is loaded the global variables would get reset to their initial value.

Using Django's sessions seems like a better approach. It does save the information in the database but I don't have to
create a separate model for it, which is what I didn't want to do before. According to Django's website at:
https://docs.djangoproject.com/en/2.0/topics/http/sessions/ I would need to add 'django.contrib.sessions' to my
INSTALLED_APPS setting but it is already there.

All I had to do was to create a ToggleCritiqueView as follows::

    class ToggleCritiquesView(View):

        def get(self, request):
            if request.session.get('critiques_visible', True):
                request.session['critiques_visible'] = False
            else:
                request.session['critiques_visible'] = True
            return redirect('/activity/welcome/')

(The redirect url is temporary until I can figure out how to get back to the same page I left.) Then I could use it
in ``base.html`` as follows::

    {% if tester %}
        {% if request.session.critiques_visible %}
            {% include "consultants/critique_area.html" %}
        {% endif %}
    {% endif %}

I did, of course, have to modify my ``constultants/urls.py`` file as follows::

    urlpatterns = [
        path('', CritiqueView.as_view(), name='save_critique'),
        path('suggestions/toggle_critiques', ToggleCritiquesView.as_view(), name='toggle_critiques'),
    ]

Now to tackle the problem of getting back to the page I came from after the toggle...

It turned out to be not too difficult. A ``request`` has a META attribute which contains, among many other things, a
QUERY_STRING header which returns whatever is sent after a question mark in a url. (See
https://docs.djangoproject.com/en/2.0/ref/request-response/ .) Thus I was able to write this in my ``header.html``::

    {% if tester %}
        <div class="dropdown u-pull-right">
            <a class="menu-button" href="{% url 'toggle_critiques' %}?next={{ request.path_info }}">
                Toggle Critiques
            </a>
        </div>
    {% endif %}

and this in consultants/views.py::

    class ToggleCritiquesView(View):

        def get(self, request):
            if request.session.get('critiques_visible', False):
                request.session['critiques_visible'] = False
            else:
                request.session['critiques_visible'] = True
            return redirect(request.META['QUERY_STRING'].replace('next=', ''))

Editing and Deleting Critiques
******************************

That turned out to be an interesting process. Since the edit page and the delete page for critiques do not come
directly from the page being commented on, I had to pass a ``page_url`` context from .html pages to views and back
again. Taking a tip from what I did to toggle the appearance of the critiques section, I used the ``?next=``
QUERY_STRING to pass the url from the ``critique_area.html`` page, and later the ``edit-critique.html`` page and
picked it up in the ``get`` methods. Then I passed it in the context sent to the html page that ``get`` returned and
picked it up in the ``post`` method. See the code segments below:

**From critique_area.html**::

    {% if critique.user == user %}
        <a href="{% url 'critique_edit' critique.pk %}?next={{ request.path_info }}"> Edit</a>
    {% endif %}

**From consultants/views.py**::

    class EditCritiqueView(View):
        template_name = 'consultants/edit-critique.html'

        def get(self, request, pk=None):
            page_url = request.META['QUERY_STRING'].replace('next=', '')        # the page from which this came
            critique = Critique.objects.get(pk=pk)
            context = {'page_url': page_url,
                       'critique': critique,
                       'critiques': get_critiques(request.path_info),
                       'tester': is_tester(request.user)}
            return render(request, self.template_name, context)

        def post(self, request, pk=None):
            page_url = request.POST['page_url']     # page_url obtained from get method passed through edit-critique.html
            if request.POST['button'] == 'OK':
                critique = Critique.objects.get(pk=pk)
                critique.text = request.POST['entry']
                critique.save()
            return redirect(page_url)

**From edit-critique.html**::

    <a class="offset-by-four four columns button"
       href="{% url 'critique_delete' critique.pk %}?next={{ page_url }}">Delete</a>

**From consultants/views.py**::

    class DeleteCritiqueView(View):
        template_name = 'consultants/delete_critique.html'

        def get(self, request, pk=None):
            page_url = request.META['QUERY_STRING'].replace('next=', '')        # handed through edit-critique.html
            critique = Critique.objects.get(pk=pk)
            context = {'page_url': page_url,
                       'critique': critique,}
            return render(request, self.template_name, context)

        def post(self, request, pk=None):
            page_url = request.POST['page_url']         # page_url as obtained from get method above
            if request.POST['user-choice'] == 'Delete':
                critique = Critique.objects.get(pk=pk)
                critique.delete()

            return redirect(page_url)

At the end I realized that the delete pages could not have a critique area since, once the correpsonding entry is
delete, it would throw an error. I supposed I could have done something with ``try... except`` but it would be
complicated, perhaps involving the deletion of comments in the database for no-longer-existing pages.

This was complicated enough!

Final Preparation Before Initial Deployment
-------------------------------------------

I don't know if I've checked whether the display is correct for all discussion types or, for that matter, whether
Anonymous discussions work at all. The idea is that for Semi-Anonymous discussions the names should be visible to team
members but not to candidates. For anonymous discussions I will need to have a generic user.

Looking at ``base_discussion.html`` I can see that there is not yet any provision for distingishing team members, and,
by looking in the admin, I can see there is not yet any Generic user. Obviously there must not be any provision in
``discussion/views.py`` for saving Anonymous responses under the Generic User either.

.. note::

    I got all that working but, apparently, without making any comments here about it. I called the generic user
    Unknown User with a USERNAME of Unknown.

    I've implemented the proper display for each type of discussion. I think it is all working and I can consider a
    test deployment just for my testers.

    Perhaps I should supply some improved content however, and maybe complete the help section.

Before going online I will have to:

*   disable the development link or send it to a page explaining what it may do (or create a suggested activities page)
*   Make sure every type of activity is represented under "Noah, the Real Story"
*   Fill out "God, are you there?"
*   Create an activity based on Chosen materials - perhaps one of the sets of challenges?
*   Complete a help page for dicussions
*   Put more information about the website on the login page for those who click in from the parish website

Notes on Updating the Activities
********************************

While doing this I discovered a bug in the way true/false responses were recorded. A user's response was always
recorded as the correct response. I've changed that to::

    if not page.opinion:
        response.correct = user_response == page.tf_answer

I will check to see that it's working...

No, it doesn't seem to be. Time to investigate...

The problem was that user_response was coming from a line that said ``user_response = request.POST['choice']`` which
returns a string. Thus ``user_response == page.tf_answer`` would always be false since an str would never match a
boolean. Doing it this way made it work::

    try:
        user_response_string = request.POST['choice']
    except KeyError:
        self.template_name = 'activity/true-false.html'
        context = {'activity':activity, 'page':page, 'response':None}
        context['error_message'] = 'You must select either True or False.'
        return render(request, self.template_name, context)
    user_response = (user_response_string == 'True')
    response = Response(user=request.user, activity=activity,
                        page=page, true_false=user_response,
                        completed=True)
    if not page.opinion:
        response.correct = (user_response == page.tf_answer)
    response.save()

But in the process of studying that I tried to delete an earlier response without deleting later ones to see what it
would do to whether a page could be reached.

I deleted page 3 from the Noah activity after having completed the first six. Clicking the 'Back' button would get me
to page 5 but not to page 4. Instead it went to the summary page. On the summary page all of the completed exercises
showed buttons that said "Review it..." except for number 3 which said "Do it...". However, I could not click "Review
it..." in number four to get there. I just stayed on the summary page. (Actually it was going to
``activity/noah/4/`` but got redirected to ``activity/noah/summary/``.

Studying ``PageView`` and the ``allowed`` method in the ``Page`` model I see that it is because the ``allowed`` method
only returns false if the PRECEDING page has not been done. It leaves all the others uninvestigated. I suppose the
``allowed`` method needs to check them all and the summary page needs to stop adding buttons once it comes to an
incomplete activity.

Here are the changes I made:

**activity/models.py PageModel.allowed**::

    def allowed(self, user, activity_slug, page_index):
        """
        Returns True if the user is allowed to go to the page at /activity/<activity_slug>/<page_index>, having
        completed the page just before this one
        :return: boolean
        """
        if self.index == 1:
            return True             # user is always allowed to go to the first page
        else:
            activity = Activity.objects.get(slug=activity_slug)
            pages = Page.objects.filter(activity=activity)
            result = True
            for page in pages:
                if page.index < page_index:
                    responses = Response.objects.filter(user=user, activity=activity, page=page)
                    if len(responses) == 0:
                        result = False
                        break
            return result

**activity/views.py PageView**::

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        pages = Page.objects.filter(activity=activity.pk)
        responses = Response.objects.filter(user=request.user, activity=activity.pk)
        data = []
        first_pass = True                          # this changes as soon as an incomplete page is found
        for page in pages:
            if responses.filter(page=page.pk) and first_pass:
                data.append((page, 'Completed'))    # If user has a response, call the page complete
            elif first_pass:
                data.append((page, 'Up next...'))   # This is the next page to do
                first_pass = False                  # after that, enter 'Pending' for the rest of the pages
            else:
                data.append((page, 'Pending'))
        group_names = get_group_names(request.user)
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data,
                                                    'group_names': group_names,
                                                    'critiques': get_critiques(request.path_info),
                                                    'tester': is_tester(request.user)})

**activity/templates/activity/summary.html**::

    <td>    <!-- Third Column -->
        {% if progress == 'Pending' %}
            ''
        {% elif progress == 'Up next...' %}
            <a class="button button u-full-width"
               href="/activity/{{ activity.slug }}/{{ page.index }}/">
                Do it...
            </a>
        {% else %}
            <a class="button button u-full-width"
               href="/activity/{{ activity.slug }}/{{ page.index }}/">
                Review it...
            </a>
        {% endif %}
    </td>

This was probably unnecessary since I probably prevent users from deleting earlier pages after completing later ones.

More Ideas
----------

But I have two big ideas perhaps to implement before going online. One is to create a 'Challenge' page to accomodate
the Challenges of the Chosen program.  The other is to create a page where team members can see the progress of the
candidates or perhaps just their candidates. The former would be easier to implement first. I think the information is
already available.

I decided to change the name of the 'Development' link in the header menu to 'Team Pages'. That won't be hard at all!...

By accident I changed the link in the help menu also, though I don't have any help pages to go to yet.

I created a ``sorry.html`` page to use for sections I don't have ready yet, and made the "Team Pages" header menu button
into a dropdown menu. The help -> Team Pages selection goes to the ``sorry.html`` page but the Team Pages -> Candidate
Reports goes nowhere at the moment. I will need a url path and a view to make that work.

Candidate Reports
-----------------

After getting the website online, at least for Sylvia, I thought of a, hopefully, easy way to create a report for team
members on how the candidates are answering the questions. A simple table at the bottom of each activity page, only
visible to team members, and reporting on which candidates have responded and information about their response. This
will not have to be done for discussion pages since it will either be visible to the team members anyway, or none of
their business.

Here is a table of what needs to be displayed on each of the other page types:

.. csv-table:: **Candidate Reports to be Visible on Each Page Type**
    :header: Page Type, Information to be Available
    :widths: auto

    Welcome, entire list of candidates with list of which numbered activities they have started
    Summary, entire list of candidates and percentage of completion for this activity
    Instruction, the date and time when each participating candidate completes it
    Essay,  each participating candidate's response - at least part of it - perhaps a link to see the whole thing
    Multi-Choice, each participating candidate's response and; if applicable; whether it is right or wrong
    True/False, each participating candidate's response and; if applicable; whether it is right or wrong
    Challenge, each participating candidate's response

Separate html files could be made for each report for each page type and they can be included (with {% include %}) into
each existing page IF the user is a team member. Each report should be alphabetized by last_name and then first_name.

It seems a different context entry may be necessary in each case, but perhaps I can always call it 'report'. I will try
to implement these reports on the Welcome Page first.

Candidate Report on the Welcome Page
************************************

This report will need an entire list of candidates with a list of activity numbers for the activities each one has
entered. It was not very difficult to write a ``get_welcome_report`` function in ``config/utilities.py`` to supply the
report::

    def get_welcome_report():
        """
        Gets the candidate report for the welcome page as to which activities the user has so far participated in.
        :return: an ordered list of tuples ordered by last_name, first_name with the user's full name in position 0
                and a string of the activities in which they have so far participated in position 1.
        """
        users = User.objects.all().order_by('last_name', 'first_name')
        activities = Activity.objects.all()
        report = []
        for user in users:
            if is_candidate(user):
                if user.first_name != 'Unknown':
                    user_name = user.last_name + ', ' + user.first_name
                    activity_list = ''
                    for activity in activities:
                        if len(Response.objects.filter(user=user, activity=activity)) != 0:
                            if len(activity_list) == 0:
                                activity_list += str(activity.slug)
                                print('activity_list = ', activity_list)
                            else:
                                activity_list += ', ' + str(activity.slug)
                    report.append((user_name, activity_list))
        return report

Candidate Report on the Summary Page
************************************

This report will need to compute the percentage of completion of this activity for each candidate.


Narrative Walkthrough of Challenge Pages
----------------------------------------

When Diego clicks into the current Challenge page he sees abbreviated names of the three challenges from Chosen next to
check boxes. He clicks the top box to choose that challenge and, immediately, a textarea appears below that line and
above the next checkbox line. He types in whatever that challenge calls for. When he clicks 'Submit' it appears below
the checkbox with an edit link.

There is also, next to each challenge name, a link or button to view current contributions. Diego wants to see what
others have entered for the same challenge he tried and so he clicks that link/button named "See All Entries." That
takes him to a page that lists everyone's entries so far to that challenge. He sees his own response at the bottom,
since he just entered it, and it has an 'Edit' link next to it in case he wants to edit it from this page. There is also
a button at the bottom that will take him back to the challenge page. ("Return to Challenges").

Later, a little later in the month, Diego returns to the Challenge page and decides to do another one. This is permitted
and works out as described above.
