# instance-name Database Toolkit

## Warning
This application authenticates the user against an internal instance-name API and will only work if they are part of the instance-name-admin group. **This app requires a VPN connection to operate and should not be distributed outside of the instance-name team.**

## Prerequisites
Before you start using the instance-name Database Toolkit, you need to set up your environment:

1. Download and install Docker:
   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Restart your computer after the installation is complete.
3. Download or clone this repository to your local machine.
4. Log in to Docker Desktop or create a new account if you don't have one.
5. Run `Create Image.bat` to build the Docker image for this application.
6. Wait for the image to be built. You will see a confirmation message once the build is complete.
7. Run `1. RUN.bat`. After a short delay, it will automatically open the `http://localhost:5000` page in your default web browser.

## Application Screenshots

### Login Screen
![Login Screen](imgref/image1.png)

### Options Screen
![Options Screen](imgref/image2.png)

## How to Use the instance-name Database Toolkit
To effectively use the toolkit, follow these steps:

1. Authenticate using your credentials or a bearer token as required by the application.
2. Utilize the on-screen options to:
   - Search for existing users.
   - Create new users or schemas.
   - Add users to schemas.
3. Always check if the user requesting access already has an account before creating a new one.
4. Be mindful to follow the on-screen instructions regarding naming conventions for schemas and read users, such as `readschema_xyz` and `readuser_xyz_username`.

### Documentation and Tracking Changes
After adding new users or creating new schemas, make sure to update the documentation and track these changes on Confluence:
[Available Schemas on Confluence](https://confluence.instance-name.com/pages/viewpage.action?spaceKey=instance-name&title=Available+Schemas)

## Support
For any issues or queries, please contact via Slack:
contact@instance-name.com
