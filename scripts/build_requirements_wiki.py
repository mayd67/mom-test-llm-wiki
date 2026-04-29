from __future__ import annotations
import re
from collections import Counter, OrderedDict, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'raw' / '需求文档'
WIKI = ROOT / 'wiki'
TODAY = date.today().isoformat()

GROUPS = OrderedDict([
    ('01_标准功能', {'label': '标准功能', 'title': '标准功能需求地图', 'path': WIKI / '03_业务系统' / 'MOM' / '系统总览' / '标准功能需求地图.md'}),
    ('02_MOM-AI', {'label': 'MOM-AI', 'title': 'MOM-AI需求地图', 'path': WIKI / '03_业务系统' / 'MOM' / '系统总览' / 'MOM-AI需求地图.md'}),
    ('03_优化需求', {'label': '优化需求', 'title': '优化需求地图', 'path': WIKI / '03_业务系统' / 'MOM' / '系统总览' / '优化需求地图.md'}),
])
OVERVIEW = {'title': 'MOM需求分析总览', 'path': WIKI / '03_业务系统' / 'MOM' / '系统总览' / 'MOM需求分析总览.md'}
NAVS = OrderedDict([
    ('登录权限模块', {'title': '登录权限需求导航', 'path': WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '登录权限模块' / '登录权限需求导航.md'}),
    ('后台管理模块', {'title': '后台管理需求导航', 'path': WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '后台管理模块' / '后台管理需求导航.md'}),
    ('核心业务模块', {'title': '核心业务需求导航', 'path': WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '核心业务模块' / '核心业务需求导航.md'}),
    ('第三方对接模块', {'title': '智能能力需求导航', 'path': WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / '第三方对接模块' / '智能能力需求导航.md'}),
])
MANUAL_GROUPS = {
    'DNW30320-变更管理.md': '变更管理',
    'DNW30320-变更管理_业务正向主流程.md': '变更管理',
    'DNW30320-变更管理_变更执行方案.md': '变更管理',
    'DNW30900-工装工具管理-业务分析.md': '工装工具管理',
    'DNW30900-工装工具管理-功能设计.md': '工装工具管理',
    'AI-DA-01_智能问数需求文档.md': '智能问数',
    'DNW31500-智能问数.md': '智能问数',
    'DNW30600-计划排产通用能力.md': '计划排产',
    'DNW30600-计划排产（AP）.md': '计划排产',
    'DNW32000-产品标准化问题需求规格.md': '产品标准化问题',
    'KMMOM产品标准化问题_用户故事清单_V1.0.md': '产品标准化问题',
}
SKIP = {'文档信息', '概述', '原始需求', '需求来源', '用户画像', '术语及缩写解释', '参考文献', '变更记录', '附录', '外部依赖', '需求分析过程', '行业标准与友商分析'}
INTRO_K = ('概述', '业务背景', '功能概述', '摘要', '原始需求', '业务描述', '价值主张', '需求分析')
RULE_K = ('规则', '约束', '边界', '依赖', '校验', '逻辑', '验收', '限制', '处理')
FEAT_K = ('功能', '页面', '界面', '流程', '方案', '工作台', '模块', '清单', '导入', '编辑', '查询', '详情', '报工', '报检', '排产', '排程', '履历', '仓储', '物流', '设备', '工装', '报表', '分析', '识别', '问数', '智能体', '卡片', '建模', '菜单', '布局')
WEAK_FEATURES = {'需求分析', '业务描述', '功能描述', '功能清单', '页面&功能设计', '界面原型描述'}


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + '\n', encoding='utf-8')


def clean_inline(text: str) -> str:
    text = text.replace('\ufeff', '').replace('\u200b', '')
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = text.replace('**', '').replace('__', '').replace('`', '')
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def heading_text(text: str) -> str:
    text = clean_inline(text)
    text = re.sub(r'^[#\s]+', '', text)
    text = re.sub(r'^\d+(?:\.\d+)*[.、]?\s*', '', text)
    text = re.sub(r'^[一二三四五六七八九十]+[、.]\s*', '', text)
    text = re.sub(r'^\[[^\]]+\]\s*', '', text)
    return text.strip(' -—:：')


