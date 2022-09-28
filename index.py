import requests
import time

trashes = open("tokens.txt", "r").read().splitlines()          

def write(filename, token, status_code):
    with open("{}.txt".format(filename), "a+") as f:
        f.write('Token: {} | Status_code: {}\n'.format(token, status_code))

def write_valid(filename, token, status_code, email, phone, verify, nitro = 'None', billing = 'None'):
    with open("{}.txt".format(filename), "a+") as f:
        f.write('Token: {} | Status_code: {} | Email: {} | Phone: {} | Verify: {} | Nitro: {} | Billing: {}\n'.format(token, status_code, email, phone, verify, nitro, billing))

def check_token(token):
    response = requests.get('https://discord.com/api/v9/auth/login', headers = {"Authorization": token})
    if response.status_code == 429: # to many requests
        time.sleep(120)
        check_token(token)
    elif response.status_code == 200: # good response 
        print('Token {} valid! '.format(token))
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': token}).json()
        subscriptions = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers={'authorization': token}).json()
        if len(subscriptions) > 1:
            write_valid('billing', token, 200, response['email'], response['phone'], response['verified'], 'True', 'True')
        else:
            write_valid('billing', token, 200, response['email'], response['phone'], response['verified'], 'True')
        if 'premium_type' in response:
            write_valid('valid', token, 200, response['email'], response['phone'], response['verified'], 'True')
        else: 
            write_valid('valid', token, 200, response['email'], response['phone'], response['verified'])
    elif response.status_code == 400 or response.status_code == 403:
        print('Token {} invalid! '.format(token))
        write('invalid', token, response.status_code) 
    else:
        write('errors', token, response.status_code)

if __name__  == "__main__":
    for token in trashes:
        check_token(token)