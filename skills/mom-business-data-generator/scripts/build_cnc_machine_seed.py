from __future__ import annotations
import copy
import json, sys
from pathlib import Path
from tooling_strategy_profiles import apply_profile
from scene_seed_upgrades import apply_scene_upgrade
from production_order_seed import apply_production_orders
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
WB_SYSTEM='系统配置_模板.xlsx'; WB_FACTORY='工厂资源_模板.xlsx'; WB_PRODUCT='产品与工艺_模板.xlsx'
SH_ADMIN='行政组织'; SH_BIZ='业务组织'; SH_USER='用户'; SH_SUP='供应商'; SH_EQ='设备'; SH_EQ_USER='设备与用户的关系实体类'; SH_TOOL='工装工具'; SH_WC='工作中心'; SH_WC_USER='工作中心与用户关系'; SH_WC_SUP='工作中心与供应商的关系'; SH_WC_EQ='工作中心与设备的关系'; SH_WH='库房'; SH_LOC='库位'; SH_PLIB='工序库'; SH_MAT='物料'; SH_MBOM='MBOM'; SH_MBOM_NODE='MBOM节点'; SH_ROUTE='工艺路线'; SH_OP='工艺路线工序'; SH_SEQ='工艺路线工序序列'; SH_OPMAT='工艺路线工序物料'; SH_STEP='工艺路线工步'
SEC='内部'; VER='A.01'; YES='是'; NO='否'; TIME='分钟'; ROUTE_TYPE='正式工艺'; MAT_CLASS='物料'; TOOL_CLASS='工装工具'; CAT_RAW='原材料'; CAT_AUX='辅助材料'; CAT_PART='零部件'; CAT_KIT='配套件'; CAT_SPARE='设备备件'; MAKE_SELF='自制件'; MAKE_BUY='外购件'; FEATURE_KEY='关键件'; FEATURE_IMPORTANT='重要件'; FEATURE_NORMAL='一般件'; SEQ_TYPE='ES'; STAGE='量产'; NAMESPACE='CNC85001'
ASSET_PATH=Path(__file__).resolve().parent.parent/'assets'/'cnc_machine_seed.json'
seed={'metadata':{'name':'数控机床MOM种子','product_family':'高端数控机床','product_model':'VMC-850-5X五轴立式加工中心','description':'基于高端五轴立式加工中心整机制造场景构建的MOM主数据种子，用于售前演示与模板快速出数。','default_version':VER,'default_security':SEC},'external_references':['0'],'workbooks':{WB_SYSTEM:{SH_ADMIN:[],SH_BIZ:[],SH_USER:[]},WB_FACTORY:{SH_SUP:[],SH_EQ:[],SH_EQ_USER:[],SH_TOOL:[],SH_WC:[],SH_WC_USER:[],SH_WC_SUP:[],SH_WC_EQ:[],SH_WH:[],SH_LOC:[],SH_PLIB:[]},WB_PRODUCT:{SH_MAT:[],SH_MBOM:[],SH_MBOM_NODE:[],SH_ROUTE:[],SH_OP:[],SH_SEQ:[],SH_OPMAT:[],SH_STEP:[]}}}
SEED_TEMPLATE=copy.deepcopy(seed)
VARIANT_SPECS=[('cnc_machine_seed.json', NAMESPACE, '标准版'), ('cnc_machine_seed_big.json', 'CNC85031', '大体量版'), ('cnc_machine_seed_ultra.json', 'CNC85042', '超大体量版')]
MAT={}; PROC=set(); EQ_USER=set(); WC_USER=set(); WC_SUP=set(); WC_EQ=set(); MBOM_SEQ={1:10,2:10,3:10}
def reset():
    global seed, MAT, PROC, EQ_USER, WC_USER, WC_SUP, WC_EQ, MBOM_SEQ
    seed=copy.deepcopy(SEED_TEMPLATE)
    MAT={}; PROC=set(); EQ_USER=set(); WC_USER=set(); WC_SUP=set(); WC_EQ=set(); MBOM_SEQ={1:10,2:10,3:10}
def add(wb,sh,row): seed['workbooks'][wb][sh].append(row)
def uniq(store,key,wb,sh,row):
    if key not in store:
        store.add(key); add(wb,sh,row)
def next_mbom(level):
    v=MBOM_SEQ[level]; MBOM_SEQ[level]+=10; return v
def a_admin(parent,typ,code,name,short): add(WB_SYSTEM,SH_ADMIN,{'*父组织编码':parent,'行政组织类型':typ,'*编码':code,'*名称':name,'简称':short})
def a_biz(parent,code,name,short,typ,admin,factory=''):
    row={'*父组织编码':parent,'*密级':SEC,'*编码':code,'*名称':name,'简称':short,'工厂组织类型':typ,'行政组织编码':admin}
    if factory: row['工厂类型']=factory
    add(WB_SYSTEM,SH_BIZ,row)
