
"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
from Util.Const import Const
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import email.encoders as encoders
import os, os.path
 
# Class to connect to email server and send error reports 
class Email(object):
	def __init__(self, config):
		self.m_config = config
		
	def __enter__(self):
		self.m_server = smtplib.SMTP_SSL(self.m_config[Const.EMAIL_HOST_KEY], self.m_config[Const.EMAIL_PORT_KEY])
		self.m_server.ehlo()
		print(self.m_config[Const.EMAIL_USER_KEY], self.m_config[Const.EMAIL_PASS_KEY])
		self.m_server.login(self.m_config[Const.EMAIL_USER_KEY], self.m_config[Const.EMAIL_PASS_KEY])
		return self
		
	def __exit__(self, type, value, traceback):
		self.m_server.quit()
		
	def send_message(self, message, header):
		msg = MIMEMultipart()
		users = self.m_config[Const.EMAIL_ADDRESS_KEY]
		if (isinstance(users, type(""))):
			users = [users]
		for user in users:
			msg['From'] = self.m_config[Const.EMAIL_USER_KEY]
			msg['To'] = user
			msg['Subject'] = header
		 
			msg.attach(MIMEText(message, 'plain'))
		 
			text = msg.as_string()
			self.m_server.sendmail(self.m_config[Const.EMAIL_USER_KEY], self.m_config[Const.EMAIL_ADDRESS_KEY], text)

	def send_message_to(self, email, header, message):
		msg = MIMEMultipart()
		msg['From'] = self.m_config[Const.EMAIL_USER_KEY]
		msg['To'] = email
		msg['Subject'] = header
		 
		msg.attach(MIMEText(message, 'html'))
		
		text = msg.as_string()
		self.m_server.sendmail(self.m_config[Const.EMAIL_USER_KEY], self.m_config[Const.EMAIL_ADDRESS_KEY], text)


	def send_error_report(self, output_path):
		msg = MIMEMultipart()
		msg['From'] = self.m_config[Const.EMAIL_USER_KEY]
		msg['To'] = self.m_config[Const.EMAIL_ADDRESS_KEY]
		msg['Subject'] = self.m_config[Const.EMAIL_MSG_HEADER_KEY]
		 
		msg.attach(MIMEText(self.m_config[Const.EMAIL_MSG_TEXT_KEY]))

		filename = os.path.join(output_path, self.m_config[Const.DOUBLET_FILE_KEY])
			
		with open(filename, "rb") as attachment:
			 
			part = MIMEApplication(
				attachment.read(),
				Name=os.path.basename(filename)
				)
			# After the file is closed
			part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)
			msg.attach(part)

		text = msg.as_string()
		self.m_server.sendmail(self.m_config[Const.EMAIL_USER_KEY], self.m_config[Const.EMAIL_ADDRESS_KEY], text)


