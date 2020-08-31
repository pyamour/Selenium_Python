#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import pickle
import os.path
import base64
import re
import datetime
import html2text
from config.constants import *
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install html2text

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_credit(credential_json_name, token_file_name):
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file_name):
        with open(token_file_name, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_json_name, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file_name, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_account(acc):

    service_accounts = {
        'jim':{"json": ROOT_PATH + "/utilities/" + "credentials.json", "token": ROOT_PATH + "/utilities/" + "token.pickle"}
    }

    return service_accounts[acc]


def get_labels(service):
    output = {}
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        for label in labels:
            output[label['name']] = label['id']
            # print(label['name'] + ': ' + label['id'])

    return output


# https://support.google.com/mail/answer/7190
def get_messages_by_query(service, query='', label_ids=['INBOX'], user_id='me'):
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_messages_by_labels(service, label_ids=[], user_id='me'):
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_message(service, msg_id, user_id='me', msg_format='raw'):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format=msg_format).execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        message['body'] = msg_str.decode("utf-8")

        return message

    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def html_to_text(html):
    return (' '.join(html2text.html2text(html).split())).strip()

def get_messages(service, message_ids):
    output = []

    for message_id in message_ids:
        message = get_message(service, message_id['id'])
        # print(message['body'])
        output.append(message['body'])

    return output

def search_password(text):
    return re.findall(r"Your\spassword\sis\s(.+?)\.", text)[0]

def search_reset_url(text):

    lines = text.split("\n")
    #print(lines)
    print(lines[2])
    url_left = ""
    url_right = ""
    for i in range(len(lines)):
        if lines[i].startswith("http"):
            url_left = lines[i]
            url_right = lines[i+1]
            break

    reset_url = "".join([str(html_to_text(url_left)), str(url_right)])
    url_parts = reset_url.split("=")
    url_part1 = url_parts[0]
    url_part2 = "="
    url_part3 = url_parts[1][2:]
    url_part4 = url_parts[2]
    reset_url = "".join([url_part1, url_part2, url_part3, url_part4])
    return (reset_url)


def check_password_in_gmail(receiver, acc="jim"):
    account = get_account(acc)
    service = get_credit(account["json"], account["token"])

    messages_ids = get_messages_by_query(service,
                                         'from:xxxxxx to:' + receiver + ' subject:"Your account has been successfully created."')

    messages = get_messages(service, messages_ids)
    if len(messages) > 0:
        password = search_password(messages[0])
        return password
    else:
        return ""

def get_reset_password_url_in_gmail(receiver, acc="jim", after="1595552691"):
    account = get_account(acc)
    service = get_credit(account["json"], account["token"])

    search_str = 'from:xxxxxxx to:' + receiver + ' subject:"Password Reset." after:' + after
    #print(search_str)

    messages_ids = get_messages_by_query(service, search_str)
    messages = get_messages(service, messages_ids)
    while len(messages) == 0:
        print("Start to wait  email")
        time.sleep(10)
        print("Start to retrieve email")
        messages_ids = get_messages_by_query(service, search_str)
        messages = get_messages(service, messages_ids)

    if len(messages) > 0:
        reset_url = search_reset_url(messages[0])
    else:
        reset_url = ""

    print("reset_url:  " + reset_url)
    return reset_url
