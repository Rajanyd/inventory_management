import boto3
from django.conf import settings

# def send_low_stock_alert(item_name, quantity, threshold):
#     sns_client = boto3.client(
#         'sns',
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         region_name=settings.AWS_REGION
#     )
    
#     message = f"ALERT: {item_name} is low on stock. Current quantity: {quantity}, Threshold: {threshold}."
#     subject = f"Low Stock Alert: {item_name}"

#     sns_client.publish(
#         TopicArn=settings.SNS_TOPIC_ARN,
#         Message=message,
#         Subject=subject
#     )

import boto3
from django.conf import settings

def send_low_stock_alert(item_name, current_quantity, threshold, user_email):
    """
    Sends a low stock alert via AWS SNS to the user's email.
    """
    print(item_name, current_quantity, threshold, user_email)
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    # Subscribe the user's email to the SNS topic (if not already subscribed)
    # In a production environment, you might want to add logic to check if the email is already subscribed

    # This will subscribe the email to the SNS topic
    sns_client.subscribe(
        TopicArn=settings.SNS_TOPIC_ARN,
        Protocol='email',  # Protocol is 'email' for email notifications
        Endpoint=user_email  # The logged-in user's email
    )

    # Publish a low stock alert message to the SNS topic
    message = f"Alert: The stock of '{item_name}' has fallen below the threshold. Current stock: {current_quantity}, Threshold: {threshold}."

    sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Message=message,
        Subject="Low Stock Alert"
    )
    print(sns_client)


# import boto3
# from django.conf import settings

# def send_low_stock_alert(product_name, current_stock):
#     try:
#         # Initialize SNS client
#         sns_client = boto3.client(
#             'sns',
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_REGION,
#         )

#         # Construct the message
#         message = (
#             f"Low Stock Alert!\n"
#             f"Product: {product_name}\n"
#             f"Current Stock: {current_stock}\n"
#             "Please restock as soon as possible."
#         )

#         # Publish the message
#         response = sns_client.publish(
#             TopicArn=settings.SNS_TOPIC_ARN,
#             Message=message,
#             Subject="Low Stock Alert"
#         )
#         return response
#     except Exception as e:
#         print(f"Error sending notification: {e}")
#         return None



# import boto3
# from django.conf import settings

# def send_low_stock_alert(item_name, current_quantity, threshold, user_email):
#     """
#     Sends a low stock alert via AWS SNS to the user's email.
#     """
#     sns_client = boto3.client(
#         'sns',
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         region_name=settings.AWS_REGION
#     )

#     # Subscribe the user's email to the SNS topic (if not already subscribed)
#     # In a production environment, you might want to add logic to check if the email is already subscribed

#     # This will subscribe the email to the SNS topic
#     sns_client.subscribe(
#         TopicArn=settings.SNS_TOPIC_ARN,
#         Protocol='email',  # Protocol is 'email' for email notifications
#         Endpoint=user_email  # The logged-in user's email
#     )

#     # Publish a low stock alert message to the SNS topic
#     message = f"Alert: The stock of '{item_name}' has fallen below the threshold. Current stock: {current_quantity}, Threshold: {threshold}."

#     sns_client.publish(
#         TopicArn=settings.SNS_TOPIC_ARN,
#         Message=message,
#         Subject="Low Stock Alert"
#     )