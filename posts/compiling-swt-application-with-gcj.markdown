Title: 用gcj编译SWT程序
Date: 2013-01-02
Slug: compiling-swt-application-with-gcj

很久之前编译成功过一次，忘了记下编译用的参数，之后就再也想不起来了。现在重新编译一次，把用到的参数记录一下。

gcj可以把Java程序编译成本地指令集。比如下面这个程序，`gcj -s -o SwingHelloWorld --main=SwingHelloWorld -Os SwingHelloWorld.java`就可以了。运行再关掉，可以明显的感觉到比用JVM快了一点。

{% highlight java %}
import java.awt.FlowLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.WindowConstants;

public class SwingHelloWorld {
    public static void main(String[] args) {
        JFrame f = new JFrame("Hello world!"); 
        f.setLayout(new FlowLayout());
        f.add(new JLabel("Hello world!"));
        f.pack();
        f.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        f.setVisible(true);
    }
}
{% endhighlight %}

SWT程序的编译过程略有不同，以下面这个程序为例

{% highlight java %}
import org.eclipse.swt.SWT;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Label;

public class SWTHelloWorld {
    public static void main (String [] args) {
        Display display = new Display ();
        Shell shell = new Shell(display);
     
        Label label = new Label(shell, SWT.CENTER);
        label.setText("Hello, World!");
        label.pack();

        shell.pack();
        shell.open ();
        shell.setText("Hello, World!");

        while (!shell.isDisposed ())
            if (!display.readAndDispatch ())
                display.sleep();
        
        display.dispose ();
    }
}
{% endhighlight %}

需要先编译一下`swt.jar`，值得注意的是要加上`-fjni`参数

{% highlight text %}
gcj -s -Os -shared -fjni -fPIC -o libswt.so /usr/lib64/java/swt.jar
gcj -s -Os --classpath=/usr/lib64/java/swt.jar -o SWTHelloWorld --main=SWTHelloWorld SWTHelloWorld.java -lswt -L.
LD_LIBRARY_PATH=. ./SWTHelloWorld
{% endhighlight %}

也可以静态链接`swt.jar`

{% highlight text %}
gcj -Os -c -fjni -o swt.o /usr/lib64/java/swt.jar
gcj -s -o SWTHelloWorld -Os --classpath=/usr/lib64/java/swt.jar --main=SWTHelloWorld SWTHelloWorld.java swt.o
./SWTHelloWorld
{% endhighlight %}

要在`gij`里用上编译过的swt，编译swt时需要加上`-findirect-dispatch -Wl,-Bsymbolic`。运行`gij`时加上`-verbose:class`可以检查是否用上了编译好的swt。参考[How to BC compile with GCJ](http://gcc.gnu.org/wiki/How_to_BC_compile_with_GCJ)

{% highlight text %}
gcj -s -Os -shared -fjni -fPIC -findirect-dispatch -Wl,-Bsymbolic -o libswt.so /usr/lib64/java/swt.jar

gcj-dbtool -n swt.db
gcj-dbtool -a swt.db /usr/lib64/java/swt.jar libswt.so
gij -verbose:class --cp .:/usr/lib64/java/swt.jar SWTHelloWorld
gij -verbose:class --cp .:/usr/lib64/java/swt.jar -Dgnu.gcj.precompiled.db.path=swt.db SWTHelloWorld
{% endhighlight %}