def a_user(code,name,level,gender,admin,biz,remark=''): add(WB_SYSTEM,SH_USER,{'*编号':code,'名称':name,'备注':remark,'用户安全等级':level,'性别':gender,'行政组织编码':admin,'业务组织编码':biz})
def a_sup(code,name,short): add(WB_FACTORY,SH_SUP,{'*密级':SEC,'*编码':code,'*名称':name,'简称':short,'启用':YES})
def a_eq(code,name,model,biz,bottle=NO): add(WB_FACTORY,SH_EQ,{'*名称':name,'型号规格':model,'瓶颈资源':bottle,'*编码':code,'*密级':SEC,'*工厂组织':biz})
def l_eq_user(eq,user): uniq(EQ_USER,(eq,user),WB_FACTORY,SH_EQ_USER,{'*设备编码':eq,'*用户':user})
def a_tool(code,name,cat=CAT_KIT,make=MAKE_SELF,tool_cat='专用工装',feat=FEATURE_IMPORTANT): add(WB_FACTORY,SH_TOOL,{'*物料分类':TOOL_CLASS,'*名称':name,'物料类别':cat,'图号':code,'*制造类型':make,'计量单位':'个','特性分类':feat,'启用批次标记':NO,'启用序列号标记':NO,'工装类别':tool_cat,'一次性工装标记':NO,'单件工装标记':NO,'物料阶段':STAGE,'*版本号':VER,'*编码':code,'*密级':SEC})
def a_wc(code,name,biz): add(WB_FACTORY,SH_WC,{'*名称':name,'*类型':'组织','*分类':'检验' if code=='WC-QUALITY' else '加工','*编码':code,'*密级':SEC,'*工厂组织':biz})
def l_wc_user(wc,user): uniq(WC_USER,(wc,user),WB_FACTORY,SH_WC_USER,{'*工作中心编码':wc,'*用户':user})
def l_wc_sup(wc,sup): uniq(WC_SUP,(wc,sup),WB_FACTORY,SH_WC_SUP,{'*工作中心编码':wc,'*供应商':sup})
def l_wc_eq(wc,eq): uniq(WC_EQ,(eq,wc),WB_FACTORY,SH_WC_EQ,{'*设备编码':eq,'*工作中心编码':wc})
def a_wh(code,name,biz,biz_type): add(WB_FACTORY,SH_WH,{'*工厂组织':biz,'*名称':name,'作业模式':'普通库房','*业务类型':biz_type,'*编码':code,'*密级':SEC})
def a_loc(code,name,biz,wh): add(WB_FACTORY,SH_LOC,{'*工厂组织':biz,'*库房编码':wh,'*名称':name,'*编码':code,'*密级':SEC})
def a_proc(name,op_type,wc,prep,run,spec,content=''): uniq(PROC,(name,wc),WB_FACTORY,SH_PLIB,{'序专业类型':spec,'*名称':name,'*工序类型':op_type,'*工作中心编码':wc,'*定额准备时间':prep,'*定额加工时间':run,'执行标记':YES,'*时间单位':TIME,'产出比':1,'工序内容':content or name,'*密级':SEC})
def a_mat(code,name,cat,make,feat,dwg,remark=''):
    row={'*物料分类':MAT_CLASS,'*名称':name,'物料类别':cat,'图号':dwg,'*制造类型':make,'计量单位':'个','特性分类':feat,'启用批次标记':YES,'启用序列号标记':NO,'物料阶段':STAGE,'*版本号':VER,'*编码':code,'*密级':SEC}
    if remark: row['备注']=remark
    add(WB_PRODUCT,SH_MAT,row); MAT[code]={'name':name,'category':cat,'make':make,'dwg':dwg,'unit':'个'}
def a_mbom(code,mat_code,name): add(WB_PRODUCT,SH_MBOM,{'*物料版本号':VER,'*物料编码':mat_code,'*版本号':VER,'*编码':code,'*密级':SEC,'名称':name})
def a_mbom_node(mbom,level,mat_code,qty,parent=''):
    meta=MAT[mat_code]; row={'*MBOM版本号':VER,'*MBOM编码':mbom,'*物料编码':mat_code,'物料名称':meta['name'],'物料图号':meta['dwg'],'*物料版本':VER,'*物料类别':meta['category'],'制造类型':meta['make'],'数量':qty,'计量单位':'个','*层级':level,'*序号':next_mbom(level),'物料阶段':STAGE}
    if parent: row['父物料编码']=parent; row['父物料版本']=VER
    add(WB_PRODUCT,SH_MBOM_NODE,row)
def a_route(code,name,spec,biz,mat_code): add(WB_PRODUCT,SH_ROUTE,{'*名称':name,'*工艺类型':ROUTE_TYPE,'工艺专业':spec,'物料版本号':VER,'物料编码':mat_code,'*版本号':VER,'*编码':code,'*密级':SEC,'*工厂组织':biz})
def a_op(route,no,name,op_type,wc,prep,run,spec,out_code,content='',prev=''):
    row={'*工序号':no,'*工序类型':op_type,'工序内容':content or name,'*工作中心编码':wc,'*定额辅助工时':prep,'*定额加工时间':run,'*时间单位':TIME,'执行标记':YES,'产出比':1,'*工艺路线版本号':VER,'*工艺路线编码':route,'*工序名称':name,'产出物料版本号':VER,'产出物料编码':out_code,'工序专业类型':spec}
    if prev: row['前置工序']=prev
    add(WB_PRODUCT,SH_OP,row)
