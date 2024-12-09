FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script
COPY write_to_s3.py /app/

# Install necessary tools and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip && \
    rm -rf /var/lib/apt/lists/* && \
    # Install AWS CLI v2
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    # Install boto3 using pip
    pip install boto3

# Set the default command to run the script
CMD ["python", "/app/write_to_s3.py"]