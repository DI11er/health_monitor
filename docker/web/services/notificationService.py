import requests

import config


class NotificationService(object):
	_instance = None

	@classmethod
	def get_instance(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls, *args, **kwargs)
			cls.__init__(cls._instance, *args, **kwargs)
		return cls._instance
	
	def __notify_push(self, message, *args, **kwargs):
		requests.post(f'http://{config.GOTIFY_IP}:{config.GOTIFY_PORT}/message?token={config.GOTIFY_APP_TOKEN}', json={
			'message': message,
			'priority': kwargs.pop('priority', 5),
			'title': kwargs.pop('title', 'INFO')
		})

	def __notify_bot(self, message, *args, **kwargs):
		with requests.Session() as sess:
			for chat_id in config.CHATS_ID:
				sess.post(f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage', json={
					'chat_id': chat_id,
					'text': message
				})

	def notify(self, message, *args, **kwargs):
		""" kwargs: title, priority = 5 """
		if config.FORMAT_NOTIFICATION == 'push':
			self.__notify_push(message=message, *args, **kwargs)
		if config.FORMAT_NOTIFICATION == 'bot':
			self.__notify_bot(message=message, *args, **kwargs)
		if config.FORMAT_NOTIFICATION == 'all':
			self.__notify_push(message=message, *args, **kwargs)
			self.__notify_bot(message=message, *args, **kwargs)

		