def a_seq(route,no,up): add(WB_PRODUCT,SH_SEQ,{'*接续关系':SEQ_TYPE,'*工序号':no,'*上道工序号':up,'*工艺路线版本号':VER,'*工艺路线编码':route})
def a_opmat(route,no,mat_code,qty): add(WB_PRODUCT,SH_OPMAT,{'*工艺路线版本号':VER,'*工艺路线编码':route,'*物料版本号':VER,'*物料编码':mat_code,'*工序号':no,'数量':qty})
def a_step(route,no,step_no,name): add(WB_PRODUCT,SH_STEP,{'*工艺路线版本号':VER,'*工艺路线编码':route,'*工序号':no,'*工步序号':step_no,'*工步名称':name,'工步内容':name})
def seed_system():
    for r in [('0','公司','ADM-MT','高端机床公司','机床公司'),('ADM-MT','部门','ADM-CNC-BU','数控机床事业部','机床事业部'),('ADM-CNC-BU','工厂','ADM-CNC-PLANT','五轴机床工厂','五轴工厂'),('ADM-CNC-PLANT','部门','ADM-MFG','制造部','制造部'),('ADM-CNC-PLANT','部门','ADM-ENG','工程技术部','工程部'),('ADM-CNC-PLANT','部门','ADM-QA','质量保证部','质量部'),('ADM-CNC-PLANT','部门','ADM-SCM','供应链部','供应链'),('ADM-CNC-PLANT','部门','ADM-DIGI','数字化制造部','数制部'),('ADM-CNC-PLANT','部门','ADM-AFTER','调试与售后部','调试售后'),('ADM-CNC-PLANT','部门','ADM-WM','仓储物流部','物流部')]: a_admin(*r)
    for r in [('0','BIZ-MT','机床业务组织','机床业务','公司','ADM-MT',''),('BIZ-MT','BIZ-CNC-BU','数控机床事业部','数控机床','部门','ADM-CNC-BU',''),('BIZ-CNC-BU','BIZ-CNC-CENTER','五轴加工中心制造中心','制造中心','工厂','ADM-CNC-PLANT','装配专业'),('BIZ-CNC-CENTER','BIZ-CAST','床身结构件车间','结构件','车间','ADM-MFG','机械加工专业'),('BIZ-CNC-CENTER','BIZ-SPINDLE','主轴与传动车间','主轴传动','车间','ADM-MFG','装配专业'),('BIZ-CNC-CENTER','BIZ-ATC','刀库换刀车间','刀库换刀','车间','ADM-MFG','装配专业'),('BIZ-CNC-CENTER','BIZ-ELEC','电气数控车间','电气数控','车间','ADM-MFG','装配专业'),('BIZ-CNC-CENTER','BIZ-FINAL','总装调试车间','总装调试','车间','ADM-AFTER','装配专业'),('BIZ-CNC-CENTER','BIZ-QUALITY','质量中心','质量中心','部门','ADM-QA',''),('BIZ-CNC-CENTER','BIZ-WARE','仓储物流中心','仓储物流','部门','ADM-WM',''),('BIZ-CNC-CENTER','BIZ-DIGI','数字化制造中心','数字化','部门','ADM-DIGI','')]: a_biz(*r)
    for r in [('U-CNC-001','张昊天','核心','男','ADM-CNC-BU','BIZ-CNC-BU','事业部负责人'),('U-CNC-002','李景行','核心','男','ADM-MFG','BIZ-CNC-CENTER','制造中心主任'),('U-CNC-003','王若帆','核心','男','ADM-ENG','BIZ-CNC-CENTER','工艺总师'),('U-CNC-004','陈思远','核心','男','ADM-QA','BIZ-QUALITY','质量经理'),('U-CNC-005','刘知行','重要','男','ADM-SCM','BIZ-CNC-CENTER','供应链经理'),('U-CNC-006','赵文昊','重要','男','ADM-DIGI','BIZ-DIGI','MOM平台主管'),('U-CNC-007','黄嘉宁','重要','女','ADM-ENG','BIZ-CAST','结构件工艺工程师'),('U-CNC-008','周承泽','重要','男','ADM-ENG','BIZ-SPINDLE','主轴工艺工程师'),('U-CNC-009','吴雅雯','重要','女','ADM-QA','BIZ-QUALITY','精度检测工程师'),('U-CNC-010','徐靖涵','重要','女','ADM-AFTER','BIZ-FINAL','整机调试主管'),('U-CNC-011','孙博文','重要','男','ADM-MFG','BIZ-FINAL','总装工程师'),('U-CNC-012','马睿哲','一般','男','ADM-MFG','BIZ-CAST','结构件班组长'),('U-CNC-013','朱彦霖','一般','男','ADM-MFG','BIZ-SPINDLE','主轴装配班组长'),('U-CNC-014','胡明轩','一般','男','ADM-MFG','BIZ-ATC','刀库班组长'),('U-CNC-015','郭星宇','一般','男','ADM-MFG','BIZ-ELEC','电气装配班组长'),('U-CNC-016','何雨桐','重要','女','ADM-ENG','BIZ-ELEC','数控系统工程师'),('U-CNC-017','高成蹊','一般','男','ADM-WM','BIZ-WARE','物流计划工程师'),('U-CNC-018','唐子墨','一般','男','ADM-MFG','BIZ-CNC-CENTER','设备工程师'),('U-CNC-019','程悦然','重要','女','ADM-QA','BIZ-QUALITY','三坐标检测工程师'),('U-CNC-020','魏嘉树','一般','男','ADM-AFTER','BIZ-FINAL','切削试验工程师')]: a_user(*r)

