# TestVPNService

## Project Information

This project is a minimal working functionality written in Django (monolith) with simple CSS templates to enhance the visual appearance. The project has basic features for working with users and their profiles.

### Project Features:

- **Users:** Registration, login, viewing, and editing profiles.

- **Proxies:** Creating websites for subsequent access through the application and tracking statistics for each site.

### Paths for Modernization:

1. **AWS S3 for avatar storage:**
   - Add support for storing avatars in the AWS S3 service.

2. **Email verification via SMTP server:**
   - Add functionality to confirm email through sending a letter via an SMTP server.

3. **Selenium for fetching page styles:**
   - Integrate Selenium for automated testing and fetching page styles.

4. **Other possibilities:**
   - Essentially, this functionality is unlimited in terms of modernization.

## Running Instructions

1. **Step 1:** Clone the repository to your local computer.

    ```bash
    git clone https://github.com/Mishakivskiy/TestVPNService.git
    ```

2. **Step 2:** Navigate to the project directory.

    ```bash
    cd TestVPNService
    ```

3. **Step 3:** Execute database migrations.

    ```bash
    docker-compose run web python manage.py migrate
    ```

4. **Step 4:** Run the project with rebuilding Docker containers.

    ```bash
    docker-compose up --build
    ```

Now your project should be accessible. Make sure you have Docker and docker-compose installed on your computer.
