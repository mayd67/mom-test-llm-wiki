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
SEC='内部'; VER='A.01'; YES='是'; NO='否'; TIME='分钟'; ROUTE_TYPE='正式工艺'; MAT_CLASS='物料'; TOOL_CLASS='工装工具'; CAT_RAW='原材料'; CAT_AUX='辅助材料'; CAT_PART='零部件'; CAT_KIT='配套件'; CAT_SPARE='设备备件'; MAKE_SELF='自制件'; MAKE_BUY='外购件'; FEATURE_KEY='关键件'; FEATURE_IMPORTANT='重要件'; FEATURE_NORMAL='一般件'; SEQ_TYPE='ES'; STAGE='量产'; NAMESPACE='B7L1B01'
ASSET_PATH=Path(__file__).resolve().parent.parent/'assets'/'boeing_737_leap1b_seed.json'
seed={
  'metadata':{
    'name':'波音737 MAX LEAP-1B航空发动机MOM种子',
    'aircraft_family':'Boeing 737 MAX',
    'engine_model':'CFM LEAP-1B',
    'description':'基于公开资料构建的波音737 MAX / CFM LEAP-1B航空发动机拟真制造MOM主数据种子。',
    'public_fact_note':'采用737 MAX配套发动机LEAP-1B作为公开事实基线，体现69英寸风扇、约28000磅级推力、复合材料风扇叶片与机匣、TAPS II喷嘴和CMC热端件等公开特征。',
    'default_version':VER,'default_security':SEC},
  'external_references':['ROOT-ADMIN','ROOT-BIZ'],
  'workbooks':{WB_SYSTEM:{SH_ADMIN:[],SH_BIZ:[],SH_USER:[]},WB_FACTORY:{SH_SUP:[],SH_EQ:[],SH_EQ_USER:[],SH_TOOL:[],SH_WC:[],SH_WC_USER:[],SH_WC_SUP:[],SH_WC_EQ:[],SH_WH:[],SH_LOC:[],SH_PLIB:[]},WB_PRODUCT:{SH_MAT:[],SH_MBOM:[],SH_MBOM_NODE:[],SH_ROUTE:[],SH_OP:[],SH_SEQ:[],SH_OPMAT:[],SH_STEP:[]}}}
SEED_TEMPLATE=copy.deepcopy(seed)
VARIANT_SPECS=[('boeing_737_leap1b_seed.json', NAMESPACE, '标准版'), ('boeing_737_leap1b_seed_big.json', 'B7L1B31', '大体量版'), ('boeing_737_leap1b_seed_ultra.json', 'B7L1B42', '超大体量版')]
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
def a_tool(code,name,cat=CAT_KIT,make=MAKE_SELF,tool_cat='装配工装',unit='套',feat=FEATURE_IMPORTANT): add(WB_FACTORY,SH_TOOL,{'*物料分类':TOOL_CLASS,'*名称':name,'物料类别':cat,'图号':code,'*制造类型':make,'计量单位':unit,'特性分类':feat,'启用批次标记':NO,'启用序列号标记':NO,'工装类别':tool_cat,'一次性工装标记':NO,'单件工装标记':NO,'物料阶段':STAGE,'*版本号':VER,'*编码':code,'*密级':SEC})
def a_wc(code,name,wc_type,wc_class,biz): add(WB_FACTORY,SH_WC,{'*名称':name,'*类型':wc_type,'*分类':wc_class,'*编码':code,'*密级':SEC,'*工厂组织':biz})
def l_wc_user(wc,user): uniq(WC_USER,(wc,user),WB_FACTORY,SH_WC_USER,{'*工作中心编码':wc,'*用户':user})
def l_wc_sup(wc,sup): uniq(WC_SUP,(wc,sup),WB_FACTORY,SH_WC_SUP,{'*工作中心编码':wc,'*供应商':sup})
def l_wc_eq(wc,eq): uniq(WC_EQ,(eq,wc),WB_FACTORY,SH_WC_EQ,{'*设备编码':eq,'*工作中心编码':wc})
def a_wh(code,name,biz,biz_type): add(WB_FACTORY,SH_WH,{'*工厂组织':biz,'*名称':name,'作业模式':'普通库房','*业务类型':biz_type,'*编码':code,'*密级':SEC})
def a_loc(code,name,biz,wh): add(WB_FACTORY,SH_LOC,{'*工厂组织':biz,'*库房编码':wh,'*名称':name,'*编码':code,'*密级':SEC})
def a_proc(name,op_type,wc,prep,run,spec,content=''): uniq(PROC,(name,wc),WB_FACTORY,SH_PLIB,{'序专业类型':spec,'*名称':name,'*工序类型':op_type,'*工作中心编码':wc,'*定额准备时间':prep,'*定额加工时间':run,'执行标记':YES,'*时间单位':TIME,'产出比':1,'工序内容':content or name,'*密级':SEC})
def a_mat(code,name,cat,make,feat,dwg,unit='件',remark=''):
    row={'*物料分类':MAT_CLASS,'*名称':name,'物料类别':cat,'图号':dwg,'*制造类型':make,'计量单位':unit,'特性分类':feat,'启用批次标记':YES,'启用序列号标记':NO,'物料阶段':STAGE,'*版本号':VER,'*编码':code,'*密级':SEC}
    if remark: row['备注']=remark
    add(WB_PRODUCT,SH_MAT,row); MAT[code]={'name':name,'category':cat,'make':make,'dwg':dwg,'unit':unit}
