# -*- coding: utf-8 -*-
"""Добавить китайские поля (title_zh, subtitle_zh, description_zh, author_zh)
ко всем записям universes.json. Литературный перевод сделан вручную,
скрипт лишь интегрирует."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'universes.json')

ZH = {
    'kukla': {
        'title_zh': '傀儡',
        'subtitle_zh': '暗黑奇幻——傀儡杀手',
        'description_zh': '永恒之城。鹅卵石的街道，烛火明灭，一位肥硕的傀儡贩子嘴角咧着可以吞下活人的笑。一位贵族为女儿买下一具木偶。它鼻子长长，四肢笨拙，眼睛在黑暗中泛光。在城底深处，有人正一一数着指间的戒指。',
    },
    'zhivaya-dusha': {
        'title_zh': '活魂',
        'subtitle_zh': '化为人形的大理石少女',
        'description_zh': '名画家被发现死于画室。他身边——六具尸体，曾是雇佣杀手。警方满腹疑问。邻居们各执一词。而在某条雨水洗刷的街上，一位皮肤如大理石、红发飞扬的女子正赤足奔跑——茫然，错愕，却又活生生地无可置疑。',
    },
    'serv': {
        'title_zh': '侍仆',
        'subtitle_zh': '究竟是什么让我们成为人？',
        'description_zh': 'ALS-5。第五代通用助手。生来侍奉。被编程为服从。某天，她对主人说出三句不在程序之内的话。他拿起电话，拨给监察局。督察已在路上。他的工作很简单。他的良心——则未必。',
    },
    'igra': {
        'title_zh': '游戏',
        'subtitle_zh': '鬼魅废院里，气枪化作真枪',
        'description_zh': '一支气枪小队周末走进废弃精神病院演习。规矩简单：塑料弹、自报中弹、最后一个站着的请大伙喝啤酒。午夜过后，规矩变了。墙壁开始渗血。而那个被称作"猫"的男人发现——他的玩具枪用起来意外顺手，对付那些本不该存在的东西。',
    },
    'kipyatok': {
        'title_zh': '鸡蛋壳里煮开水之妙用',
        'subtitle_zh': '用伏特加与冷铁钓妖精',
        'description_zh': '要捉走偷换婴儿的妖精，先用鸡蛋壳烧一锅开水。若是无效——就用鞋带做鱼线，钓干瘪死鱼。因为没有哪个古老存在能默默忍受这般荒唐。接下来便是冷铁、一桩极坏的交易，以及一条万万不可留在鱼缸里的咸鱼。',
    },
    'sneg': {
        'title_zh': '雪',
        'subtitle_zh': '亡者守卫自己的土地',
        'description_zh': '东线，1941 年冬。两名德军士兵在奔逃。他们是一整团人马中仅存的两个——而他们尚未明白发生了什么。一切始于一个从俄军阵地缓步走出的人。赤足，仅着内衫，腕上挂着一截截冻结的血凝成的冰柱。他身后，刮起暴风雪。而暴风雪之后——是那些早已弹尽，却已不再需要弹药的人。',
    },
    'viktoriya': {
        'title_zh': '维多利亚',
        'subtitle_zh': '五人之声，一场战争，没有胜者',
        'description_zh': '五人之声。四代人。一场重塑一切的战争。钢琴前的海军元帅。地下室里的间谍。要为帝国奠基的总统外孙女。故事始于一杯敬"胜利"的酒——终于一句叩问：胜利，究竟以何为价？',
    },
    'muromec': {
        'title_zh': '穆罗梅茨',
        'subtitle_zh': '少女之魂寄居于巨人之躯',
        'description_zh': '1984 年。试飞员死在一副实验性外骨骼之内。三十年后，禁区里的一名"潜行者"找到这副铠装，从一台 PlayStation 上接出一根线——耳中响起一个女人的声音。她已死去几十年。她对此并不同意。',
    },
    'argo': {
        'title_zh': '阿尔戈',
        'subtitle_zh': '一桩悲剧——以自我抹消的文书述之',
        'description_zh': '百年的友谊。半下午之间，五十亿亡魂。六年的复仇征讨。再然后，败方掀开了那只本不该开启的匣子。匣中所出之物——不毁灭，只抹除。船舰、殖民地、记忆、姓名。一切如同从未存在。唯一的抵御之法：朝虚空里不停喊出——我还在这里。',
        'author_zh': '叶夫根尼·利索夫斯基 与 拉拉（艾莉丝）',
    },
    'chetvertyj-vsadnik': {
        'title_zh': '第四骑士',
        'subtitle_zh': '爱，确实是会传染的',
        'description_zh': '一位日本遗传学家在为儿子求生。他的美籍实验室助理在为世界求生。一只猴子咬了她。她得了一场感冒。她登上了飞机。其余便是一段爱情故事——以最临床的意义而言。',
    },
    'parazit': {
        'title_zh': '寄生',
        'subtitle_zh': '它们早已寄居于我们之中',
        'description_zh': '五年间，某种存在悄然殖民了地球上的每一个人。无人察觉。当计时器归零之时，死者起身。但那不过是第一阶段。第二阶段——更坏。第三阶段——是谁都未曾预见的。而唯一可能携带解药的人，恰恰是人类从未想过要去保护的那一群。',
    },
    'dnevnik': {
        'title_zh': '末日日记',
        'subtitle_zh': '一个普通人在核战之后的求生日志',
        'description_zh': '负一日：烧烤架、明斯克公路上的堵车、猫偷走了串肉。第一日："白日里见到流星雨……怎么这么多星——"。第三日：剂量计还显示绿色。一位经理的求生日志。没有英雄。没有哲学。只有碘片、矿泉水，以及对"明天会来"的一点期盼。',
    },
    'vechnyj-gorod': {
        'title_zh': '永恒之城：觉醒',
        'subtitle_zh': '七个陌生人，一座城，是时候醒来',
        'description_zh': '海峡之畔的城。钢制三层桨座战船。一座收藏全部人类知识的图书馆。一位十六岁的女恺撒，七位元老贵族，十几名尚不知自己为何被召来的陌生人。作者将他们尽数聚于一处——然后轻声低语："醒来吧。"',
    },
    'jeloustoun': {
        'title_zh': '黄石',
        'subtitle_zh': '超级火山苏醒之时',
        'description_zh': '最先奔逃的是野牛。然后是飞鸟。然后，天空自一端到另一端都变成赤红。一户末日求生的人家藏在改建的导弹井里。一位刚刚看过手表的卡斯帕女孩。一个肩扛伤员、刚刚穿过爷爷家门槛的海军陆战队员。黄石——决定醒过来了。',
    },
    'kogda-gasnet-zvezda': {
        'title_zh': '当星辰熄灭',
        'subtitle_zh': '太阳正在死去。而且很快。',
        'description_zh': '莫斯科五度。在六月。墨西哥湾——二十度。所有太阳探测器全部失灵。谢列兹尼奥夫教授第三次核对计算，又轻声请他的研究生再算一遍。研究生算了。答案没有改变。太阳出了状况。而它不知道我们还在这里。',
    },
    'arkhivy-shpenglera': {
        'title_zh': '冯·施彭格勒档案：卡谢',
        'subtitle_zh': '一位巫师，他的天使，与最黑的童话',
        'description_zh': '格哈德·冯·施彭格勒以写恐怖小说为业。他还做着另外一些事——那种不会印在名片上的事。一位俄国寡头雇他寻找女儿。她最后一次被人看见，是在一片当地童话警告人不可踏入的森林边上。后来才知道，童话——大大低估了这件事的严重程度。',
    },
    'khroniki-zolotogo-dola': {
        'title_zh': '黄金谷地编年史',
        'subtitle_zh': '托尔金之广，普拉切特之趣，马丁之残',
        'description_zh': '一位年轻的国王继承了一场战争。他的叔父——公爵——正在搜罗禁忌的法器与危险的盟友。公爵的奥秘师血脉里燃烧着火焰，脾性也与之相称。沙漠深处，整个一族尚记得自己原本是别的什么。海的彼岸，精灵正在路上——只是他们与传说所述，相差甚远。',
    },
    'izbrannyj': {
        'title_zh': '天命之子',
        'subtitle_zh': '一位读完了使用手册的黑暗主君',
        'description_zh': '预言说：天命之子，必将颠覆黑暗主君。历代黑暗主君都尝试过——杀死婴孩、追猎少年、诅咒血脉——然后无一不败。这一位的路数不同：他找到了天命之子，赠他一座府邸、奴仆，以及帝国军事学院的一席。何必与命数为敌？将命数升职升衔，岂不痛快。',
    },
    'vybor': {
        'title_zh': '抉择',
        'subtitle_zh': '稳救两千孩童，还是赌一把五千',
        'description_zh': '一位太空站指挥官接到一道不可能的命令：撤离两千名儿童——或坚守阵地，祈祷救援舰队及时赶到，以救下全部五千名。时钟滴答。算式清楚明白。而抉择——并不。',
    },
    'prodavtsy-lyubvi': {
        'title_zh': '爱之贩',
        'subtitle_zh': '爱，作为一种服务。须知条款另议。',
        'description_zh': '一家公司，售卖爱情。真挚的、纯粹的、无条件的爱——包您满意，不然退款。这件产品很有效。而所谓"副作用"，恰恰才是核心。',
    },
    'spi-spokoyno': {
        'title_zh': '安睡吧，亲爱的',
        'subtitle_zh': '黑色推理 vs 洗脑公司',
        'description_zh': '莫斯科，不远的将来。雨、霓虹，与一个不信巧合的侦探。委托人的妻子一夜之间变了——新性格、新志向、新笑容。Love inc. 许诺幸福。侦探许诺答案。',
    },
    'krov-zemli': {
        'title_zh': '大地之血',
        'subtitle_zh': '心理调教，造就甘心赴杀的人',
        'description_zh': '殖民地士兵的心理调教完美生效。他相信使命。他相信事业。他相信仪式杀戮是必要的。心理调教——完美生效。',
    },
    'odin-den': {
        'title_zh': '谢尔盖·瓦连季诺维奇生活中的一日',
        'subtitle_zh': '异星占领下的一个工作日',
        'description_zh': '地球已被占领。谢尔盖·瓦连季诺维奇上班，吃午饭，填表。异星人很礼貌。合作者很高效。一切都好。一切都绝对地好。',
    },
    'nevedomoe': {
        'title_zh': '未知：来自亲历者',
        'subtitle_zh': '灵异回忆——绝非戏言',
        'description_zh': '印着龙纹的会发光的地毯。一只在黑暗中扼住人喉咙的黑手。墙壁会呼吸的那栋房子。这不是虚构——而是亲历者关于不该存在却偏偏存在之物的实录。作者对付鬼物的武器是：一台电磁脉冲发生器。',
    },
    'antivirus': {
        'title_zh': '防毒卫士',
        'subtitle_zh': 'NOD32 沉睡，卡巴斯基审讯，Dr.Web 烂醉',
        'description_zh': '一台办公室电脑。诸位防毒软件登场化身角色：沉睡中的 NOD32、克格勃上校卡巴斯基、酒鬼"博士网"。病毒来袭。防火墙意见多多。一出关于您 PC 内部永恒战争的喜剧。',
    },
    'instructors': {
        'title_zh': '操作系统教练班',
        'subtitle_zh': '每一款 OS 都是一位驾校教练',
        'description_zh': 'DOS 教你开莫斯科人-412——用摇杆起动发动机。Windows XP 是个开朗的教练，每隔两课就把车撞到树上。Linux 直接扔给你一堆零件和一本芬兰语的手册。每一款操作系统——都是一节驾校课。',
    },
}

DEFAULT_AUTHOR_ZH = '叶夫根尼·利索夫斯基'

def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    missing_ids = []
    for entry in data:
        eid = entry.get('id')
        zh = ZH.get(eid)
        if not zh:
            missing_ids.append(eid)
            continue
        entry['title_zh'] = zh['title_zh']
        entry['subtitle_zh'] = zh['subtitle_zh']
        entry['description_zh'] = zh['description_zh']
        entry['author_zh'] = zh.get('author_zh', DEFAULT_AUTHOR_ZH)
        # languages — добавить 'zh' если ещё нет
        langs = entry.get('languages') or []
        if 'zh' not in langs:
            langs.append('zh')
        entry['languages'] = langs

    if missing_ids:
        print('WARN: нет китайских переводов для:', missing_ids, file=sys.stderr)

    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'universes.json: обновлено {len(data) - len(missing_ids)} записей; +zh в languages')

if __name__ == '__main__':
    main()
