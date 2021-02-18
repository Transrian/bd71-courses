```md
[2021-02-17T18:14:38,651][ERROR][o.e.b.ElasticsearchUncaughtExceptionHandler] [X970670] uncaught exception in thread [main]
org.elasticsearch.bootstrap.StartupException: BindHttpException[Failed to bind to [::1]:80]; nested: BindException[Permission non accordée];
	at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:163) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Elasticsearch.execute(Elasticsearch.java:150) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.cli.EnvironmentAwareCommand.execute(EnvironmentAwareCommand.java:75) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.cli.Command.mainWithoutErrorHandling(Command.java:116) ~[elasticsearch-cli-7.11.1.jar:7.11.1]
	at org.elasticsearch.cli.Command.main(Command.java:79) ~[elasticsearch-cli-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:115) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Elasticsearch.main(Elasticsearch.java:81) ~[elasticsearch-7.11.1.jar:7.11.1]
Caused by: org.elasticsearch.http.BindHttpException: Failed to bind to [::1]:80
	at org.elasticsearch.http.AbstractHttpServerTransport.bindAddress(AbstractHttpServerTransport.java:180) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.http.AbstractHttpServerTransport.bindServer(AbstractHttpServerTransport.java:145) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.http.netty4.Netty4HttpServerTransport.doStart(Netty4HttpServerTransport.java:231) ~[?:?]
	at org.elasticsearch.xpack.security.transport.netty4.SecurityNetty4HttpServerTransport.doStart(SecurityNetty4HttpServerTransport.java:67) ~[?:?]
	at org.elasticsearch.common.component.AbstractLifecycleComponent.start(AbstractLifecycleComponent.java:48) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.node.Node.start(Node.java:898) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Bootstrap.start(Bootstrap.java:310) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Bootstrap.init(Bootstrap.java:396) ~[elasticsearch-7.11.1.jar:7.11.1]
	at org.elasticsearch.bootstrap.Elasticsearch.init(Elasticsearch.java:159) ~[elasticsearch-7.11.1.jar:7.11.1]
	... 6 more
Caused by: java.net.BindException: Permission non accordée
	at sun.nio.ch.Net.bind0(Native Method) ~[?:?]
	at sun.nio.ch.Net.bind(Net.java:550) ~[?:?]
	at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:249) ~[?:?]
	at io.netty.channel.socket.nio.NioServerSocketChannel.doBind(NioServerSocketChannel.java:134) ~[?:?]
	at io.netty.channel.AbstractChannel$AbstractUnsafe.bind(AbstractChannel.java:550) ~[?:?]
	at io.netty.channel.DefaultChannelPipeline$HeadContext.bind(DefaultChannelPipeline.java:1334) ~[?:?]
	at io.netty.channel.AbstractChannelHandlerContext.invokeBind(AbstractChannelHandlerContext.java:506) ~[?:?]
	at io.netty.channel.AbstractChannelHandlerContext.bind(AbstractChannelHandlerContext.java:491) ~[?:?]
	at io.netty.channel.DefaultChannelPipeline.bind(DefaultChannelPipeline.java:973) ~[?:?]
	at io.netty.channel.AbstractChannel.bind(AbstractChannel.java:248) ~[?:?]
	at io.netty.bootstrap.AbstractBootstrap$2.run(AbstractBootstrap.java:356) ~[?:?]
	at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:164) ~[?:?]
	at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:472) ~[?:?]
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:500) ~[?:?]
	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:989) ~[?:?]
	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74) ~[?:?]
	at java.lang.Thread.run(Thread.java:832) [?:?]
uncaught exception in thread [main]
BindHttpException[Failed to bind to [::1]:80]; nested: BindException[Permission non accordée];
Likely root cause: java.net.BindException: Permission non accordée
	at java.base/sun.nio.ch.Net.bind0(Native Method)
	at java.base/sun.nio.ch.Net.bind(Net.java:550)
	at java.base/sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:249)
	at io.netty.channel.socket.nio.NioServerSocketChannel.doBind(NioServerSocketChannel.java:134)
	at io.netty.channel.AbstractChannel$AbstractUnsafe.bind(AbstractChannel.java:550)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.bind(DefaultChannelPipeline.java:1334)
	at io.netty.channel.AbstractChannelHandlerContext.invokeBind(AbstractChannelHandlerContext.java:506)
	at io.netty.channel.AbstractChannelHandlerContext.bind(AbstractChannelHandlerContext.java:491)
	at io.netty.channel.DefaultChannelPipeline.bind(DefaultChannelPipeline.java:973)
	at io.netty.channel.AbstractChannel.bind(AbstractChannel.java:248)
	at io.netty.bootstrap.AbstractBootstrap$2.run(AbstractBootstrap.java:356)
	at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:164)
	at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:472)
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:500)
	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:989)
	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
	at java.base/java.lang.Thread.run(Thread.java:832)
```