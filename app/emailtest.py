import emailer

em = emailer.Email()

email = em.create_email("This is a test email.")
em.send_email(email)