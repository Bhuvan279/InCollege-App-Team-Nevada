#TEST CASES FILE

import sqlite3

import pytest
from _pytest.capture import capfd

from main import (
  add_account,
  all_accounts,
  all_friends,
  all_pending,
  check_password,
  check_user,
  navigate_inCollege_links,
  print_menu,
  print_success_story,
  display_video,
  post_job,
  all_jobs,
  change_langauge,
  change_controls,
  print_useful_links,
  print_inCollege_links,
  find_someone,
  send_invite,
  check_invites,
  confirm_invite,
  delete_last
)


# ========================================================#
# ==========Epic 1 test cases as of 9/19/2023=============#
# ========================================================#
# test the main screen has two options plus option to exit
def test_main_screen(capfd):
  print_menu()
  out, err = capfd.readouterr()
  assert out == "\nEnter '1' to create a new InCollege account\nEnter '2' to log in with an existing InCollege account\nEnter '3' to check if someone is part of the InCollege system\nEnter '4' to watch the video of why join InCollege\nEnter '5' to exit the interface\n\n"

  print_success_story()
  out, err = capfd.readouterr()
  assert out == "Meet Sarah, a college senior who used InCollege to find her dream job. She created her profile, connected with alumni, and discovered job listings tailored to her major. Through InCollege, she secured an interview and landed the job before graduation. Join InCollege today for your own success story!\n\n"


# Test the password validation function
def test_valid_password():
    assert check_password('ValidPass1!') is True
    assert check_password('ThisWorks2@') is True
  
def test_short_password():
    assert check_password('Short1!') is False

def test_long_password():
    assert check_password('TooLong123456!') is False

def test_missing_uppercase():
    assert check_password('nopass1!') is False

def test_missing_digit():
    assert check_password('NoDigitPass!') is False

def test_missing_special_char():
    assert check_password('NoSpecial123') is False

#Test if the add account function works properly

def test_add_account():
  conn = sqlite3.connect('accounts.db')

  username = "test_user"
  password = "Test123!"
  first_name = "Spongebob"
  last_name = "Squarepants"
  uni = "FakeUni"
  major = "MockMajor"
  
  accounts = all_accounts(conn)
  prev_num_accounts = len(accounts)
  add_account(conn, username, password, first_name, last_name, uni, major)
  accounts = all_accounts(conn)
  new_num_accounts = len(accounts)
  
  # Assert
  assert new_num_accounts == prev_num_accounts + 1
  assert accounts[-1][1] == username
  assert accounts[-1][2] == password

# ========================================================#
# ==========Epic 2 test cases as of 9/25/2023=============#
# ========================================================#

# test whether the main screen displays a success story
def test_main_screen(capfd):
  print_success_story()
  out, err = capfd.readouterr()
  assert out == "Meet Sarah, a college senior who used InCollege to find her dream job. She created her profile, connected with alumni, and discovered job listings tailored to her major. Through InCollege, she secured an interview and landed the job before graduation. Join InCollege today for your own success story!\n\n"

# Test the check_user function with an existing user
def test_check_user_existing_user(monkeypatch):
    # Add a test account to the in-memory database
    # add_account(in_memory_db, 'test_user', 'Test123!', 'John', 'Doe')
    conn = sqlite3.connect('accounts.db')
    
    add_account(conn, 'test_user', 'Test123!', 'Spongebob', 'Squarepants', 'FakeUni', 'MockMajor')
    accounts = all_accounts(conn)
    input_values = ["Spongebob", "Squarepants"]
    
    # Monkey-patch the input() function to return the predefined input values
    def mock_input(prompt):
        return input_values.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
    
    # Call the function under test
    result = check_user(accounts, len(accounts))
    
    # Check that the function correctly identifies the existing user
    assert result is True
