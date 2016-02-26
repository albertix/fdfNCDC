# 需要Python
    
    https://www.python.org/downloads/release/python-2711/
    

# 用法

    ./mutli_http.py start_year end_year dest_dir theards

    ./untar.py src_dir dest_file [size(MB)]

# 说明
    
    mutli_http会使用ftp方式（使用了[1]中代码）获取年度数据表，并写入`year.json`；而后使用指定的进程数，按照`year.json`，采用http方式下载。
    
    untar会将指定文件夹内所有`.gz`解压，写入单一`dest_file.gz`，目标文件大小默认为4GB，若超出，会将后续文件命名为`dest_file.x.gz`。
    

[1](http://www.cnblogs.com/fengfenggirl/archive/2013/04/04/2998997.html)
[2](http://blog.csdn.net/liufeng1980423/article/details/39004095)
