# Content Project

Welcome to the Content project! This repository contains the back-end and front-end components for managing and displaying content.

## Back-end

### Manual Setup

1. **Database Setup**: First, you need to set up the MySQL database management system. Make sure it is installed and running on port 3306. To access the database, you'll need the necessary information stored in the `.env` file.

2. **Python Environment**: Create a Python environment for the back-end and activate it. This will help isolate the project dependencies. You can use a tool like `virtualenv` or `conda` to create the environment.

3. **Install Dependencies**: Once the Python environment is activated, navigate to the back-end directory in your terminal and run the following command to install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Server**: To start the back-end server, execute the following command from the back-end directory:

    ```bash
    uvicorn main:app --reload
    ```

### Setup with Script

1. **Docker Setup**: If you prefer an automated setup, you can use Docker to create a MySQL container. Make sure Docker is installed and running on your system.

2. **Database Initialization**: Run the `create_db.sh` script to create and initialize the database. This script will handle the necessary setup steps for you.

3. **Dependency Initialization**: Next, run the `create_env.sh` script. This script will set up the required dependencies for the project.

4. **Start the Server**: Finally, start the back-end server by executing the same command as mentioned in the manual setup above.

## Front-end

The front-end component is responsible for displaying and interacting with the content. To set it up, follow the steps below:

1. **Installation**: Open a command prompt or terminal and navigate to the front-end directory.

2. **Install Dependencies**: Run the following command to install the project dependencies:

    ```bash
    npm install
    ```

3. **Start the Server**: Once the installation is complete, start the front-end server using the following command:

    ```bash
    npm start
    ```

That's it! You should now have the back-end and front-end components of the Content project up and running. Feel free to explore and use the application as needed.

If you encounter any issues or need further assistance, please refer to the project documentation or reach out to the project maintainer.

Happy content managing!
