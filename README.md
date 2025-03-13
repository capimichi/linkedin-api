# LinkedIn API

## Overview

This project provides an API for interacting with LinkedIn data. It allows you to perform various operations such as logging in, searching for job postings, retrieving detailed job information, and getting information about companies and hirers.

## Features

- **Login**: Authenticate with LinkedIn using your credentials.
- **Job Postings**: Search for job postings and retrieve detailed information about specific job postings.
- **Companies**: Get detailed information about companies.
- **Hirers**: Get detailed information about hirers.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/linkedin-api.git
    cd linkedin-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your secret key:
    ```plaintext
    SECRET_KEY=your_secret_key
    ```

## Usage

1. Run the API server:
    ```bash
    python -m linkedinapi.api
    ```

2. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Endpoints

- **Login**
  - `POST /login`: Authenticate with LinkedIn.

- **Job Postings**
  - `GET /job-postings/{job_id}`: Get detailed information about a specific job posting.
  - `GET /job-postings`: Search for job postings based on search criteria.

- **Companies**
  - `GET /companies/{company_slug}`: Get detailed information about a specific company.

- **Hirers**
  - `GET /hirers/{hirer_slug}`: Get detailed information about a specific hirer.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