def a_mbom(code,mat_code,name): add(WB_PRODUCT,SH_MBOM,{'*物料版本号':VER,'*物料编码':mat_code,'*版本号':VER,'*编码':code,'*密级':SEC,'名称':name})
def a_mbom_node(mbom,level,mat_code,qty,parent=''):
    meta=MAT[mat_code]; row={'*MBOM版本号':VER,'*MBOM编码':mbom,'*物料编码':mat_code,'物料名称':meta['name'],'物料图号':meta['dwg'],'*物料版本':VER,'*物料类别':meta['category'],'制造类型':meta['make'],'数量':qty,'计量单位':meta['unit'],'*层级':level,'*序号':next_mbom(level),'物料阶段':STAGE}
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
    for r in [
        ('ROOT-ADMIN','公司','ADM-AERO','航空动力公司','航动公司'),('ADM-AERO','事业部','ADM-737BU','737发动机事业部','737事业部'),('ADM-737BU','工厂','ADM-PLANT','LEAP-1B总装工厂','LEAP工厂'),('ADM-PLANT','部门','ADM-MFG','制造部','制造部'),('ADM-PLANT','部门','ADM-ENG','工程技术部','工程部'),('ADM-PLANT','部门','ADM-QA','质量保证部','质量部'),('ADM-PLANT','部门','ADM-SCM','供应链部','供应链'),('ADM-PLANT','部门','ADM-DIGI','数字化制造部','数制部'),('ADM-PLANT','部门','ADM-EHS','试验与安环部','试安部'),('ADM-PLANT','部门','ADM-WM','仓储物流部','物流部')]: a_admin(*r)
    for r in [
        ('ROOT-BIZ','BIZ-AERO','航空动力业务组织','航空动力','公司','ADM-AERO','离散制造'),('BIZ-AERO','BIZ-737BU','737发动机事业部','737事业部','事业部','ADM-737BU',''),('BIZ-737BU','BIZ-LEAP-CENTER','LEAP-1B制造中心','LEAP中心','工厂','ADM-PLANT','离散制造'),('BIZ-LEAP-CENTER','BIZ-FAN','风扇与机匣车间','风扇车间','车间','ADM-MFG',''),('BIZ-LEAP-CENTER','BIZ-COMP','压气机车间','压气机','车间','ADM-MFG',''),('BIZ-LEAP-CENTER','BIZ-COMB','燃烧室车间','燃烧室','车间','ADM-MFG',''),('BIZ-LEAP-CENTER','BIZ-TURB','涡轮车间','涡轮车间','车间','ADM-MFG',''),('BIZ-LEAP-CENTER','BIZ-AGB','附件机匣车间','附件车间','车间','ADM-MFG',''),('BIZ-LEAP-CENTER','BIZ-FINAL','总装试车车间','总装试车','车间','ADM-EHS',''),('BIZ-LEAP-CENTER','BIZ-QUALITY','质量中心','质量中心','中心','ADM-QA',''),('BIZ-LEAP-CENTER','BIZ-WARE','仓储物流中心','仓储物流','中心','ADM-WM',''),('BIZ-LEAP-CENTER','BIZ-DIGI','数字化制造中心','数字化','中心','ADM-DIGI','')]: a_biz(*r)
    for r in [
        ('U-LEAP-001','张昊天','核心','男','ADM-737BU','BIZ-737BU','事业部总经理'),('U-LEAP-002','李景行','核心','男','ADM-MFG','BIZ-LEAP-CENTER','制造中心主任'),('U-LEAP-003','王若帆','核心','男','ADM-ENG','BIZ-LEAP-CENTER','工艺总师'),('U-LEAP-004','陈思远','核心','男','ADM-QA','BIZ-QUALITY','质量保证经理'),('U-LEAP-005','刘知行','重要','男','ADM-SCM','BIZ-LEAP-CENTER','供应链经理'),('U-LEAP-006','赵文昊','重要','男','ADM-DIGI','BIZ-DIGI','数字化制造平台主管'),('U-LEAP-007','黄嘉宁','重要','女','ADM-ENG','BIZ-FAN','复材工艺工程师'),('U-LEAP-008','周承泽','重要','男','ADM-ENG','BIZ-COMP','压气机工艺工程师'),('U-LEAP-009','吴雅雯','重要','女','ADM-QA','BIZ-QUALITY','质量工程师'),('U-LEAP-010','徐靖涵','重要','女','ADM-EHS','BIZ-FINAL','试车平台主管'),('U-LEAP-011','孙博文','重要','男','ADM-MFG','BIZ-FINAL','总装工程师'),('U-LEAP-012','马睿哲','一般','男','ADM-MFG','BIZ-FAN','风扇班组长'),('U-LEAP-013','朱彦霖','一般','男','ADM-MFG','BIZ-COMP','压气机班组长'),('U-LEAP-014','胡明轩','一般','男','ADM-MFG','BIZ-COMB','燃烧室班组长'),('U-LEAP-015','郭星宇','一般','男','ADM-MFG','BIZ-TURB','涡轮班组长'),('U-LEAP-016','何雨桐','重要','女','ADM-ENG','BIZ-AGB','控制系统工程师'),('U-LEAP-017','高成蹊','一般','男','ADM-WM','BIZ-WARE','物流计划工程师'),('U-LEAP-018','唐子墨','一般','男','ADM-MFG','BIZ-LEAP-CENTER','设备工程师'),('U-LEAP-019','程悦然','重要','女','ADM-QA','BIZ-QUALITY','无损检测工程师'),('U-LEAP-020','魏嘉树','一般','男','ADM-EHS','BIZ-FINAL','性能试车工程师')]: a_user(*r)

