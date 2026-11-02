# Deimos200 测试 Issue 仓库

本仓库**仅用于记录和跟踪「Deimos200」的测试缺陷与测试相关问题**，不存放产品源码。

---

## 一、如何提交 Issue

1. 点击仓库的 **Issues → New Issue**
2. 选择模板：
   - **🐞 测试缺陷** —— 测试中发现的 Bug（表单化，必填项已约束）
   - **📝 用例补充 / 测试建议** —— 非缺陷类内容
3. 按模板填写后提交，系统会自动打上 `triage` 标签等待分诊

> 提交前请先搜索是否已有相同 Issue，重复提交会被关闭并关联到原 Issue。

## 二、严重级别定义

| 级别 | 含义 | 响应要求 |
| --- | --- | --- |
| **P0** | 崩溃、主流程完全不可用、数据丢失/错乱 | 立即处理，阻塞发版 |
| **P1** | 主要功能异常且无绕行方案 | 当版本必须修复 |
| **P2** | 功能异常但存在绕行方案 | 排期修复 |
| **P3** | UI、文案、交互体验等轻微问题 | 择机修复 |

## 三、标签规范

| 类别 | 标签 |
| --- | --- |
| 类型 | `bug` `enhancement` `question` |
| 状态 | `triage`（待分诊）`confirmed`（已确认）`wontfix` `duplicate` `need-more-info` |
| 严重级别 | `P0` `P1` `P2` `P3` |
| 模块 | `模块:登录` `模块:支付` ……（按实际模块增减） |
| 版本 | `v2.3.1` 形式，或用 Milestone 管理 |

### 快速创建标签

```bash
# 类型与状态
for l in "bug:ed0722:缺陷" "enhancement:a2eeef:改进建议" "triage:fbca04:待分诊" \
         "confirmed:0e8a16:已确认" "need-more-info:d876e3:信息不足" \
         "wontfix:ffffff:不修复" "duplicate:cfd3d7:重复"; do
  name="${l%%:*}"; rest="${l#*:}"; color="${rest%%:*}"; desc="${rest#*:}"
  gh label create "$name" --color "$color" --description "$desc" --force
done

# 严重级别
for p in P0 P1 P2 P3; do gh label create "$p" --color "b60205" --description "严重级别 $p" --force; done
```

## 四、Issue 生命周期

```
新建(triage) → 分诊确认(confirmed/P0-P3/模块) → 修复中 → 待验证 → 关闭
                     ↓
        信息不足(need-more-info) / 重复(duplicate) / 不修复(wontfix)
```

- 修复完成后由**测试人员**在Issue下评论验证结果，再关闭
- 已关闭 Issue 若复发，请重新打开并在评论区说明复发版本

## 五、仓库结构

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml   # 测试缺陷表单
│   ├── other.md         # 用例补充/建议
│   └── config.yml       # 模板入口配置
docs/                    # 测试计划、用例文档（可选）
```
