# Discord-Tool - Schuh Rewrite
![Tool](https://schuh.wtf/resources/images/schuhrewrite.png)
<br>

> [!NOTE]
> Supports: Windows 10, 11 [Other Versions untested]<br>
> Star the Repo for more amazing Updates in the Future.<br>
> You may give me Suggestions for features or just ask me about stuff in the [issues](https://github.com/Schuh1337/Discord-MultiTool/issues/new) Tab.<br>
> Make sure that you have `VirtualTerminalLevel` set to `1` for the best experience. --> [Tutorial](https://www.youtube.com/watch?v=HeJOyEw3RtM)<br>

> [!WARNING]
> 
> This project is not intended for production use, and its code may not adhere to best practices or security standards. It is solely meant for educational purposes, providing examples, and encouraging experimentation.<br>
>
> I am not responsible for any misuse or damage caused using this tool. Users are advised to comply with the terms of the [MIT License](https://github.com/Schuh1337/Discord-MultiTool?tab=MIT-1-ov-file) and use this tool responsibly.

> [!TIP]
> 
> To get started with this tool, follow these steps:
> 
> 1. **Download:**
>    - If you prefer the source code, download the repo as a [zip file](https://github.com/Schuh1337/Discord-MultiTool/archive/refs/heads/main.zip). Extract the contents and navigate to the extracted directory.
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

#
> ### 🛠️ Updates & Changes

Update 15 - 16.07.2024

* Overall Code Optimizations<br>
  ⮡&nbsp;&nbsp; More Compact & Readable Code<br>
  ⮡&nbsp;&nbsp; Some more Error Handling for some Functions<br>
  ⮡&nbsp;&nbsp; Improved some Inputs<br>

<details>
<summary>Past Updates & Changes</summary>
<br>

<details>
<summary>Bugfix - 15.07.24</summary>
<br>
  
* Fixed Code Issue causing 'Token Information' to crash when Token has no Nitro

</details>

<details>
<summary>Hotfix - 15.07.24</summary>
<br>

* Small "Fix" for 'Message Reacter'
  
</details>

<details>
<summary>Update 14 - 14.07.24</summary>
<br>

* Removed 'Webhook Animator' - Useless & Bad
* Added 'Get Your Token'

</details>

<details>
<summary>Update 13 - 12.07.2024 </summary>
<br>

* Renamed 'Invite Information' to 'Server Lookup'<br>
  ⮡&nbsp;&nbsp; Added Choice between 'Server ID' and 'Server Invite' for Lookup Types<br>
* Added Total Spent to 'Token Payments'

</details>

<details>
<summary>Update 12 - 11.07.2024</summary>
<br>

* Added 'Group Chat Clearer'
* Added 'Invite Information'
* Menu & Code Layout Changes

</details>

<details>
<summary>Update 11 - 10.07.2024</summary>
<br>
  
* Added 'Nitro Expiry' to 'Token Information'
  
</details>

<details>
<summary>Hotfix - 05.07.24</summary>
<br>

* Fixes

</details>

<details>
<summary>Update 10 :tada: - 04.07.24</summary>
<br>

* Made 'Scrape Emojis' & 'Scrape Stickers' about 10x faster
* Other minor Internal Code & Layout Changes

</details>

<details>
<summary>Update 9 - 03.07.24</summary>
<br>

* Added Scroll Disabler for Menu (this was SO complex to perfectionate)
* Internal Code Changes
  
</details>

<details>
<summary>Update 8 - 02.07.24</summary>
<br>

* New Menu
* Improved 'Channel Spammer'
* Fixed Bug in 'Channel Monitoring'

</details>

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

</details>


#
> ### 🚨 Known Issues / "Bugs"

* Message Reacter doesn't work with default Discord Emojis<br>
  ⮡&nbsp;&nbsp; It works if you input the actual emoji, not something like :​joy​:<br>
* DM Channel Clearer only closes DMs with messages in them<br>
  ⮡ &nbsp;&nbsp;Pretty sure this is a discord api limitation<br>