def seed_factory():
    for r in [('SUP-ALBANY','Albany航空复合材料公司','Albany'),('SUP-HEXCEL','Hexcel航空复材公司','Hexcel'),('SUP-CARPENTER','Carpenter高温合金公司','Carpenter'),('SUP-PCC','PCC精密铸件公司','PCC'),('SUP-COORSTEK','CoorsTek先进陶瓷公司','CoorsTek'),('SUP-SKF','SKF航空轴承公司','SKF'),('SUP-HONEYWELL','Honeywell航空系统公司','Honeywell'),('SUP-COLLINS','Collins宇航系统公司','Collins')]: a_sup(*r)
    for r in [('EQ-AFP-01','自动铺丝机','AFP-1600','BIZ-FAN',YES),('EQ-RTM-01','RTM成型固化单元','RTM-450','BIZ-FAN',YES),('EQ-AUTOCLAVE-01','复材高温固化釜','AC-550','BIZ-FAN',YES),('EQ-5AXIS-01','五轴叶片加工中心','MC-5X-1200','BIZ-FAN',NO),('EQ-EBW-01','电子束焊机','EBW-60','BIZ-COMB',NO),('EQ-LASER-01','激光打孔单元','LD-24','BIZ-COMB',NO),('EQ-HT-01','真空热处理炉','VHT-780','BIZ-TURB',YES),('EQ-BRAZE-01','真空钎焊炉','VB-900','BIZ-TURB',YES),('EQ-AM-01','金属增材制造设备','AM-280','BIZ-COMB',YES),('EQ-CMM-01','三坐标测量机','CMM-12','BIZ-QUALITY',NO),('EQ-CT-01','工业CT检测系统','CT-450','BIZ-QUALITY',YES),('EQ-FPI-01','荧光渗透检测线','FPI-300','BIZ-QUALITY',NO),('EQ-BAL-01','转子动平衡机','BAL-160','BIZ-TURB',YES),('EQ-COREASM-01','核心机装配台','ASM-CORE-01','BIZ-FINAL',YES),('EQ-FINALASM-01','整机总装吊装台','ASM-FINAL-01','BIZ-FINAL',YES),('EQ-COLDTEST-01','冷态试车台','TEST-COLD-01','BIZ-FINAL',NO),('EQ-HOTTEST-01','热态性能试车台','TEST-HOT-01','BIZ-FINAL',YES),('EQ-VIB-01','振动监测与校准台','VIB-600','BIZ-FINAL',NO)]: a_eq(*r)
    for r in [('TOOL-FAN-BLADE-LAYUP','复材风扇叶片铺层模具',CAT_KIT,MAKE_SELF,'成型模具','套',FEATURE_KEY),('TOOL-FAN-CASE-MOLD','风扇机匣成型模具',CAT_KIT,MAKE_SELF,'成型模具','套',FEATURE_KEY),('TOOL-HPC-ROTOR-FIX','高压压气机转子装配工装',CAT_KIT,MAKE_SELF,'装配工装','套',FEATURE_IMPORTANT),('TOOL-HPT-ASM-FIX','高压涡轮装配工装',CAT_KIT,MAKE_SELF,'装配工装','套',FEATURE_IMPORTANT),('TOOL-CORE-CART','核心机转运车',CAT_PART,MAKE_SELF,'转运工装','台',FEATURE_NORMAL),('TOOL-ENG-HOIST','整机吊装梁',CAT_PART,MAKE_SELF,'吊装工装','件',FEATURE_IMPORTANT)]: a_tool(*r)
    for r in [('WC-FAN-BLADE','风扇叶片制造中心','单元','复材制造','BIZ-FAN'),('WC-FAN-CASE','风扇机匣制造中心','单元','复材制造','BIZ-FAN'),('WC-FAN-MOD','风扇模块装配中心','单元','装配','BIZ-FAN'),('WC-LPC-MOD','低压压气机装配中心','单元','装配','BIZ-COMP'),('WC-HPC-MOD','高压压气机装配中心','单元','装配','BIZ-COMP'),('WC-COMB-MOD','燃烧室装配中心','单元','装配','BIZ-COMB'),('WC-HPT-MOD','高压涡轮装配中心','单元','装配','BIZ-TURB'),('WC-LPT-MOD','低压涡轮装配中心','单元','装配','BIZ-TURB'),('WC-AGB-MOD','附件机匣装配中心','单元','装配','BIZ-AGB'),('WC-CTRL-SYS','控制系统集成中心','单元','集成','BIZ-AGB'),('WC-CORE-ASM','核心机装配中心','单元','装配','BIZ-FINAL'),('WC-FINAL-ASM','整机总装中心','单元','装配','BIZ-FINAL'),('WC-TEST','性能试车中心','试车台','试验','BIZ-FINAL'),('WC-QUALITY','质量检测中心','中心','检测','BIZ-QUALITY')]: a_wc(*r)
    for r in [('WH-RM','原材料库','BIZ-WARE','ERP一级库'),('WH-CF','复材洁净库','BIZ-WARE','ERP一级库'),('WH-WIP','在制品库','BIZ-WARE','生产在制库'),('WH-FG','成品发动机库','BIZ-WARE','ERP成品库')]: a_wh(*r)
    for r in [('LOC-RM-A01','原材料区-A01','BIZ-WARE','WH-RM'),('LOC-RM-B01','原材料区-B01','BIZ-WARE','WH-RM'),('LOC-CF-A01','复材洁净区-A01','BIZ-WARE','WH-CF'),('LOC-CF-B01','复材洁净区-B01','BIZ-WARE','WH-CF'),('LOC-WIP-A01','模块在制区-A01','BIZ-WARE','WH-WIP'),('LOC-WIP-B01','模块在制区-B01','BIZ-WARE','WH-WIP'),('LOC-FG-A01','成品区-A01','BIZ-WARE','WH-FG'),('LOC-FG-B01','成品区-B01','BIZ-WARE','WH-FG')]: a_loc(*r)
    for r in [('EQ-AFP-01','U-LEAP-007'),('EQ-RTM-01','U-LEAP-007'),('EQ-AUTOCLAVE-01','U-LEAP-012'),('EQ-5AXIS-01','U-LEAP-012'),('EQ-EBW-01','U-LEAP-014'),('EQ-LASER-01','U-LEAP-014'),('EQ-HT-01','U-LEAP-015'),('EQ-BRAZE-01','U-LEAP-015'),('EQ-AM-01','U-LEAP-014'),('EQ-CMM-01','U-LEAP-009'),('EQ-CT-01','U-LEAP-019'),('EQ-FPI-01','U-LEAP-019'),('EQ-BAL-01','U-LEAP-015'),('EQ-COREASM-01','U-LEAP-011'),('EQ-FINALASM-01','U-LEAP-011'),('EQ-COLDTEST-01','U-LEAP-010'),('EQ-HOTTEST-01','U-LEAP-020'),('EQ-VIB-01','U-LEAP-020')]: l_eq_user(*r)
    for r in [('WC-FAN-BLADE','U-LEAP-007'),('WC-FAN-BLADE','U-LEAP-012'),('WC-FAN-CASE','U-LEAP-007'),('WC-FAN-MOD','U-LEAP-012'),('WC-LPC-MOD','U-LEAP-013'),('WC-HPC-MOD','U-LEAP-008'),('WC-HPC-MOD','U-LEAP-013'),('WC-COMB-MOD','U-LEAP-014'),('WC-HPT-MOD','U-LEAP-015'),('WC-LPT-MOD','U-LEAP-015'),('WC-AGB-MOD','U-LEAP-016'),('WC-CTRL-SYS','U-LEAP-016'),('WC-CTRL-SYS','U-LEAP-006'),('WC-CORE-ASM','U-LEAP-011'),('WC-FINAL-ASM','U-LEAP-002'),('WC-FINAL-ASM','U-LEAP-011'),('WC-TEST','U-LEAP-010'),('WC-TEST','U-LEAP-020'),('WC-QUALITY','U-LEAP-009'),('WC-QUALITY','U-LEAP-019')]: l_wc_user(*r)
    for r in [('WC-FAN-BLADE','SUP-ALBANY'),('WC-FAN-BLADE','SUP-HEXCEL'),('WC-FAN-CASE','SUP-HEXCEL'),('WC-LPC-MOD','SUP-SKF'),('WC-HPC-MOD','SUP-CARPENTER'),('WC-COMB-MOD','SUP-HONEYWELL'),('WC-COMB-MOD','SUP-CARPENTER'),('WC-HPT-MOD','SUP-PCC'),('WC-HPT-MOD','SUP-COORSTEK'),('WC-LPT-MOD','SUP-SKF'),('WC-AGB-MOD','SUP-COLLINS'),('WC-CTRL-SYS','SUP-HONEYWELL'),('WC-FINAL-ASM','SUP-COLLINS')]: l_wc_sup(*r)
    for r in [('WC-FAN-BLADE','EQ-AFP-01'),('WC-FAN-BLADE','EQ-RTM-01'),('WC-FAN-BLADE','EQ-5AXIS-01'),('WC-FAN-CASE','EQ-AUTOCLAVE-01'),('WC-COMB-MOD','EQ-EBW-01'),('WC-COMB-MOD','EQ-LASER-01'),('WC-COMB-MOD','EQ-AM-01'),('WC-HPT-MOD','EQ-HT-01'),('WC-HPT-MOD','EQ-BRAZE-01'),('WC-LPT-MOD','EQ-BAL-01'),('WC-QUALITY','EQ-CMM-01'),('WC-QUALITY','EQ-CT-01'),('WC-QUALITY','EQ-FPI-01'),('WC-CORE-ASM','EQ-COREASM-01'),('WC-FINAL-ASM','EQ-FINALASM-01'),('WC-TEST','EQ-COLDTEST-01'),('WC-TEST','EQ-HOTTEST-01'),('WC-TEST','EQ-VIB-01')]: l_wc_eq(*r)