# Test the check_user function with a nonexisting user
def test_check_user_non_existing_user(monkeypatch):
    conn = sqlite3.connect('accounts.db')
    add_account(conn, 'test_user', 'Test123!', 'TestPerson', 'TestPerson', 'FakeUni', 'MockMajor')
    accounts = all_accounts(conn)
    input_values = ["IDont", "Exist"]
    
    # Monkey-patch the input() function to return the predefined input values
    def mock_input(prompt):
        return input_values.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
    
    # Call the function under test
    result = check_user(accounts, len(accounts))
    
    # Check that the function correctly identifies the existing user
    assert result is False

#test cases to test marketing video displayability
def test_display_video(monkeypatch, capsys):
    input_value = ["yes"]
  
    def mock_input(prompt):
        return input_value.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
    
    display_video()

    captured = capsys.readouterr()
    assert captured.out == "\nVideo is now playing.\n\n"


def test_display_video_invalid(monkeypatch, capsys):
    input_value = ["Invalid", "yes"]
  
    def mock_input(prompt):
        return input_value.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
    
    display_video()

    captured = capsys.readouterr()
    assert captured.out == "\nVideo is now playing.\n\n"

#test the post job functionality
def test_post_job():
  conn = sqlite3.connect('accounts.db')

  first_name = "test_user"
  last_name = "Test123!"
  title = "Software Engineer"
  description = "Code your pants off"
  employer = "JP Morgan Chase"
  location = "Tampa, FL"
  salary = 150000.0
  
  jobs = all_jobs(conn)
  prev_num_jobs = len(jobs)
  post_job(conn,first_name,last_name,title,description,\
                     employer, location, salary)
  jobs = all_jobs(conn)
  new_num_jobs = len(jobs)
  
  # Assert
  assert new_num_jobs == prev_num_jobs + 1
  assert jobs[-1][1] == 'test_user'
  assert jobs[-1][2] == 'Test123!'
  assert jobs[-1][3] == 'Software Engineer'
  assert jobs[-1][4] == 'Code your pants off'
  assert jobs[-1][5] == 'JP Morgan Chase'
  assert jobs[-1][6] == 'Tampa, FL'
  assert jobs[-1][7] == 150000.0


# ========================================================#
# ==========Epic 3 test cases as of 9/29/2023=============#
# ========================================================#
#testing the change_language() story
def test_change_language(monkeypatch):
    # Insert a mock user into the database
    conn = sqlite3.connect('accounts.db')
    add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
    cursor = conn.cursor()
    # mock_db_connection.commit()
    accounts = all_accounts(conn)

    account_num = cursor.execute("SELECT user_num FROM accounts WHERE user_name = 'mock_user'").fetchone()[0]
  
    user_input = ['1', '2']  
  
    def mock_input(prompt):
        return user_input.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)

    # Call the function
    result = change_langauge(conn, accounts, account_num-1)

    # Verify the result
    assert result is True

    # Check if the language was updated in the database
    cursor.execute("SELECT language FROM accounts WHERE user_num = ?", (account_num,))
    updated_language = cursor.fetchone()[0]
    assert updated_language == 's' 

#testing the change_controls() story
def test_change_controls(monkeypatch):
    conn = sqlite3.connect('accounts.db')
    add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
    cursor = conn.cursor()
    # mock_db_connection.commit()
    accounts = all_accounts(conn)
    account_num = cursor.execute("SELECT user_num FROM accounts WHERE user_name = 'mock_user'").fetchone()[0]

    user_input = ['1','2','4']  
  
    def mock_input(prompt):
        return user_input.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)

    result = change_controls(conn, accounts, account_num-1)

    assert result is True

    cursor.execute("SELECT controls FROM accounts WHERE user_num = ?", (account_num,))
    updated_controls = cursor.fetchone()[0]
    assert updated_controls == 'n,n,y' 

#testing print_general_links function
def test_useful_links(capfd):
  print_useful_links()
  out, err = capfd.readouterr()
  assert out == "\nUseful Links:\n 1.) General\n 2.) Browse InCollege\n 3.) Business Solutions\n 4.) Directories\n 5.) Go back.\n"
  
