import json, requests, sys, os


def main(config):
	# read config
	print('Reading', config, 'for configuration')
	with open(config, 'r') as f:
		config = json.load(f)

	# "download" stuff
	print('Downloading certs for', config['domain']);
	records = json.loads(requests.post(config['endpoint'] + '/ssl/retrieve/' + config['domain'], data = json.dumps(config)).text)
	assert records['status'] != 'ERROR', 'Error retrieving SSL.\n' + records['message']

	print()

	# write stuff
	for key, val in {'domainCertLocation': 'certificatechain', 'privateKeyLocation': 'privatekey', 'publicKeyLocation': 'publickey', 'intermediateCertLocation': 'intermediatecertificate'}.items():
		if not config[key]:
			continue
		print('Installing', config[key])
		try:
			os.mkdir(os.path.dirname(config[key]))
		except FileExistsError:
			pass
		if __debug__:
			print('Writing', val, 'to', config[key])
		os.system(f'rm -f {config[key]}')
		with open(config[key], 'w') as f:
			f.write(records[val])

		# set permissions
		os.chmod(config[key], 0o444)

	# run command
	if config['commandToReloadWebserver']:
		print('', 'Executing system command:', config['commandToReloadWebserver'], '', sep='\n')
		commandOutput=os.popen(config['commandToReloadWebserver']).read()		
		print(commandOutput)	


if __name__ == '__main__':
	argv = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__) + '/config.json'
	main(argv)