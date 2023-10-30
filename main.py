#InCollege Solution Team Nevada

#Connect to SQLite database
import json
import os
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)

def create_db():
  conn = sqlite3.connect('accounts.db')
  # Create a cursor object to execute SQL commands
  cursor = conn.cursor()

# Execute a SQL command to create the main accounts table
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS accounts (
          user_num INTEGER PRIMARY KEY,
          user_name TEXT,
          password TEXT,
          first_name TEXT,
          last_name TEXT,
          controls TEXT,
          language TEXT,
          university TEXT,
          major TEXT,
          friends TEXT,
          invites_sent TEXT,
          invites_received TEXT
          )
  ''')
# Execute SQL command to create a table storing posted jobs - added a column to account for jobs marked as applied for
  
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS jobs (
          job_num INTEGER PRIMARY KEY,
          user_num INTEGER, 
          first_name TEXT,
          last_name TEXT,
          title TEXT,
          description TEXT,
          employer TEXT,
          location TEXT,
          salary TEXT,
          applied BOOLEAN DEFAULT FALSE)
  ''')

  return conn

# function to delete a job posting from the database using SQL, job_num is the number of the desired job to delete

def all_job_list(conn, user_num):
  cursor = conn.cursor()  
  cursor.execute('SELECT * FROM jobs WHERE user_num = ?', (user_num,))
  jobs = cursor.fetchall()
  return jobs

def delete_job(conn, job_num):
  cursor = conn.cursor()  
  cursor.execute('DELETE FROM jobs WHERE job_num = ?', (job_num,))
  conn.commit()

# function to mark a job as "saved" for a specified user
def save_job(conn, user_num, job_num):
  cursor = conn.cursor()
  cursor.execute('INSERT INTO saved_jobs (user_num, job_num) VALUES (?, ?)', (user_num, job_num))
  conn.commit()

# function to provide a list of saved jobs for a specified user
def get_saved_jobs(conn, user_num):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM jobs INNER JOIN saved_jobs ON jobs.job_num = saved_jobs.job_num WHERE saved_jobs.user_num = ?', (user_num,))
  return cursor.fetchall()

# function to unmark a job from being "saved" for a specified user
def unsave_job(conn, user_num, job_num):
  cursor = conn.cursor()
  cursor.execute('DELETE FROM saved_jobs WHERE user_num = ? AND job_num = ?', (user_num, job_num))
  conn.commit()