#testing print_useful_links function
def test_useful_links(capfd):
  print_inCollege_links()
  out, err = capfd.readouterr()
  assert out == "\nInCollege Important Links:\n 1.) Copyright Notice\n 2.) About\n 3.) Accessibility\n 4.) User Agreement\n 5.) Privacy Policy\n 6.) Cookie Policy\n 7.) Copyright Policy\n 8.) Brand Policy\n 9.) Langauages\n 10.) Go Back\n"

#test navigate inCollege links
def test_navigate_inCollege_links(capfd,monkeypatch):
  print_inCollege_links()
  out, err = capfd.readouterr()

  #Insert a mock user into the database
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  cursor = conn.cursor()
  account_num = cursor.execute("SELECT user_num FROM accounts WHERE user_name = 'mock_user'").fetchone()[0]
  language = cursor.execute("SELECT language FROM accounts WHERE user_name = 'mock_user'").fetchone()[0]
  language = "English" if language == "e" else "Spanish"
  #check that a newly created account is set to English
  assert language == "English" 
  
  accounts = all_accounts(conn)

  user_input = ['1','2','3','4','5','6','7','8','9','10']  
  
  def mock_input(prompt):
    return user_input.pop(0)

  monkeypatch.setattr('builtins.input', mock_input)

  navigate_inCollege_links(conn, accounts, account_num-1, False)
  out, err = capfd.readouterr()
  assert "\nCopyright © 2023 InCollege, All Rights Reserved. All content, trademarks, and intellectual property on this platform are the property of InCollege or its licensors, and may not be reproduced or used without permission." in out 

  assert "InCollege is a dynamic online platform created to empower college students by connecting them with opportunities for personal and professional growth. Our mission is to facilitate networking, job searches, and knowledge sharing among students from diverse educational backgrounds." in out

  assert "At InCollege, we are dedicated to making our platform accessible to everyone, regardless of disabilities or impairments. We strive to adhere to the Web Content Accessibility Guidelines (WCAG) to provide an inclusive experience." in out

  assert "By accessing and using InCollege, you agree to comply with our User Agreement. This agreement outlines the terms and conditions governing your use of our platform, including your responsibilities and the rules for engaging with other users." in out

  assert "InCollege values your privacy and is committed to protecting your personal information. Our Privacy Policy describes how we collect, use, store, and safeguard your data. We also explain your rights and choices regarding your information. Your trust in us is of utmost importance, and we take your privacy seriously." in out

  assert "InCollege uses cookies and similar technologies to enhance your browsing experience. Our Cookie Policy explains the types of cookies we use, their purposes, and how you can manage your cookie preferences. By using our platform, you consent to the use of cookies as described in our policy." in out

  assert "Respect for intellectual property rights is fundamental to InCollege. Our Copyright Policy outlines the procedures for reporting copyright infringement and our commitment to addressing such claims promptly. If you believe your copyrighted material has been used improperly on our platform, please follow the procedures outlined in this policy." in out

  assert "Our Brand Policy provides guidelines for the use of InCollege's brand assets and trademarks. Please follow these guidelines when using our brand materials." in out

  assert "InCollege will be available in two languages ,Spanish and English, to cater to a diverse user base. You will be able to change your language preferences in your account settings." in out

  #now test language and controls if user is logged in
  user_input.extend(['5','1','4','2','9','2','10'])

  monkeypatch.setattr('builtins.input', mock_input)

  navigate_inCollege_links(conn, accounts, account_num-1, True)
  out, err = capfd.readouterr()
  #check change controls and language options outputted correctly
  assert "Here are your guest controls:" in out
  assert "Your current language is {}".format(language) in out 


# ========================================================#
# ==========Epic 4 test cases as of 10/12/2023============#
# ========================================================#


#Once a student has logged into the InCollege system,test the "Find someone you know" feature to search for students in the system by last name

