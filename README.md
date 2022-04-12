# <h1 align="center" >HunterXray</h1>  
奇安信Hunter平台与Xray扫描器的联动，实现Xray批量扫描Hunter的查询结果，并导出html文件。
## :headphones:声明：

1.本程序的`xray`批量扫描部分参考了`Cl0ud`师傅的文章：[Xray批量化自动扫描](https://www.cnblogs.com/Cl0ud/p/14001908.html)  
2.本程序仅供学习交流，若有拿本程序行违法之事的，后果自负。

## :book:如何使用：
1.直接去`release`下载可执行文件打开使用。  
2.需要确保：①把下载的`xray`文件改名为`xray.exe`②`data.conf`、`config.yaml`、`hunter-xray.exe`、`xray.exe`这几个文件在同一个文件下，`data.conf`文件名不可改变。  
3.`data.conf`中的参数务必填好：

| 参数&emsp;&emsp;&emsp;| 说明 |
| ------- | ------- |
|    api-key     |     在`https://hunter.qianxin.com/home/userInfo` 可以看到。|
|    cookie     |     登录之后，在`https://hunter.qianxin.com/`下按`F12`打开调试工具，点击`Console`，输入`document.cookie`，然后复制两个单引号内的内容，填上去就行。
| start_time | 例如`2021-04-12 00:00:00` |
| end_time | 例如`2022-04-11 00:00:00` |
| status_code | 以逗号分隔，如`200,401`，也可以直接写`200`或者`401` |
| sender | 发送人的QQ邮箱，例如`xxxxxx@qq.com` |
| pw | 在`https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256`可以查看，注意填写的是授权码，不是QQ邮箱密码。 |
| receivers | 接收人的QQ邮箱，例如`xxxxxxxx@qq.com` |  

（本程序目前只支持QQ邮箱）  
4.`xray`文件需自己下载，然后放入同一文件夹下。下载地址：[Xray](https://github.com/chaitin/xray)  
5.联系方式：  
&emsp;:snowflake:mailto:sharecat2022@qq.com  
&emsp;:sunny:https://github.com/W01fh4cker/HunterXray/issues
