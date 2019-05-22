import jks
import sys, base64, textwrap
import subprocess
import getpass
import argparse
import secrets

def parse_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument("--d", dest='decrypt', action='store_true')
	parser.add_argument("--c", dest='chall', action='store_true')
	parser.add_argument("--mode", dest='mode', type=str, required=True)
	parser.add_argument("--keystore", dest='keystore', type=str, required=True)
	parser.add_argument("--files", nargs='+', dest='files', type=str)
	parser.add_argument("--alias", dest='alias', type=str, required=True)

	return parser.parse_args()

def main():
	MODE = {
  	"cbc": "aes-256-cbc",
 	"ecb": "aes-256-ecb",
 	"ofb": "aes-256-ofb",
 	"ctr": "aes-256-ctr"
	}
	arguments = parse_arg()
	try:
		selected_mode = MODE[arguments.mode]
	except KeyError:
		print("Incorrect mode. Using default mode - cbc")
		selected_mode = MODE["cbc"]
	try:
		test = getpass.getpass()
		ks = jks.KeyStore.load(arguments.keystore, test)
		key = ks.secret_keys[arguments.alias].key
	except (FileNotFoundError, KeyError):
		gen_keystore = subprocess.Popen(["keytool", "-genseckey", "-alias", f"{arguments.alias}", "-keysize", "256", "-keyalg", "aes", "-keystore", f"{arguments.keystore}", "-storepass", f"{test}", "-storetype", "jceks"])
		gen_keystore.wait()
		ks = jks.KeyStore.load(arguments.keystore, test)
		key = ks.secret_keys[arguments.alias].key
	if arguments.files:
		if not arguments.decrypt:
			if not arguments.chall:
				for file in arguments.files:
					if arguments.mode == "ecb":
						test = subprocess.Popen(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-K", f"{key.hex()}", "-in", file, "-out", f"{file}.enc"], stderr=subprocess.DEVNULL)
						test.wait()
					else:
						with open('/dev/random', 'rb') as f:
							iv = f.read(16).hex()
						test = subprocess.Popen(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-K", f"{key.hex()}","-iv",f"{iv}", "-in", file, "-out", f"{file}.enc2"], stderr=subprocess.DEVNULL)
						test.wait()
			else:
				if len(arguments.files) >= 2:
					file = secrets.choice((arguments.files[0], arguments.files[1]))
					test = subprocess.Popen(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}", "-in", file, "-out", "chall_file.enc"], stderr=subprocess.DEVNULL)
					test.wait()
		else:
			for file in arguments.files:
				test = subprocess.Popen(["openssl", "enc","-d", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}", "-in", file, "-out", f"{file}.dec"], stderr=subprocess.DEVNULL)
				test.wait()
	else:
		if not arguments.decrypt:
			while 1:
				if not arguments.chall:
					mess = input("Enter the message: ")
					if arguments.mode == "ecb":
						echo = subprocess.Popen(["echo", "-n", mess], stdout=subprocess.PIPE)
						output = subprocess.check_output(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}"], stderr=subprocess.DEVNULL, stdin=echo.stdout)
						print(output)
						echo2 = subprocess.Popen(["echo","-n", output], stdout=subprocess.PIPE)
						output2 = subprocess.check_output(["openssl", "enc", "-d", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}"], stderr=subprocess.DEVNULL, stdin=echo2.stdout)
						print(mess == output2.decode())
					else:
						with open('/dev/random', 'rb') as f:
							iv = f.read(16).hex()
						echo = subprocess.Popen(["echo", "-n", mess], stdout=subprocess.PIPE)
						output = subprocess.check_output(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-K", f"{key.hex()}","-iv",f"{iv}"], stderr=subprocess.DEVNULL, stdin=echo.stdout)
						print(output)
						echo2 = subprocess.Popen(["echo","-n", output], stdout=subprocess.PIPE)
						output2 = subprocess.check_output(["openssl", "enc", "-d", f"-{selected_mode}", "-nosalt", "-K", f"{key.hex()}","-iv",f"{iv}"], stderr=subprocess.DEVNULL, stdin=echo2.stdout)
						print(mess == output2.decode())
				else:
					mess = input("Enter the first message: ")
					mess2 = input("Enter the second message: ")
					message = secrets.choice((mess, mess2))
					echo = subprocess.Popen(["echo", "-n", message], stdout=subprocess.PIPE)
					output = subprocess.check_output(["openssl", "enc", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}"], stderr=subprocess.DEVNULL, stdin=echo.stdout)
					print(output)
					# echo2 = subprocess.Popen(["echo","-n", output], stdout=subprocess.PIPE)
					# output2 = subprocess.check_output(["openssl", "enc", "-d", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}"], stderr=subprocess.DEVNULL, stdin=echo2.stdout)
					# print(mess == output2.decode())
		else:
			mess = input("Enter the ciphertext: ")
			echo2 = subprocess.Popen(["echo","-n", mess], stdout=subprocess.PIPE)
			output2 = subprocess.check_output(["openssl", "enc", "-d", f"-{selected_mode}", "-nosalt", "-pass",f"pass:{key.hex()}"], stderr=subprocess.DEVNULL, stdin=echo2.stdout)
			print(output2.decode())

if __name__ == '__main__':
	main()