def seed_materials():
    mats=[
        ('MAT-LEAP1B-ENG','LEAP-1B航空发动机总成',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-ENG','台'),('MAT-MOD-FAN','风扇模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-FAN','套'),('MAT-MOD-LPC','低压压气机模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-LPC','套'),('MAT-MOD-HPC','高压压气机模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-HPC','套'),('MAT-MOD-COMB','燃烧室模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-COMB','套'),('MAT-MOD-HPT','高压涡轮模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-HPT','套'),('MAT-MOD-LPT','低压涡轮模块',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-MOD-LPT','套'),('MAT-MOD-AGB','附件驱动机匣模块',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-MOD-AGB','套'),('MAT-MOD-CTRL','控制系统模块',CAT_KIT,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-MOD-CTRL','套'),('MAT-MOD-QEC','QEC快换安装包',CAT_KIT,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-MOD-QEC','套'),('MAT-MOD-IGN','点火起动模块',CAT_KIT,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-MOD-IGN','套'),
        ('MAT-FAN-BLADE-SET','3D编织复合材料风扇叶片组',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-FAN-BLD','套'),('MAT-FAN-CASE','复合材料风扇机匣',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-FAN-CASE','件'),('MAT-FAN-DISK','钛合金风扇盘',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-FAN-DISK','件'),('MAT-FAN-OGV','风扇出口导向叶片组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-FAN-OGV','套'),
        ('MAT-LPC-ROTOR','低压压气机转子组件',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-LPC-ROTOR','套'),('MAT-LPC-STATOR','低压压气机静子组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-LPC-STATOR','套'),('MAT-LPC-CASE','低压压气机机匣',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-LPC-CASE','件'),
        ('MAT-HPC-IBR1','高压压气机整体叶盘1级',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPC-IBR1','件'),('MAT-HPC-IBR2','高压压气机整体叶盘2级',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPC-IBR2','件'),('MAT-HPC-IBR3','高压压气机整体叶盘3级',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPC-IBR3','件'),('MAT-HPC-IBR4','高压压气机整体叶盘4级',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPC-IBR4','件'),('MAT-HPC-IBR5','高压压气机整体叶盘5级',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPC-IBR5','件'),('MAT-HPC-STATOR','高压压气机静子组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-HPC-STATOR','套'),('MAT-HPC-REAR-FRAME','高压压气机后机匣',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-HPC-RFRAME','件'),
        ('MAT-COMB-LINER-IN','燃烧室内衬',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-COMB-LINER-IN','件'),('MAT-COMB-LINER-OUT','燃烧室外衬',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-COMB-LINER-OUT','件'),('MAT-COMB-DOME','燃烧室穹顶组件',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-COMB-DOME','件'),('MAT-TAPS2-NOZZLE','TAPS II燃油喷嘴组件',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-TAPS2','套'),('MAT-COMB-CASE','燃烧室机匣',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-COMB-CASE','件'),
        ('MAT-HPT-NGV','高压涡轮导向叶片组件',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-HPT-NGV','套'),('MAT-HPT-ROTOR1','高压涡轮一级盘',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPT-ROTOR1','件'),('MAT-HPT-BLADE1','高压涡轮一级叶片组',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-HPT-BLADE1','套'),('MAT-HPT-ROTOR2','高压涡轮二级盘',CAT_PART,MAKE_SELF,FEATURE_KEY,'DWG-LEAP1B-HPT-ROTOR2','件'),('MAT-HPT-BLADE2','高压涡轮二级叶片组',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-HPT-BLADE2','套'),('MAT-CMC-SHROUD','CMC高压涡轮隔热罩组',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-CMC-SHROUD','套'),
        ('MAT-LPT-ROTOR-A','低压涡轮前级转子组件',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-LPT-ROTOR-A','套'),('MAT-LPT-ROTOR-B','低压涡轮中级转子组件',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-LPT-ROTOR-B','套'),('MAT-LPT-ROTOR-C','低压涡轮后级转子组件',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-LPT-ROTOR-C','套'),('MAT-LPT-CASE','低压涡轮机匣',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-LPT-CASE','件'),('MAT-LPT-EXH-FRAME','低压涡轮排气机架',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-LPT-EXH','件'),
        ('MAT-AGB-GEARBOX','附件齿轮箱',CAT_PART,MAKE_SELF,FEATURE_IMPORTANT,'DWG-LEAP1B-AGB-GBX','件'),('MAT-AGB-FUEL-PUMP','主燃油泵',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-AGB-FP','件'),('MAT-AGB-OIL-PUMP','滑油泵',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-AGB-OP','件'),('MAT-AGB-STARTER','起动机',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-AGB-STR','件'),('MAT-AGB-GENERATOR','发电机',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-AGB-GEN','件'),
        ('MAT-CTRL-FADEC','FADEC全权限数字控制器',CAT_PART,MAKE_BUY,FEATURE_KEY,'DWG-LEAP1B-CTRL-FADEC','件'),('MAT-CTRL-HARNESS','发动机线束组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-CTRL-HARNESS','套'),('MAT-CTRL-SENSOR-KIT','传感器套件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-CTRL-SENSOR','套'),('MAT-CTRL-ACTUATOR','执行机构套件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-CTRL-ACT','套'),
        ('MAT-QEC-MOUNT','发动机吊点组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-QEC-MOUNT','套'),('MAT-QEC-LINK','短舱连接件组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-QEC-LINK','套'),('MAT-QEC-TUBE','发动机管路包',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-QEC-TUBE','套'),('MAT-QEC-DUCT','发动机导管组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-QEC-DUCT','套'),('MAT-IGN-EXCITER','点火励磁器',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-IGN-EXCITER','件'),('MAT-IGN-IGNITER','点火器组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-IGN-IGNITER','套'),('MAT-IGN-CABLE','点火电缆组件',CAT_PART,MAKE_BUY,FEATURE_IMPORTANT,'DWG-LEAP1B-IGN-CABLE','套'),
        ('MAT-RAW-CF-PREFORM','复材预制体',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-CF-PREFORM','件'),('MAT-RAW-RTM-RESIN','RTM树脂',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-RTM-RESIN','千克'),('MAT-RAW-TI-FORGING','钛合金锻坯',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-TI-FORGING','件'),('MAT-RAW-NI-FORGING','镍基高温合金锻件',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-NI-FORGING','件'),('MAT-RAW-NI-POWDER','镍基高温合金粉末',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-NI-POWDER','千克'),('MAT-RAW-CMC-PREFORM','CMC坯料',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-CMC-PREFORM','件'),('MAT-RAW-SS-TUBE','不锈钢管材',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-SS-TUBE','米'),('MAT-RAW-FASTENER-KIT','航空紧固件包',CAT_RAW,MAKE_BUY,FEATURE_NORMAL,'MAT-RAW-FASTENER-KIT','套'),('MAT-RAW-BEARING-KIT','轴承与密封件包',CAT_RAW,MAKE_BUY,FEATURE_IMPORTANT,'MAT-RAW-BEARING-KIT','套'),('MAT-AUX-BRAZE','钎焊填料',CAT_AUX,MAKE_BUY,FEATURE_NORMAL,'MAT-AUX-BRAZE','千克'),('MAT-AUX-THERMAL-COATING','热障涂层材料',CAT_AUX,MAKE_BUY,FEATURE_NORMAL,'MAT-AUX-THERMAL-COATING','千克'),('MAT-AUX-SEALANT','高温密封剂',CAT_AUX,MAKE_BUY,FEATURE_NORMAL,'MAT-AUX-SEALANT','千克')]
    for r in mats: a_mat(*r)

def seed_mbom():
    a_mbom('MBOM-LEAP1B-A01','MAT-LEAP1B-ENG','LEAP-1B航空发动机总成MBOM')
    for code,qty in [('MAT-MOD-FAN',1),('MAT-MOD-LPC',1),('MAT-MOD-HPC',1),('MAT-MOD-COMB',1),('MAT-MOD-HPT',1),('MAT-MOD-LPT',1),('MAT-MOD-AGB',1),('MAT-MOD-CTRL',1),('MAT-MOD-QEC',1),('MAT-MOD-IGN',1)]: a_mbom_node('MBOM-LEAP1B-A01',1,code,qty,'MAT-LEAP1B-ENG')
    groups=[('MAT-MOD-FAN',[('MAT-FAN-BLADE-SET',1),('MAT-FAN-CASE',1),('MAT-FAN-DISK',1),('MAT-FAN-OGV',1)]),('MAT-MOD-LPC',[('MAT-LPC-ROTOR',1),('MAT-LPC-STATOR',1),('MAT-LPC-CASE',1)]),('MAT-MOD-HPC',[('MAT-HPC-IBR1',1),('MAT-HPC-IBR2',1),('MAT-HPC-IBR3',1),('MAT-HPC-IBR4',1),('MAT-HPC-IBR5',1),('MAT-HPC-STATOR',1),('MAT-HPC-REAR-FRAME',1)]),('MAT-MOD-COMB',[('MAT-COMB-LINER-IN',1),('MAT-COMB-LINER-OUT',1),('MAT-COMB-DOME',1),('MAT-TAPS2-NOZZLE',1),('MAT-COMB-CASE',1)]),('MAT-MOD-HPT',[('MAT-HPT-NGV',1),('MAT-HPT-ROTOR1',1),('MAT-HPT-BLADE1',1),('MAT-HPT-ROTOR2',1),('MAT-HPT-BLADE2',1),('MAT-CMC-SHROUD',1)]),('MAT-MOD-LPT',[('MAT-LPT-ROTOR-A',1),('MAT-LPT-ROTOR-B',1),('MAT-LPT-ROTOR-C',1),('MAT-LPT-CASE',1),('MAT-LPT-EXH-FRAME',1)]),('MAT-MOD-AGB',[('MAT-AGB-GEARBOX',1),('MAT-AGB-FUEL-PUMP',1),('MAT-AGB-OIL-PUMP',1),('MAT-AGB-STARTER',1),('MAT-AGB-GENERATOR',1)]),('MAT-MOD-CTRL',[('MAT-CTRL-FADEC',1),('MAT-CTRL-HARNESS',1),('MAT-CTRL-SENSOR-KIT',1),('MAT-CTRL-ACTUATOR',1)]),('MAT-MOD-QEC',[('MAT-QEC-MOUNT',1),('MAT-QEC-LINK',1),('MAT-QEC-TUBE',1),('MAT-QEC-DUCT',1)]),('MAT-MOD-IGN',[('MAT-IGN-EXCITER',1),('MAT-IGN-IGNITER',1),('MAT-IGN-CABLE',1)])]
    for parent,children in groups:
        for code,qty in children: a_mbom_node('MBOM-LEAP1B-A01',2,code,qty,parent)
    for parent,children in [('MAT-FAN-BLADE-SET',[('MAT-RAW-CF-PREFORM',18),('MAT-RAW-RTM-RESIN',12),('MAT-AUX-THERMAL-COATING',2)]),('MAT-FAN-CASE',[('MAT-RAW-CF-PREFORM',1),('MAT-RAW-RTM-RESIN',8),('MAT-RAW-FASTENER-KIT',1)]),('MAT-HPC-IBR1',[('MAT-RAW-TI-FORGING',1)]),('MAT-HPC-IBR2',[('MAT-RAW-TI-FORGING',1)]),('MAT-HPC-IBR3',[('MAT-RAW-TI-FORGING',1)]),('MAT-HPC-IBR4',[('MAT-RAW-TI-FORGING',1)]),('MAT-HPC-IBR5',[('MAT-RAW-TI-FORGING',1)]),('MAT-TAPS2-NOZZLE',[('MAT-RAW-NI-POWDER',6),('MAT-AUX-THERMAL-COATING',1)]),('MAT-HPT-ROTOR1',[('MAT-RAW-NI-FORGING',1)]),('MAT-HPT-ROTOR2',[('MAT-RAW-NI-FORGING',1)]),('MAT-CMC-SHROUD',[('MAT-RAW-CMC-PREFORM',1)]),('MAT-QEC-TUBE',[('MAT-RAW-SS-TUBE',12),('MAT-AUX-SEALANT',1)]),('MAT-AGB-GEARBOX',[('MAT-RAW-BEARING-KIT',1),('MAT-RAW-FASTENER-KIT',1)])]:
        for code,qty in children: a_mbom_node('MBOM-LEAP1B-A01',3,code,qty,parent)
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
        ('RT-FAN-BLADE-A01','复合材料风扇叶片组制造工艺','复材','BIZ-FAN','MAT-FAN-BLADE-SET',[
            ('0010','预制体铺层','加工','WC-FAN-BLADE',45,180,'复材制造专业',[('MAT-RAW-CF-PREFORM',18),('MAT-RAW-RTM-RESIN',6)],['模具准备','铺层装袋']),
            ('0020','RTM成型固化','加工','WC-FAN-BLADE',30,240,'复材制造专业',[('MAT-RAW-CF-PREFORM',18),('MAT-RAW-RTM-RESIN',6)],['装模灌注','固化冷却']),
            ('0030','五轴修整与表面处理','加工','WC-FAN-BLADE',20,90,'复材制造专业',[('MAT-AUX-THERMAL-COATING',1),('MAT-RAW-FASTENER-KIT',1)],['轮廓修整','表面处理']),
            ('0040','无损检测与分组选配','检验','WC-QUALITY',15,60,'检测专业',[('MAT-AUX-THERMAL-COATING',1)],['CT检测','分组选配'])]),
        ('RT-FAN-CASE-A01','复合材料风扇机匣制造工艺','复材','BIZ-FAN','MAT-FAN-CASE',[
            ('0010','机匣预制体缠绕','加工','WC-FAN-CASE',60,220,'复材制造专业',[('MAT-RAW-CF-PREFORM',1),('MAT-RAW-RTM-RESIN',4)],['预制体定位','缠绕铺放']),
            ('0020','树脂灌注固化','加工','WC-FAN-CASE',40,260,'复材制造专业',[('MAT-RAW-CF-PREFORM',1),('MAT-RAW-RTM-RESIN',4)],['灌注准备','固化定型']),
            ('0030','机匣机加与钻孔','加工','WC-FAN-CASE',30,120,'复材制造专业',[('MAT-RAW-FASTENER-KIT',1),('MAT-AUX-SEALANT',1)],['法兰加工','孔系加工']),
            ('0040','CT检测与防护涂覆','检验','WC-QUALITY',15,80,'检测专业',[('MAT-AUX-THERMAL-COATING',1)],['CT检测','涂覆放行'])]),
        ('RT-FAN-MOD-A01','风扇模块装配工艺','装配','BIZ-FAN','MAT-MOD-FAN',[
            ('0010','风扇盘与叶片装配','装配','WC-FAN-MOD',30,100,'装配专业',[('MAT-FAN-DISK',1),('MAT-FAN-BLADE-SET',1)],['盘件定位','叶片装入']),
            ('0020','机匣与导向叶片装配','装配','WC-FAN-MOD',30,90,'装配专业',[('MAT-FAN-CASE',1),('MAT-FAN-OGV',1)],['机匣定位','导向叶片装入']),
            ('0030','动平衡与间隙校准','检验','WC-FAN-MOD',20,70,'装配专业',[('MAT-AUX-SEALANT',1),('MAT-RAW-FASTENER-KIT',1)],['动平衡','间隙校准']),
            ('0040','模块检验放行','检验','WC-QUALITY',15,60,'检测专业',[('MAT-RAW-FASTENER-KIT',1),('MAT-AUX-SEALANT',1)],['尺寸复核','放行确认'])]),
        ('RT-LPC-MOD-A01','低压压气机模块装配工艺','装配','BIZ-COMP','MAT-MOD-LPC',[
            ('0010','转子预装与同轴检测','装配','WC-LPC-MOD',25,90,'装配专业',[('MAT-LPC-ROTOR',1),('MAT-RAW-BEARING-KIT',1)],['转子装配','同轴检测']),
            ('0020','静子与机匣装配','装配','WC-LPC-MOD',30,100,'装配专业',[('MAT-LPC-STATOR',1),('MAT-LPC-CASE',1)],['静子定位','机匣闭合']),
            ('0030','间隙校准与锁固','装配','WC-LPC-MOD',20,60,'装配专业',[('MAT-RAW-FASTENER-KIT',1),('MAT-AUX-SEALANT',1)],['间隙测量','扭矩锁固']),
            ('0040','模块检验放行','检验','WC-QUALITY',15,55,'检测专业',[('MAT-RAW-FASTENER-KIT',1)],['文件核对','放行确认'])]),
        ('RT-HPC-MOD-A01','高压压气机模块装配工艺','装配','BIZ-COMP','MAT-MOD-HPC',[
            ('0010','前级整体叶盘装配','装配','WC-HPC-MOD',35,110,'装配专业',[('MAT-HPC-IBR1',1),('MAT-HPC-IBR2',1)],['前级定位','堆叠装配']),
            ('0020','中级整体叶盘装配','装配','WC-HPC-MOD',35,110,'装配专业',[('MAT-HPC-IBR3',1),('MAT-HPC-IBR4',1)],['中级定位','夹紧测量']),
            ('0030','后级与静子机匣装配','装配','WC-HPC-MOD',40,120,'装配专业',[('MAT-HPC-IBR5',1),('MAT-HPC-STATOR',1)],['后级装配','静子装配']),
            ('0040','后机匣与通流复检','检验','WC-QUALITY',20,70,'检测专业',[('MAT-HPC-REAR-FRAME',1),('MAT-AUX-SEALANT',1)],['机匣确认','通流检测'])]),
        ('RT-COMB-MOD-A01','燃烧室模块装配工艺','装配','BIZ-COMB','MAT-MOD-COMB',[
            ('0010','TAPS II喷嘴复检与装入','装配','WC-COMB-MOD',25,80,'装配专业',[('MAT-TAPS2-NOZZLE',1),('MAT-AUX-THERMAL-COATING',1)],['喷嘴复检','喷嘴装入']),
            ('0020','穹顶与内衬装配','装配','WC-COMB-MOD',30,90,'装配专业',[('MAT-COMB-DOME',1),('MAT-COMB-LINER-IN',1)],['穹顶安装','内衬配合']),
            ('0030','外衬与机匣装配','装配','WC-COMB-MOD',30,100,'装配专业',[('MAT-COMB-LINER-OUT',1),('MAT-COMB-CASE',1)],['外衬装入','机匣闭合']),
            ('0040','模块泄漏检验','检验','WC-QUALITY',20,75,'检测专业',[('MAT-AUX-SEALANT',1),('MAT-RAW-FASTENER-KIT',1)],['密封加压','结果判定'])]),
        ('RT-HPT-MOD-A01','高压涡轮模块装配工艺','装配','BIZ-TURB','MAT-MOD-HPT',[
            ('0010','导向叶片与一级盘装配','装配','WC-HPT-MOD',35,100,'装配专业',[('MAT-HPT-NGV',1),('MAT-HPT-ROTOR1',1)],['导向叶片定位','一级盘装配']),
            ('0020','一级叶片与二级盘装配','装配','WC-HPT-MOD',35,110,'装配专业',[('MAT-HPT-BLADE1',1),('MAT-HPT-ROTOR2',1)],['一级叶片装入','二级盘装配']),
            ('0030','二级叶片与CMC隔热罩装配','装配','WC-HPT-MOD',40,120,'装配专业',[('MAT-HPT-BLADE2',1),('MAT-CMC-SHROUD',1)],['二级叶片装入','隔热罩安装']),
            ('0040','热端尺寸复检与放行','检验','WC-QUALITY',20,80,'检测专业',[('MAT-AUX-THERMAL-COATING',1),('MAT-RAW-FASTENER-KIT',1)],['关键尺寸复检','放行评审'])]),
        ('RT-LPT-MOD-A01','低压涡轮模块装配工艺','装配','BIZ-TURB','MAT-MOD-LPT',[
            ('0010','前级转子装配','装配','WC-LPT-MOD',30,100,'装配专业',[('MAT-LPT-ROTOR-A',1),('MAT-RAW-BEARING-KIT',1)],['转子定位','轴承装入']),
            ('0020','后级转子装配','装配','WC-LPT-MOD',30,100,'装配专业',[('MAT-LPT-ROTOR-B',1),('MAT-LPT-ROTOR-C',1)],['中级装配','后级装配']),
            ('0030','机匣与排气机架装配','装配','WC-LPT-MOD',35,110,'装配专业',[('MAT-LPT-CASE',1),('MAT-LPT-EXH-FRAME',1)],['机匣闭合','排气机架安装']),
            ('0040','动平衡复检与放行','检验','WC-QUALITY',20,70,'检测专业',[('MAT-RAW-FASTENER-KIT',1)],['复检平衡','放行确认'])]),
        ('RT-AGB-MOD-A01','附件机匣模块装配工艺','装配','BIZ-AGB','MAT-MOD-AGB',[
            ('0010','齿轮箱体与传动系装配','装配','WC-AGB-MOD',30,90,'装配专业',[('MAT-AGB-GEARBOX',1),('MAT-RAW-BEARING-KIT',1)],['齿轮箱定位','传动系装配']),
            ('0020','燃油与滑油附件装配','装配','WC-AGB-MOD',25,80,'装配专业',[('MAT-AGB-FUEL-PUMP',1),('MAT-AGB-OIL-PUMP',1)],['燃油泵安装','滑油泵安装']),
            ('0030','起动发电附件装配','装配','WC-AGB-MOD',25,80,'装配专业',[('MAT-AGB-STARTER',1),('MAT-AGB-GENERATOR',1)],['起动机装配','发电机装配']),
            ('0040','台架检验与封存','检验','WC-QUALITY',20,60,'检测专业',[('MAT-RAW-FASTENER-KIT',1),('MAT-AUX-SEALANT',1)],['台架校验','封存放行'])]),
        ('RT-CTRL-MOD-A01','控制系统集成工艺','集成','BIZ-AGB','MAT-MOD-CTRL',[
            ('0010','FADEC安装','装配','WC-CTRL-SYS',20,60,'控制集成专业',[('MAT-CTRL-FADEC',1),('MAT-CTRL-HARNESS',1)],['控制器安装','主线束布设']),
            ('0020','传感器与执行机构接入','装配','WC-CTRL-SYS',25,70,'控制集成专业',[('MAT-CTRL-SENSOR-KIT',1),('MAT-CTRL-ACTUATOR',1)],['传感器接入','执行机构接入']),
            ('0030','线束导通与绝缘检验','检验','WC-CTRL-SYS',20,50,'控制集成专业',[('MAT-CTRL-HARNESS',1),('MAT-AUX-SEALANT',1)],['导通测试','绝缘检测']),
            ('0040','软件参数装载与放行','检验','WC-QUALITY',15,45,'检测专业',[('MAT-CTRL-FADEC',1)],['参数装载','集成放行'])]),
        ('RT-ENG-FINAL-A01','LEAP-1B整机总装工艺','总装','BIZ-FINAL','MAT-LEAP1B-ENG',[
            ('0010','核心机装配','装配','WC-CORE-ASM',40,160,'总装专业',[('MAT-MOD-LPC',1),('MAT-MOD-HPC',1)],['模块对接','核心测量']),
            ('0020','燃烧与涡轮模块对接','装配','WC-CORE-ASM',45,180,'总装专业',[('MAT-MOD-COMB',1),('MAT-MOD-HPT',1),('MAT-MOD-LPT',1)],['热端对接','低压系统闭合']),
            ('0030','风扇与附件系统集成','装配','WC-FINAL-ASM',40,150,'总装专业',[('MAT-MOD-FAN',1),('MAT-MOD-AGB',1)],['风扇模块装入','附件系统连接']),
            ('0040','控制QEC点火系统集成','装配','WC-FINAL-ASM',35,140,'总装专业',[('MAT-MOD-CTRL',1),('MAT-MOD-QEC',1),('MAT-MOD-IGN',1)],['控制系统接入','QEC点火集成'])]),
        ('RT-ENG-TEST-A01','LEAP-1B整机性能试车工艺','试验','BIZ-FINAL','MAT-LEAP1B-ENG',[
            ('0010','冷态联检与通电','试验','WC-TEST',30,70,'试验专业',[('MAT-LEAP1B-ENG',1)],['冷态联检','通电盘车']),
            ('0020','控制系统校验','试验','WC-TEST',20,50,'试验专业',[('MAT-LEAP1B-ENG',1)],['参数核对','告警校验']),
            ('0030','热态性能试车','试验','WC-TEST',25,120,'试验专业',[('MAT-LEAP1B-ENG',1)],['工况拉升','性能采集']),
            ('0040','振动分析与放行复核','检验','WC-QUALITY',20,60,'检测专业',[('MAT-LEAP1B-ENG',1)],['振动分析','放行复核'])])]
    for r in routes: make_route(*r)



def normalize_seed():
    normalize_seed_safe()

def build_variant(namespace: str, volume_profile: str | None = None) -> dict:
    reset()
    seed_system(); seed_factory(); seed_materials(); seed_mbom(); seed_routes(); normalize_seed_safe(); apply_profile(seed, 'boeing_737_leap1b'); apply_scene_upgrade(seed, 'boeing_737_leap1b', namespace, volume_profile=volume_profile); apply_production_orders(seed, 'boeing_737_leap1b', namespace)
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


def normalize_seed_safe():
    PARENT='*\u7236\u7ec4\u7ec7\u7f16\u7801'
    BIZ_TYPE='\u5de5\u5382\u7ec4\u7ec7\u7c7b\u578b'
    FACTORY_TYPE='\u5de5\u5382\u7c7b\u578b'
    UNIT='\u8ba1\u91cf\u5355\u4f4d'
    TOOL_CAT='\u5de5\u88c5\u7c7b\u522b'
    WC_TYPE='*\u7c7b\u578b'
    WC_CLASS='*\u5206\u7c7b'
    ROUTE_SPEC='\u5de5\u827a\u4e13\u4e1a'
    OP_TYPE='*\u5de5\u5e8f\u7c7b\u578b'
    OP_SPEC='\u5de5\u5e8f\u4e13\u4e1a\u7c7b\u578b'
    PROC_SPEC='\u5e8f\u4e13\u4e1a\u7c7b\u578b'
    WC_CODE='*\u5de5\u4f5c\u4e2d\u5fc3\u7f16\u7801'
    CODE='*\u7f16\u7801'
    NAME='*\u540d\u79f0'
    def clean_rows(rows):
        for row in rows:
            for key in list(row.keys()):
                if '?' in str(key):
                    row.pop(key, None)
    for wb in seed['workbooks'].values():
        for rows in wb.values():
            clean_rows(rows)
    seed['external_references']=['0']
    for row in seed['workbooks'][WB_SYSTEM][SH_ADMIN]:
        if row.get(PARENT) in {'ROOT-ADMIN','ROOT-BIZ'}:
            row[PARENT]='0'
        if row.get('\u884c\u653f\u7ec4\u7ec7\u7c7b\u578b') == '\u4e8b\u4e1a\u90e8':
            row['\u884c\u653f\u7ec4\u7ec7\u7c7b\u578b']='\u90e8\u95e8'
    biz_factory_map={
        'BIZ-FAN':'\u673a\u68b0\u52a0\u5de5\u4e13\u4e1a',
        'BIZ-COMP':'\u673a\u68b0\u52a0\u5de5\u4e13\u4e1a',
        'BIZ-COMB':'\u88c5\u914d\u4e13\u4e1a',
        'BIZ-TURB':'\u88c5\u914d\u4e13\u4e1a',
        'BIZ-AGB':'\u88c5\u914d\u4e13\u4e1a',
        'BIZ-FINAL':'\u88c5\u914d\u4e13\u4e1a',
    }
    biz_type_map={'\u4e8b\u4e1a\u90e8':'\u90e8\u95e8','\u4e2d\u5fc3':'\u90e8\u95e8'}
    for row in seed['workbooks'][WB_SYSTEM][SH_BIZ]:
        if row.get(PARENT) in {'ROOT-ADMIN','ROOT-BIZ'}:
            row[PARENT]='0'
        row[BIZ_TYPE]=biz_type_map.get(row.get(BIZ_TYPE), row.get(BIZ_TYPE))
        code=row.get(CODE,'')
        if code in biz_factory_map:
            row[FACTORY_TYPE]=biz_factory_map[code]
        elif row.get(FACTORY_TYPE) not in {'\u673a\u68b0\u52a0\u5de5\u4e13\u4e1a','\u88c5\u914d\u4e13\u4e1a'}:
            row.pop(FACTORY_TYPE, None)
    for row in seed['workbooks'][WB_FACTORY][SH_TOOL]:
        row[UNIT]='\u4e2a'
        if row.get(TOOL_CAT) not in {'\u4e13\u7528\u5de5\u88c5','\u901a\u7528\u5de5\u5177','\u5de5\u88c5\u5907\u4ef6'}:
            row[TOOL_CAT]='\u4e13\u7528\u5de5\u88c5'
    for row in seed['workbooks'][WB_PRODUCT][SH_MAT]:
        row[UNIT]='\u4e2a'
    for row in seed['workbooks'][WB_PRODUCT][SH_MBOM_NODE]:
        row[UNIT]='\u4e2a'
    for row in seed['workbooks'][WB_FACTORY][SH_WH]:
        biz_type=row.get('*\u4e1a\u52a1\u7c7b\u578b')
        if biz_type == '\u751f\u4ea7\u5728\u5236\u5e93':
            row['*\u4e1a\u52a1\u7c7b\u578b']='\u8f66\u95f4\u4e8c\u7ea7\u5e93'
        elif biz_type == 'ERP\u6210\u54c1\u5e93':
            row['*\u4e1a\u52a1\u7c7b\u578b']='ERP\u4e00\u7ea7\u5e93'
    for row in seed['workbooks'][WB_FACTORY][SH_WC]:
        row[WC_TYPE]='\u7ec4\u7ec7'
        row[WC_CLASS]='\u68c0\u9a8c' if row.get(CODE)=='WC-QUALITY' else '\u52a0\u5de5'
    route_spec_map={
        '\u590d\u6750':'\u673a\u52a0',
        '\u96c6\u6210':'\u88c5\u914d',
        '\u603b\u88c5':'\u88c5\u914d',
        '\u8bd5\u9a8c':'\u901a\u7528'
    }
    assembly_wcs={'WC-FAN-MOD','WC-LPC-MOD','WC-HPC-MOD','WC-COMB-MOD','WC-HPT-MOD','WC-LPT-MOD','WC-AGB-MOD','WC-CTRL-SYS','WC-CORE-ASM','WC-FINAL-ASM'}
    for row in seed['workbooks'][WB_PRODUCT][SH_ROUTE]:
        spec=row.get(ROUTE_SPEC,'')
        row[ROUTE_SPEC]=route_spec_map.get(spec, spec if spec in {'\u673a\u52a0','\u88c5\u914d','\u70ed\u8868','\u94f8\u9020','\u94a3\u710a','\u953b\u9020','\u901a\u7528'} else '\u901a\u7528')
    for row in seed['workbooks'][WB_PRODUCT][SH_OP]:
        wc=row.get(WC_CODE,'')
        if row.get(OP_TYPE) not in {'\u52a0\u5de5','\u68c0\u9a8c','\u5382\u9645\u8f6c\u5de5','\u5382\u5185\u8f6c\u5de5','\u5916\u59d4'}:
            row[OP_TYPE]='\u68c0\u9a8c' if '\u68c0' in row.get(NAME,'') else '\u52a0\u5de5'
        row[OP_SPEC]='\u88c5\u914d\u4e13\u4e1a' if wc in assembly_wcs else '\u673a\u68b0\u52a0\u5de5\u4e13\u4e1a'
    for row in seed['workbooks'][WB_FACTORY][SH_PLIB]:
        wc=row.get(WC_CODE,'')
        if row.get(OP_TYPE) not in {'\u52a0\u5de5','\u68c0\u9a8c','\u5382\u9645\u8f6c\u5de5','\u5382\u5185\u8f6c\u5de5','\u5916\u59d4'}:
            row[OP_TYPE]='\u68c0\u9a8c' if '\u68c0' in row.get(NAME,'') else '\u52a0\u5de5'
        row[PROC_SPEC]='\u88c5\u914d\u4e13\u4e1a' if wc in assembly_wcs else '\u673a\u68b0\u52a0\u5de5\u4e13\u4e1a'

if __name__=='__main__': main()
