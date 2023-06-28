import subprocess
import sys
import os


def check_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker is already installed.")
        return True
    except subprocess.CalledProcessError:
        print("Docker is not installed.")
        return False


def check_docker_compose_installed():
    try:
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker Compose is already installed.")
        return True
    except subprocess.CalledProcessError:
        print("Docker Compose is not installed.")
        return False


def install_docker():
    print("Installing Docker...")
    subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"])
    subprocess.run(["sudo", "sh", "get-docker.sh"])
    print("Docker installation completed.")


def install_docker_compose():
    print("Installing Docker Compose...")
    subprocess.run(
        [
            "sudo",
            "curl",
            "-fsSL",
            "-o",
            "/usr/local/bin/docker-compose",
            "https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64",
        ]
    )
    subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/docker-compose"])
    print("Docker Compose installation completed.")


def create_wordpress_site(site_name):
    print(f"Creating WordPress site '{site_name}'...")
    os.makedirs(site_name, exist_ok=True)
    os.chdir(site_name)

    # Create Docker Compose file
    compose_content = f"""
version: '3'

services:
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: somewordpress
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - '8000:80'
    volumes:
      - ./wp:/var/www/html
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
"""
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

    # Create WordPress folder
    os.makedirs("wp", exist_ok=True)

    # Run Docker Compose
    subprocess.run(["docker-compose", "up", "-d"])

    print(f"WordPress site '{site_name}' created successfully.")


def setup_etc_hosts_entry(site_name):
    try:
        with open("/etc/hosts", "a") as f:
            f.write(f"127.0.0.1 {site_name}\n")
        print(f"Added /etc/hosts entry for '{site_name}'.")
    except PermissionError:
        print("Permission denied. Please run the script as root or with sudo.")


def open_site_in_browser(site_name):
    response = input("Do you want to open the site in a browser? (Y/N): ")
    if response.lower() == "y":
        url = f"http://{site_name}"
        try:
            subprocess.run(["xdg-open", url], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to open '{url}' in a browser.")


def enable_site():
    subprocess.run(["docker-compose", "start"])
    print("Site enabled.")


def disable_site():
    subprocess.run(["docker-compose", "stop"])
    print("Site disabled.")


def delete_site(site_name):
    response = input(f"Are you sure you want to delete the site '{site_name}'? (Y/N): ")
    if response.lower() == "y":
        subprocess.run(["docker-compose", "down"])
        os.chdir("..")
        shutil.rmtree(site_name)
        print(f"Site '{site_name}' deleted successfully.")


if __name__ == "__main__":
    # Check if Docker and Docker Compose are installed
    docker_installed = check_docker_installed()
    docker_compose_installed = check_docker_compose_installed()

    if not docker_installed:
        install_docker()

    if not docker_compose_installed:
        install_docker_compose()

    # Check if site name is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the site name as a command-line argument.")
        sys.exit(1)

    site_name = sys.argv[1]

    # Available subcommands
    subcommands = {
        "create": create_wordpress_site,
        "enable": enable_site,
        "disable": disable_site,
        "delete": delete_site,
    }

    # Check if a valid subcommand is provided
    if len(sys.argv) < 3 or sys.argv[2] not in subcommands:
        print("Please provide a valid subcommand: create, enable, disable, or delete.")
        sys.exit(1)

    subcommand = sys.argv[2]

    # Execute the selected subcommand
    if subcommand == "create":
        create_wordpress_site(site_name)
        setup_etc_hosts_entry(site_name)
        open_site_in_browser(site_name)
    elif subcommand == "enable":
        enable_site()
    elif subcommand == "disable":
        disable_site()
    elif subcommand == "delete":
        delete_site(site_name)