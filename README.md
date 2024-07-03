# Discord-Tool - Schuh Rewrite
![Tool](https://schuh.wtf/resources/images/sr.png)
<br>
> [!WARNING]
> 
> This project is not intended for production use, and its code may not adhere to best practices or security standards. It is solely meant for educational purposes, providing examples, and encouraging experimentation.<br>
> I am not responsible for any misuse or damage caused using this tool. Users are advised to comply with the terms of the [MIT License](https://github.com/Schuh1337/Discord-MultiTool?tab=MIT-1-ov-file) and use this tool responsibly.

> [!TIP]
> 
> To get started with this tool, follow these steps:
> 
> 1. **Download:**
>    - If you prefer the source code, download the repo as a [zip file](https://github.com/Schuh1337/Discord-MultiTool/archive/refs/heads/main.zip). Extract the contents and navigate to the directory.
>    - If you prefer the compiled executable (exe), download it directly from the [Releases](https://github.com/Schuh1337/Discord-MultiTool/releases) section.
> 
> 2. **For Source Code:**
>    - Ensure [Python](https://www.python.org/downloads/) 3.10 or later is installed on your system.
>    - Run `setup.bat` to install the required libraries.
>    - After that's done, run `schuh.py`
> 
> 3. **For Executable (exe):**
>    - Simply run the downloaded executable file.
> 

> [!NOTE]
> Make sure that you have `VirtualTerminalLevel` set to `1` for the best experience. --> [Tutorial](https://www.youtube.com/watch?v=HeJOyEw3RtM)<br>
> Yes, the window not being able to be maximized / resized is intented.

#
> ### 🛠️ Updates & Changes

Update 8 - 02.07.24
* New Menu
* Improved 'Channel Spammer'
* Fixed Bug in 'Channel Monitoring'

<details>
<summary>Update 7 - 01.07.24</summary>
<br>

* Added additional information to 'Token Information' (Friend Requests, Standing, Available & Used Boosts)
* Improved 'Message Deleter' by adding more Error handling and better Logic

</details>

<details>
<summary>Hotfix - 30.06.24</summary>
<br>

* Fixed big issue in 'Message Deleter'

</details>

<details>
<summary>Update 6 - 30.06.24</summary>
<br>

* Added 'Message Deleter'
* Added count displays for 'Token Payments'
* Added additional information to 'Token Information' (Clan, Locale, Created)

</details>

<details>
<summary>Small Update - 30.06.24</summary>
<br>

* Removed 'Created By' in 'Webhook Information' due to discord changes
* Added Colors to 'Token Payments' Success & Failed Values

</details>

<details>
<summary>Update 5 - 29.06.24</summary>
<br>
  
* Added 'Token Payments'

</details>

<details>
<summary>Update 4 - 23.06.24</summary>
<br>
  
* Added 'Token Login'

</details>

<details>
<summary>Update 3 - 23.06.24</summary>
<br>

* Added Custom Emoji support to 'Animated Status'
* Added Choice between 'Plain Text' Statuses and 'Emoji & Text' Statuses to 'Animated Status'

</details>

<details>
<summary>Hotfix - 22.06.24</summary>
<br>

* Fixed Animated Stickers being downloaded as Static

</details>

<details>
<summary>Update 2 - 22.06.24</summary>
<br>

* Added 'Scrape Emojis'
* Added 'Scrape Stickers'

</details>

<details>
<summary>Hotfix - 22.12.23</summary>
<br>
  
* Added .strip() to the validate_input function to remove leading and trailing Spaces
* Other minor fixes & adjustments

</details>

<details>
<summary>Update 1 - 21.12.23</summary>
<br>

* Added 'Remove Hypesquad' to HypeSquad Changer
* Added 'IP Address Lookup'
* Improved Channel Monitoring
* Improved Inputs

</details>

#
> ### 🚨 Known Issues / "Bugs"

* Message Reacter doesn't work with default Discord Emojis<br>
  ⮡&nbsp;&nbsp; It works if you input the actual emoji, not something like :​joy​:<br>
* DM Channel Clearer only closes DMs with messages in them<br>
  ⮡ &nbsp;&nbsp;Pretty sure this is a discord api limitation<br>
