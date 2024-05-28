FROM ubuntu:20.04

# Install dependencies
RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip

# Set the working directory
WORKDIR /app

# Copy the current directory contents
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Add new user
RUN addgroup --system vhc_guest && adduser --system --no-create-home --group vhc_guest
RUN chown -R vhc_guest:vhc_guest /app && chmod -R 755 /app

# Change to the new user
USER vhc_guest

# Run the application
CMD ["python3", "main.py"]