def test_find_someone_you_know_by_lastname(capfd, monkeypatch):
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  accounts = all_accounts(conn)
  account_num = accounts[-1][0]
  # Setup user inputs for `find_someone` function
  user_input = ['1','Star','0']  
    
  def mock_input(prompt):
    return user_input.pop(0)
  monkeypatch.setattr('builtins.input', mock_input)  # simulate user selecting '1' and then inputting 'Star' for the lastname
  
  find_someone(conn, accounts, account_num)
  # Capture what's printed to stdout
  out, err = capfd.readouterr()
  # assert that the output includes 'Patrick Star'
  assert 'Patrick Star' in out

  conn.close()
  
#Once a student has logged into the InCollege system,test the "Find someone you know" feature to search for students in the system by university

def test_find_someone_you_know_by_university(capfd, monkeypatch):
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  accounts = all_accounts(conn)
  account_num = accounts[-1][0]
  # Setup user inputs for `find_someone` function
  user_input = ['2','FakeUni','0']  
    
  def mock_input(prompt):
    return user_input.pop(0)
  monkeypatch.setattr('builtins.input', mock_input)  # simulate user selecting '2' and then inputting 'FakeUni' to search by university name
  
  find_someone(conn, accounts, account_num)
  # Capture what's printed to stdout
  out, err = capfd.readouterr()
  # assert that the output includes 'Patrick Star'
  assert 'Patrick Star' in out

  conn.close()

#Once a student has logged into the InCollege system,test the "Find someone you know" feature to search for students in the system by major.

def test_find_someone_you_know_by_major(capfd, monkeypatch):
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  accounts = all_accounts(conn)
  account_num = accounts[-1][0]
  # Setup user inputs for `find_someone` function
  user_input = ['3','MockMajor','0']  
    
  def mock_input(prompt):
    return user_input.pop(0)
  monkeypatch.setattr('builtins.input', mock_input)  # simulate user selecting '3' and then inputting 'MockMajor' to search by major
  
  find_someone(conn, accounts, account_num)
  # Capture what's printed to stdout
  out, err = capfd.readouterr()
  # assert that the output includes 'Patrick Star'
  assert 'Patrick Star' in out

  conn.close()

#Perform test with user who exists in the system and a student who doesnt exist in the system for the cases above

def test_find_nonexistent_user(capfd, monkeypatch):
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  accounts = all_accounts(conn)
  account_num = accounts[-1][0]
  # Setup user inputs for `find_someone` function
  user_input = ['1','Starry','0']  
    
  def mock_input(prompt):
    return user_input.pop(0)
  monkeypatch.setattr('builtins.input', mock_input)  # simulate user selecting '1' and then inputting 'Star' for the lastname
  
  find_someone(conn, accounts, account_num)
  # Capture what's printed to stdout
  out, err = capfd.readouterr()
  # assert that the output includes 'Patrick Star'
  assert 'No results found' in out

  conn.close()

#Test output if no such user is found
#conn,accounts,account_num
def test_request_with_nonexistent_user(capfd, monkeypatch):
  conn = sqlite3.connect('accounts.db')
  add_account(conn, 'mock_user', 'Test123!', 'Patrick', 'Star', 'FakeUni', 'MockMajor')
  accounts = all_accounts(conn)
  account_num = accounts[-1][0]
  
  send_invite(conn,accounts,len(accounts),\
                      'mock_first','mock_last',account_num)
  # Capture what's printed to stdout
  out, err = capfd.readouterr()
  # assert that the system informs that no such user exists
  assert 'User not in InCollege System!' in out

  conn.close()



#Create 2 mock users, 1 is the user who logs in and 2 is the pending friend request. 

