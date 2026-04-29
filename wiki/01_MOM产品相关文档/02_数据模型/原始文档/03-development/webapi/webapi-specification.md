# KM-MOM WebAPI 开发规范

## 概述

WebAPI 用于对外公开 MOM 产品接口，支持项目扩展和外部系统集成。

**依赖组件：** `km-common-apidoc`

该组件基于 `springdoc-openapi-starter-webmvc-api` 自动扫描加了 `@Tag` 注解的 RestController，并在 `km-mom-gateway` 层进行聚合生成。

## 1.1 API 定义位置

所有对外公开的 WebAPI 接口必须在所属模块的 `remote` 包下创建专门的 `api` 子包。

**包结构规范：**

```text
{module-name}
└── remote/
    └── api/              # WebAPI 专用包
        ├── XxxApi.java   # API 接口类
        └── ...
```

**示例：**

- MES 生产订单 API：`com.kmsoft.mom.mes.biz.planning.remote.api.ProdOrderApi`

## 1.2 注解使用规范

### @Tag - Controller 类级别注解

用于标识和分组 API 接口，在 OpenAPI 文档中显示为接口分组。

**@RequestMapping 路径规范：**

WebAPI 的 URL 路径必须遵循以下结构：

```text
{version}/{resource}/...
```

**路径组成说明：**

- `api`：固定前缀，标识这是对外 API

- `{module}`：模块标识（小写），如 `mes`、`approval`、`platform`

- `{version}`：API 版本号，格式为 `v1`、`v2` 等

- `{resource}`：资源名称（驼峰命名），如 `prodOrder`、`flowExecApi`

  ```
  注意：api和module 系统会自动生成 ，不用手动维护(km-common-apidoc会自动根据当前微服务的服务名生成module)。
  ```

  

**完整示例：**

```java
@RestController
@RequestMapping("v1/prodOrder")
@Tag(name = "生产订单API", description = "提供生产订单的释放、查询等功能")
public class ProdOrderApi {
    // ...
}
```

**@Tag 参数说明：**

- `name`：API 分组名称，简短明确
- `description`：详细描述该 API 组的功能范围

### @Operation - 方法级别注解

用于描述具体的 API 操作，包括功能说明和执行流程。

```java
@PostMapping("/simulateRelease")
@Operation(
    summary = "模拟释放生产订单",
    description = "执行流程：\n" +
                  "1. 校验订单状态，确保可以释放\n" +
                  "2. 校验释放数量的合法性\n" +
                  "3. 根据订单数据和释放参数生成释放预览数据\n" +
                  "4. 返回预览数据，但不保存到数据库\n"
)
public Response<List<SimulateReleaseManuOrderVO>> simulateRelease(
    @RequestBody Request<List<SimulatedProdOrderDTO>> request) {
    // ...
}
```

**参数说明：**

- `summary`：简短摘要，一句话说明接口功能
- `description`：详细描述，可包含执行流程、注意事项等，支持换行

### @Schema - DTO/VO 字段级别注解

用于描述数据模型的字段信息，生成详细的 API 文档。

```java
public class SimulatedProdOrderDTO {

    @Schema(description = "生产订单ID", required = true, example = "123456")
    private Long id;

    @Schema(description = "本次释放数量", required = true, example = "100.0")
    private BigDecimal currentQty;

    @Schema(description = "每份数量", required = true, example = "10.0")
    private BigDecimal unitQty;

    @Schema(description = "备注信息", required = false, example = "紧急订单")
    private String remark;
}
```

**参数说明：**

- `description`：字段描述，说明字段的业务含义
- `required`：是否必填，默认 false
- `example`：示例值，帮助理解字段内容
- `allowableValues`：可选值范围（枚举类型）

### @Schema - 类级别注解

用于描述整个 DTO/VO 类的用途。

```java
@Schema(description = "模拟释放DTO")
public class SimulatedProdOrderDTO {
    // ...
}
```

### @Parameter - 方法参数注解

用于描述 GET 请求的查询参数。

```java
@GetMapping("/judgeJoinedFLow")
@Operation(summary = "判断实体是否加入过流程")
public Response<Boolean> judgeJoinedFLow(
    @Parameter(description = "业务实体ID", required = true, example = "123456")
    @RequestParam Long bizEntityId) {
    // ...
}
```

**参数说明：**

- `description`：参数描述
- `required`：是否必填
- `example`：示例值

### 完整示例

```java
package com.kmsoft.mom.mes.biz.planning.remote.api;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("v1/prodOrder")
@Tag(name = "生产订单API", description = "提供生产订单的释放、查询等功能")
public class ProdOrderApi {

    @PostMapping("/simulateRelease")
    @Operation(
        summary = "模拟释放生产订单",
        description = "执行流程：\n1. 校验订单状态\n2. 校验释放数量\n3. 生成预览数据\n4. 返回预览数据"
    )
    public Response<List<SimulateReleaseManuOrderVO>> simulateRelease(
        @RequestBody Request<List<SimulatedProdOrderDTO>> request) {
        // 实现逻辑
    }

    @GetMapping("/getById")
    @Operation(summary = "根据ID查询生产订单")
    public Response<ProdOrderVO> getById(
        @Parameter(description = "生产订单ID", required = true)
        @RequestParam Long id) {
        // 实现逻辑
    }
}
```

## 1.3 API 文档生成

**生成流程：**

1. 启动所有微服务（platform、mes、approval 等）
2. 浏览器打开 `http://localhost:40100/api-docs/build` 执行文档生成
3. 根据返回的 `filePath` 打开文件确认内容
4. 将生成的文件覆盖到 `km-mom-gateway/src/main/resources/api-docs/` 目录

**参考实现：** `com.kmsoft.gateway.apidocs.controller.ApiDocController`

---

**文档版本：** v1.0
**最后更新：** 2026-03-05
**维护者：** KM-MOM 开发团队