def seed_factory():
    for r in [('SUP-CAST','高强度铸件供应商','铸件'),('SUP-LM','线轨丝杠供应商','线轨丝杠'),('SUP-BEAR','精密轴承供应商','轴承'),('SUP-CNC','数控系统供应商','数控系统'),('SUP-SERVO','伺服电机供应商','伺服'),('SUP-ELEC','电气元件供应商','电气'),('SUP-ATC','刀库机械手供应商','刀库'),('SUP-HYD','液压润滑冷却供应商','液压润滑')]: a_sup(*r)
    for r in [('EQ-GANTRY-GRIND','龙门导轨磨床','GG-4020','BIZ-CAST',YES),('EQ-HBM','卧式镗铣加工中心','HBM-160','BIZ-CAST',YES),('EQ-VMC','立式加工中心','VMC-1270','BIZ-CAST',NO),('EQ-BORING','坐标镗床','TPX6111','BIZ-CAST',NO),('EQ-SPINDLE-BAL','主轴动平衡机','BAL-SP-01','BIZ-SPINDLE',YES),('EQ-BALLSCREW-ASM','丝杠预拉伸装配台','BS-ASM-01','BIZ-SPINDLE',NO),('EQ-ATC-ASM','刀库机械手装配台','ATC-ASM-01','BIZ-ATC',NO),('EQ-WIRING','电气线束测试台','WIRE-TEST-01','BIZ-ELEC',NO),('EQ-CNC-BURN','数控系统参数烧录台','CNC-BURN-01','BIZ-ELEC',NO),('EQ-LASER-INT','激光干涉仪','XL-80','BIZ-QUALITY',YES),('EQ-BALLBAR','球杆仪','QC20-W','BIZ-QUALITY',NO),('EQ-CMM','三坐标测量机','CMM-15','BIZ-QUALITY',YES),('EQ-TRACKER','激光跟踪仪','AT960','BIZ-QUALITY',NO),('EQ-GEO-PLAT','几何精度检测平台','GEO-PLAT-01','BIZ-FINAL',YES),('EQ-RUNIN','整机空载跑合台','RUNIN-01','BIZ-FINAL',NO),('EQ-CUTTEST','负载切削试验台','CUTTEST-01','BIZ-FINAL',YES),('EQ-HYD-TEST','液压润滑测试台','HYD-TEST-01','BIZ-FINAL',NO),('EQ-PACK','包装打包工位','PACK-01','BIZ-WARE',NO)]: a_eq(*r)
    for r in [('TOOL-BED-FIX','床身找正定位工装',CAT_KIT,MAKE_SELF,'专用工装',FEATURE_KEY),('TOOL-SPINDLE-FIX','主轴箱装配工装',CAT_KIT,MAKE_SELF,'专用工装',FEATURE_IMPORTANT),('TOOL-BSCREW-FIX','滚珠丝杠安装工装',CAT_KIT,MAKE_SELF,'专用工装',FEATURE_IMPORTANT),('TOOL-TABLE-FIX','回转工作台安装工装',CAT_KIT,MAKE_SELF,'专用工装',FEATURE_IMPORTANT),('TOOL-ELEC-CART','电柜转运车',CAT_PART,MAKE_SELF,'通用工具',FEATURE_NORMAL),('TOOL-PACK-KIT','随机工具包',CAT_PART,MAKE_BUY,'通用工具',FEATURE_NORMAL)]: a_tool(*r)
    for r in [('WC-BED-MACH','床身机加工中心','BIZ-CAST'),('WC-COLUMN-MACH','立柱机加工中心','BIZ-CAST'),('WC-TABLE-MACH','工作台机加工中心','BIZ-CAST'),('WC-SPINDLE-ASM','主轴部件装配中心','BIZ-SPINDLE'),('WC-FEED-ASM','丝杠导轨装配中心','BIZ-SPINDLE'),('WC-ATC-ASM','刀库换刀装配中心','BIZ-ATC'),('WC-ELEC-PANEL','电柜装配中心','BIZ-ELEC'),('WC-CNC-INTEG','数控系统集成中心','BIZ-ELEC'),('WC-FINAL-ASM','整机总装中心','BIZ-FINAL'),('WC-QUALITY','精度检测中心','BIZ-QUALITY'),('WC-TEST','整机试车中心','BIZ-FINAL'),('WC-PACK','包装发运中心','BIZ-WARE')]: a_wc(*r)
    for r in [('WH-RM','原材料库','BIZ-WARE','ERP一级库'),('WH-PUR','外购件库','BIZ-WARE','ERP二级库'),('WH-WIP','在制品库','BIZ-WARE','车间二级库'),('WH-FG','成品机床库','BIZ-WARE','ERP一级库')]: a_wh(*r)
    for r in [('LOC-RM-A01','铸件区-A01','BIZ-WARE','WH-RM'),('LOC-RM-B01','钢材区-B01','BIZ-WARE','WH-RM'),('LOC-PUR-A01','电气件区-A01','BIZ-WARE','WH-PUR'),('LOC-PUR-B01','传动件区-B01','BIZ-WARE','WH-PUR'),('LOC-WIP-A01','机加在制区-A01','BIZ-WARE','WH-WIP'),('LOC-WIP-B01','总装在制区-B01','BIZ-WARE','WH-WIP'),('LOC-FG-A01','待验成品区-A01','BIZ-WARE','WH-FG'),('LOC-FG-B01','待发运区-B01','BIZ-WARE','WH-FG')]: a_loc(*r)
    for r in [('EQ-GANTRY-GRIND','U-CNC-007'),('EQ-HBM','U-CNC-012'),('EQ-VMC','U-CNC-012'),('EQ-BORING','U-CNC-012'),('EQ-SPINDLE-BAL','U-CNC-008'),('EQ-BALLSCREW-ASM','U-CNC-013'),('EQ-ATC-ASM','U-CNC-014'),('EQ-WIRING','U-CNC-015'),('EQ-CNC-BURN','U-CNC-016'),('EQ-LASER-INT','U-CNC-009'),('EQ-BALLBAR','U-CNC-019'),('EQ-CMM','U-CNC-019'),('EQ-TRACKER','U-CNC-009'),('EQ-GEO-PLAT','U-CNC-010'),('EQ-RUNIN','U-CNC-011'),('EQ-CUTTEST','U-CNC-020'),('EQ-HYD-TEST','U-CNC-010'),('EQ-PACK','U-CNC-017')]: l_eq_user(*r)
    for r in [('WC-BED-MACH','U-CNC-007'),('WC-BED-MACH','U-CNC-012'),('WC-COLUMN-MACH','U-CNC-007'),('WC-TABLE-MACH','U-CNC-007'),('WC-SPINDLE-ASM','U-CNC-008'),('WC-SPINDLE-ASM','U-CNC-013'),('WC-FEED-ASM','U-CNC-013'),('WC-ATC-ASM','U-CNC-014'),('WC-ELEC-PANEL','U-CNC-015'),('WC-CNC-INTEG','U-CNC-016'),('WC-FINAL-ASM','U-CNC-002'),('WC-FINAL-ASM','U-CNC-011'),('WC-QUALITY','U-CNC-009'),('WC-QUALITY','U-CNC-019'),('WC-TEST','U-CNC-010'),('WC-TEST','U-CNC-020'),('WC-PACK','U-CNC-017')]: l_wc_user(*r)
    for r in [('WC-BED-MACH','SUP-CAST'),('WC-COLUMN-MACH','SUP-CAST'),('WC-TABLE-MACH','SUP-LM'),('WC-SPINDLE-ASM','SUP-BEAR'),('WC-SPINDLE-ASM','SUP-SERVO'),('WC-FEED-ASM','SUP-LM'),('WC-ATC-ASM','SUP-ATC'),('WC-ELEC-PANEL','SUP-ELEC'),('WC-CNC-INTEG','SUP-CNC'),('WC-CNC-INTEG','SUP-SERVO'),('WC-FINAL-ASM','SUP-HYD'),('WC-QUALITY','SUP-CNC'),('WC-TEST','SUP-HYD')]: l_wc_sup(*r)
    for r in [('WC-BED-MACH','EQ-GANTRY-GRIND'),('WC-BED-MACH','EQ-HBM'),('WC-COLUMN-MACH','EQ-VMC'),('WC-TABLE-MACH','EQ-BORING'),('WC-SPINDLE-ASM','EQ-SPINDLE-BAL'),('WC-FEED-ASM','EQ-BALLSCREW-ASM'),('WC-ATC-ASM','EQ-ATC-ASM'),('WC-ELEC-PANEL','EQ-WIRING'),('WC-CNC-INTEG','EQ-CNC-BURN'),('WC-QUALITY','EQ-LASER-INT'),('WC-QUALITY','EQ-BALLBAR'),('WC-QUALITY','EQ-CMM'),('WC-QUALITY','EQ-TRACKER'),('WC-FINAL-ASM','EQ-GEO-PLAT'),('WC-TEST','EQ-RUNIN'),('WC-TEST','EQ-CUTTEST'),('WC-TEST','EQ-HYD-TEST'),('WC-PACK','EQ-PACK')]: l_wc_eq(*r)
