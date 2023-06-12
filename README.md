# amalitech
Amalitech digital training 2023
# Project: Access Key Manager
A web application that schools can use to purchase access keys. It was built using django framework
Following are the requirements of this project:
### Customer Requirements
### School IT Personnel
1. Should be able to signup & log in with an email and password with account verification.
There should be a reset password feature to recover lost passwords.
2. Should be able to see a list of all access keys granted: active, expired or revoked.
3. For each access key, the personnel should be able to see the status, date of
procurement and expiry date.
4. A user should not be able to get a new key if there is an active key already assigned to
him/her. Only one key can be active at a time.

### Micro-Focus Admin
1. Should be able to log in with an email and password.
2. Should be able to manually revoke a key.
3. Should be able to see all keys generated on the platform and see the status, date of
4. procurement and expiry date.
5. Should be able to access an endpoint, such that if the school email is provided, the
endpoint should return status code 200 and details of the active key if any is found, else
it should return 404. This is to enable them to integrate their school software with your
key manager.
