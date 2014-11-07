#! /usr/bin/env python
#all the imports
import sqlite3
import cgi,cgitb

cgitb.enable()
form = cgi.FieldStorage()
conn = sqlite3.connect('participants.db')
db = conn.cursor()

name = form.getvalue('name')
email = form.getvalue('email')
android = form.getvalue('android')
twitter_account = form.getvalue('twitter_account')
twitter_freq = form.getvalue('twitter_freq')
facebook_account = form.getvalue('facebook_account')
facebook_freq = form.getvalue('facebook_freq')
whatsapp_account = form.getvalue('whatsapp_account')
whatsapp_freq = form.getvalue('whatsapp_freq')
google_account = form.getvalue('google_account')
google_freq = form.getvalue('google_freq')
instagram_account = form.getvalue('instagram_account')
instagram_freq = form.getvalue('instagram_freq')
foursquare_account = form.getvalue('foursquare_account')
foursquare_freq = form.getvalue('foursquare_freq')
device_analyzer = form.getvalue('device_analyzer')
android_sms = form.getvalue('android_sms')
gmail_account = form.getvalue('gmail_account')
facebook_account_details = form.getvalue('facebook_account_details')
whatsapp_account_details = form.getvalue('whatsapp_account_details')
social_media_account_details = form.getvalue('social_media_account_details')
sms_messages = form.getvalue('sms_messages')

#debugging
print 'Content-Type: text/html'
print
print '<html>'
print '<head><title>Thanks for submitting!</title></head>'
print '<body>'
print '<h2>Thanks for submitting, we will get back to you soon if you meet the necessary qualifications!</h2>'
print '</body>'
print '</html>'



db.execute('insert into participants (name,email,android,twitter_account,twitter_freq,facebook_account,facebook_freq,whatsapp_account,whatsapp_freq,google_account,google_freq,instagram_account,instagram_freq,foursquare_account,foursquare_freq,device_analyzer,android_sms,gmail_account,facebook_account_details,whatsapp_account_details,social_media_account_details,sms_messages) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ', [name,email,android,twitter_account,twitter_freq,facebook_account,facebook_freq,whatsapp_account,whatsapp_freq,google_account,google_freq,instagram_account,instagram_freq,foursquare_account,foursquare_freq,device_analyzer,android_sms,gmail_account,facebook_account_details,whatsapp_account_details,social_media_account_details,sms_messages])

conn.commit()
conn.close()
