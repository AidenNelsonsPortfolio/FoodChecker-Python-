# FoodChecker-Python-
Food Checking App that utilizes AI to scan a passed image for potentially dangerous allergens, selected by user. 
Stores user login info in DBS, connected via pip module (MySQL).

The app was built because a food allergy that is in the family, making it easier to check foods online with only an ingredients label than it was previously.

Logging in screen: 

![image](https://user-images.githubusercontent.com/104726926/180318168-5293a710-e3c9-4d33-ba15-6d5f5e535a68.png)

Or, you can create a new account, which will be saved to the database: 

![image](https://user-images.githubusercontent.com/104726926/180318140-dc3fed39-0821-44b8-a616-3c355dccd4e5.png)

After logging in, you will see the following. Click on upload file to be able to select your ingredients label to scan!

![image](https://user-images.githubusercontent.com/104726926/180317419-f38575a3-e3aa-473d-8152-45c3065fcb8d.png)

After selecting a file (all rights go to the Twinkie company for their food label, available online for their products): 

![image](https://user-images.githubusercontent.com/104726926/180318343-ddcf1200-694a-4a94-a156-ee5d6b17d00f.png)

Lastly, after scanning the label (and selecting the allergens you want to look out for, in my case milk, soy and wheat):

![image](https://user-images.githubusercontent.com/104726926/180318498-7aede587-6e8b-4316-9fad-6eebfaa2b116.png)

The app must be connected to local dbs, as mySQL was not globally stored on cloud as of writing. 

Commands are commented out that would be required to initialize new dbs and table before the usage of the password and username storing features.
(See script)

Written in a PyCharm IDE using Python 3.9

Author: Aiden Nelson


Date Of Last Update: July 19, 2022
