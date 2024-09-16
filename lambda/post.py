import json
import boto3

# Initialize the DynamoDB resource and SNS client
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Reference your DynamoDB table
table = dynamodb.Table('Nebula')

# Define the SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:905418453416:NewUserCreatedAlert'

def lambda_handler(event, context):
    # Log the incoming event for debugging
    print("Received event: ", json.dumps(event))

    try:
        # Extract values from the event object
        first_name = event.get('firstName', 'Beatrice')
        last_name = event.get('lastName', 'Francis')
        email = event.get('email', 'beatrice@gmail.com')
        nationality = event.get('nationality', 'USA')
        age = event.get('age', '16')
        marital_status = event.get('maritalStatus', 'Single')
        occupation = event.get('occupation', 'student')

        # Write the data to DynamoDB
        response = table.put_item(
            Item={
                'FirstName': first_name,
                'LastName': last_name,
                'Email': email,
                'Nationality': nationality,
                'Age': age,
                'MaritalStatus': marital_status,
                'Occupation': occupation
            }
        )

        # Prepare the message for the SNS notification
        message = f"New entry added to DynamoDB:\nFirstName: {first_name}\nLastName: {last_name}\nEmail: {email}\nNationality: {nationality}\nAge: {age}\nMarital Status: {marital_status}\nOccupation: {occupation}"

        # Publish the message to the SNS topic
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='Lambda Function Triggered'
        )

        # Return a properly formatted JSON object
        return {
            'statusCode': 200,
            'body': json.dumps('User data saved successfully and notification sent!')
        }

    except Exception as e:
        # Log the exception and return a failure response
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
