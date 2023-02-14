# bug_tracking_tool

tracking bug ticket on jira platform

## jira_bug_tracking.py <br>
<br>
Step 1. Connect to JIRA <br>
Step 2. download data in data file (.json) <br>
Step 3. analyzing  json file <br>

  * story_number <br>
  * story_title <br>
  * story_point <br>
  * sprint_number <br>
  * subtask_number <br>
  * subtask_title <br>
  
  * Save the above contents result file (.txt) <br>
  
Step 4 visualization  <br>
  * generate .html store in result file <br>
  * x -> story number in a sprint <br>
  * y -> story point , number of each subtasks(eg. bug ticket) <br>
<br>

Step 5 sending email <br>

-------------

## send_email.py <br>

use SMTP protocol and mime to implement the sending email function

-------------

## config.ini (external args file) <br>



JURL = jira server <br>
JUSER =  user account <br>
JPASSWD = user auth token <br>
SEARCH = what you want to search in summary <br>
JPROJECT = not yet <br>
JSPRINT = not yet <br>
JVERSION = not yeet. <br>

[MAIL]

default is using outlook, if you need to use another email server (eg. gmail), you need to check the port number and server <br>
PORT = 587 <br>
SERVER = smtp.office365.com  <br>
MSG_FROM = email account <br>
PASSWD = email passwrod <br>
MSG_TO = receiver <br>




  
  

