# certbun

Porkbun's minimalist Certbot alternative leaves the certificate generation to Porkbun and simply downloads certs to the location of your choosing, then reloads your web server with the command of your choosing.

## Why?
Automated SSL cert generation software such as Certbot can be tricky to set up, especially if you want a wildcard certificate, which requires DNS access, or you use an unusual web server. Porkbun already has a massive certificate generation infrastructure, and a certificate API. You can let Porkbun handle the hassle of generating the certificate, and use certbun to pull it via the API and install it locally.

## Before you install
We recommend [manually downloading the certificate bundle](https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works) and getting it working with your web server first, before trying to automate the process via certbun. Once your web server is reliably serving HTTPS traffic with no issue, you can automate the renewal process with certbun.

## Installation 

 1. Install Python if it's not already installed. If you're running Windows, you should download the most recent production Python version.
 2. Download and uncompress certbun to the folder of your choice
 3. Install the *requests* library:
 	`pip install requests`
 4. Rename config.json.example to config.json and paste in your generated API and Secret keys. Save the config file. If you haven't yet generated the keys, check out our [Getting Started Guide.](https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api) 
 5. Configure the config file's **domain**
field with the domain you wish to pull certs from.
6. Configure the config file's  **domainCertLocation**, **privateKeyLocation**, **intermediateCertLocation**, and **publicKeyLocation** fields with where you want the retrieved certificates to be saved. If your web server doesn't need the intermediate cert and public key, you can leave it blank.
7. Configure the config file's **commandToReloadWebserver** field with the command you typically execute to get your web server to load the new certificate bundle. This command will run immediately after the files have been copied into place. You can also leave this blank.


## Running the client

    python certbun.py /path/to/config.json 

Will default to using the config.json file in the same directory as the script.

### Add it to cron
Since this client works in a fairly non-sophisticated way, you probably just want to download certs every week or so and restart your web server. 

Edit your crontab with:

	crontab -e

If you've never done this before, you may want to read a guide on how to do it. 

Assuming you wanted certbun to run once per week, you'd add a line like:

	23 1 * * 1 python /path/to/certbun.py /path/to/config.json | logger
