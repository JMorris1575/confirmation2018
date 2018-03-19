==========
Deployment
==========

I just created a new website called **Confirmation18** on webfaction.com. It has a domain of
confirmation.jmorris.webfactional.com and has two apps: one, a Django 2.02 app called conf18, and another, a static app
called conf_static.

I also created a new Mailbox, called st_basil, and a new e-mail address:
st_basil_confirmation@confirmation.jmorris.webfactional.com which automatically forwards anything coming in to
FrJimMorris@SaintBasilCatholicChurch.org.

Using ``ssh jmorris@jmorris@webfactional.com`` I checked out the website and it is ready to go when I am ready to
deploy the website -- even if only for testing and comments.

Challenges
----------

Remembering what I did so I can write it here

Problems generated until I changed to a static only app on webfaction

sending the database to webfaction

Testing
-------

Without documenting it, unfortunately, at least not here (maybe it's in team_sections?) I implemented a whole testing
system where the testers are in their own group and can see and make comments and critiques on the website as it
appears at ``confirmation.jmorris.webfactional.com``. The testing has been very valuable but I find I am far from
being ready to go completely public with the site. Here are the problems unearthed so far:

Multiple Hits on Submit Buttons
*******************************

If a user clicked a submit button several times in rapid succession, before the system left the form page, their
response got saved several times when it wasn't supposed to be.

To solve this I created a ``can_respond`` method in the activity Page model and used it for all of the different page
types in the post method of the activity PageView. I made similar changes to the Response model and DeleteView to
prevent a response from being deleted if other responses had been made later.

Building a More Responsive Website
**********************************

I looked at the website on my Android tablet and it didn't look very good. I'm working my way through a course called
something like "Responsive Design for Beginners" on Udacity to learn more on how to make the site look better on
different size devices.

Problems With Security
**********************

I didn't think it would be a problem not using the https protocol but, as it turns out, the Chrome Browser does not
seem to allow ANY logging in on what it deems to be an insecure website. I am looking into how to use the https
protocol on a webfaction website. There is a non-profit outfit called Let's Encrypt at https://letsencrypt.org that
offers free ssl certificates that webfaction can use but their preferred method of installation doesn't actually work
for webfaction websites. Searching around some I found the following websites with the most promising set of
instructions:

http://bcc.npdoty.name/directions-to-migrate-your-WebFaction-site-to-HTTPS

https://github.com/will-in-wi/letsencrypt-webfaction

I will summarize the instructions on the first website below:

#.  Create a secure version of the website with the WebFaction Control Panel

    *   suggested name for new site: existingname-secure
    *   suggested domains: my custom domain confirmation.jmorris.webfactional.com
    *   I don't have a custom domain so I suppose the latter will be enough
    *   Under Contents, click "Re-use an existing application" use all the applications (static too)

#.  Test to make sure the site works over https

    *   He says it should work without disrupting the original site
    *   But there may be issues with images and other content still being loaded from the insecure site
    *   I'm not sure this will apply to me since I'm using the static app which may also be under https

#.  Get a free certificate for the domain

    *   use ssh to get into web506.webfaction.com
    *   run: ``GEM_HOME=$HOME/.letsencrypt_webfaction/gems RUBYLIB=$GEM_HOME/lib gem2.2 install letsencrypt_webfaction``
    *   Edit ~/.bash_profile to include: ``function letsencrypt_webfaction {PATH=$PATH:$GEM_HOME/bin GEM_HOME=$HOME/.letsencrypt_webfaction/gems RUBYLIB=$GEM_HOME/lib ruby2.2 $HOME/.letsencrypt_webfaction/gems/bin/letsencrypt_webfaction $*}``
    *   run: ``letsencrypt_webfaction --letsencrypt_account_email FrJamesMorris@gmail.com --domains confirmation.jmorris.webfactional.com --public /home/jmorris/webapps/conf18/confirmation/webfaction_wellknown/ --username jmorris --password dylan-selfie``
    *   that should put a certificate in the SSL certificates tab in the WebFaction Control Panel
    *   go to the Websites tab, select the secure version of the website and choose the new certificate

#.  Test the website again

    *   this time should work without mixed content warnings

#.  Set up automatic renewal of the certificate

    *   run: ``EDITOR=nano crontab -e``
    *   add: ``* * * * * echo "cron is running" >> $HOME/logs/user/cron.log 2>&1`` to the file that appears(?)
    *   check ``~/logs/user/cron.log`` after a few minutes to see that it is echoing "cron is running"
    *   run the following commands or complete the indicated steps:

        *   ``mkdir le_certs``
        *   ``touch le_certs/config.yml``
        *   edit config.yml in notepad++ to include the following:

            *   letsencrypt_account_email: 'FrJamesMorris@gmail.com'
            *   api_url: 'https://api.webfaction.com/'
            *   username: 'jmorris'
            *   password: 'dylan-selfie'

        *   edit crontab

            *   erase the existing test line
            *   add the following all on one line (see the bcc website above)
            *   0 4 15 \*/2 * PATH=$PATH:$GEM_HOME/bin GEM_HOME=$HOME/.letsencrypt_webfaction/gems
            *   RUBYLIB=$GEM_HOME/lib /usr/local/bin/ruby2.2 $HOME/.letsencrypt_webfaction/gems/bin/letsencrypt_webfaction
            *   --domains confirmation.jmorris.webfactional.com --public /home/jmorris/webapps/conf18/
            *   --config /home/jmorris/le_certs/config.yml >> $HOME/logs/user/cron.log 2>&1

#.  Redirect the original http:// site to the new https:// site as explained on the bcc website

Possible Solutions
++++++++++++++++++

Getting a free certificate for the domain hasn't worked very well yet. The problem has to do with the ACME Challenge not
being served by my Django application. There are numerous instructions online as to how to go about doing this but I'm
not up to following them right now.

Here are some places to check:

https://github.com/will-in-wi/letsencrypt-webfaction    the third bullet point of the Usage/Options section

https://github.com/will-in-wi/letsencrypt-webfaction/issues/24  the website linked to from the one above

https://github.com/will-in-wi/letsencrypt-webfaction/wiki/Django    the Django wiki page referred to in the link above

https://github.com/will-in-wi/letsencrypt-webfaction/issues/85  the alternative method referred to in the link above

https://stackoverflow.com/questions/38443572/using-lets-encrypt-without-control-over-the-root-directory from link above

It seems that the ``.well-known`` directory's location is set by the ``letsencrypt_webfaction`` --public parameter. If I
change that to something accessible, and perhaps adjust my site's urlconfig accordingly, it may solve the problem. But,
again, that's a problem for another day.

By following a link on the last page listed above I came to this possibility:

https://pypi.python.org/pypi/django-letsencrypt

Since I don't know what the docs are talking about when it come to creating and testing my ACME challenge objects I'm
hoping that's what letsencrypt_webfaction takes care of on its own -- once it has a way to create and access a
``/.well-known/`` folder.

A Plan for Installing a SSL Certificate
+++++++++++++++++++++++++++++++++++++++

#.  ``pip install django_letsencrypt`` in PyCharm's Terminal

    *   It turns out it was already installed in my ``conf`` environment
    *   Is that true for all my machines considering the different ways the ``conf`` env might have been created?

#.  Find out where the app ``letsencrypt`` goes and add it to INSTALLED_APPS
    *   in ``config/base.py`` I entered ``'letsencrypt.app.LetsEncryptConfig',`` to the existing list

#.  Add ``path('\.well-known/', include('letsencrypt.urls')),`` to config/urls.py

    *   I converted the url() on the pypi website to a path() and had to remove the r and the ^
    *   Done

#.  Run ``python manage.py migrate`` on the local machine.

    *   Done -- this is what warned me about the '^' character

#.  Research ACME Challenge objects and try to create some in the admin.

    *   The letsencrypt app added a Let's Encrypt section to the admin
    *   It includes an ACME Challenges section with no challenges
    *   Each challenge consists of
        *   Challenge -- an identifier for this challenge
        *   Response -- the response expected for this challenge
        *   There is also a Metadata section with ID and Link
    *   I created a challenge named ``Jim`` with response: ``James Alfred Thomas Morris``

#.  Test some ACME Challenge objects by visiting them at ``[website]/.well-known/acme-challenge/challenge_text``

#.  Figure out how to move all this to webfaction.

I don't think this will work as is. It requires me to put challenges into the model but ``letsencrypt_webfaction`` does
that, not me. I may, however, be able to design my own app, based on this one to deliver whatever text in whatever file
``letsencrypt_webfaction`` places into the .well-known directory.

Yet, there may be a better solution buried someplace on the websites listed above. I should look there first.

I did, but no solution as simple as making my own app jumped out at me. So, here goes:

Making an App to Handle .well-known Tests
+++++++++++++++++++++++++++++++++++++++++

I think what I have to do is:

#.  Create a webfaction_wellknown app with ``startapp``. Add it to INSTALLED_APPS
#.  Create a path in ``config/urls.py`` to include ``webfaction_wellknown.urls``
#.  Create ``webfaction_wellknown.urls`` to point ``.well-known/<str:challenge_file>/`` to the proper view
#.  Create the corresponding view in ``webfaction_wellknown.views`` to return the text from the file
#.  Test it with some silly files.
#.  Try it out on webfaction

My app works on the local machine, now to try it out on webfaction. I will do a commit and write down the names of the
files and directories that need to be transferred, transfer them, and then try to run ``letsencrypt_webfaction`` again.

So far no luck. But I'm getting closer. The oddball files are being saved in
``webfaction_wellknown/.well-known/acme-challenge/``, I just haven't been able to deliver them yet.

I realized, a little later, that I hadn't restarted the apache2 server. That may have been the reason I got the 404
error. I will try again now, and if that doesn't work, after restarting...

Setting My bash_profile for SSH
*******************************

While reading the instructions to create the above summary I discovered something I've been wanting to know: how to get
the prompt the way I like it when I ssh into my webfaction site. I created a .bash_profile file with  the PS1="\\w\\$: "
command in it and it gets done! :-) :-) :-)

