# **Authentication-PoC**
Authentication method Proof of Concept

## Systems
- #### Hashed
- #### Salted Hash
- #### Encrypted with Salted Hash

## Testing Metrics
- #### Population Speed
  - ##### Mesured by the creation of 200 users
- #### Login Speed
    - ##### Testesd by checking the user-pswd combos on all 200 users and dividing by 200
- #### Cracking Speed
  - ##### Rainbow table cracking
  - ##### Bruteforce cracking
         - ##### Removed because systems can be artificially adjusted and improved by exponential sleep

## Testing System
- #### Rainbow Tables
  - ##### Built with rainbow table maker disgned in python
