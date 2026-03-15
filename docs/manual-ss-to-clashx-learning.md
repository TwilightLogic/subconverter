# 手动把 `ss://` 节点转成 ClashX / Clash Meta 配置

这份文档记录了我们在 fork 当前仓库后，通过一次真实排障学到的内容：如何把单条 `ss://` 分享链接手动转成 ClashX / Clash Meta 可导入的 YAML 配置，以及为什么这个方法能工作。

这不是 `subconverter` 的自动转换说明，而是一份学习文档。它适合用来理解节点格式、验证单个节点是否可用，以及帮助后续把人工流程对照到项目源码中的自动流程。

## 1. 背景：`ss://` 链接是什么

单条 Shadowsocks 节点通常长这样：

```txt
ss://BASE64(method:password@server:port)#name
```

或者：

```txt
ss://BASE64(method:password)@server:port#name
```

它表示的是一个节点分享链接，不是 Clash 订阅文档，也不是一份完整的 YAML 配置。

这条链接里真正有用的信息通常只有几类：

- `method` / `cipher`
- `password`
- `server`
- `port`
- `name`

我们的手动转换，本质上就是把这些字段提取出来，再按 Clash 的字段名重新组织。

## 2. 为什么不能直接把 `ss://` 当 Clash 订阅导入

这是这次排障里最关键的认知。

`ss://` 链接是“单节点分享格式”，而 ClashX / Clash Meta 更常吃的是：

- 一份完整的 Clash YAML
- 或者一个返回 Clash YAML 的订阅地址

所以：

```txt
ss:// 单节点分享链接
  !=
Clash 订阅文档
```

如果客户端没有直接支持把 `ss://` 作为单节点导入，就需要先把它翻译成 Clash YAML。

## 3. 手动转换流程

整体思路可以看成下面这条链：

```txt
ss:// 链接
  ↓
手动解析 Base64 和结构
  ↓
得到 server / port / cipher / password / name
  ↓
写成 Clash YAML 的 proxies
  ↓
把节点挂到 proxy-groups
  ↓
给出最小 rules
  ↓
导入 ClashX / Clash Meta
```

### 3.1 从链接里取出字段

以下用脱敏后的示例说明：

```txt
ss://BASE64(aes-256-gcm:your-password@example.com:7793)#example-ss-node
```

人工解析后，最终会得到类似这样的字段：

- `name`: `example-ss-node`
- `server`: `example.com`
- `port`: `7793`
- `cipher`: `aes-256-gcm`
- `password`: `your-password`

### 3.2 写成最小可用的 Clash Meta 配置

下面这份配置适合先做“节点是否真正可用”的验证：

```yaml
mode: global
log-level: warning
ipv6: false

proxies:
  - name: example-ss-node
    type: ss
    server: example.com
    port: 7793
    cipher: aes-256-gcm
    password: your-password
    udp: true

proxy-groups:
  - name: GLOBAL
    type: select
    proxies:
      - example-ss-node
      - DIRECT

proxy-providers:

rule-providers:

rules:
  - MATCH,GLOBAL
```

这份配置里最重要的不是语法，而是结构：

- `proxies`: 定义节点本身
- `proxy-groups`: 定义客户端里真正可选择的组
- `rules`: 决定流量走向

如果只是写了 `proxies`，但没有把节点放进 `proxy-groups`，客户端里往往不会出现可切换的选项。

## 4. 为什么 `proxy-groups` 很重要

这是这次排障里另一个非常具体的收获。

很多时候问题不是“节点不通”，而是：

```txt
节点定义成功
  !=
客户端里一定能选到它
```

只有当节点被放进一个组里，比如：

```yaml
proxy-groups:
  - name: GLOBAL
    type: select
    proxies:
      - example-ss-node
      - DIRECT
```

ClashX / Clash Meta 才会把它暴露成可切换的代理入口。

可以把它理解成：

```txt
proxies      = 原材料
proxy-groups = 用户真正操作的入口
```

## 5. 如何确认代理真的生效了

能看到节点，不代表流量一定经过它。

实际验证时，至少要确认下面几件事：

