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
		requests.get(
			f'https://{config.GOTIFY_IP}:{config.GOTIFY_PORT}/message?token={config.GOTOFY_APP_TOKEN}"' + \
			f'-F "title={kwargs.pop("title", "Warning")}"' + \
			f'-F "message={message}" -F "priority={kwargs.pop("priority", 5)}'
		)

	def __notify_bot(self, message, *args, **kwargs):
		requests.get(
			f'https://api.telegram.org/bot{config.BOT_TOKEN}' + \
				f'/sendMessage?chat_id={config.CHAT_ID}&text={message}'
		)

	def notify(self, message, *args, **kwargs):
		""" kwargs: title, priority = 5 """
		if config.FORMAT_NOTIFICATION == 'push':
			self.__notify_push(message=message, *args, **kwargs)
		if config.FORMAT_NOTIFICATION == 'bot':
			self.__notify_bot(message=message, *args, **kwargs)
		if config.FORMAT_NOTIFICATION == 'all':
			self.__notify_push(message=message, *args, **kwargs)
			self.__notify_bot(message=message, *args, **kwargs)

		