from os import path, listdir, mkdir
from shutil import move
from datetime import datetime, timedelta
from getpass import getuser
from optparse import OptionParser

# Define number of days as threshold, used if no command line args found
threshold_days = 30
# Get netid to build path to current users desktop
user = getuser()
desktop_path = f"C:/Users/{user}/Desktop"
# Specifiy where to archive files, used if no command line args found
old_files_sub_dir = "old_files"


def archive(days, sub_folder):

    # Get list of files
    files = listdir(desktop_path)
    # Get the date of today - threshold days for comparison
    date_one_month_ago = datetime.today() - timedelta(days=days)

    # Create the archive folder if it doesn't already exist
    if not path.exists(path.join(desktop_path, sub_folder)):
        mkdir(path.join(desktop_path, sub_folder))

    # Loop through all files on desktop and move if they haven't been modified in after the threshold days
    for f in files:
        # Only work on file if it is not a shortcut
        _, file_extension = path.splitext(f)
        if not file_extension == '.lnk':
            mod_date = datetime.fromtimestamp(path.getmtime(path.join(desktop_path, f)))
            if mod_date < date_one_month_ago:
                move(path.join(desktop_path, f), path.join(desktop_path, sub_folder, f))
                print(f"{f} moved to {sub_folder}")

if __name__ == "__main__":

    days = None
    sub_folder = None

    # Setup option parsing for command line inputs
    parser = OptionParser()
    parser.add_option("-d", "--days", dest="days", help="How many days as a threshold", metavar="DAYS")
    parser.add_option("-f", "--folder", dest="sub_folder", help="Sub folder name for files to be archived too", metavar="FOLDER")
    (options, args) = parser.parse_args()

    # Check for inputs or just use default global values
    if(options.days):
        days = int(options.days)
    else:
        days = threshold_days

    print(f"Usinging {days} days threshold")

    if(options.sub_folder):
        sub_folder = options.sub_folder
    else:
        sub_folder = old_files_sub_dir

    print(f"Usinging {sub_folder} as subfolder")
 
    # Run archiving
    archive(days, sub_folder)