Later, when trying to follow the directions to get a certificate, I discovered that I was saving .bash_profile in dos
format and it needs to be in unix format -- line endings are different. Using:

``dos2unix .bash_profile``

did the trick. Then using:

``source $HOME/.bash_profile``

read it in... I think.

Making the Website Secure
*************************

When I finally got ``letsencrypt_webfaction`` to work it gave me the following message:

``Your new certificate is now created and installed.
You will need to change your application to use the confirmation_jmorris_webfactional_com certificate.
Add the `--quiet` parameter in your cron task to remove this message.``

I notice that it doesn't say HOW to change my application but I hope it just means to add it to the application with
webfaction's control panel.

I don't yet know where my cron task is but I think that is one of the later steps I am going to follow.

Once I managed to create a certificate, I went to the original Website record on webfaction (Domains/Websites ->
Websites), deleted the Conf18-Secure website, since it didn't seem to be doing anything and was getting in the way of
adding the certificate to the original website, and added the new certificate to the ``Confirmation18`` website.

Writing a cron Task
+++++++++++++++++++

I pretty much had to use one of linux's editors for this -- yechhh!

The easiest to use was nano which I used to edit crontab as follows:

``EDITOR=nano crontab -e``

After adding the new line I wanted to add I pressed ctrl-O to save and ctrl-X to exit. The test cron job worked alright.

