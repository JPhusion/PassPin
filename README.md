# PassPin Password Manager
## What is it?
PassPin is a secure password manager that utilises AES256 encryption and SHA256 hashing with the use of salts and peppers. 

## Security Features
- All data is encrypted using AES256 encryption, including usernames, emails, birthdays, passwords etc.

- No encryption key is stored un-encrypted.

- Each password is encrypted using a seperate encryption key.

- Only one password can be decrypted at a time. 

- When a password has been retrieved, it is immediately re-encrypted.

- Email verification is required to modify security options.

- Encryption keys can be changed at anytime.

- All passwords can be re-encrypted using a new randomly generated encryption key.

## Functionality
- Store all data about any account (fully encrypted).

- Retrieve any data about any account.

- Modify existing accounts.

- Delete accounts.

- Generate secure passwords.

- Update security settings.

## Installation*
### Using an Environment with Python Installed
1. Download the zip file of the latest release.

2. Unzip folder to desired location

4. Navigate to the directory `PassPin`

5. Enter the following command:
```
# Windows:
pip install requirements.txt

# Mac/Linux
pip3 install requirements.txt
# or
sudo pip3 install requirements.txt
```
6. Run main.py

##### *Installers/packages are not yet supported. Feel free to contact me if you have any questions or have a method to package this software for cross platform.

## Setup
- When the software is first run, you will be promted to enter the master password. The default password is `Password1`

- Enter this password to get started.

- You will be prompted to enter an email. This email will be used to send verification codes to when updating security settings.

- You should immediately change the master password to a secure password (reccommend minimum length of 12 with capital letters, lowercase letters, numbers, and special characters).

- Enter your accounts!
