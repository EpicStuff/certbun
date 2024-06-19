import json, requests, sys, os


def main(config):
	with open(config, 'r') as f:
		config = json.load(f)
	print('Downloading certs for ' + config['domain']);
	records = json.loads(requests.post(config['endpoint'] + '/ssl/retrieve/' + config['domain'], data = json.dumps(config)).text)
	if records['status'] == 'ERROR':
		print('Error retrieving SSL.');
		print(records['message']);
		sys.exit();
	

	if config['domainCertLocation']:
		print('Installing ' + config['domainCertLocation'])
		with open(config['domainCertLocation'], 'w') as f:
			f.write(records['certificatechain'])

	if config['privateKeyLocation']:
		print('Installing ' + config['privateKeyLocation'])
		with open(config['privateKeyLocation'], 'w') as f:
			f.write(records['privatekey'])

	if config['publicKeyLocation']:
		print('Installing ' + config['publicKeyLocation'])
		with open(config['publicKeyLocation'], 'w') as f:
			f.write(records['publickey'])

	if config['intermediateCertLocation']:
		print('Installing ' + config['intermediateCertLocation'])
		with open(config['intermediateCertLocation'], 'w') as f:
			f.write(records['intermediatecertificate'])
	
	if config['commandToReloadWebserver']:
		print('\nExecuting system command:\n' + config['commandToReloadWebserver'] + '\n')
		commandOutput=os.popen(config['commandToReloadWebserver']).read()		
		print(commandOutput + '\n')	
	

if __name__ == '__main__':
	argv = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
	main(argv)