1. 这份 YAML 已经被 ClashX / Clash Meta 正确加载
2. `GLOBAL` 或对应组里，当前选中的确实是目标节点，不是 `DIRECT`
3. 路由模式适合测试。初次验证最简单的是 `mode: global`
4. 客户端已经开启系统代理，例如 `Set as System Proxy`

可以把这条链记成：

```txt
配置能加载
  ↓
节点能显示
  ↓
组里能选中
  ↓
系统代理已开启
  ↓
浏览器 / App 流量才会经过 Clash
  ↓
公网 IP 才会变化
```

## 6. 常见问题排查

### 6.1 `GLOBAL` 组里没有我的节点

优先检查：

- YAML 里 `proxy-groups` 是否为空
- 组里的 `proxies` 列表里是否真的写了节点名
- 节点名是否和 `proxies` 里的 `name` 完全一致
- 文件里是否混进了多余文本，导致 YAML 解析异常

### 6.2 测速成功，但查 IP 还是中国

这通常说明“节点能连”，但不一定说明“当前测试流量真的走了代理”。

优先检查：

- 当前组是否选中了节点而不是 `DIRECT`
- 当前是否处于 `global` 或符合预期的规则模式
- 是否打开了系统代理
- 查 IP 的浏览器或 App 是否真的使用系统代理

需要特别记住：

```txt
测速成功
  !=
所有流量都已走代理
```

### 6.3 只有一条 `ss://`，这算配置了机场吗

更准确地说，这是“成功配置并使用了一条机场节点”，但还不是完整的订阅式机场配置。

区别在于：

- 手动方式：适合单个节点验证和学习
- 订阅方式：适合自动更新、多节点维护、长期使用

## 7. 这种手动方法适合什么时候

这条路径很适合以下场景：

- 只有一条单独的 `ss://` 节点，想尽快验证它是否可用
- 想理解 `ss://` 和 Clash YAML 之间是怎么映射的
- 想在阅读 `subconverter` 源码前，先建立正确的格式心智模型
- 想确认问题出在节点本身，还是出在客户端配置

但它不适合直接替代完整订阅方案，因为它没有自动处理：

- 机场节点变更
- 多节点更新
- 自动测速与分组维护
- 长期订阅同步

## 8. 这和项目里的自动流程是什么关系

这次手动方法，并不是发明了一条新的转换路径，而是在人工复现项目内部已经存在的思路。

项目里的自动流程可以粗略理解为：

```txt
ss:// 链接
  ↓
解析成统一内部节点结构 Proxy
  ↓
再导出成目标格式
  - clash
  - surge
  - quanx
  - 其他
```

和这次学习直接相关的源码位置有：

- [subparser.cpp](/Users/zibin/Downloads/My/app/subconverter/src/parser/subparser.cpp): 解析 `ss://`、`ssr://`、`vmess://` 等输入格式
- [subexport.cpp](/Users/zibin/Downloads/My/app/subconverter/src/generator/config/subexport.cpp): 把内部 `Proxy` 结构导出成 Clash 等目标格式

对 Shadowsocks 来说，我们手动做的事近似于：

```txt
ss://
  ↓
手动得到 method / password / server / port / name
  ↓
手动写成 Clash YAML
```

而项目自动做的是：

```txt
ss://
  ↓
explodeSS()
  ↓
Proxy
  ↓
proxyToClash()
  ↓
Clash YAML
```

## 9. 后续可以继续探索什么

如果要把这份学习进一步沉淀成可复用能力，后面很适合继续做这些方向：

- 增加“多节点手动示例”
- 增加“`/sub?target=clash&url=...` 调用链”源码导读
- 增加“从 `Proxy` 统一模型到不同目标格式”的结构图
- 把人工步骤整理成脚本或测试样例
- 给仓库补一个更显眼的学习入口，把这类文档链接到主 README

## 10. 一句话总结

这次学到的核心不是“会写一份 YAML”，而是：

```txt
ss:// 是单节点分享格式
  ↓
ClashX 需要的是 Clash 配置结构
  ↓
只要把节点字段正确解析并放进 proxies + proxy-groups + rules
  ↓
单节点就能被手动导入并实际使用
```
