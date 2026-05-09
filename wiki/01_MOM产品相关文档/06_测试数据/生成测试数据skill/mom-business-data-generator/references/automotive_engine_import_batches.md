# 汽车发动机场景导入批次说明

## 一、用途

本说明用于指导“汽车发动机 / 2.0T缸内直喷涡轮增压汽油发动机”场景在同一套环境中连续导入多套数据时，如何选择批次、如何避免编码冲突，以及推荐的导入顺序。

## 二、先看结论

如果你要把多套汽车发动机数据导入同一个环境，优先使用下面这三套：

1. `标准版`：命名空间 `AE20T01`
2. `大体量版`：命名空间 `AE31T01`
3. `超大体量版`：命名空间 `AE42T01`

这三套已经做了唯一命名空间隔离，可以直接共存在同一环境中。

## 三、推荐导入批次

### 批次 1：标准版

- 命名空间：`AE20T01`
- 种子文件：`assets/automotive_engine_seed.json`
- 导出目录：`output/automotive_engine_seed`
- 适用场景：先做基础 POC、先验证模板字段与引用关系、先演示汽车发动机标准规模版本。

### 批次 2：大体量版

- 命名空间：`AE31T01`
- 种子文件：`assets/automotive_engine_seed_big.json`
- 导出目录：`output/automotive_engine_seed_big`
- 适用场景：在标准版导入成功后，继续展示更多操作工、更多并行设备与工作中心、更多工艺与备料数据。

### 批次 3：超大体量版

- 命名空间：`AE42T01`
- 种子文件：`assets/automotive_engine_seed_ultra.json`
- 导出目录：`output/automotive_engine_seed_ultra`
- 适用场景：进一步展示高体量自动生成能力，突出多工厂协同场景下的用户、设备、工作中心、物料与工艺扩容效果。

## 四、每一批内部的推荐导入顺序

每一套数据内部，建议按以下顺序导入：

1. `系统配置_模板.xlsx`
2. `工厂资源_模板.xlsx`
3. `产品与工艺_模板.xlsx`
4. `生产订单_模板.xlsx`

## 五、推荐的同环境连续导入顺序

如果你要在一套环境里逐步扩容演示，推荐顺序如下：

1. 先导入 `output/automotive_engine_seed`
2. 再导入 `output/automotive_engine_seed_big`
3. 最后导入 `output/automotive_engine_seed_ultra`

## 六、当前三套可并存版本的数据规模

### 标准版 / `AE20T01`

- 用户：`170`
- 设备：`40`
- 工作中心：`38`
- 物料：`108`
- MBOM节点：`60`
- 工序：`189`
- 工步：`378`
- 备料清单：`166`

### 大体量版 / `AE31T01`

- 用户：`240`
- 设备：`60`
- 工作中心：`56`
- 物料：`174`
- MBOM节点：`87`
- 工序：`252`
- 工步：`504`
- 备料清单：`229`

### 超大体量版 / `AE42T01`

- 用户：`310`
- 设备：`100`
- 工作中心：`93`
- 物料：`240`
- MBOM节点：`114`
- 工序：`315`
- 工步：`630`
- 备料清单：`292`

## 七、导入时的注意事项

- 三套版本都采用唯一命名空间，可用于同环境连续导入。
- 当前场景保留 `1` 条 `工作中心与供应商的关系`，用于体现外协热处理。
- `工艺路线工序序列` 默认采用 `ES`；`工艺路线` sheet 的 `发布人` 留空；`工装工具`、`物料`、`MBOM` 的 `发布人` 已按用户编号引用。
- 导出时如果用户、设备或工作中心关系行数超过模板预留，会出现结构警告，但当前三套版本均已完成校验与 Excel 导出。
- 历史目录 `output/_deprecated/automotive_engine_seed_v2`、`output/_deprecated/automotive_engine_seed_v3`、`output/_deprecated/automotive_engine_seed_big_ns31`、`output/_deprecated/automotive_engine_seed_ultra_ns42` 已迁入归档目录；当前推荐使用标准目录 `output/automotive_engine_seed`、`output/automotive_engine_seed_big`、`output/automotive_engine_seed_ultra`。

## 八、给同事的简短说明话术

可以直接把下面这段发给同事：

```text
如果你要把汽车发动机的多套数据导入同一个环境，请按 AE20T01（标准版）→ AE31T01（大体量版）→ AE42T01（超大体量版）的顺序导入。
每一套内部都按 系统配置 → 工厂资源 → 产品与工艺 → 生产订单 的顺序导入。
这三套已经做了唯一命名空间隔离，可以直接并存。
```
