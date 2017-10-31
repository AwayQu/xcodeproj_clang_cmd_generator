CPP_HEADERMAP_FILE_FOR_ALL_TARGET_HEADERS = u'CPP_HEADERMAP_FILE_FOR_ALL_TARGET_HEADERS'
FRAMEWORK_SEARCH_PATHS = u'FRAMEWORK_SEARCH_PATHS'
PRODUCT_NAME = u'PRODUCT_NAME'
TEMP_DIR = u'TEMP_DIR'

class BuildSettings(object):
	user_default_from_command_line = {}
	build_settings_from_command_line = {}
	build_settings_for_action_build_and_target = {}

	dynamic_setting = {}

	config = None

	workspace = None
	target = None
	sdk = None
	configuration = None
	scheme = None
	derivedDataPath = None

	def get(self, k, default=None):
		v = self.user_default_from_command_line.get(k)
		if not v:
			v = self.build_settings_from_command_line.get(k)
		if not v:
			v = self.build_settings_for_action_build_and_target.get(k)
		return v

	def __init__(self, **kwargs):
		super(BuildSettings, self).__init__()
		self.config = kwargs
		self.workspace = kwargs.get(u'workspace')
		self.target = kwargs.get(u'target')
		self.sdk = kwargs.get(u'sdk')
		self.configuration = kwargs.get(u'configuration')
		self.scheme = kwargs.get(u'scheme')
		self.derivedDataPath = kwargs.get(u'derivedDataPath')

	def _cmd(self):
		opts = [u'xcodebuild']
		for k,v in enumerate(self.config):
			opts += [u'-{}'.format(k), v]
		opts += [u'-showBuildSettings']
		return u' '.join(opts)

	def read_settings(self):
		import os
		import string
		# TODO: fix fail
		l = os.popen(self._cmd()).read().split(u'\n')
		read_ctx = None
		for v in l:

			if  v.strip(string.whitespace) == u'':
				continue
			if u'User defaults from command line:' in v:
				read_ctx = self.user_default_from_command_line
				continue
			if u'Build settings from command line:' in v:
				read_ctx = self.build_settings_from_command_line
				continue
			if u'Build settings for action build and target' in v:
				read_ctx = self.build_settings_for_action_build_and_target
				continue
			if read_ctx:
				kv = v.split(u'=')
				if not len(kv) == 2:
					raise ValueError('settings not key value')
				read_ctx[kv[0].strip(string.whitespace)] = kv[1].strip(string.whitespace)


	def _CPP_HEADERMAP_FILE(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME).hmap
		'''
		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}.hmap'.format(product_name))

	def _CPP_HEADERMAP_FILE_FOR_ALL_NON_FRAMEWORK_TARGET_HEADERS(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME)-all-non-framework-target-headers.hmap
		'''

		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}-all-non-framework-target-headers.hmap'.format(product_name))

	def _CPP_HEADERMAP_FILE_FOR_ALL_TARGET_HEADERS(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME)-all-target-headers.hmap
		'''
		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}-all-target-headers.hmap'.format(product_name))

	def _CPP_HEADERMAP_FILE_FOR_GENERATED_FILES(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME)-generated-files.hmap
		'''
		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}-generated-files.hmap'.format(product_name))

	def _CPP_HEADERMAP_FILE_FOR_OWN_TARGET_HEADERS(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME)-own-target-headers.hmap
		'''
		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}-own-target-headers.hmap'.format(product_name))

	def _CPP_HEADERMAP_FILE_FOR_PROJECT_FILES(self):
		'''
		$(TEMP_DIR)/$(PRODUCT_NAME)-project-headers.hmap
		'''
		tmp_dir = self.get(TEMP_DIR)
		product_name = self.get(PRODUCT_NAME)
		import os
		return os.path.join(tmp_dir, u'{}-project-headers.hmap'.format(product_name))