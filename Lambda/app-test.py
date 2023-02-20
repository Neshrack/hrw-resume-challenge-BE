import os
import boto3

import smtplib
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

dynamo_client = boto3.resource('dynamodb', region_name='us-east-1')
client = boto3.client('sns')
# def lambda_handler(event, context):
#     dynamo_helper.update_table('test_Visitors', 'VisitorCount', 'vc')


# if __name__ == '__main__':
#     lambda_handler(None, None) yes

def get_count(table, pk, column):
    dynamodb = boto3.resource('dynamodb', table='Visitors' region_name='us-east-1')
    table = dynamo_client.Table(table)
    response = table.get_item(
            Key={pk: 1}
        )
    count = response['Item'][column]
    print(response)
    print ("count is", count)

    return(count)

# get_count('test_Visitors', 'VisitorCount', 'vc')

# def lambda_handler(event, context):
#     dynamo_helper.update_table('test_Visitors', 'VisitorCount', 'vc')



older_value = get_count('test_Visitors','VisitorCount', 'vc')
dynamo_helper.update_table('test_Visitors', 'VisitorCount', 'vc')
newer_value = get_count('test_Visitors','VisitorCount', 'vc')

def email_error():
    s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com')

    s.connect('email-smtp.us-east-1.amazonaws.com', '587')

    s.starttls()
    s.login('AKIAVSUUTP6SH6GR7Q62', 'BvsmtAWYGew0+tstYq30Q0EvVaSbyxh2b0gyVXtX')

    msg = 'From: hunter.walls61@gmail.com\nTo: hunter.walls61@gmail.com\nSubject: Test Email\n\nThis is simply an error message, to inform you that your script failed miserably, you baffoon!'

    s.sendmail('hunter.walls61@gmail.com', 'hunter.walls61@gmail.com', msg)
    return()


assert newer_value == older_value + 1, email_error()
    
