FROM python:3.7-stretch

# Create the workdir
RUN mkdir -p /opt/bootstrap

# Set the workdir
WORKDIR /opt/bootstrap

# Copy the pipfiles
COPY Pipfile* ./

# Install dependencies
RUN pip install pipenv &&  pipenv install

# Copy the code
COPY . .

CMD pipenv run python main.py