#CASE 1: The user rejects the friend request from mock user 2 and displays an empty friend list.
def test_list_of_friends_reject(capfd, monkeypatch):
   # Insert 2 mock users into the database
    conn = sqlite3.connect('accounts.db')
    delete_last(conn)
    add_account(conn,'mock_user1', 'Test123!', 'Patrick1', 'Star1', 'FakeUni1', 'MockMajor1')
    add_account(conn,'mock_user2', 'Test123!', 'Patrick2', 'Star2', 'FakeUni2', 'MockMajor2')
    accounts = all_accounts(conn)
    mock_user1_num = accounts[-2][0]-1
    mock_user2_num = accounts[-1][0]-1
  
    mock_user1 = accounts[mock_user1_num]

    # Simulate a friend request from mock_user2
    mock_user2_fn = accounts[mock_user2_num][3]
    mock_user2_ln = accounts[mock_user2_num][4]
    send_invite(conn,accounts,len(accounts),mock_user2_fn,mock_user2_ln,mock_user1_num)
    conn.commit()
    accounts = all_accounts(conn)

    # Simulate rejecting the friend request by entering 'n'
    user_input = ['n']  

    def mock_input(prompt):
        return user_input.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
  
     # Simulate rejecting the friend request by removing the friend request from the invites received list
    confirmed = check_invites(conn,accounts,mock_user2_num)

    #assert confirmed list is empty since user was rejected
    assert len(confirmed) == 0

    delete_last(conn)
    delete_last(conn)

  
#CASE 2: The user accepts the friend request from mock user 2 
def test_list_of_friends_accept(capfd, monkeypatch):
   # Insert 2 mock users into the database
    conn = sqlite3.connect('accounts.db')
    add_account(conn,'mock_user1', 'Test123!', 'Patrick1', 'Star1', 'FakeUni1', 'MockMajor1')
    add_account(conn,'mock_user2', 'Test123!', 'Patrick2', 'Star2', 'FakeUni2', 'MockMajor2')
    accounts = all_accounts(conn)
    mock_user1_num = accounts[-2][0]-1
    mock_user2_num = accounts[-1][0]-1

    # Simulate a friend request from mock_user2
    mock_user2_fn = accounts[mock_user2_num][3]
    mock_user2_ln = accounts[mock_user2_num][4]
    send_invite(conn,accounts,len(accounts),mock_user2_fn,mock_user2_ln,mock_user1_num)
    conn.commit()
    accounts = all_accounts(conn)

    # Simulate rejecting the friend request by entering 'n'
    user_input = ['y']  

    def mock_input(prompt):
        return user_input.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
  
     # Simulate rejecting the friend request by removing the friend request from the invites received list
    confirmed = check_invites(conn,accounts,mock_user2_num)

    #assert confirmed list is empty since user was rejected
    assert mock_user2_num in confirmed

    delete_last(conn)
    delete_last(conn)

#mock user 1 disconnects with mock user 2. mock user 1 disconnect with nonexistent user.

def test_disconnect_with_valid_friend(capfd, monkeypatch):
  # Insert 2 mock users into the database
  conn = sqlite3.connect('accounts.db')
  accounts = all_accounts(conn)
  add_account(conn, 'mock_user1', 'Test123!', 'Patrick1', 'Star1', 'FakeUni1', 'MockMajor1')
  add_account(conn, 'mock_user2', 'Test123!', 'Patrick2', 'Star2', 'FakeUni2', 'MockMajor2')
  
  conn.commit()
  
  accounts = all_accounts(conn)
  mock_user1_num = accounts[-1][0]-1
  mock_user2_num = accounts[-2][0]-1

  # simulate the login of mock user 1
  account_num = accounts[-2][0]-1
  mock_user1 = accounts[account_num]
  friends_list = accounts[mock_user1_num][9]
    
  # Simulate disconnecting with mock_user2
  user_input = ['y']
  
  def mock_input(prompt):
      return user_input.pop(0)
  monkeypatch.setattr('builtins.input', mock_input)
  
  # confirm mock_user2's user_num is not in the friends list
  assert str(mock_user2_num) not in friends_list

  delete_last(conn)
  delete_last(conn)
  
  
