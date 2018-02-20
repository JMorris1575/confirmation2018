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

The Development App
*******************

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
    develop/activities/<activity>/, DevActivitySummaryView, dev_activity_summary, goes to the development summary page
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

I may need two models for comments, one for general comments and one for parnter comments. Perhaps TeamComment and
PartnerComment can be the names of the models. There will have to be enough detail in both so that the Activity and
Page can be determined that the comment applies to and there will have to be some means of assuring that only
partners on this activity can see the current state of the activity and other partner's comments.

Once an activity is open for general comments, should I maintain two copies of it, one that was published for all the
team to see and one, the updated version, that only the partners can see? That sounds difficult, and perhaps a waste
of database space unless the extra copies are deleted when they are no longer needed. 