### Before you run the server, you'll need to set some values in constants.py (mainly emails) and also set up an app password on gmail. Follow the steps below:

1. Create an app password for the gmail account that you want this code to send emails from. Learn how to do that
   from [support.google](https://support.google.com/accounts/answer/185833?hl=en.)
   or [devanswers](https://devanswers.co/create-application-specific-password-gmail/). If you don't trust doing this on
   your main email account, consider creating a new gmail account for this purpose.
2. Open up constants.py. Set the SENDER and SUPER_SECRET_PASSWORD strings to be your email address and app password,
   respectively. Note: your Gmail password is NOT an app password!
3. Add all email recipients to CHANGE_LISTENERS. Maybe you want to add all your friends who are also looking for product
   updates or just yourself.
4. Add a list of emails (or just 1) to ADMINS. These emails will receive an hourly monitoring email as well as an email
   if the main loop crashes (although the loop will wait and retry on crash). If you don't want to receive these emails,
   leave this blank or deactivate the ACTIVATE_HOURLY_MONITORING constant.

An example of what the final result might look like:

```
SENDER = 'pokemon.for.all@gmail.com'
SUPER_SECRET_PASSWORD = 'ABCDEFGHIJKLMNOP'
CHANGE_LISTENERS = ['my.email.address@gmail.com', 'my.buddy@gmail.com']
ADMINS = ['my.email.address@gmail.com']
```

Once you're done setting these values, you can simply run the server with Python either in cmd/bash OR
download [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) and run it from there. Otherwise,
installing the latest version of Python3 and running `python main.py` from this directory should suffice.