__author__ = 'euriion'

from pywebhdfs.webhdfs import PyWebHdfsClient

hdfs = PyWebHdfsClient(host='192.168.5.182', port='50070', user_name='ndap')
# dirs = hdfs.list_dir("/")
# for dir in dirs['FileStatuses']['FileStatus']:
#     print(dir)

print(hdfs.make_dir("ndash/test1"))




