## Prerequisites

Before you get started, make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/) (3.6 or higher)
- [pip](https://pypi.org/project/pip/)
- [Virtualenv](https://pypi.org/project/virtualenv/) (recommended for isolating your project environment)

## Installation

  #### Clone the repository:

   ```bash
   https://github.com/siva1002/assesment.git

  cd Assessment
  ```
#### Create a virtual environment (if applicable) and install project dependencies

```shell
py -m virtualenv venv
source venv/bin/activate  # On macOS and Linux
pip install -r requirements.txt
```
### Migration
```shell
py manage.py makemigrations #Create migration
py manage.py migrate #Apply migrations to db
```

#### Running the project
```shell
python manage.py runserver
```


### Api docs

- installed swagger for API documentation path **<host>/swagger**

