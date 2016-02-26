import gzip
import sys
import os

def list_files(path):
    return os.listdir(path)

def filter_files(filenames, filetype):
    len_of_type = len(filetype)
    return filter(lambda fname:
            len(fname)>=len_of_type and fname[-len_of_type:] == filetype,
            filenames)

def read_gzip(src):
    with gzip.open(src, 'rb') as gzf:
        f_content = gzf.read()
    return f_content

if __name__ == '__main__':
    src_path = sys.argv[1]
    dest     = sys.argv[2]

    # 4GB
    length = 4 * 1024 * 1024 * 1024
    if len(sys.argv) > 3:
        length = int(sys.argv[3])
        if length > 0:
            # x MB
            length = length * 1024 * 1024

    filelist = filter_files(list_files(src_path), '.gz')
    f = gzip.open(dest + '.gz', 'wb')
    nl = 1
    for filename in filelist:
        content = read_gzip(os.path.join(src_path,filename))
        for line in content:
            if f.tell() + len(line) <= nl * length:
                f.write(line)
            else:
                f.close()
                print('part ' + nl + 'done')
                f = gzip.open(dest + '.' + nl + '.gz', 'wb')
    f.close()

    print('all done')
