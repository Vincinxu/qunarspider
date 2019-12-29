# 去哪儿网景点门票搜索爬虫


## 主要使用技术：
  requests，urllib，mongodb，xpath

## 流程：
  先分析要爬取的URL的组成规律，提取变量，删掉不需要的参数，重新组织一个爬取的URL，然后获取页面源码，接着获取源码后使用xpath方法提取各景点的信息，如景点的图片，名称， 票价，地点等等一些信息。最后将提取的信息用字典表示并保存到mongodb里，此次对整个爬取过程使用的方法都进行封装成一个类，仅把要常改变的三个参数留下来， 分别是搜索关键词，爬取总页数和mongodb的连接uri， 方便下次调用该类时可以根据自己的要求去定义爬取范围， 数量和连接其他的mongodb进行保存。
