'''
    
    Entropy AppleScript Wrapper
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Copyright (C) 2011 Eigenlogik. All Rights Reserved.
    Released under the MIT License    
    
'''

# Requires AppScript: http://appscript.sourceforge.net/
from appscript import app, k as konst
from datetime import datetime

entropy = app('Entropy')

class ArchiveItem(object):
    '''Represents a single file/folder within an archive'''
    
    def __init__(self, entryString):
        '''
        Initializes the instance using the description
        returned by the inspect command
        '''
        
        #The 4 parts are delimited using double space
        (is_dir, md, fs, path) = entryString.split("  ", 3)
        
        self.description = entryString
        self.is_dir = (is_dir=="F")
        self.file_size = fs
        self.path = path
        
        if len(md)>3:
            self.date_modified = datetime.strptime(md, "%b %d, %Y %I:%M %p")
        else:
            self.date_modified = None
                    
    def __repr__(self):
        return self.description


class ArchiveSettings(object):
    '''Settings for creating a new archive'''
    
    valid_keys = ('compression_level', 'password', 'encryption_method', 'volume_size')
    
    def __init__(self, compression_level=None, password=None, encryption_method=None, volume_size=None):
        
        # An integer specifying the level of compression
        # Valid values are 0 (Normal), 1 (Low), 2 (High) and 3 (No compression/Store)
        self.compression_level = compression_level
        
        # If specified, the archive contents will be encrypted using this password
        self.password = password
        
        # An integer specifying the encryption method.
        # Valid values are as follows.
        # Zip - 0: AES-256 Data Encryption
        # 7z  - 0: AES-256 Data Encryption, 1: AES-256 Data + Header Encryption
        # RAR - 0: AES-128 Data Encryption, 1: AES-128 Data + Header Encryption
        self.encryption_method = encryption_method
        
        # A string indicating the maximum volume size for a single split archive file
        # Example: "500 KB" , "700 MB", "4 GB". If no units are provided, MB is assumed.
        self.volume_size = volume_size
        
    def to_applescript(self):
        
        v=[(getattr(konst, x), getattr(self, x)) for x in self.valid_keys]
        return dict([x for x in v if x[1] is not None])

    
def unarchive(path, destination=None, password=None):
    """
    Extract an existing archive
    :param path: The archive to be extracted.
    :param destination: The destination folder for the extracted files.
                        The path must exist.
                        If omitted, Entropy follows the user preferences.
    :param password: The password for the archive.
                     If omitted, Entropy promps the user for a password if it
                     encounters an encrypted archive.
    """
    
    args = [x for x in (('destination',destination), ('password',password)) if x[1] is not None]    
    entropy.unarchive(path, **dict(args))

    
def archive(path, files, settings=None):
    """
    Create a new archive
    The format of the archive is automatically deduced from the file extension.
    :param path: The path of the new archive.
                 There should be no existing file at the given path.
                 The parent directory of the archive should exist.
    :param files: The files to add to the archive.
    :param settings: An ArchiveSettings instance populated with the desired settings.
                     If omitted, Entropy follows the user preferences.
    """
    args = { 'files':files }

    conv_settings = settings.to_applescript() if settings else None    
    if conv_settings:
        args['settings'] = conv_settings

    entropy.archive(path, **args)


def inspect(path):
    '''
    List the files inside an archive
    :return: A list of ArchiveItem instances representing the archive contents.
    '''
    return map(ArchiveItem, entropy.inspect(path, details=True))
    
