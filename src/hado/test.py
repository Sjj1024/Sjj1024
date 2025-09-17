from ascript.ios.node import Selector
from ascript.ios import system
from ascript.ios import action
from threading import Thread
import time

# 存储问题和答案的字典
topic_list = {
    '根据《中华人民共和国爱国主义教育法》，中国人民解放军、中国人民武装警察部队依照本法和中央军事委员会的有关规定开展爱国主义教育工作，并充分利用自身资源面向（\xa0 ）开展爱国主义教育。': [
        '社会'
    ],
    '根据《中华人民共和国爱国主义教育法》，网络信息服务（\xa0 ）应当加强网络爱国主义教育内容建设，制作、传播体现爱国主义精神的网络信息和作品，开发、运用新平台新技术新产品，生动开展网上爱国主义教育活动。': [
        '提供者',
    ],
    '根据《中华人民共和国爱国主义教育法》，县级以上人民政府文化和旅游、住房城乡建设、文物等部门应当加强对（\xa0 ）等历史文化遗产的保护和利用，发掘所蕴含的爱国主义精神，推进文化和旅游深度融合发展，引导公民在游览观光中领略壮美河山，感受悠久历史和灿烂文化，激发爱国热情。 ①文物古迹②传统村落③传统技艺④文化遗存': [
        '①②③'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家（\xa0 ）企业事业单位、社会组织和公民依法开展爱国主义教育活动。': [
        '鼓励和支持',
    ],
    '根据《中华人民共和国爱国主义教育法》，国家鼓励和支持创作爱国主义题材的文学、影视、音乐、舞蹈、戏剧、美术、书法等文艺作品，在优秀文艺作品评选、表彰、展览、展演时突出（\xa0 ）导向。': [
        '爱国主义',
    ],
    '根据《中华人民共和国爱国主义教育法》，爱国主义教育应当坚持传承和发展中华优秀传统文化，弘扬社会主义核心价值观，推进中国特色社会主义文化建设，坚定文化自信，建设（\xa0 ）。': [
        '中华民族现代文明',
    ],
    '根据《中华人民共和国爱国主义教育法》，工会、共产主义青年团、妇女联合会、工商业联合会、文学艺术界联合会、作家协会、科学技术协会、归国华侨联合会、台湾同胞联谊会、残疾人联合会、青年联合会和其他群团组织，应当发挥各自优势，面向（\xa0 ）开展爱国主义教育。': [
        '所联系的领域和群体',
    ],
    '根据《中华人民共和国爱国主义教育法》，祖国的壮美河山和历史文化遗产是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，依法（\xa0 ）宪法宣誓、军人和预备役人员服役宣誓等仪式时，应当在宣誓场所悬挂国旗、奏唱国歌，誓词应当体现爱国主义精神。': [
        '公开举行',
    ],
    '根据《中华人民共和国爱国主义教育法》，任何公民和组织都应当弘扬爱国主义精神，自觉维护国家安全、荣誉和利益，不得有侮辱国旗、国歌、国徽或者其他有损国旗、国歌、国徽尊严的行为。这一表述是否正确？（\xa0 ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，国家鼓励和支持（\xa0 ）开展爱国主义教育，增强宗教教职人员和信教群众的国家意识、公民意识、法治意识和爱国情感，引导宗教与社会主义社会相适应。 ①宗教团体②宗教院校③宗教活动场所': [
        '①②③',
    ],
    '根据《中华人民共和国爱国主义教育法》，县级以上人民政府应当加强对（\xa0 ）的保护、管理和利用，发掘具有历史价值、纪念意义的红色资源，推动红色旅游融合发展示范区建设，发挥红色资源教育功能，传承爱国主义精神。': [
        '红色资源'
    ],
    '根据《中华人民共和国爱国主义教育法》，各级各类学校应当将爱国主义教育贯穿（\xa0 ）全过程，办好、讲好思想政治理论课，并将爱国主义教育内容融入各类学科和教材中。': [
        '学校教育',
    ],
    '根据《中华人民共和国爱国主义教育法》，组织举办（\xa0 ），应当依法举行庄严、隆重的升挂国旗、奏唱国歌仪式。 ①重大庆祝②纪念活动③大型文化体育活动④展览会': [
        '①②③④'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家支持开展爱国主义教育理论研究，加强（\xa0 ）专业人才的教育和培训。': [
        '多层次'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家机关应当加强对公职人员的爱国主义教育，发挥公职人员在忠于国家、为国奉献，维护国家统一、促进民族团结，维护国家安全、荣誉和利益方面的（\xa0 ）作用。': [
        '模范带头'
    ],
    '根据《中华人民共和国爱国主义教育法》，任何公民和组织都应当弘扬爱国主义精神，自觉维护国家安全、荣誉和利益，不得侵占、破坏、污损爱国主义教育设施。这一表述是否正确？（\xa0 ）': [
        '正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，在每年10月1日中华人民共和国国庆日，国家和社会各方面举行多种形式的庆祝活动，集中开展爱国主义教育。这一表述是否正确？（\xa0 ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，国家采取多种形式开展（\xa0 ），增强公民的法治意识、国家安全和国防观念，引导公民自觉履行维护国家统一和民族团结，维护国家安全、荣誉和利益的义务。①法治宣传教育②国家安全和国防教育③思想品德教育': [
        'B．①②'
    ],
    '根据《中华人民共和国爱国主义教育法》，在（\xa0 ）及其他重要节日，组织开展各具特色的民俗文化活动、纪念庆祝活动，增进家国情怀。 ①春节②元宵节③清明节④端午节⑤中秋节⑥元旦⑦国际妇女节⑧国际劳动节⑨青年节⑩国际儿童节⑪中国农民丰收节': [
        '①②③④⑤⑥⑦⑧⑨⑩⑪',
    ],
    '根据《中华人民共和国爱国主义教育法》，任何公民和组织都应当弘扬爱国主义精神，自觉维护国家安全、荣誉和利益，可以适当宣扬、美化、否认侵略战争、侵略行为和屠杀惨案。这一表述是否正确？（\xa0 ）': [
        '不正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，为了加强新时代爱国主义教育，（\xa0 ），凝聚全面建设社会主义现代化国家、全面推进中华民族伟大复兴的磅礴力量，根据宪法，制定本法。': [
        '传承和弘扬爱国主义精神',
    ],
    '根据《中华人民共和国爱国主义教育法》，国旗、国歌、国徽等国家象征和标志是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，爱国主义教育应当坚持（\xa0 ）。 ①思想引领、文化涵育②教育引导、实践养成③主题鲜明、融入日常④因地制宜、注重实效': [
        '①②③④',
    ],
    '根据《中华人民共和国爱国主义教育法》，国家开展铸牢中华民族共同体意识教育，促进各民族交往交流交融，增进对伟大祖国、中华民族、中华文化、中国共产党、中国特色社会主义的认同，构筑中华民族共有（\xa0 ）。': [
        '精神家园'
    ],
    '《中华人民共和国爱国主义教育法》自2024年（\xa0 ）起施行。': [
        '45292'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家在（\xa0 ）中开展爱国主义教育，培育和增进对中华民族和伟大祖国的情感，传承民族精神、增强国家观念，壮大和团结一切爱国力量，使爱国主义成为全体人民的坚定信念、精神力量和自觉行动。': [
        '全体人民'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家通过（\xa0 ）表彰制度，褒奖在强国建设、民族复兴中做出突出贡献的人士，弘扬以爱国主义为核心的民族精神和以改革创新为核心的时代精神。': [
        '功勋荣誉',
    ],
    '根据《中华人民共和国爱国主义教育法》，未成年人的父母或者其他监护人应当把热爱祖国融入家庭教育，支持、配合学校开展爱国主义教育教学活动，引导、鼓励未成年人参加爱国主义教育（\xa0 ）。': [
        '社会活动'
    ],
    '根据《中华人民共和国爱国主义教育法》，中国是世界上历史最悠久的国家之一，中国各族人民共同创造了光辉灿烂的文化、共同缔造了（\xa0 ）的多民族国家。': [
        '统一',
    ],
    '根据《中华人民共和国爱国主义教育法》，中国特色社会主义制度，中国共产党带领人民团结奋斗的重大成就、历史经验和生动实践是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，国家加强与海外侨胞的交流，做好（\xa0 ）和服务工作，增进海外侨胞爱国情怀，弘扬爱国传统。': [
        '权益保障'
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）等应当创新宣传报道方式，通过制作、播放、刊登爱国主义题材的优秀作品，开设专题专栏，加强新闻报道，发布公益广告等方式，生动讲好爱国故事，弘扬爱国主义精神。 ①广播电台②电视台③报刊出版单位④网站': [
        '①②③'
    ],
    '根据《中华人民共和国爱国主义教育法》，地方爱国主义教育主管部门负责本地区爱国主义教育工作的指导、监督和（\xa0 ）。': [
        '统筹协调',
    ],
    '根据《中华人民共和国爱国主义教育法》，未成年人的父母或者其他监护人应当把热爱祖国融入（\xa0 ），支持、配合学校开展爱国主义教育教学活动，引导、鼓励未成年人参加爱国主义教育社会活动。': [
        '家庭教育',
    ],
    '根据《中华人民共和国爱国主义教育法》，组织举办重大庆祝、纪念活动和大型文化体育活动、展览会，应当依法举行庄严、隆重的升挂国旗、奏唱（\xa0 ）仪式。': [
        '国歌'
    ],
    '根据《中华人民共和国爱国主义教育法》，县级以上地方文化和旅游、新闻出版、广播电视、电影、网信、文物等部门和其他有关部门应当在各自职责范围内，开展爱国主义教育工作。这一表述是否正确？（\xa0 ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，企业事业单位应当将爱国主义教育列入本单位教育计划，大力弘扬（\xa0 ），结合经营管理、业务培训、文化体育等活动，开展爱国主义教育。 ①劳模精神②劳动精神③工匠精神': [
        '①②③'
    ],
    '根据《中华人民共和国爱国主义教育法》，中央和省级爱国主义教育主管部门应当加强对爱国主义教育工作的统筹，指导推动有关部门和单位创新爱国主义（\xa0 ），充分利用各类爱国主义教育资源和平台载体，推进爱国主义教育有效实施。': [
        '教育方式'
    ],
    '根据《中华人民共和国爱国主义教育法》，中央爱国主义教育主管部门建立健全爱国主义教育基地的（\xa0 ）制度，制定爱国主义教育基地保护利用规划，加强对爱国主义教育基地保护、管理、利用的指导和监督。': [
        '认定、保护、管理',
    ],
    '根据《中华人民共和国爱国主义教育法》，基层人民政府和基层群众性自治组织应当把爱国主义教育融入社会主义精神文明建设活动，在市民公约、村规民约中体现爱国主义精神，鼓励和支持开展以爱国主义为主题的（\xa0 ）文化、体育等活动。': [
        '群众性'
    ],
    '根据《中华人民共和国爱国主义教育法》，教育、科技、文化、卫生、体育等事业单位应当大力弘扬科学家精神和专业精神，宣传和培育知识分子、专业技术人员、运动员等（\xa0 ）的爱国情感和爱国行为。 ①胸怀祖国②服务人民③为国争光': [
        '①②③',
    ],
    '根据《中华人民共和国爱国主义教育法》，中华优秀传统文化、革命文化、社会主义先进文化是爱国主义教育的主要内容，这一表述是否正确？（ ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，中国共产党史、新中国史、改革开放史、社会主义发展史、中华民族发展史是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）应当加强对公职人员的爱国主义教育，发挥公职人员在忠于国家、为国奉献，维护国家统一、促进民族团结，维护国家安全、荣誉和利益方面的模范带头作用。': [
        '国家机关',
    ],
    '根据《中华人民共和国爱国主义教育法》，马克思列宁主义、毛泽东思想、邓小平理论、“三个代表”重要思想、科学发展观、习近平新时代中国特色社会主义思想是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确',
    ],
    '根据《中华人民共和国爱国主义教育法》，依法公开举行宪法宣誓、军人和预备役人员服役宣誓等仪式时，应当在宣誓场所悬挂（\xa0 ）、奏唱国歌，誓词应当体现爱国主义精神。': [
        '国旗',
    ],
    '根据《中华人民共和国爱国主义教育法》，爱国主义教育坚持中国共产党的领导，健全（\xa0 ）的工作格局。 ①统一领导②齐抓共管③各方参与④共同推进': [
        '①②③④'
    ],
    '根据《中华人民共和国爱国主义教育法》，中央和国家机关各部门在各自（\xa0 ）范围内，组织开展爱国主义教育工作。': [
        '职责'
    ],
    '根据《中华人民共和国爱国主义教育法》，基层人民政府和基层群众性自治组织应当把爱国主义教育融入（\xa0 ）活动，在市民公约、村规民约中体现爱国主义精神，鼓励和支持开展以爱国主义为主题的群众性文化、体育等活动。': [
        '社会主义精神文明建设',
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）应当加强内容建设，丰富展览展示方式，打造精品陈列，为国家机关、企业事业单位、社会组织、公民开展爱国主义教育活动和参观学习提供便利服务，发挥爱国主义教育功能。': [
        '爱国主义教育基地',
    ],
    '根据《中华人民共和国爱国主义教育法》，各级各类学校应当将课堂教学与课外实践和体验相结合，把爱国主义教育内容融入（\xa0 ）和学校各类主题活动，组织学生参观爱国主义教育基地等场馆设施，参加爱国主义教育校外实践活动。': [
        '校园文化建设'
    ],
    '根据《中华人民共和国爱国主义教育法》，在（\xa0 ）和其他重要纪念日，县级以上人民政府应当组织开展纪念活动，举行敬献花篮、瞻仰纪念设施、祭扫烈士墓、公祭等纪念仪式。 ①中国人民抗日战争胜利纪念日②烈士纪念日③南京大屠杀死难者国家公祭日④世界反法西斯胜利纪念日': [
        '①②③'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家采取多种形式开展法治宣传教育、国家安全和国防教育，增强公民的法治意识、国家安全和国防观念，引导公民自觉履行维护国家统一和民族团结，维护国家安全、荣誉和利益的（\xa0 ）。': [
        '义务',
    ],
    '根据《中华人民共和国爱国主义教育法》，行业协会商会等社会团体应当把爱国主义精神体现在团体章程、行业规范中，根据本团体本行业特点开展爱国主义教育，培育会员的爱国热情和社会担当，发挥会员中（\xa0 ）和有社会影响力人士的示范作用。': [
        '公众人物',
    ],
    '根据《中华人民共和国爱国主义教育法》，各级各类学校和其他教育机构应当按照国家规定建立爱国主义教育相关课程（ ）机制，针对各年龄段学生特点，确定爱国主义教育的重点内容，采取丰富适宜的教学方式，增强爱国主义教育的针对性、系统性和亲和力、感染力。': [
        '联动',
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）负责全国爱国主义教育工作的指导、监督和统筹协调。': [
        '中央爱国主义教育主管部门'
    ],
    '根据《中华人民共和国爱国主义教育法》，对在爱国主义教育工作中做出突出贡献的单位和个人，按照国家有关规定给予（\xa0 ）。': [
        '表彰和奖励'
    ],
    '根据《中华人民共和国爱国主义教育法》，英雄烈士和先进模范人物的事迹及体现的民族精神、时代精神是爱国主义教育的主要内容，这一表述是否正确？（\xa0 ）': [
        '正确'
    ],
    '根据《中华人民共和国爱国主义教育法》，国家将爱国主义教育纳入（\xa0 ）。': [
        '国民教育体系',
    ],
    '根据《中华人民共和国爱国主义教育法》，广播电台、电视台、报刊出版单位等应当创新宣传报道方式，通过制作、播放、刊登爱国主义题材的优秀作品，开设专题专栏，加强新闻报道，发布公益广告等方式，（\xa0 ），弘扬爱国主义精神。': [
        '生动讲好爱国故事',
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）爱国主义教育主管部门应当加强对爱国主义教育工作的统筹，指导推动有关部门和单位创新爱国主义教育方式，充分利用各类爱国主义教育资源和平台载体，推进爱国主义教育有效实施。': [
        '中央和省级',
    ],
    '根据《中华人民共和国爱国主义教育法》，爱国主义教育应当把弘扬爱国主义精神与扩大对外开放结合起来，坚持（\xa0 ），尊重各国历史特点和文化传统，借鉴吸收人类一切优秀文明成果。': [
        '理性、包容、开放'
    ],
    '根据《中华人民共和国爱国主义教育法》，（\xa0 ）以上地方人民政府教育行政部门应当加强对学校爱国主义教育的组织、协调、指导和监督。': [
        '县级'
    ]
}

# 统计次数
total_count = 0
count_dict = {
    'title': "",
}


# 找到按钮并点击
def find_and_click(label: str):
    count = 0
    while True:
        print(f"等待label:{label}....")
        know_btn = Selector().xpath(f"//*[@name='{label}']").find()
        if count < 3:
            count += 1
            if know_btn:
                know_btn.click()
                time.sleep(2)
                return True
        else:
            return False
        return False


def index_and_click(index: int):
    count = 0
    while True:
        print(f"等待index:{index}....")
        know_btn = Selector().index(index).find()
        if count < 3:
            count += 1
            if know_btn:
                print("找到了:", index)
                know_btn.click()
                time.sleep(2)
                return True
        else:
            print("没有找到:", index)
            return False


def xy_and_click(x: int, y: int):
    count = 0
    while True:
        print(f"等待xy:{x}{y}....")
        know_btn = Selector().x(x).y(y).find()
        if count < 3:
            count += 1
            if know_btn:
                print("找到了xy: ", x, y)
                know_btn.click()
                time.sleep(2)
                return True
        else:
            print("没有找xy:", x, y)
            return False


def count_func(key):
    print("统计次数")
    global total_count
    global count_dict
    if count_dict.get("title") == key:
        print("不统计")
    else:
        print("统计一次")
        count_dict["title"] = key
        total_count += 1


def wait_label(label):
    while True:
        print(f"等待:{label}....")
        know_btn = Selector().xpath(f"//*[@name='{label}']").find()
        if know_btn:
            know_btn.click()
            break
        else:
            time.sleep(3)


def open_huzhijiao():
    # 音量调至最低
    # action.key_press(action.KEY_VOLUMDOWN)
    # action.key_press(action.KEY_VOLUMDOWN)
    # action.key_press(action.KEY_VOLUMDOWN)
    # action.key_press(action.KEY_VOLUMDOWN)
    action.key_press(action.KEY_volumedown)
    # time.sleep(2)
    # 根据包名启动,推荐使用
    system.app_start(bundle_id="com.tencent.xin")
    time.sleep(2)
    # 执行沪智慧矫正
    action_huzhijiao()


def action_huzhijiao():
    # 点击我的
    to_see = Selector().xpath("//*[@name='我的']").find()
    if to_see:
        to_see.click()
        time.sleep(2)
    # 点击可选任务
    node = Selector().xpath("//*[@name='可选任务']").find()
    if node:
        # 找到了控件
        print("找到了可选任务")
        # 打印控件属性,比较耗时
        node.click()
        time.sleep(2)
        # 去做题
        try:
            do_work("去答题")
        except Exception as e:
            print("do_work error:", e)
        print("do_work 去答题 done")
        # 去闯关
        # chuang_guan()
        try:
            do_work("去闯关")
        except Exception as e:
            print("do_work error:", e)
        print("do_work 去闯关 done")
        # 看视频
        try:
            see_movide()
        except Exception as e:
            print("see_movide error:", e)
        print("see_movide done")
        # 学图文
        try:
            see_picture()
        except Exception as e:
            print("see_picture error:", e)
        print("see_picture done")
        # 完成后返回到微信
        # Selector().label("关闭").click(0).find()
        # print("自动任务已完成")
        to_see = Selector().xpath("//*[@name='我的']").find()
        if to_see:
            to_see.click()
            time.sleep(2)
    else:
        print('没有找到任何控件')


def task_page():
    to_see = Selector().xpath("//*[@name='我的']").find()
    if to_see:
        print("点击了我的")
        to_see.click()
        time.sleep(2)
    else:
        print("没有找到我的")
    # 点击可选任务
    node = Selector().xpath("//*[@name='可选任务']").find()
    if node:
        # 找到了控件
        print("找到了可选任务")
        # 打印控件属性,比较耗时
        node.click()
        time.sleep(2)
    else:
        print("没有找到可选任务")


def see_movide():
    time.sleep(2)
    print("开始观看视频")
    to_see = Selector().xpath("//*[@name='我的']").find()
    if to_see:
        to_see.click()
        time.sleep(2)
    # 点击可选任务
    node = Selector().xpath("//*[@name='可选任务']").find()
    if node:
        # 找到了控件
        print("找到了可选任务")
        # 打印控件属性,比较耗时
        node.click()
        time.sleep(2)
        # 去观看
        to_see = Selector().xpath("//*[@name='去观看']").find()
        if to_see:
            to_see.click()
            # 点击民俗
            time.sleep(2)
            # 去观看
            minsu = Selector().xpath("//*[@name='民俗']").find()
            if minsu:
                minsu.click()
            # 点击春节
            time.sleep(2)
            # 去观看 重复4次
            for i in range(0, 5):
                tuhua = Selector().xpath("//*[@name='春节年俗图画']").find()
                if tuhua:
                    tuhua.click()
                # 等待6:10分=370秒
                time.sleep(375)
                # click back
                back = Selector().xpath("//*[@name='返回']").find()
                if back:
                    back.click()
                time.sleep(2)


def find_fanzha(name):
    print("找到反诈提醒")
    while True:
        # Selector().x(15).y(318).scroll("down").find()
        # time.sleep(2)
        zhapian = Selector().xpath(f"//*[@name='{name}']").find()
        if zhapian:
            # 滚动到显示
            zhapian.scroll()
            print("找到了反诈提醒")
            return
        else:
            print("没有找到反诈提醒")
            return


def see_picture():
    print("看图文知识")
    to_see = Selector().xpath("//*[@name='我的']").find()
    if to_see:
        to_see.click()
        time.sleep(2)
    # 点击可选任务
    node = Selector().xpath("//*[@name='可选任务']").find()
    if node:
        # 找到了控件
        print("找到了可选任务")
        # 打印控件属性,比较耗时
        node.click()
        time.sleep(2)
        # 去观看
        to_see = Selector().xpath("//*[@name='去学习']").find()
        if to_see:
            to_see.click()
            time.sleep(2)
            # 点击其他
            find_and_click("其它")
            # 滑动找到反诈提醒
            pic_name = "邪教有“五险一金”吗？“神”能贷款吗？都没有？那我信它干嘛！"
            find_fanzha(pic_name)
            # see fanzhapian
            for i in range(0, 9):
                zhapian = Selector().xpath(f"//*[@name='{pic_name}']").find()
                if zhapian:
                    zhapian.click()
                    time.sleep(32)
                    # back
                    back = Selector().x(16).y(47).find()
                    if back:
                        back.click()
                        time.sleep(2)
                else:
                    print("没找到 zhapian")
            print("图文知识看完了")


# 点击提交或者下一题
def submit_or_next():
    if find_and_click("下一题"):
        print("下一题")
    else:
        find_and_click("提交")
        print("提交")
    # 并点击返回按钮
    # find_and_click("返回")


def chuang_guan():
    print("闯关")
    global total_count
    global topic_list
    while True:
        try:
            # 单选题 在 就检测查找
            single = Selector().name("单选题").find()
            if single:
                # 判断找到的值长度要大于5
                target = Selector().index(9).find()
                target2 = Selector().index(10).find()
                print("target", target)
                print("target2", target2)
                if target and hasattr(target, 'value') and topic_list.get(target.value):
                    print("找到了单选题1")
                    # 找到答案
                    answer1 = Selector().index(10).find()
                    answer2 = Selector().index(11).find()
                    answer = topic_list.get(target.value)
                    if answer and len(answer) == 1:
                        if answer1.value == answer[0]:
                            answer1.click()
                            print("点击了第一个答案")
                            # time.sleep(2)
                        if answer2.value == answer[0]:
                            answer2.click()
                            print("点击了第2个答案")
                            # time.sleep(2)
                        count_func(target.value)
                    else:
                        print("求助...................................")
                        print("问题答案是", {target.value: [answer1.value, answer2.value]})
                        count_func(target.value)
                elif target2 and hasattr(target2, 'value') and topic_list.get(target2.value):
                    print("找到了单选题2")
                    # 找到答案
                    answer1 = Selector().index(11).find()
                    answer2 = Selector().index(12).find()
                    answer = topic_list.get(target2.value)
                    if answer and len(answer) == 1:
                        if answer1.value == answer[0]:
                            answer1.click()
                            print("点击了第一个答案")
                            # time.sleep(2)
                        if answer2.value == answer[0]:
                            answer2.click()
                            print("点击了第2个答案")
                            # time.sleep(2)
                        count_func(answer2.value)
                    else:
                        print("求助...................................")
                        print("问题答案是", {target2.value: [answer1.value, answer2.value]})
                        count_func(target2.value)
                else:
                    target3 = Selector().index(11).find()
                    target4 = Selector().index(12).find()
                    print("没找到单选题1", {target.value: [""]})
                    print("没找到单选题2", {target2.value: [""]})
                    print("答案是", target3.value, target4.value)
                    count_func(target2.value)
                # 点击提交或者下一题
                submit_or_next()
            else:
                print("没找到单选题")
                # 并点击返回按钮
                find_and_click("返回")
                return
            print(f"总分数：{total_count}")
        except Exception as e:
            print("异常", e)
            return


def signle_v2free():
    system.open_url("https://w1.v2free.cc/user")
    time.sleep(3)
    wait_label("知道了")
    time.sleep(3)
    # 滑动显示签到
    action.slide(15, 655, 15, 311)
    time.sleep(3)
    # 点击签到
    single_btn = Selector().xpath("//*[@name='check  点我签到获取流量']").find()
    if single_btn:
        print("点我获取流量")
        single_btn.click()
        wait_label("知道了")
    else:
        print("没有找到点我获取流量")
    time.sleep(3)


# 找到可选答案
# def find_answer(title: str, index: int):
#     print("找到可选答案")
#     answer1 = Selector().index(index + 1).find()
#     answer2 = Selector().index(index + 2).find()
#     global topic_list
#     if answer1 and answer2 and answer1.value and answer2.value:
#         print("可选答案选项是:", answer1.value, answer2.value)
#         topic_list[title] = [answer1.value, answer2.value]
#     print("问题和答案映射关系是\n", topic_list)
#     print('问题和答案获取长度是', len(topic_list))


def listen_target():
    print("听目标")
    global topic_list
    while True:
        try:
            # 单选题 在 就检测查找
            single = Selector().name("单选题").find()
            if single:
                # 判断找到的值长度要大于5
                target = Selector().index(9).find()
                target2 = Selector().index(10).find()
                if target and target.value and len(target.value) > 10 and topic_list.get(target.value) is None:
                    print("找到问题target1", target.value)
                    answer1 = Selector().index(10).find()
                    answer2 = Selector().index(11).find()
                    topic_list[target.value] = [answer1.value, answer2.value]
                    print("找到答案:", answer1.value, answer2.value)
                    print("问题和答案映射关系是\n", topic_list)

                elif target2 and target2.value and len(target2.value) > 10 and topic_list.get(target2.value) is None:
                    print("找到问题target2", target2.value)
                    answer1 = Selector().index(11).find()
                    answer2 = Selector().index(12).find()
                    topic_list[target2.value] = [answer1.value, answer2.value]
                    print("找到答案:", answer1.value, answer2.value)
                    print("问题和答案映射关系是\n", topic_list)
                elif topic_list.get(target.value) is not None:
                    print("已经找到答案", topic_list.get(target.value))
                elif topic_list.get(target2.value) is not None:
                    print("已经找到答案", topic_list.get(target2.value))
                print("问题和答案获取长度是", len(topic_list))
            else:
                print("没找到单选题")
                time.sleep(2)
        except Exception as e:
            print("异常", e)


def do_work(label: str):
    print("做题和闯关", label)
    global total_count
    # 到任务页面
    task_page()
    if find_and_click("去答题"):
        total_count = 0
        if xy_and_click(15, 191):
            while True:
                if total_count < 30:
                    if find_and_click("开始答题"):
                        print("开始答题")
                        chuang_guan()
                else:
                    print("do_work返回到菜单页面")
                    try:
                        back = Selector().x(16).y(47).find()
                        # 点击返回菜单
                        if back:
                            back.click()
                            time.sleep(2)
                        to_see = Selector().xpath("//*[@name='我的']").find()
                        if to_see:
                            to_see.click()
                            time.sleep(2)
                        # 点击可选任务
                        node = Selector().xpath("//*[@name='可选任务']").find()
                        if node:
                            # 找到了控件
                            print("找到了可选任务")
                            # 打印控件属性,比较耗时
                            node.click()
                            time.sleep(2)
                    except Exception as e:
                        print("do_work返回到菜单页面异常", e)
                        break
                    break

    if find_and_click("去闯关"):
        total_count = 0
        if xy_and_click(11, 186):
            while True:
                if total_count < 30:
                    if find_and_click("开始闯关"):
                        print("开始闯关")
                        chuang_guan()
                else:
                    print("find_and_click返回到菜单页面")
                    try:
                        back = Selector().x(16).y(47).find()
                        # 点击返回菜单
                        if back:
                            back.click()
                            time.sleep(2)
                    except Exception as e:
                        print("find_and_click返回到菜单页面异常", e)
                        break
                    break
    print("做题和闯关 done")


def test_click():
    print("测试点击")
    # listen_target()
    # do_work("去答题")
    # do_work("去闯关")


def main():
    system.app_start(bundle_id="com.tencent.xin")
    time.sleep(2)
    # 判断是做题还是自动执行
    # 如果每题1分有的话，就是做题
    zuo = Selector().name("每题1分").find()
    if zuo:
        print("开始做题")
        # 做题和闯关
        do_work("label")
    else:
        volume = 0
        while volume < 18:
            print("减小音量......")
            action.key_press(action.KEY_volumedown)
            volume += 1
            time.sleep(0.1)
        open_huzhijiao()
        signle_v2free()


# 测试
# test_click()

# see_picture()

# 加载网页
# ui = WebWindow(R.ui("a.html"), tunner)
# ui.show()

# 自动视频和阅读
main()
