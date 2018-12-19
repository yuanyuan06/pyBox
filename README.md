* 打包
 
`
pyinstaller -F boxplus.py -i E:\pySpaces\msgParse\ico.ico -w
`
* 性能分析

`
python -m cProfile -o result.out boxplus.py
`
