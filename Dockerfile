# Use the official Python image as a base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY req.txt .

# Install the necessary packages
RUN pip install --no-cache-dir -r req.txt

# Copy the entire project into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