def seed_materials():
    for r in [
        ('MAT-CNC-850','VMC-850-5X五轴立式加工中心整机',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-CNC-850','高端五轴立式加工中心整机'),
        ('MAT-MOD-BASE','床身基础模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-BASE',''),('MAT-MOD-COLUMN','立柱滑鞍模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-COLUMN',''),('MAT-MOD-TABLE','工作台回转模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-TABLE',''),('MAT-MOD-SPINDLE','主轴箱模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-SPINDLE',''),('MAT-MOD-FEED','进给传动模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-FEED',''),('MAT-MOD-ATC','刀库换刀模块',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-MOD-ATC',''),('MAT-MOD-ELEC','数控电气模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-MOD-ELEC',''),('MAT-MOD-HYD','液压润滑冷却模块',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-MOD-HYD',''),('MAT-MOD-GUARD','防护与排屑模块',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-MOD-GUARD',''),('MAT-MOD-PKG','检测附件与交付包',CAT_KIT,MAKE_BUY,FEATURE_NORMAL,'DWG-MOD-PKG',''),
        ('MAT-BED-CAST','床身铸件',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-BED-CAST',''),('MAT-COLUMN-CAST','立柱铸件',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-COLUMN-CAST',''),('MAT-SADDLE','滑鞍铸件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-SADDLE',''),('MAT-WORKTABLE','工作台体',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-WORKTABLE',''),('MAT-ROTARY-AC','A/C轴回转工作台',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-ROTARY-AC',''),('MAT-SPINDLE-HOUSING','主轴箱体',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-SPINDLE-HOUSING',''),('MAT-E-SPINDLE','电主轴单元',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-E-SPINDLE',''),('MAT-DRAWBAR','主轴拉刀机构',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-DRAWBAR',''),
        ('MAT-BSCREW-X','X轴滚珠丝杠副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-BSCREW-X',''),('MAT-BSCREW-Y','Y轴滚珠丝杠副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-BSCREW-Y',''),('MAT-BSCREW-Z','Z轴滚珠丝杠副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-BSCREW-Z',''),('MAT-LM-X','X轴线性导轨副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LM-X',''),('MAT-LM-Y','Y轴线性导轨副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LM-Y',''),('MAT-LM-Z','Z轴线性导轨副',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LM-Z',''),('MAT-SERVO-X','X轴伺服电机',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-SERVO-X',''),('MAT-SERVO-Y','Y轴伺服电机',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-SERVO-Y',''),('MAT-SERVO-Z','Z轴伺服电机',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-SERVO-Z',''),
        ('MAT-ATC-MAG','刀库盘',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-ATC-MAG',''),('MAT-ATC-ARM','机械手ATC组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-ATC-ARM',''),('MAT-ATC-DRIVE','刀库驱动组件',CAT_PART,MAKE_BUY,FEATURE_NORMAL,'DWG-ATC-DRIVE',''),('MAT-CNC-SYS','数控系统',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-CNC-SYS',''),('MAT-SERVO-DRV','伺服驱动器组',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-SERVO-DRV',''),('MAT-ELEC-CAB','机床电柜',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-ELEC-CAB',''),('MAT-PANEL','操作面板',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-PANEL',''),('MAT-SCALE','光栅尺编码器套件',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-SCALE',''),
        ('MAT-HYD-STA','液压站',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-HYD-STA',''),('MAT-LUBE-PUMP','润滑泵组',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LUBE-PUMP',''),('MAT-COOL-TANK','冷却液箱',CAT_PART,MAKE_SELF,FEATURE_NORMAL,'DWG-COOL-TANK',''),('MAT-PIPING','液压润滑管路包',CAT_PART,MAKE_BUY,FEATURE_NORMAL,'DWG-PIPING',''),('MAT-GUARD-SHEET','钣金护罩',CAT_PART,MAKE_SELF,FEATURE_NORMAL,'DWG-GUARD-SHEET',''),('MAT-COVER-TELE','伸缩防护罩',CAT_PART,MAKE_BUY,FEATURE_NORMAL,'DWG-COVER-TELE',''),('MAT-CHIP','排屑器',CAT_PART,MAKE_BUY,FEATURE_NORMAL,'DWG-CHIP',''),('MAT-CABLE-CHAIN','拖链组件',CAT_PART,MAKE_BUY,FEATURE_NORMAL,'DWG-CABLE-CHAIN',''),
        ('MAT-TOOLSET','随机工具包',CAT_KIT,MAKE_BUY,FEATURE_NORMAL,'DWG-TOOLSET',''),('MAT-PROBE','工件测头',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-PROBE',''),('MAT-TOOL-PRESET','对刀仪',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-TOOL-PRESET',''),('MAT-DOC-KIT','随机文件资料包',CAT_KIT,MAKE_BUY,FEATURE_NORMAL,'DWG-DOC-KIT',''),
        ('MAT-RAW-HT300','HT300铸件毛坯',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-HT300',''),('MAT-RAW-QT500','QT500铸件毛坯',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-QT500',''),('MAT-RAW-40CR','40Cr轴类毛坯',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-40CR',''),('MAT-RAW-45STEEL','45钢板材',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-45STEEL',''),('MAT-RAW-FASTENER','标准紧固件包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-FASTENER',''),('MAT-RAW-BEARING','精密轴承包',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-BEARING',''),('MAT-RAW-CABLE','电缆线束包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-CABLE',''),('MAT-RAW-LOWV','低压电器包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-LOWV',''),('MAT-RAW-HYDFIT','液压管件包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-HYDFIT',''),('MAT-RAW-LUBEFIT','润滑管件包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-LUBEFIT',''),('MAT-AUX-GREASE','润滑脂',CAT_AUX,MAKE_BUY,FEATURE_NORMAL,'MAT-AUX-GREASE',''),('MAT-AUX-SEAL','密封胶',CAT_AUX,MAKE_BUY,FEATURE_NORMAL,'MAT-AUX-SEAL','')]: a_mat(*r)

def seed_mbom():
    a_mbom('MBOM-CNC-850-A01','MAT-CNC-850','VMC-850-5X整机MBOM')
    for code in ['MAT-MOD-BASE','MAT-MOD-COLUMN','MAT-MOD-TABLE','MAT-MOD-SPINDLE','MAT-MOD-FEED','MAT-MOD-ATC','MAT-MOD-ELEC','MAT-MOD-HYD','MAT-MOD-GUARD','MAT-MOD-PKG']: a_mbom_node('MBOM-CNC-850-A01',1,code,1,'MAT-CNC-850')
    groups=[('MAT-MOD-BASE',[('MAT-BED-CAST',1)]),('MAT-MOD-COLUMN',[('MAT-COLUMN-CAST',1),('MAT-SADDLE',1)]),('MAT-MOD-TABLE',[('MAT-WORKTABLE',1),('MAT-ROTARY-AC',1)]),('MAT-MOD-SPINDLE',[('MAT-SPINDLE-HOUSING',1),('MAT-E-SPINDLE',1),('MAT-DRAWBAR',1)]),('MAT-MOD-FEED',[('MAT-BSCREW-X',1),('MAT-BSCREW-Y',1),('MAT-BSCREW-Z',1),('MAT-LM-X',1),('MAT-LM-Y',1),('MAT-LM-Z',1),('MAT-SERVO-X',1),('MAT-SERVO-Y',1),('MAT-SERVO-Z',1)]),('MAT-MOD-ATC',[('MAT-ATC-MAG',1),('MAT-ATC-ARM',1),('MAT-ATC-DRIVE',1)]),('MAT-MOD-ELEC',[('MAT-CNC-SYS',1),('MAT-SERVO-DRV',1),('MAT-ELEC-CAB',1),('MAT-PANEL',1),('MAT-SCALE',1)]),('MAT-MOD-HYD',[('MAT-HYD-STA',1),('MAT-LUBE-PUMP',1),('MAT-COOL-TANK',1),('MAT-PIPING',1)]),('MAT-MOD-GUARD',[('MAT-GUARD-SHEET',1),('MAT-COVER-TELE',1),('MAT-CHIP',1),('MAT-CABLE-CHAIN',1)]),('MAT-MOD-PKG',[('MAT-TOOLSET',1),('MAT-PROBE',1),('MAT-TOOL-PRESET',1),('MAT-DOC-KIT',1)])]
    for parent,children in groups:
        for code,qty in children: a_mbom_node('MBOM-CNC-850-A01',2,code,qty,parent)
    raw_groups=[('MAT-BED-CAST',[('MAT-RAW-HT300',1)]),('MAT-COLUMN-CAST',[('MAT-RAW-HT300',1)]),('MAT-SADDLE',[('MAT-RAW-QT500',1)]),('MAT-SPINDLE-HOUSING',[('MAT-RAW-40CR',1)]),('MAT-DRAWBAR',[('MAT-RAW-40CR',1),('MAT-RAW-BEARING',1)]),('MAT-ELEC-CAB',[('MAT-RAW-45STEEL',1),('MAT-RAW-LOWV',1)]),('MAT-PIPING',[('MAT-RAW-HYDFIT',1),('MAT-RAW-LUBEFIT',1)]),('MAT-GUARD-SHEET',[('MAT-RAW-45STEEL',1)]),('MAT-CABLE-CHAIN',[('MAT-RAW-CABLE',1)]),('MAT-TOOLSET',[('MAT-RAW-FASTENER',1)]),('MAT-BSCREW-X',[('MAT-RAW-BEARING',1)]),('MAT-BSCREW-Y',[('MAT-RAW-BEARING',1)]),('MAT-BSCREW-Z',[('MAT-RAW-BEARING',1)])]
    for parent,children in raw_groups:
        for code,qty in children: a_mbom_node('MBOM-CNC-850-A01',3,code,qty,parent)
def make_route(code,name,spec,biz,mat_code,ops):
    a_route(code,name,spec,biz,mat_code); prev=''
    for no,op_name,op_type,wc,prep,run,op_spec,inputs,steps in ops:
        a_op(code,no,op_name,op_type,wc,prep,run,op_spec,mat_code,op_name,prev); a_proc(op_name,op_type,wc,prep,run,op_spec,op_name)
        if prev: a_seq(code,no,prev)
        for m,q in inputs: a_opmat(code,no,m,q)
        for idx,sn in enumerate(steps,1): a_step(code,no,f'{idx*10}',sn)
        prev=no

def seed_routes():
    routes=[
        ('RT-BASE-A01','床身基础模块机加工工艺','机加','BIZ-CAST','MAT-MOD-BASE',[( '0010','床身粗加工','加工','WC-BED-MACH',40,180,'机械加工专业',[('MAT-BED-CAST',1),('MAT-RAW-FASTENER',1)],['粗基准加工','安装面粗铣']),( '0020','导轨面精磨','加工','WC-BED-MACH',30,150,'机械加工专业',[('MAT-BED-CAST',1),('MAT-AUX-GREASE',1)],['导轨精磨','安装面精修']),( '0030','关键孔系镗削','加工','WC-BED-MACH',20,120,'机械加工专业',[('MAT-BED-CAST',1),('MAT-RAW-FASTENER',1)],['孔系定位','镗削加工']),( '0040','床身精度复检','检验','WC-QUALITY',20,60,'机械加工专业',[('MAT-BED-CAST',1)],['几何检测','记录放行'])]),
        ('RT-COLUMN-A01','立柱滑鞍模块机加工工艺','机加','BIZ-CAST','MAT-MOD-COLUMN',[( '0010','立柱粗加工','加工','WC-COLUMN-MACH',35,160,'机械加工专业',[('MAT-COLUMN-CAST',1),('MAT-SADDLE',1)],['基面粗加工','装配面粗铣']),( '0020','滑鞍配合面精加工','加工','WC-COLUMN-MACH',30,140,'机械加工专业',[('MAT-SADDLE',1),('MAT-AUX-GREASE',1)],['滑鞍导轨面加工','配合面精修']),( '0030','孔系与丝杠座加工','加工','WC-COLUMN-MACH',25,110,'机械加工专业',[('MAT-COLUMN-CAST',1),('MAT-SADDLE',1)],['孔位找正','座体加工']),( '0040','立柱模块复检','检验','WC-QUALITY',20,55,'机械加工专业',[('MAT-COLUMN-CAST',1)],['尺寸检测','精度放行'])]),
        ('RT-TABLE-A01','工作台回转模块装配工艺','装配','BIZ-CAST','MAT-MOD-TABLE',[( '0010','工作台体加工','加工','WC-TABLE-MACH',30,130,'机械加工专业',[('MAT-WORKTABLE',1),('MAT-RAW-FASTENER',1)],['台面精铣','定位孔加工']),( '0020','回转台安装','加工','WC-TABLE-MACH',25,100,'机械加工专业',[('MAT-ROTARY-AC',1),('MAT-RAW-FASTENER',1)],['回转台定位','连接锁固']),( '0030','零位校准','检验','WC-QUALITY',20,70,'机械加工专业',[('MAT-ROTARY-AC',1)],['零位设定','重复定位检测']),( '0040','模块放行','检验','WC-QUALITY',15,40,'机械加工专业',[('MAT-WORKTABLE',1)],['文件核对','放行确认'])]),
        ('RT-SPINDLE-A01','主轴箱模块装配工艺','装配','BIZ-SPINDLE','MAT-MOD-SPINDLE',[( '0010','主轴箱体加工复核','检验','WC-SPINDLE-ASM',20,45,'装配专业',[('MAT-SPINDLE-HOUSING',1)],['箱体清洁','基准复核']),( '0020','电主轴安装','加工','WC-SPINDLE-ASM',25,90,'装配专业',[('MAT-E-SPINDLE',1),('MAT-RAW-BEARING',1)],['主轴吊装','配合锁紧']),( '0030','拉刀机构装配','加工','WC-SPINDLE-ASM',25,80,'装配专业',[('MAT-DRAWBAR',1),('MAT-AUX-GREASE',1)],['拉刀装入','动作测试']),( '0040','动平衡与振动检测','检验','WC-QUALITY',20,60,'装配专业',[('MAT-E-SPINDLE',1)],['动平衡检测','振动记录'])]),
        ('RT-FEED-A01','进给传动模块装配工艺','装配','BIZ-SPINDLE','MAT-MOD-FEED',[( '0010','线轨安装','加工','WC-FEED-ASM',25,85,'装配专业',[('MAT-LM-X',1),('MAT-LM-Y',1),('MAT-LM-Z',1)],['导轨定位','扭矩锁固']),( '0020','丝杠安装','加工','WC-FEED-ASM',30,100,'装配专业',[('MAT-BSCREW-X',1),('MAT-BSCREW-Y',1),('MAT-BSCREW-Z',1)],['丝杠就位','预拉伸调整']),( '0030','伺服电机联接','加工','WC-FEED-ASM',20,70,'装配专业',[('MAT-SERVO-X',1),('MAT-SERVO-Y',1),('MAT-SERVO-Z',1)],['电机联轴','间隙调整']),( '0040','往复精度检测','检验','WC-QUALITY',20,60,'装配专业',[('MAT-LM-X',1)],['激光补偿','精度确认'])]),
        ('RT-ATC-A01','刀库换刀模块装配工艺','装配','BIZ-ATC','MAT-MOD-ATC',[( '0010','刀库盘装配','加工','WC-ATC-ASM',20,70,'装配专业',[('MAT-ATC-MAG',1),('MAT-ATC-DRIVE',1)],['刀盘定位','驱动安装']),( '0020','机械手装配','加工','WC-ATC-ASM',25,80,'装配专业',[('MAT-ATC-ARM',1),('MAT-AUX-GREASE',1)],['机械手装入','原点设定']),( '0030','换刀动作联调','检验','WC-ATC-ASM',20,60,'装配专业',[('MAT-ATC-MAG',1)],['动作联调','节拍确认']),( '0040','模块放行','检验','WC-QUALITY',15,40,'装配专业',[('MAT-ATC-ARM',1)],['记录核对','放行确认'])]),
        ('RT-ELEC-A01','数控电气模块装配工艺','装配','BIZ-ELEC','MAT-MOD-ELEC',[( '0010','电柜装配','加工','WC-ELEC-PANEL',25,90,'装配专业',[('MAT-ELEC-CAB',1),('MAT-RAW-LOWV',1)],['柜体装配','元件安装']),( '0020','数控系统集成','加工','WC-CNC-INTEG',30,100,'装配专业',[('MAT-CNC-SYS',1),('MAT-SERVO-DRV',1)],['系统安装','驱动接入']),( '0030','面板与光栅尺接线','加工','WC-CNC-INTEG',25,85,'装配专业',[('MAT-PANEL',1),('MAT-SCALE',1),('MAT-RAW-CABLE',1)],['面板接线','反馈接入']),( '0040','通电测试','检验','WC-QUALITY',20,50,'装配专业',[('MAT-CNC-SYS',1)],['绝缘测试','通电确认'])]),
        ('RT-HYD-A01','液压润滑冷却模块装配工艺','装配','BIZ-FINAL','MAT-MOD-HYD',[( '0010','液压站安装','加工','WC-FINAL-ASM',20,70,'装配专业',[('MAT-HYD-STA',1),('MAT-RAW-HYDFIT',1)],['液压站定位','接口连接']),( '0020','润滑系统安装','加工','WC-FINAL-ASM',20,65,'装配专业',[('MAT-LUBE-PUMP',1),('MAT-RAW-LUBEFIT',1)],['润滑泵安装','油路连接']),( '0030','冷却液箱与管路安装','加工','WC-FINAL-ASM',20,60,'装配专业',[('MAT-COOL-TANK',1),('MAT-PIPING',1)],['冷却箱安装','管路布置']),( '0040','压力与泄漏检测','检验','WC-TEST',20,50,'装配专业',[('MAT-AUX-SEAL',1)],['压力测试','泄漏确认'])]),
        ('RT-GUARD-A01','防护与排屑模块装配工艺','装配','BIZ-FINAL','MAT-MOD-GUARD',[( '0010','钣金护罩安装','加工','WC-FINAL-ASM',20,75,'装配专业',[('MAT-GUARD-SHEET',1),('MAT-RAW-FASTENER',1)],['护罩定位','锁紧安装']),( '0020','伸缩防护安装','加工','WC-FINAL-ASM',20,65,'装配专业',[('MAT-COVER-TELE',1),('MAT-RAW-FASTENER',1)],['导轨防护安装','动作检查']),( '0030','排屑器与拖链安装','加工','WC-FINAL-ASM',20,70,'装配专业',[('MAT-CHIP',1),('MAT-CABLE-CHAIN',1)],['排屑器装配','拖链布置']),( '0040','外观与动作复检','检验','WC-QUALITY',15,40,'装配专业',[('MAT-GUARD-SHEET',1)],['外观检查','动作确认'])]),
        ('RT-FINAL-A01','整机总装工艺','装配','BIZ-FINAL','MAT-CNC-850',[( '0010','基础部件总装','加工','WC-FINAL-ASM',40,150,'装配专业',[('MAT-MOD-BASE',1),('MAT-MOD-COLUMN',1)],['床身立柱对接','几何初调']),( '0020','工作台主轴总装','加工','WC-FINAL-ASM',45,170,'装配专业',[('MAT-MOD-TABLE',1),('MAT-MOD-SPINDLE',1)],['工作台装入','主轴箱装入']),( '0030','进给与电气总装','加工','WC-FINAL-ASM',45,160,'装配专业',[('MAT-MOD-FEED',1),('MAT-MOD-ELEC',1),('MAT-MOD-ATC',1)],['进给装配','电气接入']),( '0040','液压防护附件装配','加工','WC-FINAL-ASM',35,130,'装配专业',[('MAT-MOD-HYD',1),('MAT-MOD-GUARD',1),('MAT-MOD-PKG',1)],['液压模块装配','附件装入'])]),
        ('RT-GEO-A01','几何精度检测工艺','机加','BIZ-QUALITY','MAT-CNC-850',[( '0010','坐标轴回零检测','检验','WC-QUALITY',20,45,'机械加工专业',[('MAT-CNC-850',1)],['回零确认','重复定位检测']),( '0020','激光干涉补偿','检验','WC-QUALITY',25,70,'机械加工专业',[('MAT-CNC-850',1)],['激光测量','补偿导入']),( '0030','球杆圆度检测','检验','WC-QUALITY',20,50,'机械加工专业',[('MAT-CNC-850',1)],['球杆测试','圆度分析']),( '0040','整机精度放行','检验','WC-QUALITY',20,40,'机械加工专业',[('MAT-CNC-850',1)],['精度判定','放行归档'])]),
        ('RT-TEST-A01','整机试运行与切削验证工艺','通用','BIZ-FINAL','MAT-CNC-850',[( '0010','空载跑合','加工','WC-TEST',20,90,'装配专业',[('MAT-CNC-850',1)],['空载运行','温升观察']),( '0020','换刀与联锁验证','检验','WC-TEST',20,60,'装配专业',[('MAT-CNC-850',1)],['换刀验证','联锁确认']),( '0030','负载切削试验','加工','WC-TEST',25,100,'装配专业',[('MAT-CNC-850',1)],['试件切削','表面质量检测']),( '0040','最终交付确认','检验','WC-QUALITY',20,40,'装配专业',[('MAT-CNC-850',1)],['报告归档','交付确认'])])]
    for r in routes: make_route(*r)

def normalize_seed_safe():
    for row in seed['workbooks'][WB_SYSTEM][SH_ADMIN]:
        if row.get('*父组织编码') in {'ROOT-ADMIN','ROOT-BIZ'}: row['*父组织编码']='0'
    for row in seed['workbooks'][WB_SYSTEM][SH_BIZ]:
        if row.get('*父组织编码') in {'ROOT-ADMIN','ROOT-BIZ'}: row['*父组织编码']='0'
    for row in seed['workbooks'][WB_FACTORY][SH_MAT] if SH_MAT in seed['workbooks'][WB_FACTORY] else []: row['计量单位']='个'

def build_variant(namespace: str, volume_profile: str | None = None) -> dict:
    reset()
    seed_system(); seed_factory(); seed_materials(); seed_mbom(); seed_routes(); apply_profile(seed, 'cnc_machine'); apply_scene_upgrade(seed, 'cnc_machine', namespace, volume_profile=volume_profile); apply_production_orders(seed, 'cnc_machine', namespace)
    return seed

def build() -> dict:
    return build_variant(NAMESPACE)

def summarize(seed_data: dict) -> dict:
    return {'metadata':seed_data['metadata'],'counts':{wb:{sh:len(rows) for sh,rows in sheets.items()} for wb,sheets in seed_data['workbooks'].items()}}

def summary():
    return summarize(seed)

def main():
    ASSET_PATH.parent.mkdir(parents=True,exist_ok=True)
    for asset_name, namespace, volume_profile in VARIANT_SPECS:
        variant_seed = build_variant(namespace, volume_profile)
        asset_path = ASSET_PATH.parent / asset_name
        asset_path.write_text(json.dumps(variant_seed,ensure_ascii=False,indent=2),encoding='utf-8-sig')
        print(json.dumps(summarize(variant_seed),ensure_ascii=False,indent=2))
        print(f'已写入种子文件: {asset_path}')
if __name__=='__main__': main()