To create the config.yml file in a new le_certs directory I did the following:

``mkdir le_certs``
``touch le_certs/config.yml``
``nano le_certs/config.yml``

then I added the following lines to the file thus created and entered for editing::

    letsencrypt_account_email: 'FrJamesMorris@gmail.com'
    api_url: 'https://api.webfaction.com/'
    username: 'jmorris'
    password: 'dylan selfie'

Finally, I edited crontab as follows:

EDITOR=nano crontab -e

and added the following all on one line::

    0 4 15 */2 * PATH=$PATH:$GEM_HOME/bin GEM_HOME=$HOME=$HOME/.letsencrypt_webfaction/gems
    RUBYLIB=$GEM_HOME/lib /usr/local/bin/ruby2.2 $HOME/.letsencrypt_webfaction/gems/bin/letsencrypt_webfaction
    --domains confirmation.jmorris.webfactional.com
    --public /home/jmorris/webapps/conf18/confirmation/webfaction_wellknown/
    --config /home/jmorris/le_certs/config.yml >> $HOME/logs/user/cron.log 2>&1

I put a reminder in my palm organizer for May 15 to check to see if this gets done. It should show some kind of report
in ``jmorris/logs/user/cron.log``

Redirecting Traffic to the Secure Website
+++++++++++++++++++++++++++++++++++++++++

So far, though I can get into the website in Firefox, the static content does not serve well -- including the css so the
site looks awful!

Following the instructions at:

https://docs.webfaction.com/software/static.html#static-redirecting-from-http-to-https

I will try to alleviate that problem.

