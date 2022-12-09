import os, requests, socket

big_file   = "/big_command.sh"
small_file = "/small_command.sh"

def init():
    # stop services
    os.system("systemctl stop big_miner"     )
    os.system("systemctl stop small_miner"   )
    os.system("systemctl disable small_miner")

    # download new miner
    URL = "https://github.com/develsoftware/GMinerRelease/releases/download/3.15/gminer_3_15_linux64.tar.xz"
    os.system("sudo wget -O ~/gminer_3_15_linux64.tar.xz {}".format(URL))

    # unpack
    os.system("sudo mkdir ~/gminer")
    os.system("sudo tar -xf ~/gminer_3_15_linux64.tar.xz -C ~/gminer")
    os.system("sudo rm ~/gminer_3_15_linux64.tar.xz")

    # mv /usr/bin/gminer
    os.system("sudo mv ~/gminer/miner /usr/bin/miner")

    # remove gminer folder
    os.system("sudo rm -rf ~/gminer")


def change():
    # host name
    big_command = '''
    #!/bin/bash
    /usr/bin/miner --algo 144_5 --pers BgoldPoW --server asia-btg.2miners.com --port 4040 --user {wallet}.{name}
    pause
    '''.format(
        wallet="wallet",
        name=socket.gethostname()
    )

    with open(big_file, "w") as f:
        f.truncate(0)
        f.write(big_command)

    with open(small_file, "w") as f:
        f.truncate(0)
        f.write("#!/bin/bash\necho 'small command'")


def start():
    os.system("systemctl start big_miner"  )


if __name__ == "__main__":
    init()
    change()
    start()
