Docker WordPress Site Management Script
This script is a Python program that provides a command-line interface for managing WordPress sites using Docker and Docker Compose. It allows you to create, enable, disable, and delete WordPress sites with ease.

Prerequisites
Before using this script, make sure you have the following prerequisites installed on your system:

Docker: The script checks if Docker is installed and installs it if necessary.
Docker Compose: The script checks if Docker Compose is installed and installs it if necessary.
Usage
To use the script, follow these steps:

Clone or download the script to your local machine.
Open a terminal or command prompt.
Navigate to the directory where the script is located.
Run the script with the following command:

python wordpress_management.py <site_name> <subcommand>

Arguments
<subcommand>: The action to perform on the WordPress site. Available subcommands are:
create: Create a new WordPress site with the specified name.
enable: Start the containers for the WordPress site.
disable: Stop the containers for the WordPress site.
delete: Delete the WordPress site and its associated files.

Additional Notes
The script automatically checks if Docker and Docker Compose are installed. If they are not found, it will install them for you.
When creating a WordPress site, the script generates a Docker Compose file and sets up the necessary configuration for running WordPress and MySQL containers.
The site files are stored in a directory with the same name as the site name.
The script uses the /etc/hosts file to add an entry for the site name, allowing you to access the site using a custom domain name.
You can choose to open the site in a browser after creating it.
The script provides basic error handling and feedback messages for each operation.
Please ensure that you have the necessary permissions to run Docker and Docker Compose commands. 
If you encounter any issues, make sure you have the latest versions of Docker and Docker Compose installed on your system.
