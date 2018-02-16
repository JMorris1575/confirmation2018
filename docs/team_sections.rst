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