#retrieve all accounts from database
def all_accounts(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM accounts')
  rows = cursor.fetchall()
  return rows

# function to mark a job as "applied"
def apply_job(conn, cursor, job_num):
  cursor.execute("UPDATE jobs SET applied = TRUE WHERE job_num = ?", (job_num,))
  conn.commit() 

# function to display a list of all jobs applied for to the user
def get_applied_jobs(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM jobs WHERE applied = TRUE')
  applied_jobs = cursor.fetchall()
  return applied_jobs

# function to display a list of all jobs not yet applied for
def get_unapplied_jobs(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM jobs WHERE applied = FALSE')
  unapplied_jobs = cursor.fetchall()
  return unapplied_jobs

#retrieve all jobs from database
def all_jobs(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM jobs')
  rows = cursor.fetchall()
  return rows


#given username and valid password, add into database
def add_account(conn, username, password, first_name, last_name, uni, major):
  cursor = conn.cursor()
  cursor.execute(
      '''
    INSERT INTO accounts (user_name, password, first_name, last_name, controls, language, university, major, friends, invites_sent, invites_received) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (username, password, first_name, last_name, 'y,y,y', 'e', uni, major, '', '', ''))


# ================== EPIC 5 - Profiles ==================#
# loads profiles info and returns a python dictionary
def load_profiles():
  if not os.path.exists('profiles.json'):
    file = open('profiles.json','w')
    file.write('{}')
    file.close()
  file = open('profiles.json')
  profiles = json.load(file)
  file.close()
  return profiles

# updates database with uni, major info when user updates profile
def update_db_uni_major(conn,user_name,uni,major):
  cursor = conn.cursor()
  cursor.execute("UPDATE accounts SET university = ?, major = ? WHERE user_name = ?", (uni,major,user_name))
  conn.commit()

def create_profile(account, conn):
  cursor = conn.cursor()
  print(account[0])
  print("Creating your profile:")

  title = input(
      "Enter your title (e.g., '3rd year Computer Science student'): ")
  major = input("Enter your major: ").title()
  university = input("Enter your university: ").title()
  about = input("Enter a paragraph about yourself: ")

  cursor.execute(
        "INSERT INTO profiles ( user_name, title, major, university, about) VALUES (?, ?, ?, ?, ?);",
        (account[0][1], title, major, university, about))
  conn.commit()
  print("Profile created successfully!")

# Function to build a profile
def build_profile(profiles, user_name, first_name, last_name):
  print("\nBuild your profile here. 'q' at any stage to quit")
  #create dictionary entry if it does not exist
  if user_name not in profiles.keys():
    profiles[user_name] = {}
    
    #initialize profile fields to empty fields
    profiles[user_name]['title'] = ''
    profiles[user_name]['major'] = ''
    profiles[user_name]['uni'] = ''
    profiles[user_name]['uni_abbr'] = ''
    profiles[user_name]['about'] = ''
    profiles[user_name]['school'] = ''
    profiles[user_name]['degree'] = ''
    profiles[user_name]['yrs'] = ''
    profiles[user_name]['num_jobs'] = 0
    profiles[user_name]['exp'] = {}

  #track num of changes made
  num_changes = 0
  #ask for user input to fill in fields
  if len(profiles[user_name]['title']) == 0:
    title = input("Enter your title: ")
    if title == 'q':
      return
    profiles[user_name]['title'] = title
    num_changes += 1
  else:
    print('Title:',profiles[user_name]['title'])

  if len(profiles[user_name]['major']) == 0:
    major = input("Enter your major: ").title()
    if major == 'q':
      return
    profiles[user_name]['major'] = major
    num_changes += 1
  else:
    print('Major:',profiles[user_name]['major'])

  if len(profiles[user_name]['uni']) == 0:
    uni = input("Enter your university's name: ").title()
    if uni == 'q':
      return
    profiles[user_name]['uni'] = uni
    num_changes += 1
  else:
    print('University:',profiles[user_name]['uni'])

  if len(profiles[user_name]['uni_abbr']) == 0:
    uni_abbr = input("Enter your university's abbreviation: ").upper()
    if uni_abbr == 'q':
      return
    profiles[user_name]['uni_abbr'] = uni_abbr
    num_changes += 1
  else:
    print('University:',profiles[user_name]['uni'])

  if len(profiles[user_name]['about']) == 0:
    about = input("Enter your about section: ")
    if about == 'q':
      return
    profiles[user_name]['about'] = about
    num_changes += 1
  else:
    print('About:',profiles[user_name]['about'])
  
  #enter a job, for up to ten jobs
  num_jobs = profiles[user_name]['num_jobs']
  if num_jobs == 0:
    num_changes += 1
    job_choice = input("Would you like to enter work experience? ('y' or 'n') ")
    while job_choice not in ['y','n','q']:
      job_choice = input("Enter ('y' or 'n' or 'q') ")
    if job_choice == 'q':
      return
    elif job_choice == 'y':   
      while num_jobs < 11:
        num_jobs += 1
        #initialize job fields to empty
        profiles[user_name]['exp'][f'job{num_jobs}'] = {}
        profiles[user_name]['exp'][f'job{num_jobs}']['title'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['employer'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['start'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['end'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['location'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['descr'] = ''
        job_title = input("Enter your job title: ")
        if job_title == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['title'] = job_title
        job_company = input("Enter your employer's name: ").title()
        if job_title == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['employer'] = job_company
        start = input('Enter date started: ')
        if start == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['start'] = start
        end = input('Enter date ended: ')
        if end == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['end'] = end
        location = input("Enter your location: ")
        if location == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['location'] = location
        descr = input("Enter your job description: ")
        if descr == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['descr'] = descr
        if num_jobs == 10:
          break
          # ask if user wishes to enter another job
        job_choice = input("Would you like to enter another work experience? ('y' or 'n') ")
        while job_choice not in ['y','n','q']:
          job_choice = input("Enter ('y' or 'n' or 'q') ")
        if job_choice == 'q':
          return
        elif job_choice == 'y':
          if num_jobs == 10:
            break
          continue
        else:
          break
    profiles[user_name]['num_jobs'] = num_jobs
  else:
    print("Work experience already entered. Please use update feature to add/update.")
  
  # prompt user for education section of profile
  if len(profiles[user_name]['school']) == 0:
    school = input("Enter your school name (for previous education): ")
    if school == 'q':
      return
    profiles[user_name]['school'] = school
    num_changes += 1
  else:
    print("Previous Education:")
    print("    School:",profiles[user_name]['school'])
  if len(profiles[user_name]['degree']) == 0:
    degree = input("Enter degree earned from this school: ")
    if degree == 'q':
      return
    profiles[user_name]['degree'] = degree
    num_changes += 1
  else:
    print("    Degree:",profiles[user_name]['degree'])

  if len(profiles[user_name]['yrs']) == 0:
    yrs = input("Enter number of years attended at this school: ")
    if yrs == 'q':
      return
    profiles[user_name]['yrs'] = yrs
    num_changes += 1
  else:
    print("    Years:",profiles[user_name]['yrs'])

  if num_changes == 0:
    print("\nYou have finished building your profile. \nUse the 'update profile' feature to edit your existing profile.")
  else:
    print("\nProfile saved! ")

# Function to allow user to add a work experience (up to max of 10)
def update_work_experience(profiles, user_name):
  num_jobs = profiles[user_name]['num_jobs']
  while True:
    add_or_edit = input("\nDo you wish to add a work experience or edit one? ('a' or 'e') ")
    #input validation
    while add_or_edit not in ['a','e','q']:
      add_or_edit = input("Enter ('a' or 'e') or 'q' to quit: ")
    if add_or_edit == 'q':
      return
    elif add_or_edit == 'e':
      job_num = 0
      try:
        job_num = int(input("Enter job number you wish to modify: "))
        if job_num < 1 or job_num > num_jobs:
          raise ValueError
      except ValueError:
        print(f"Please enter a valid number between 1 and {num_jobs}")
        continue

      if job_num == 0:
        continue
      options = list(profiles[user_name]['exp'][f"job{job_num}"].keys())     
     
      print(f"Your options to edit job fields are : {options}")
      while True:
        field = input("Enter the field you wish to edit: ").lower()
        if field == 'q':
          return
        elif field not in options:
          print("Invalid field. Try again. Enter 'q' to quit.")
          continue
        else:
          new_field = input(f'Enter new {field}: ')
          profiles[user_name]['exp'][f"job{job_num}"][field] = new_field
          print("Change successfully saved. Enter 'q' to exit.")
    elif add_or_edit == 'a' and num_jobs >= 10:
      print("Maximum jobs allowed is 10. Please edit existing job.")
      break  
    else:
        num_jobs += 1
        #initialize job fields to empty
        profiles[user_name]['exp'][f'job{num_jobs}'] = {}
        profiles[user_name]['exp'][f'job{num_jobs}']['title'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['employer'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['start'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['end'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['location'] = ''
        profiles[user_name]['exp'][f'job{num_jobs}']['descr'] = ''
        job_title = input("Enter your job title: ")
        if job_title == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['title'] = job_title
        job_company = input("Enter your employer's name: ").title()
        if job_company == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['employer'] = job_company
        start = input('Enter date started: ')
        if start == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['start'] = start
        end = input('Enter date ended: ')
        if end == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['end'] = end
        location = input("Enter your location: ")
        if location == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['location'] = location
        descr = input("Enter your job description: ")
        if descr == 'q':
          return
        profiles[user_name]['exp'][f'job{num_jobs}']['descr'] = descr
        if num_jobs == 10:
          break
  profiles[user_name]['num_jobs'] = num_jobs
  
# Function to allow user to update their profile
def update_profile(profiles, user_name, first_name, last_name):
  if user_name not in profiles.keys():
    print("\nYou have not created a profile yet. Please build a profile first.")
    return
  
  print("\nHere is your current profile:")
  view_profile(profiles, user_name, first_name, last_name)
  options = list(profiles[user_name].keys())
  options.remove('num_jobs')
  print("\nEnter the name of the field you want to update ('exp' to edit job fields)\n")
  print(f"Your options for fields are : {options}")
  while True:
    field = input("Enter the field you wish to edit: ").lower()
    if field == 'q':
      break
    elif field not in options:
      print("Invalid field. Try again. Enter 'q' to quit.")
      continue
    elif field == 'exp':
      update_work_experience(profiles,user_name)
      break
    else:
      new_field = input(f'Enter new {field}: ')
      # maintain proper capitalization for university of major fields
      if field == 'uni' or field == 'major':
        new_field = new_field.title()
      profiles[user_name][field] = new_field
      print("Change successfully saved. Enter 'q' to exit.")
  

  
# Function to display the a user's profile
def view_profile(profiles, user_name, first_name, last_name):
  if user_name not in profiles.keys():
    print("\nYou have not created a profile yet. Please build a profile first.")
    return
    
  print("\n=================================")
  print(f"{first_name} {last_name}".center(33))
  print("=================================")
  print("Title: ", profiles[user_name]['title'])
  print("Major: ", profiles[user_name]['major'])
  print("University: ", profiles[user_name]['uni'] + ',' + profiles[user_name]['uni_abbr'])
  print("About: ", profiles[user_name]['about'])
  
  exp = profiles[user_name]['exp']
  if profiles[user_name]['num_jobs'] > 0:
    print("Work Experience: ")
  count = 1
  for i in exp:
    print('  Job #' + str(count))
    print('    Title: ', exp[f'job{count}']['title'])
    print('    Employer: ', exp[f'job{count}']['employer'])
    print('    Start Date: ', exp[f'job{count}']['start'])
    print('    End Date: ', exp[f'job{count}']['end'])
    print('    Location: ', exp[f'job{count}']['location'])
    print('    Description: ', exp[f'job{count}']['descr'])
    count += 1

  print('Previous Education: ')
  print('    School: ', profiles[user_name]['school'])
  print('    Degree: ', profiles[user_name]['degree'])
  print('    Years Spent: ', profiles[user_name]['yrs'])
  print("=================================")
  input("Press enter to proceed. ")


#post a job to the jobs table in accounts database
def post_job(conn, first_name, last_name, title, descr, employer, location,
             salary, user_num):
  cursor = conn.cursor()
  jobs = all_jobs(conn)
  #do not permit the 6th job entry, only 5 jobs allowed
  if len(jobs) >= 5:
    print("\nAll permitted job entries have been made!\n")
    return False
  cursor.execute(
      '''
    INSERT INTO jobs (user_num, first_name,last_name,title,description,employer,location, salary)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (user_num, first_name, last_name, title, descr, employer, location, salary))
  return True


#given first and last name, check if user is in the system.
def check_user(accounts, num_accounts):
  print()
  in_system = input("Enter first name: ")
  in_system2 = input("Enter last name: ")

  #check if first and last name already exists in system
  name_exists = False
  for i in range(num_accounts):
    if accounts[i][3] == in_system and accounts[i][4] == in_system2:
      name_exists = True
  return name_exists


#establish connection btwn two people in connections table in database
def add_friend(conn, person1, person2):
  cursor = conn.cursor()
  cursor.execute(
      '''
      INSERT INTO connections (person1, person2)
      VALUES (?, ?)
  ''', (person1, person2))
  conn.commit()


#change guest controls of signed in user
def change_controls(conn, accounts, account_num):
  cursor = conn.cursor()
  controls = accounts[account_num][5]
  options = controls.split(',')
  while True:
    print("\nHere are your guest controls:")
    email, sms, targeted_ads = options[0], options[1], options[2]
    print("1.) InCollege Email: {}".format("Yes" if email == 'y' else "No"))
    print("2.) SMS: {}".format("Yes" if sms == 'y' else "No"))
    print("3.) Targeted Advertising Features: {}".format(
        "Yes" if targeted_ads == 'y' else "No"))

    try:
      toggle = int(
          input("Enter option number to toggle (4 to save and exit): "))
    except ValueError:
      toggle = -1
    if toggle == 1:
      options[0] = 'n' if email == 'y' else 'y'
    elif toggle == 2:
      options[1] = 'n' if sms == 'y' else 'y'
    elif toggle == 3:
      options[2] = 'n' if targeted_ads == 'y' else 'y'
    elif toggle == 4:
      break
    else:
      print("\nInput not understood. Try again.")
  #save guest control options to database
  cursor.execute('''UPDATE accounts
SET controls = ?
WHERE user_num = ?;''', (','.join(options), account_num + 1))
  return True


def change_langauge(conn, accounts, account_num):
  cursor = conn.cursor()
  language = accounts[account_num][6]
  while True:
    print("\nYour current language is {}.".format("English" if language ==
                                                  'e' else "Spanish"))
    try:
      toggle = int(
          input("Enter '1' to switch languages (2 to save and exit): "))
    except ValueError:
      toggle = -1
    if toggle == 1:
      language = 's' if language == 'e' else 'e'
    elif toggle == 2:
      break
    else:
      print("\nInput not understood. Try again.")
  #save guest control options to database
  cursor.execute('''UPDATE accounts
SET language = ?
WHERE user_num = ?;''', (language, account_num + 1))
  return True


#generate a list all friends of a person
def all_friends(conn, accounts, account_num, profiles):
  all_friends = accounts[account_num][9]
  if len(all_friends) == 0:
    print("\nYou have no friends!")
    return
  else:
    print("\nHere are your friends:")
    all_friends = all_friends.split(',')
    all_friends = [accounts[int(i) - 1] for i in all_friends]
    num_friends = len(all_friends)
    count = 1
    profile_friends = []
    for i in all_friends:
      if i[1] in profiles.keys():
        print('{}). '.format(count), i[3], i[4], '(view profile)')
        profile_friends.append(count)
      else:
        print('{}). '.format(count), i[3], i[4]) 
      count += 1
     

    #view friends' profiles
    while True:
      view_friend = input("Index of friend to view profile: ('q' to quit) ")
      if view_friend == 'q':
        break
      else:
        try:
          view_friend = int(view_friend)
          if view_friend not in profile_friends:
            raise ValueError
        except ValueError:
          print("\nPlease enter a valid number of a friend who has a profile.")
          continue
        view_profile(profiles,all_friends[view_friend-1][1],all_friends[view_friend-1][3],all_friends[view_friend-1][4])
        count = 1
        for i in all_friends:
          if i[1] in profiles.keys():
            print('{}). '.format(count), i[3], i[4], '(view profile)')
          else:
            print('{}). '.format(count), i[3], i[4]) 
          count += 1

    
    print("\nHere are your friends:")
    count = 1
    for i in all_friends:
      print('{}). '.format(count), i[3], i[4])
      count += 1
    
    delete = input("Do you wish to disconnect from someone? ('y' or 'n') ")
    while delete != 'n' and delete != 'y':
      delete = input("Invalid input. Enter ('y' or 'n') ")
    if delete == 'y':
      try:
        index = int(
            input("\nEnter number of the friend you want to disconnect: "))
        while index > num_friends or index < 1:
          index = int(input("Invalid number: (Enter 0 to quit) "))
          if index == 0:
            break
        else:
          disconnect(conn, accounts, account_num,
                     all_friends[index - 1][0] - 1)
      except ValueError:
        print("\nEnter a number! ")


#generate a list all pending requests
def all_pending(accounts, account_num):
  all_pending = accounts[account_num][10]
  if len(all_pending) == 0:
    print("\nYou have no pending requests!")
  else:
    print("\nHere are your pending requests:")
    all_pending = all_pending.split(',')
    all_pending = [int(i) for i in all_pending]
    count = 1
    for i in all_pending:
      print('{}). '.format(count), accounts[i - 1][3], accounts[i - 1][4])
      count += 1


#the following function sends invite request
def send_invite(conn, accounts, num_accounts, first_name, last_name,
                cur_person_index):
  #check if first and last name already exists in system
  friend_index = -1
  for i in range(num_accounts):
    if accounts[i][3] == first_name and accounts[i][4] == last_name:
      friend_index = i
      break
  if (friend_index != -1):
    #check is not themselves
    if friend_index == cur_person_index:
      print("\nYou cannot connect with yourself!")
      return False
    current_friends = accounts[cur_person_index][9].split(',')
    if str(friend_index + 1) in current_friends:
      print("\nYou are already friends!")
      return False
    else:
      #send invite to friend
      invites_inbox = accounts[friend_index][11]
      #print('invites_inbox',invites_inbox)
      if str(cur_person_index + 1) in invites_inbox:
        print("\nYou have already sent a friend request!")
        return False
      if len(invites_inbox) != 0:
        invites_inbox = invites_inbox.split(',')
        invites_inbox.append(str(cur_person_index + 1))
        invites_inbox = ','.join(invites_inbox)
      else:
        invites_inbox += str(cur_person_index + 1)

      #add invite to pending for person who requested the invite
      invites_outbox = accounts[cur_person_index][10]
      #print('invites_outbox',invites_inbox)
      if len(invites_outbox) != 0:
        invites_outbox = invites_outbox.split(',')
        invites_outbox.append(str(friend_index + 1))
        invites_outbox = ','.join(invites_outbox)
      else:
        invites_outbox += str(friend_index + 1)
      cursor = conn.cursor()
      cursor.execute(
          "UPDATE accounts SET invites_received = ? WHERE user_num = ?",
          (invites_inbox, friend_index + 1))
      cursor.execute("UPDATE accounts SET invites_sent = ? WHERE user_num = ?",
                     (invites_outbox, cur_person_index + 1))
      print('\nInvitation Sent!\n')
      return True
  else:
    print("\nUser not in InCollege System!", end='')
    return False


#utility function to delete last user from database
def delete_last(conn):
  cursor = conn.cursor()
  cursor.execute(
      "DELETE FROM accounts WHERE user_num = (SELECT MAX(user_num) FROM accounts)"
  )
  conn.commit()


#function to confirm invites and establish friendship
# 'sender' and 'receiver' are indices to accounts
def confirm_invite(conn, accounts, sender, receiver):
  cursor = conn.cursor()
  #confirm invite
  #send invite to friend
  receiver_friends = accounts[receiver][9]
  sender_friends = accounts[sender][9]

  #add invite sender to receiver's friends
  if len(receiver_friends) != 0:
    receiver_friends = receiver_friends.split(',')
    receiver_friends.append(str(sender + 1))
    receiver_friends = ','.join(receiver_friends)
  else:
    receiver_friends += str(sender + 1)
  #add invite receiver to sender's friends
  if len(sender_friends) != 0:
    sender_friends = sender_friends.split(',')
    sender_friends.append(str(receiver + 1))
    sender_friends = ','.join(sender_friends)
  else:
    sender_friends += str(receiver + 1)

  #update database
  cursor.execute("UPDATE accounts SET friends = ? WHERE user_num = ?",
                 (sender_friends, sender + 1))
  cursor.execute("UPDATE accounts SET friends = ? WHERE user_num = ?",
                 (receiver_friends, receiver + 1))


# function to disconnect from someone
# 'sender' and 'receiver' are indices to accounts
def disconnect(conn, accounts, sender, receiver):
  cursor = conn.cursor()
  #send invite to friend
  receiver_friends = accounts[receiver][9]
  sender_friends = accounts[sender][9]

  #remove sender from receiver's friends
  receiver_friends = receiver_friends.split(',')
  receiver_friends.remove(str(sender + 1))
  receiver_friends = ','.join(receiver_friends)

  #remove receiver from sender's friends
  sender_friends = sender_friends.split(',')
  sender_friends.remove(str(receiver + 1))
  sender_friends = ','.join(sender_friends)

  #update database
  cursor.execute("UPDATE accounts SET friends = ? WHERE user_num = ?",
                 (sender_friends, sender + 1))
  cursor.execute("UPDATE accounts SET friends = ? WHERE user_num = ?",
                 (receiver_friends, receiver + 1))

  print("\nYou have disconnected with {} {}.".format(accounts[receiver][3],
                                                     accounts[receiver][4]))


#function to check if user has any new invites upon login
def check_invites(conn, accounts, account_num):
  invites = accounts[account_num][11]
  if len(invites) == 0:
    return []
  else:
    print("Please confirm the following pending friend requests: ")
    confirmed = []
    invites = invites.split(',')
    invites = [int(i) for i in invites]
    for i in invites:
      #accounts = all_accounts(conn)
      sender_first_name = accounts[i - 1][3]
      sender_last_name = accounts[i - 1][4]
      print(
          "You have recieved a friend invite from {} {}. Do you wish to confirm?"
          .format(sender_first_name, sender_last_name))
      confirm = input("Type 'y' or 'n': ").lower()
      while confirm != 'y' and confirm != 'n':
        confirm = input("Type 'y' or 'n': ").lower()
      if confirm == 'y':
        #add friend to confirmed list
        confirmed.append(i)
        print("\nYou are now friends with {} {}.\n".format(
            sender_first_name, sender_last_name))
      else:
        print("You have rejected {} {}.\n".format(sender_first_name,
                                                  sender_last_name))

      #delete from sender's invites sent outbox regardless
      invites_outbox = accounts[i - 1][10].split(',')
      #index is necessarily in the invites sent list
      index = invites_outbox.index(str(account_num + 1))
      invites_outbox.pop(index)
      invites_outbox = ','.join(invites_outbox)
      #update database
      cursor = conn.cursor()
      cursor.execute("UPDATE accounts SET invites_sent = ? WHERE user_num = ?",
                     (invites_outbox, i))
    return confirmed


# Function to search by last name, university, or major
def find_someone(conn, accounts, logged_in_user):
  cursor = conn.cursor()

  print("\nSearch for someone by:")
  print("1. Last Name")
  print("2. University")
  print("3. Major")
  print("4. Go Back")

  try:
    search_option = int(input("Enter option number: "))
    while search_option < 1 or search_option > 4:
      search_option = int(input("Invalid! Enter 1-4: "))
  except ValueError:
    search_option = 0

  if search_option == 1:
    last_name = input("Enter last name: ")
    cursor.execute("SELECT * FROM accounts WHERE last_name = ?", (last_name, ))
  elif search_option == 2:
    university = input("Enter university name or abbreviation: ")
    cursor.execute("SELECT * FROM accounts WHERE university LIKE ?",
                   ('%' + university + '%', ))
  elif search_option == 3:
    major = input("Enter major: ")
    cursor.execute("SELECT * FROM accounts WHERE major LIKE ?",
                   ('%' + major + '%', ))
  elif search_option == 4:
    return

  results = cursor.fetchall()
  counter = 1
  if len(results) == 0:
    print("\nNo results found.")
  else:
    print("\nSearch Results:\n---------------------------------")
    for result in results:
      print(f"{counter}. Name: {result[3]} {result[4]}")
      print("University:", result[7])
      print("Major:", result[8])
      print("---------------------------------")
      counter += 1

    while True:
      try:
        choice = int(
            input(
                "\nEnter the number of the student you want to connect with (0 to go back): "
            ))
      except ValueError:
        choice = -1

      if choice == 0:
        break
      elif 1 <= choice <= len(results):
        selected_user = results[choice - 1]
        if send_invite(conn, accounts, len(accounts), selected_user[3],
                       selected_user[4], logged_in_user):
          conn.commit()
          accounts = all_accounts(conn)
      else:
        print("Invalid input. Please enter a valid number.")


# display option to show marketing video when starting application
def display_video():
  video = input(
      "Would you like to watch a video of why you should join InCollege? (yes/no): "
  )
  while (video.lower() != "yes" and video.lower() != "no"):
    video = input("Invalid input. Enter 'yes' or 'no': ")
  if video == "yes":
    print("\nVideo is now playing.\n")

#Function to print initial menu screen
def print_menu():
  print(
      "\nEnter '1' to sign in or register a new InCollege account\nEnter '2' to check if someone is part of the InCollege system\nEnter '3' to watch the video of why join InCollege\nEnter '4' to see useful links\nEnter '5' to see important InCollege Links\nEnter '0' to exit the interface\n"
  )


def print_success_story():
  print(
      "Meet Sarah, a college senior who used InCollege to find her dream job. She created her profile, connected with alumni, and discovered job listings tailored to her major. Through InCollege, she secured an interview and landed the job before graduation. Join InCollege today for your own success story!\n"
  )


def print_password_requirements():
  print("Following are the requirements for your password: ")
  print(
      "-->Minimum of 8 characters\n-->maximum of 12 characters\n-->at least one capital letter\n-->at least one digit\n-->at least one special character)"
  )


#=================functions to help print groups of links================


#print useful links
def print_useful_links():
  print(
      "\nUseful Links:\n 1.) General\n 2.) Browse InCollege\n 3.) Business Solutions\n 4.) Directories\n 5.) Go back."
  )


#print important InCollege links
def print_inCollege_links():
  print(
      "\nInCollege Important Links:\n 1.) Copyright Notice\n 2.) About\n 3.) Accessibility\n 4.) User Agreement\n 5.) Privacy Policy\n 6.) Cookie Policy\n 7.) Copyright Policy\n 8.) Brand Policy\n 9.) Langauages\n 10.) Go Back"
  )


#navigate important InCollege links
def navigate_inCollege_links(conn, accounts, account_num, logged_in=False):
  while True:
    print_inCollege_links()
    try:
      choice = int(input("Go to link #: "))
    except ValueError:
      choice = -1
    if choice == 1:
      print(
          "\nCopyright © 2023 InCollege, All Rights Reserved. All content, trademarks, and intellectual property on this platform are the property of InCollege or its licensors, and may not be reproduced or used without permission."
      )
    elif choice == 2:
      print(
          "\nInCollege is a dynamic online platform created to empower college students by connecting them with opportunities for personal and professional growth. Our mission is to facilitate networking, job searches, and knowledge sharing among students from diverse educational backgrounds."
      )
    elif choice == 3:
      print(
          "\nAt InCollege, we are dedicated to making our platform accessible to everyone, regardless of disabilities or impairments. We strive to adhere to the Web Content Accessibility Guidelines (WCAG) to provide an inclusive experience. If you encounter any accessibility challenges while using our platform, please don't hesitate to contact our support team. Your feedback is valuable to us as we continuously work to enhance accessibility."
      )
    elif choice == 4:
      print(
          "\nBy accessing and using InCollege, you agree to comply with our User Agreement. This agreement outlines the terms and conditions governing your use of our platform, including your responsibilities and the rules for engaging with other users. We encourage you to read the User Agreement thoroughly before using our services."
      )
    elif choice == 5:
      if logged_in:
        while True:
          print(" 1.) Guest controls")
          print(" 2.) Go Back")
          try:
            choice = int(input("Your choice: "))
          except ValueError:
            choice = -1
          if choice == 1:
            ####function to modify guest controls####
            if change_controls(conn, accounts, account_num):
              conn.commit()
              accounts = all_accounts(conn)
          elif choice == 2:
            break
          else:
            print("\n Input not understood. Try again.")
      else:
        print(
            "\nInCollege values your privacy and is committed to protecting your personal information. Our Privacy Policy describes how we collect, use, store, and safeguard your data. We also explain your rights and choices regarding your information. Your trust in us is of utmost importance, and we take your privacy seriously."
        )
    elif choice == 6:
      print(
          "\nInCollege uses cookies and similar technologies to enhance your browsing experience. Our Cookie Policy explains the types of cookies we use, their purposes, and how you can manage your cookie preferences. By using our platform, you consent to the use of cookies as described in our policy."
      )
    elif choice == 7:
      print(
          "\nRespect for intellectual property rights is fundamental to InCollege. Our Copyright Policy outlines the procedures for reporting copyright infringement and our commitment to addressing such claims promptly. If you believe your copyrighted material has been used improperly on our platform, please follow the procedures outlined in this policy."
      )
    elif choice == 8:
      print(
          "\nOur Brand Policy provides guidelines for the use of InCollege's brand assets and trademarks. Please follow these guidelines when using our brand materials."
      )
      print("\n")
    elif choice == 9:
      if logged_in:
        ####function to modify guest language####
        if (change_langauge(conn, accounts, account_num)):
          conn.commit()
          accounts = all_accounts(conn)
      else:
        print(
            "\nInCollege will be available in two languages ,Spanish and English, to cater to a diverse user base. You will be able to change your language preferences in your account settings."
        )
    elif choice == 10:
      break
    else:
      print("Not understood. Try again.")


#print general links
def print_general_links(logged_in=False):
  if logged_in:
    print(
        "\nGeneral Links:\n 1.) Help Center\n 2.) About\n 3.) Press\n 4.) Blog\n 5.) Careers\n 6.) Developers\n 7.) Go Back"
    )
  else:
    print(
        "\nGeneral Links:\n 1.) Help Center\n 2.) About\n 3.) Press\n 4.) Blog\n 5.) Careers\n 6.) Developers\n 7.) Sign Up\n 8.) Go Back"
    )


#Function to check minimum password requirements
def check_password(password):
  #print requirements:
  special_char = "!@#$%^&*()-_+=<>,.?/:;{}[]|~"
  #requirements
  if len(password) < 8:
    print('Invalid password! Minimum length of 8.')
    return False
  elif len(password) > 12:
    print('Invalid password! Maximum length of 12.')
    return False
  elif not any(char.isupper() for char in password):
    print('Invalid password! Must contain a capital letter.')
    return False
  elif not any(char.isdigit() for char in password):
    print('Invalid password! Must contain a digit.')
    return False
  elif not any((char in special_char) for char in password):
    print('Invalid password! Must contain a special character.')
    return False
  else:
    return True


#guides the user to signing in and using app as a member
def log_in(conn, accounts, num_accounts, jobs, profiles):
  cursor = conn.cursor()
  #while loop to give unlimited login attempts to the user
  account_num = -1
  while (True):
    print("\nLogin:")
    new_username = input("Please enter your username: ")
    if new_username == 'q':
      print("Thank you for using InCollege!")
      account_num = -1
      return
    for i in range(num_accounts):
      if accounts[i][1] == new_username:
        account_num = i

    new_password = input("Please enter your password: ")

    if account_num == -1 or new_password != accounts[account_num][2]:
      print(
          "Incorrect username / password, please try again. Enter 'q' in username to quit."
      )
      continue
    else:
      break
  if account_num == -1:
    return
  else:
    print("\nYou have successfully logged in.\n")
    first_name = accounts[account_num][3]
    last_name = accounts[account_num][4]
    user_name = accounts[account_num][1]

    #check for any friend requests, confirm accordingly then reset invites inbox
    confirmed = check_invites(conn, accounts, account_num)
    for i in confirmed:
      confirm_invite(conn, accounts, i - 1, account_num)
      conn.commit()
      accounts = all_accounts(conn)

    cursor.execute(
        "UPDATE accounts SET invites_received = ? WHERE user_num = ?;",
        ("", account_num + 1))
    conn.commit()
    accounts = all_accounts(conn)

    while (True):
      print("\nSelect what you wish to do:")
      print("Enter '1' to search for a job")
      print("Enter '2' to find someone you know")
      print("Enter '3' to connect with someone you know")
      print("Enter '4' show my network")
      print("Enter '5' generate list of pending friend requests")
      print("Enter '6' to learn a new skill")
      print("Enter '7' to post a job")
      print("Enter '8' to delete a job")
      print("Enter '9' to see useful links")
      print("Enter '10' to see important InCollege links")
      print("Enter '11' to view your profile")
      print("Enter '12' to build a new profile")
      print("Enter '13' to update existing profile")
      print("Enter '0' to log out and exit.")
      try:
        choice_4 = int(input("Your choice: "))
      except ValueError:
        choice_4 = -1

      #search for a job
      if choice_4 == 1:
        print("\nunder construction\n")

      #search InCollege users
      elif choice_4 == 2:
        find_someone(conn, accounts, account_num)
        conn.commit()
        accounts = all_accounts(conn)

      #send an friend invite
      elif choice_4 == 3:
        print("\nWho do you wish to connect with?")
        connect_first = input("Enter first name: ")
        connect_last = input("Enter last name: ")
        if send_invite(conn,accounts,num_accounts,\
                      connect_first,connect_last,account_num):
          conn.commit()
          accounts = all_accounts(conn)
        else:
          print('\n')

      #generate a list of all your friends
      elif choice_4 == 4:
        all_friends(conn, accounts, account_num, profiles)
        conn.commit()
        accounts = all_accounts(conn)

      #generate a list of all your pending requests
      elif choice_4 == 5:
        all_pending(accounts, account_num)

      #learn skill
      elif choice_4 == 6:
        while (True):
          print(
              "-->Enter 1 to learn Software Development\n-->Enter 2 to learn Agile Application\n-->Enter 3 to learn Advanced Coding in Python\n-->Enter 4 to learn Efficient Team Communication\n-->Enter 5 to learn Efficient Time Management\n-->Enter 0 to return to the previous screen\n"
          )
          try:
            choice_5 = int(input("Enter skill number: "))
          except ValueError:
            choice_5 = 1
          if choice_5 == 0:
            break
          elif choice_5 == 1:
            print("\nunder construction\n")
          elif choice_5 == 2:
            print("\nunder construction\n")
          elif choice_5 == 3:
            print("\nunder construction\n")
          elif choice_5 == 4:
            print("\nunder construction\n")
          elif choice_5 == 5:
            print("\nunder construction\n")
          else:
            print("Not understood. Try again.")

      #post job
      elif choice_4 == 7:
        #guide user to post a job to jobs database
        if len(jobs) >= 5:
          print("\nAll permitted job entries have been made!")
          continue
        job_title = input("Please enter the job title: ")
        job_description = input("Please enter the job description: ")
        employer_name = input("Please enter name of the employer: ")
        job_location = input("Please enter the job location: ")
        job_salary = float(input("Please enter the salary: $"))
        user_num = accounts[account_num][0]
        if(post_job(conn,first_name,last_name,job_title,job_description,
                 employer_name, job_location, job_salary, user_num)):
          conn.commit()
        print("\nJob successfully posted under your name!\n")
      #useful links
      elif choice_4 == 8:
        print("Which Job would you like to delete")
        user_num = accounts[account_num][0]
        jobs = all_job_list(conn, user_num)

        for job in jobs:
          print(f"({job[0]} , {job[2]}, {job[3]}, {job[4]}, {job[5]}, {job[6]}, {job[7]} \n)")

        choice = int(input("Enter the job ID of the job you want to delete"))
        loop = True
        
        while(loop):
          for job in jobs:
            if choice == job[0]:
              loop = False
          choice = int(input("Job ID does not exist. Try again! "))
        

      elif choice_4 == 9: 
        while True:
          print_useful_links()
          try:
            choice = int(input("Go to link #: "))
          except ValueError:
            choice = -1
          if choice == 1:
            while True:
              print_general_links(True)
              try:
                choice = int(input("Go to link #: "))
              except ValueError:
                choice = -1
              if choice == 1:
                print("\nWe're here to help")
              elif choice == 2:
                print(
                    "\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide!"
                )
              elif choice == 3:
                print(
                    "\nIn College Pressroom: Stay on top of the latest news, updates, and reports."
                )
              elif choice in [4, 5, 6]:
                print("\nUnder construction")
              elif choice == 7:
                break
              else:
                print("Input not understood. Try again.")
          elif choice in [2, 3, 4]:
            print("\nUnder construction")
          elif choice == 5:
            break
          else:
            print("Not understood. Try again.")

      #important InCollege links
      elif choice_4 == 10:
        navigate_inCollege_links(conn, accounts, account_num, True)
        
      elif choice_4 == 11:
        view_profile(profiles,user_name,first_name,last_name)

      elif choice_4 == 12:
        build_profile(profiles,user_name,first_name,last_name)
        new_uni = ','.join([profiles[user_name]['uni'],profiles[user_name]['uni_abbr']])
        new_major = profiles[user_name]['major']
        if (new_uni != accounts[account_num][7]) or (new_major != accounts[account_num][8]):
          update_db_uni_major(conn,user_name,new_uni,new_major)
          accounts = all_accounts(conn)

      elif choice_4 == 13:
        update_profile(profiles,user_name,first_name,last_name)
        if user_name in profiles.keys():
          new_uni = ','.join([profiles[user_name]['uni'],profiles[user_name]['uni_abbr']])
          new_major = profiles[user_name]['major']
          if (new_uni != accounts[account_num][7]) or (new_major != accounts[account_num][8]):
            update_db_uni_major(conn,user_name,new_uni,new_major)
            accounts = all_accounts(conn)
          
      elif choice_4 == 0:
        print("\nYou have successfully logged out.\nThank you for using InCollege!\n")
        with open("profiles.json", "w") as file:
          json.dump(profiles, file)
        break
      else:
        print("Not understood. Try again.")


#guides user to register a new InCollege account
def register_user(conn, accounts, num_accounts):
  #NOT ALLOWING THE CREATION OF THE 11TH ACCOUNT
  if num_accounts >= 10:
    print("All permitted accounts have been created, please come back later")
    return
  #if less than 10 accounts, ask for first and last name, username, password
  while (True):
    successful = False
    exit = False

    nfirst_name = input("Enter your first name: ")
    while len(nfirst_name) == 0:
      nfirst_name = input("Enter your first name: ")
    nlast_name = input("Enter your last name: ")
    while len(nlast_name) == 0:
      nlast_name = input("Enter your last name: ")
    if nfirst_name == 'q' or nlast_name == 'q':
      break
    #check if first and last name already exists
    name_exists = False
    for i in range(num_accounts):
      if accounts[i][3] == nfirst_name and accounts[i][4] == nlast_name:
        name_exists = True
    if (name_exists):
      print("Name already exists!")
      break

    new_username = input("Enter username: ")
    while len(new_username) == 0:
      new_username = input("Enter your user name: ")
    if new_username == 'q':
      break
    #check if account already exists
    account_exists = False
    for i in range(num_accounts):
      if accounts[i][1] == new_username:
        account_exists = True
    if (account_exists):
      print("Username already exists! Try again. Enter 'q' to quit.")
      continue
    else:
      while (True):
        new_password = input("Enter new password: ")
        if check_password(new_password):
          uni = input("Enter your university full name: ")
          uni_abbr = input("Enter your university abbreviation: ")
          if ',' in uni or ',' in uni_abbr:
            uni = uni.replace(',', '')
            uni_abbr = uni_abbr.replace(',', '')
          uni = uni + ',' + uni_abbr
          major = input("Enter your major: ")
          add_account(conn, new_username, new_password, nfirst_name,
                      nlast_name, uni, major)
          successful = True
          break
        elif new_password == 'q':
          break
        else:
          exit = True
          continue
    if (successful):
      conn.commit()
      print("\nAccount successfully created.\n")
      break
    elif (exit):
      break
    else:
      continue


#drives the sign in screen which users can use to sign in or register and acccount
def sign_in_screen(conn, accounts, num_accounts, jobs, profiles):
  while True:
    print(
        "\nEnter '1' to sign in to an existing account\nEnter '2' to register a new account\nEnter '0' to go back"
    )
    try:
      choice_3 = int(input("Your choice: "))
    except ValueError:
      choice_3 = -1
    if choice_3 == 1:
      #logged in user code
      log_in(conn, accounts, num_accounts, jobs, profiles)
      accounts = all_accounts(conn)
      break
    elif choice_3 == 2:
      #register user code
      register_user(conn, accounts, num_accounts)
      accounts = all_accounts(conn)
      num_accounts = len(accounts)
      break
    elif choice_3 == 0:
      break
    else:
      print("Invalid input.")
  return accounts, num_accounts


#main application program
def main():
  #create accounts database or retrieve if it exists
  conn = create_db()
  #accounts is a list of all current accounts in database
  accounts = all_accounts(conn)
  num_accounts = len(accounts)
  jobs = all_jobs(conn)
  #uncomment following line to see current contents of accounts table
  #print(accounts)
  #load profiles into a python dictionary
  profiles = load_profiles()
  #uncomment following line to see current contents of profiles dictionary
  #print(profiles)

  #opening page of application
  print("===================================================")
  print("======Welcome to the InCollege Application!!=======")
  print("===================================================\n")

  #print success story for main screen
  print_success_story()

  #Prompt user to view marketing video upon starting app
  #display_video()

  while (True):
    #basic user prompt to either create a new account or log in to an existing one

    print_menu()
    try:
      choice = int(input("Your choice: "))
    except ValueError:
      choice = -1

    #user chooses to log in to the app
    if choice == 1:
      accounts, num_accounts = sign_in_screen(conn, accounts, num_accounts,
                                              jobs, profiles)

    #allow not logged in user to search for InCollege members
    elif choice == 2:
      if (check_user(accounts, num_accounts)):
        print("\nThey are a part of the InCollege system.\n")
      else:
        print("\nThey are not yet a part of the InCollege system.\n")

    elif choice == 3:
      display_video()
    elif choice == 4:
      while True:
        print_useful_links()
        choice = int(input("Go to link #: "))
        if choice == 1:
          while True:
            print_general_links()
            choice = int(input("Go to link #: "))
            if choice == 1:
              print("\nWe're here to help")
            elif choice == 2:
              print(
                  "\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide!"
              )
            elif choice == 3:
              print(
                  "\nIn College Pressroom: Stay on top of the latest news, updates, and reports."
              )
            elif choice in [4, 5, 6]:
              print("\nUnder construction")
            elif choice == 7:
              #sign in screen
              accounts, num_accounts = sign_in_screen(conn, accounts,
                                                      num_accounts, jobs, profiles)
            elif choice == 8:
              break
            else:
              print("Input not understood. Try again.")
        elif choice in [2, 3, 4]:
          print("\nUnder construction")
        elif choice == 5:
          break
        else:
          print("Not understood. Try again.")
    elif choice == 5:
      navigate_inCollege_links(conn, accounts, -1)
    elif choice == 0:  #else statement executes the last choice for the user to exit the interface
      print(
          "\nThank you for using InCollege!\n\nInterface exited successfully")
      break
    else:
      print("Input not recognized. Try again!\n")


if __name__ == "__main__":
  main()