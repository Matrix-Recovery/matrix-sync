# Sync a twrp minimal manifest, patch it for building Matrix Recovery, and sync the Matrix Recovery sources

[![Check Upstream Updates](https://github.com/Matrix-Recovery/matrix-sync/actions/workflows/check-upstream.yml/badge.svg)](https://github.com/Matrix-Recovery/matrix-sync/actions/workflows/check-upstream.yml)

## To fetch the manifest for the first time, follow these steps: ##
------------------------------------

### 1. Fetch these sync tools ###
	mkdir ~/Matrix_Recovery_sync
	cd ~/Matrix_Recovery_sync
	git clone https://github.com/Matrix-Recovery/matrix-sync

### 2. Do the syncing (this can take up to 1-2 hours, and can use up to 40GB-80GB of disk space) - below is an example, for 12.1 (amend as required for other branches) ##
	cd ~/Matrix_Recovery_sync
	./matrix_sync.sh --branch 12.1 --path ~/matrix_12.1
Notes:
- You *MUST* supply an *ABSOLUTE* path name for the "--path" switch
- If the sync process gets stuck, you might need to terminate it with Ctrl-C and then run the script again
- If you want to use ssh for cloning the OrangeFox sources and vendor tree, export "USE_SSH=1" before starting, or supply "--ssh 1" on the command line
- After the initial sync process, you must then clone your device trees, before you can build for your device

## These manifest branches are supported by the matrix_sync.sh script: ##
----------------------------------
	14.1
	12.1

## To update the manifest, and the recovery sources, and the vendor trees (given the example of the 12.1 branch above), follow these steps: ##
----------------------------------
	cd ~/matrix_12.1/
	repo sync # (ignore all errors and suggestions relating to "android_bootable_recovery")
	cd ~/matrix_12.1/bootable/recovery/
	git pull
	cd ~/matrix_12.1/vendor/recovery/
	git pull

## To update only the recovery sources (given the example of the 12.1 branch above), follow these steps: ##
----------------------------------
	cd ~/matrix_12.1/bootable/recovery/
	git pull

## To update only the vendor tree (given the example of the 12.1 branch above) follow these steps: ##
----------------------------------
	cd ~/matrix_12.1/vendor/recovery/
	git pull

## To update only the manifest (given the example of the 12.1 branch above), follow these steps: ##
----------------------------------
	cd ~/matrix_12.1/
	repo sync # (ignore all errors and suggestions relating to "android_bootable_recovery")

## To see the syntax of the matrix_sync.sh script, follow these steps: ##
----------------------------------
	cd ~/Matrix_Recovery_sync/sync/
	./matrix_sync.sh --help


# For instructions on building OrangeFox, see:
"https://wiki.orangefox.tech/en/dev/building"

