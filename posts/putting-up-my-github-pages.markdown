Title: 折腾一下GitHub Pages
Date: 2011-05-19
Slug: putting-up-my-github-pages


就这么几个问题：

* 对标签的支持太差劲了。
* 插入长一点代码，用`{% include %}`[^liquid-markup-escape]的话，得把代码放在`_include`目录下，这样又得搞一套命名机制或者目录结构来避免重名。
* 虽然文件名的格式是固定的，提供的脚本里却没提供建post的功能。
* GitHub不管你在`_config.yml`里把`source`设置成什么，`source`永远是仓库根目录。

要注意的是：

* 既想正确显示中文开头的列表，又想有脚注的话，`markdown`要设置成`kramdown`，不过`kramdown`的ordered list不能自动编号


[^liquid-markup-escape]: 插入`{% include %}`，请参考[How to escape liquid template tags?](http://stackoverflow.com/questions/3426182/how-to-escape-liquid-template-tags)
