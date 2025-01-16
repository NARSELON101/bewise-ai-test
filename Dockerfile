FROM python:3.12

WORKDIR src

# Install python requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy run.py (entry point)
COPY run.py ./

# Copy app-related files
COPY src ./src

CMD ["python", "-u", "run.py"]