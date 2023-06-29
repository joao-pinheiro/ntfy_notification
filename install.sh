#!/bin/bash
KLIPPER_PATH="${HOME}/klipper"
SYSTEMDDIR="/etc/systemd/system"


#------------------------------------------------------------------------------------------------------------
is_root()
{
    if [ "$EUID" -eq 0 ]; then
        echo "This script must not run as root"
        exit -1
    fi
}
#------------------------------------------------------------------------------------------------------------

restart_klipper()
{
    echo "Restarting klipper..."
    sudo systemctl restart klipper
}

klipper_installed()
{
    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F "klipper.service")" ]; then
        echo "klipper service found!"
    else
        echo "klipper service not found, please install klipper first"
        exit -1
    fi

}
#------------------------------------------------------------------------------------------------------------

run_pip()
{
   ~/klippy-env/bin/pip install -r requirements.txt

}

install()
{
    echo "Linking ntfy_notification to klipper..."
    ln -sf "${SRCDIR}/ntfy_notification.py" "${KLIPPER_PATH}/klippy/extras/ntfy_notification.py"
}

#------------------------------------------------------------------------------------------------------------
# Force script to exit if an error occurs
set -e

# Find SRCDIR from the pathname of this script
SRCDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/src/ && pwd )"

# Parse command line arguments
while getopts "k:" arg; do
    case $arg in
        k) KLIPPER_PATH=$OPTARG;;
    esac
done

# main
is_root
klipper_installed
run_pip
install
restart_klipper