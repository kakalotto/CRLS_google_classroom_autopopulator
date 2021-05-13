def create_message(p_sender, p_to, p_subject, message_text):
    """Create a message for an email.

      Args:
        p_sender: Email address of the sender.
        p_to: Email address of the receiver.
        p_subject: The subject of the email message.
        message_text: The text of the email message.

      Returns:
        An object containing a base64url encoded email object.
      """
    import base64
    from email.mime.text import MIMEText

    message = MIMEText(message_text)
    message['to'] = p_to
    message['from'] = p_sender
    message['subject'] = p_subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}
