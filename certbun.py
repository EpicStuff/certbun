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
	for key, val in {'domainCertLocation': 'certificatechain', 'privateKeyLocation': 'privatekey', 'privateKeyLocation': 'publickey', 'intermediateCertLocation': 'intermediatecertificate'}.items():
		if not config[key]:
			continue
		print('Installing', config[key])
		try:
			os.mkdir(os.path.dirname(config[key]))
		except FileExistsError:
			pass
		with open(config[key], 'w') as f:
			f.write(records[val])

	# run command
	if config['commandToReloadWebserver']:
		print('', 'Executing system command:', config['commandToReloadWebserver'], '', sep='\n')
		commandOutput=os.popen(config['commandToReloadWebserver']).read()		
		print(commandOutput)	


if __name__ == '__main__':
	argv = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__) + '/config.json'
	main(argv)