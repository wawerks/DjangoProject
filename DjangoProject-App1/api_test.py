import requests
import json
import getpass

BASE_URL = 'http://localhost:8000'

def get_token(username, password):
    response = requests.post(f'{BASE_URL}/api/token/', 
                           json={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

def make_api_request(endpoint, token, method='GET', data=None):
    headers = {'Authorization': f'Bearer {token}'}
    if method == 'GET':
        response = requests.get(f'{BASE_URL}{endpoint}', headers=headers)
    else:
        response = requests.post(f'{BASE_URL}{endpoint}', 
                               headers=headers, 
                               json=data)
    return response.json()

def main():
    # Get credentials
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    # 1. Get token
    tokens = get_token(username, password)
    if not tokens:
        print("Authentication failed!")
        return
        
    access_token = tokens['access']
    print("\nAuthentication successful!")
    
    # 2. Get users list
    print("\nFetching users...")
    users = make_api_request('/api/users/', access_token)
    print("Users:", json.dumps(users, indent=2))
    
    # 3. Get chat groups
    print("\nFetching chat groups...")
    groups = make_api_request('/api/groups/', access_token)
    print("Groups:", json.dumps(groups, indent=2))
    
    # Ask if user wants to create a new group
    if input("\nDo you want to create a new group? (y/n): ").lower() == 'y':
        group_name = input("Enter group name: ")
        new_group = make_api_request('/api/groups/', 
                                    access_token, 
                                    'POST', 
                                    {'group_name': group_name})
        print("New Group:", json.dumps(new_group, indent=2))
        
        # Ask if user wants to send a message
        if input("\nDo you want to send a message to this group? (y/n): ").lower() == 'y':
            message_text = input("Enter your message: ")
            group_id = new_group['id']
            message = make_api_request(f'/api/groups/{group_id}/messages/', 
                                     access_token, 
                                     'POST', 
                                     {'message': message_text})
            print("Sent Message:", json.dumps(message, indent=2))
            
            # Get all messages in the group
            print("\nFetching messages in the group...")
            messages = make_api_request(f'/api/groups/{group_id}/messages/', 
                                      access_token)
            print("Messages:", json.dumps(messages, indent=2))

if __name__ == '__main__':
    main()
