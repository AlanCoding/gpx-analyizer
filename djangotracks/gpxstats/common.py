import os


def get_file_list(path='archive/'):
    cwd = os.getcwd()

    if path.startswith('/'):
        archive_dir = os.listdir(path)
    else:
    	archive_dir = os.path.join(cwd, path)
    raw_filelist = os.listdir(archive_dir)

    filelist = []
    for f in raw_filelist:
    	if len(f) > 4 and f[-4:] == '.gpx':
    		filelist.append(f)

    return filelist