def module_title(stem: str) -> str:
    match = re.match(r'^[A-Za-z0-9][A-Za-z0-9.\-]*[_-](.+)$', stem)
    title = match.group(1) if match else stem
    title = title.replace('_', '').replace('-', '')
    title = re.sub(r'V\d+(?:\.\d+)?$', '', title, flags=re.I)
    title = re.sub(r'[（(]参考[）)]', '', title)
    title = re.sub(r'需求文档$|需求规格说明$|需求规格$', '需求', title)
    return title.strip()


def page_title(title: str) -> str:
    return f'{title}拆解' if title.endswith('需求') else f'{title}需求拆解'


def section_list(text: str) -> list[dict]:
    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r'^(#{1,6})\s+(.*\S)\s*$', line)
        if match:
            headings.append((index, len(match.group(1)), heading_text(match.group(2))))
    sections = []
    for idx, (line_no, level, title) in enumerate(headings):
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        sections.append({'level': level, 'title': title, 'body': lines[line_no + 1:end]})
    return sections


def snippet(lines: list[str]) -> str:
    values: list[str] = []
    for line in lines:
        if re.match(r'^\s*#', line):
            continue
        value = clean_inline(line)
        if not value or value.startswith('|') or re.fullmatch(r'[-:| ]+', value):
            continue
        if re.search(r'\.(png|jpg|jpeg|svg)$', value, re.I):
            continue
        values.append(value)
        if len('；'.join(values)) > 90 or len(values) >= 2:
            break
    return '；'.join(values)[:120]


def pick_features(sections: list[dict], limit: int = 12) -> list[str]:
    result: list[str] = []
    for section in sections:
        title = section['title']
        if not title or title in SKIP:
            continue
        if title in WEAK_FEATURES:
            continue
        if any(key in title for key in FEAT_K) and not any(key in title for key in RULE_K):
            if title not in result:
                result.append(title)
        if len(result) >= limit:
            break
    return result


def pick_rules(sections: list[dict], limit: int = 8) -> list[str]:
    result: list[str] = []
    for section in sections:
        title = section['title']
        if not title or title in SKIP or not any(key in title for key in RULE_K):
            continue
        text = snippet(section['body'])
        item = f'{title}：{text}' if text else title
        if item not in result:
            result.append(item)
        if len(result) >= limit:
            break
    return result


def pick_outline(sections: list[dict], limit: int = 10) -> list[str]:
    result: list[str] = []
    for section in sections:
        title = section['title']
        if not title or title in SKIP or section['level'] == 1 or section['level'] > 3:
            continue
        if title not in result:
            result.append(title)
        if len(result) >= limit:
            break
    return result


def pick_intro(sources: list[dict], limit: int = 3) -> list[str]:
    result: list[str] = []
    for source in sources:
        for section in source['sections']:
            if any(key in section['title'] for key in INTRO_K):
                text = snippet(section['body'])
                if text:
                    line = f"- `{source['rel']}`：{text}"
                    if line not in result:
                        result.append(line)
                break
        if len(result) >= limit:
            break
    return result[:limit]


def pick_domain(raw_group: str, title: str) -> str:
    if raw_group == '02_MOM-AI':
        return '第三方对接模块'
    if raw_group == '03_优化需求':
        return '登录权限模块' if '工作台' in title else '后台管理模块'
    if any(key in title for key in ('角色', '权限', '菜单', '工作台', '登录')):
        return '登录权限模块'
    if any(key in title for key in ('配置', '布局', '扩展', '审批流', '标准化', '卡片')):
        return '后台管理模块'
    return '核心业务模块'


def anchor_pages(raw_group: str, title: str) -> list[str]:
    links = ['产品知识库总览', '业务知识库总览', '产品功能地图']
    if raw_group != '01_标准功能' or any(key in title for key in ('AI', '优化', '标准化')):
        links.append('版本功能清单')
    if any(key in title for key in ('角色', '权限')):
        links.append('角色权限矩阵')
    if any(key in title for key in ('原型', '工作台', '交互')):
        links.append('原型评审关注点')
    links.extend(['如何为新需求建立测试分析路径', '测试策略'])
    result: list[str] = []
    for link in links:
        if link not in result:
            result.append(link)
    return result[:6]


def split_log(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return '# Wiki Log', ''
    if not stripped.startswith('# Wiki Log'):
        return '# Wiki Log', stripped
    lines = stripped.splitlines()
    body = lines[1:]
    while body and body[0].strip() == '':
        body = body[1:]
    return lines[0], '\n'.join(body).strip()


def prepend_log(entry: str) -> None:
    path = WIKI / 'log.md'
    old = read_text(path) if path.exists() else '# Wiki Log\n'
    if entry.splitlines()[0] in old:
        return
    header, body = split_log(old)
    parts = [header, '', entry.strip()]
    if body:
        parts.extend(['', body])
    write_text(path, '\n'.join(parts))


def blurb(doc: dict) -> str:
    if doc['features']:
        return '聚焦 ' + '、'.join(doc['features'][:3])
    return '查看来源文档拆解与关联关系'


def render_frontmatter(title: str, page_type: str, status: str, tags: list[str], summary: str, sources: list[str]) -> list[str]:
    lines = ['---', f'title: {title}', f'type: {page_type}', f'status: {status}', 'tags:']
    for tag in tags:
        lines.append(f'  - {tag}')
    lines.append(f'summary: {summary}')
    lines.append('source:')
    for source in sources:
        lines.append(f'  - {source}')
    lines.append(f'updated: {TODAY}')
    lines.append('---')
    return lines


def render_detail(doc: dict) -> str:
    tags = ['testing', 'mom', 'requirement', GROUPS[doc['raw_group']]['label'], doc['domain']]
    summary = f"基于{len(doc['sources'])}份原始需求文档拆解{doc['module']}的功能范围、规则边界与关联模块。"
    lines = render_frontmatter(doc['title'], 'business', doc['status'], tags, summary, [src['rel'] for src in doc['sources']])
    lines.extend(['', f"# {doc['title']}", '', '## 页面定位', '', f"- 需求分组：`{GROUPS[doc['raw_group']]['label']}`", f"- 业务域：`{doc['domain']}`", f"- 上游导航：[[{OVERVIEW['title']}]]、[[{doc['group_page']}]]、[[{doc['nav_page']}]]", '- 来源文档：'])
    for src in doc['sources']:
        lines.append(f"  - `{src['rel']}`")
    lines.extend(['', '## 需求摘要', ''])
    lines.append(f"- 本页整合了 {len(doc['sources'])} 份原始文档，当前重点覆盖：{'、'.join(doc['features'][:5]) if doc['features'] else doc['module']}。")
    if doc['intro_lines']:
        lines.extend(doc['intro_lines'])
    else:
        lines.append('- 原始文档具备较强的结构化章节，可继续在此页上补充更细的业务规则与测试重点。')
    lines.extend(['', '## 功能拆解', ''])
    for item in (doc['features'] or doc['outline'] or [doc['module']]):
        lines.append(f'- {item}')
    lines.extend(['', '## 规则与边界', ''])
    for item in (doc['rules'] or ['需结合原始文档中的业务规则、约束与验收章节继续补充。']):
        lines.append(f'- {item}')
    lines.extend(['', '## 导航链接', ''])
    for item in [OVERVIEW['title'], doc['group_page'], doc['nav_page'], *doc['anchors']]:
        if item != doc['title']:
            lines.append(f'- [[{item}]]')
    lines.extend(['', '## 同主题 / 上下游需求', ''])
    for item in doc['related']:
        lines.append(f'- [[{item}]]')
    if not doc['related']:
        lines.append(f"- 通过 [[{doc['nav_page']}]] 查看同域需求拆解页。")
    lines.extend(['', '## 原始文档结构', ''])
    for item in (doc['outline'] or doc['features'][:6] or [doc['module']]):
        lines.append(f'- {item}')
    lines.extend(['', '## 备注', '', '- 本页为依据原始需求文档形成的首轮结构化拆解，图示、细节和最终口径以原文为准。', '- 后续可继续补充测试重点、测试资产和历史缺陷链接。'])
    return '\n'.join(lines)


def render_overview(group_counts: dict[str, int], domain_counts: dict[str, int], doc_count: int) -> str:
    lines = render_frontmatter(OVERVIEW['title'], 'product', 'active', ['testing', 'mom', 'requirement', 'navigation'], '汇总 raw/需求文档 下的 MOM 标准功能、MOM-AI 与优化需求，并作为需求拆解页总入口。', ['raw/需求文档/'])
    lines.extend(['', f"# {OVERVIEW['title']}", '', '## 统计概览', '', '| 维度 | 数量 |', '| --- | ---: |', f'| 原始主文档 | {doc_count} |', f'| 生成需求拆解页 | {sum(group_counts.values())} |', f"| 需求地图页 | {len(GROUPS)} |", f"| 业务导航页 | {len(NAVS)} |", '', '## 一级地图', ''])
    for key, cfg in GROUPS.items():
        lines.append(f"- [[{cfg['title']}]]：收录 `{cfg['label']}` 主题下的结构化需求拆解页")
    lines.extend(['', '## 业务导航', ''])
    for key, cfg in NAVS.items():
        lines.append(f"- [[{cfg['title']}]]：聚合 `{key}` 主题下的拆解页与上下游关系")
    lines.extend(['', '## 分组分布', '', '| 维度 | 数量 |', '| --- | ---: |'])
    for key, cfg in GROUPS.items():
        lines.append(f"| {cfg['label']} | {group_counts.get(key, 0)} |")
    for key, cfg in NAVS.items():
        lines.append(f"| {key} | {domain_counts.get(key, 0)} |")
    lines.extend(['', '## 关联页面', '', '- [[产品功能地图]]', '- [[版本功能清单]]', '- [[业务知识库总览]]', '- [[产品知识库总览]]'])
    return '\n'.join(lines)


def render_group_map(group_key: str, docs: list[dict]) -> str:
    cfg = GROUPS[group_key]
    lines = render_frontmatter(cfg['title'], 'product', 'active', ['testing', 'mom', 'requirement', cfg['label']], f"聚合 {cfg['label']} 主题下的需求拆解页，建立产品地图与业务导航之间的链接关系。", [f"raw/需求文档/{group_key}/"])
    lines.extend(['', f"# {cfg['title']}", '', '## 范围说明', '', f"- 来源目录：`raw/需求文档/{group_key}/`", f"- 收录页面：{len(docs)}", f"- 上游导航：[[{OVERVIEW['title']}]]、[[产品功能地图]]、[[业务知识库总览]]", '', '## 按业务域拆解', ''])
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for doc in docs:
        by_domain[doc['domain']].append(doc)
    for domain_name, nav_cfg in NAVS.items():
        lines.append(f"### {domain_name}")
        domain_docs = sorted(by_domain.get(domain_name, []), key=lambda item: item['title'])
        if not domain_docs:
            lines.append('- 待补充')
        else:
            lines.append(f"- 导航页：[[{nav_cfg['title']}]]")
            for doc in domain_docs:
                lines.append(f"- [[{doc['title']}]]：{blurb(doc)}")
        lines.append('')
    lines.extend(['## 关联页面', '', f"- [[{OVERVIEW['title']}]]", '- [[产品功能地图]]', '- [[版本功能清单]]', '- [[业务知识库总览]]'])
    return '\n'.join(lines)


def render_nav(domain_name: str, docs: list[dict]) -> str:
    cfg = NAVS[domain_name]
    sources = sorted({f"raw/需求文档/{doc['raw_group']}/" for doc in docs})
    lines = render_frontmatter(cfg['title'], 'business', 'active', ['testing', 'mom', 'requirement', domain_name, 'navigation'], f"聚合 {domain_name} 下的需求拆解页，方便从业务域维度串联原始需求与结构化知识。", sources)
    lines.extend(['', f"# {cfg['title']}", '', '## 覆盖范围', '', f"- 收录页面：{len(docs)}", f"- 上游导航：[[{OVERVIEW['title']}]]、[[业务知识库总览]]、[[产品功能地图]]", '- 来源分组：'])
    for label in sorted({GROUPS[doc['raw_group']]['label'] for doc in docs}):
        lines.append(f'  - {label}')
    lines.extend(['', '## 页面清单', ''])
    by_group: dict[str, list[dict]] = defaultdict(list)
    for doc in docs:
        by_group[doc['raw_group']].append(doc)
    for group_key, group_cfg in GROUPS.items():
        lines.append(f"### {group_cfg['label']}")
        group_docs = sorted(by_group.get(group_key, []), key=lambda item: item['title'])
        if not group_docs:
            lines.append('- 待补充')
        else:
            lines.append(f"- 地图页：[[{group_cfg['title']}]]")
            for doc in group_docs:
                lines.append(f"- [[{doc['title']}]]：{blurb(doc)}")
        lines.append('')
    lines.extend(['## 关联页面', '', f"- [[{OVERVIEW['title']}]]", '- [[产品功能地图]]', '- [[版本功能清单]]', '- [[测试策略]]'])
    return '\n'.join(lines)


files = []
for path in RAW.rglob('*.md'):
    if path.name == '.gitkeep':
        continue
    if re.search(r'备份|（旧）|_旧|^Untitled$', path.stem):
        continue
    files.append(path)
files = sorted(files)

docs: OrderedDict[str, dict] = OrderedDict()
for path in files:
    rel = path.relative_to(ROOT).as_posix()
    raw_group = path.relative_to(RAW).parts[0]
    module = MANUAL_GROUPS.get(path.name) or module_title(path.stem)
    key = f'{raw_group}|{module}'
    text = read_text(path)
    item = docs.setdefault(key, {'module': module, 'raw_group': raw_group, 'sources': []})
    item['sources'].append({'path': path, 'rel': rel, 'text': text, 'stem': path.stem, 'sections': section_list(text)})

for item in docs.values():
    item['domain'] = pick_domain(item['raw_group'], item['module'])
    item['nav_page'] = NAVS[item['domain']]['title']
    item['group_page'] = GROUPS[item['raw_group']]['title']
    item['title'] = page_title(item['module'])
    item['path'] = WIKI / '03_业务系统' / 'MOM' / '模块业务手册' / item['domain'] / f"{item['title']}.md"
    item['status'] = 'review' if any('参考' in source['stem'] for source in item['sources']) else 'seed'
    merged_sections = [section for source in item['sources'] for section in source['sections']]
    item['features'] = pick_features(merged_sections) or pick_outline(merged_sections, 8)
    item['rules'] = pick_rules(merged_sections)
    item['outline'] = pick_outline(merged_sections)
    item['intro_lines'] = pick_intro(item['sources'])
    item['anchors'] = anchor_pages(item['raw_group'], item['module'])

all_docs = list(docs.values())
for item in all_docs:
    related: list[str] = []
    combined = '\n'.join(source['text'] for source in item['sources'])
    hits: Counter[str] = Counter()
    for other in all_docs:
        if other['title'] == item['title']:
            continue
        tokens = {other['module']} | {source['stem'] for source in other['sources']}
        for token in tokens:
            if len(token) < 2:
                continue
            if token in combined:
                hits[other['title']] += combined.count(token) + (2 if token == other['module'] else 0)
    for title, _ in hits.most_common(6):
        if title not in related:
            related.append(title)
    if len(related) < 4:
        for other in all_docs:
            if other['title'] == item['title'] or other['domain'] != item['domain']:
                continue
            if other['title'] not in related:
                related.append(other['title'])
            if len(related) >= 6:
                break
    item['related'] = related[:6]

for item in all_docs:
    write_text(item['path'], render_detail(item))

by_group: dict[str, list[dict]] = defaultdict(list)
by_domain: dict[str, list[dict]] = defaultdict(list)
for item in all_docs:
    by_group[item['raw_group']].append(item)
    by_domain[item['domain']].append(item)

write_text(OVERVIEW['path'], render_overview({key: len(value) for key, value in by_group.items()}, {key: len(value) for key, value in by_domain.items()}, len(files)))
for key, cfg in GROUPS.items():
    write_text(cfg['path'], render_group_map(key, sorted(by_group.get(key, []), key=lambda item: item['title'])))
for key, cfg in NAVS.items():
    write_text(cfg['path'], render_nav(key, sorted(by_domain.get(key, []), key=lambda item: item['title'])))

prepend_log('\n'.join([
    f'## {TODAY} update | 基于 raw/需求文档 生成 MOM 需求拆解页',
    '',
    f'- 读取 `raw/需求文档/` 下的主需求文档并生成 {len(all_docs)} 个需求拆解页',
    '- 新增 `MOM需求分析总览`、`标准功能需求地图`、`MOM-AI需求地图`、`优化需求地图` 作为产品侧导航入口',
    '- 新增 4 个业务导航页，连接登录权限、后台管理、核心业务与智能能力主题',
    '- 在拆解页内补充来源追溯、功能拆解、规则边界与 wikilinks 关联',
]))

print(f'generated detail pages: {len(all_docs)}')
print('generated map pages: 4')
print('generated nav pages: 4')
