"""RSS源配置 - 精选中英文优质内容，含内容类型标注"""

RSS_SOURCES = [
    # ===== AI（最前面）=====
    {"url": "https://rsshub.app/jiqizhixin/daily", "category": "AI", "name": "机器之心", "type": "简讯"},
    {"url": "https://baoyu.io/feed", "category": "AI", "name": "宝玉的工程技术分享", "type": "文章"},
    {"url": "https://rsshub.app/openai/blog", "category": "AI", "name": "OpenAI Blog", "type": "文章"},
    {"url": "https://minimaxir.com/index.xml", "category": "AI", "name": "Max Woolf", "type": "文章"},
    {"url": "https://gwern.substack.com/feed", "category": "AI", "name": "Gwern", "type": "文章"},
    {"url": "https://garymarcus.substack.com/feed", "category": "AI", "name": "Gary Marcus", "type": "文章"},
    {"url": "https://lcamtuf.substack.com/feed", "category": "AI", "name": "lcamtuf", "type": "文章"},

    # ===== 科技（中文）=====
    {"url": "https://sspai.com/feed", "category": "科技", "name": "少数派", "type": "文章"},
    {"url": "https://www.ifanr.com/feed", "category": "科技", "name": "爱范儿", "type": "文章"},
    {"url": "https://www.geekpark.net/rss", "category": "科技", "name": "极客公园", "type": "文章"},
    {"url": "https://feeds.feedburner.com/ruanyifeng", "category": "科技", "name": "阮一峰的网络日志", "type": "文章"},
    {"url": "https://diygod.cc/feed", "category": "科技", "name": "DIYgod", "type": "文章"},
    {"url": "https://lutaonan.com/rss.xml", "category": "科技", "name": "Randy's Blog", "type": "文章"},

    # ===== 科技（英文博客）=====
    {"url": "https://www.jeffgeerling.com/blog.xml", "category": "科技", "name": "Jeff Geerling", "type": "文章"},
    {"url": "https://www.seangoedecke.com/rss.xml", "category": "科技", "name": "Sean Goedecke", "type": "文章"},
    {"url": "https://daringfireball.net/feeds/main", "category": "科技", "name": "Daring Fireball", "type": "文章"},
    {"url": "https://ericmigi.com/rss.xml", "category": "科技", "name": "Eric Migi", "type": "文章"},
    {"url": "http://antirez.com/rss", "category": "科技", "name": "antirez", "type": "文章"},
    {"url": "https://idiallo.com/feed.rss", "category": "科技", "name": "Ibrahim Diallo", "type": "文章"},
    {"url": "https://pluralistic.net/feed/", "category": "科技", "name": "Pluralistic", "type": "文章"},
    {"url": "https://shkspr.mobi/blog/feed/", "category": "科技", "name": "Terence Eden", "type": "文章"},
    {"url": "https://mitchellh.com/feed.xml", "category": "科技", "name": "Mitchell Hashimoto", "type": "文章"},
    {"url": "https://dynomight.net/feed.xml", "category": "科技", "name": "Dynomight", "type": "文章"},
    {"url": "https://xeiaso.net/blog.rss", "category": "科技", "name": "Xe Iaso", "type": "文章"},
    {"url": "https://devblogs.microsoft.com/oldnewthing/feed", "category": "科技", "name": "The Old New Thing", "type": "文章"},
    {"url": "https://www.righto.com/feeds/posts/default", "category": "科技", "name": "Ken Shirriff", "type": "文章"},
    {"url": "https://lucumr.pocoo.org/feed.atom", "category": "科技", "name": "Armin Ronacher", "type": "文章"},
    {"url": "https://overreacted.io/rss.xml", "category": "科技", "name": "Dan Abramov", "type": "文章"},
    {"url": "https://www.johndcook.com/blog/feed/", "category": "科技", "name": "John D. Cook", "type": "文章"},
    {"url": "https://gilesthomas.com/feed/rss.xml", "category": "科技", "name": "Giles Thomas", "type": "文章"},
    {"url": "https://matklad.github.io/feed.xml", "category": "科技", "name": "matklad", "type": "文章"},
    {"url": "https://evanhahn.com/feed.xml", "category": "科技", "name": "Evan Hahn", "type": "文章"},
    {"url": "https://terriblesoftware.org/feed/", "category": "科技", "name": "Terrible Software", "type": "文章"},
    {"url": "https://rakhim.exotext.com/rss.xml", "category": "科技", "name": "Rakhim", "type": "文章"},
    {"url": "https://nesbitt.io/feed.xml", "category": "科技", "name": "Nesbitt", "type": "文章"},
    {"url": "https://susam.net/feed.xml", "category": "科技", "name": "Susam Pal", "type": "文章"},
    {"url": "https://entropicthoughts.com/feed.xml", "category": "科技", "name": "Entropic Thoughts", "type": "文章"},
    {"url": "https://borretti.me/feed.xml", "category": "科技", "name": "Fernando Borretti", "type": "文章"},
    {"url": "https://jayd.ml/feed.xml", "category": "科技", "name": "jayd.ml", "type": "文章"},
    {"url": "https://geohot.github.io/blog/feed.xml", "category": "科技", "name": "geohot", "type": "文章"},
    {"url": "https://blog.jim-nielsen.com/feed.xml", "category": "科技", "name": "Jim Nielsen", "type": "文章"},
    {"url": "https://jyn.dev/atom.xml", "category": "科技", "name": "jyn", "type": "文章"},
    {"url": "https://www.geoffreylitt.com/feed.xml", "category": "科技", "name": "Geoffrey Litt", "type": "文章"},
    {"url": "https://www.downtowndougbrown.com/feed/", "category": "科技", "name": "Doug Brown", "type": "文章"},
    {"url": "https://eli.thegreenplace.net/feeds/all.atom.xml", "category": "科技", "name": "Eli Bendersky", "type": "文章"},
    {"url": "https://fabiensanglard.net/rss.xml", "category": "科技", "name": "Fabien Sanglard", "type": "文章"},
    {"url": "https://hugotunius.se/feed.xml", "category": "科技", "name": "Hugo Tunius", "type": "文章"},
    {"url": "https://berthub.eu/articles/index.xml", "category": "科技", "name": "Bert Hubert", "type": "文章"},
    {"url": "https://beej.us/blog/rss.xml", "category": "科技", "name": "Beej", "type": "文章"},
    {"url": "https://danielwirtz.com/rss.xml", "category": "科技", "name": "Daniel Wirtz", "type": "文章"},
    {"url": "https://matduggan.com/rss/", "category": "科技", "name": "Mat Duggan", "type": "文章"},
    {"url": "https://refactoringenglish.com/index.xml", "category": "科技", "name": "Refactoring English", "type": "文章"},
    {"url": "https://bernsteinbear.com/feed.xml", "category": "科技", "name": "Max Bernstein", "type": "文章"},
    {"url": "https://blog.miguelgrinberg.com/feed", "category": "科技", "name": "Miguel Grinberg", "type": "文章"},
    {"url": "https://www.tedunangst.com/flak/rss", "category": "科技", "name": "Ted Unangst", "type": "文章"},
    {"url": "https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/feed.xml", "category": "科技", "name": "Simon Tatham", "type": "文章"},
    {"url": "https://grantslatton.com/rss.xml", "category": "科技", "name": "Grant Slatton", "type": "文章"},
    {"url": "https://simone.org/feed/", "category": "科技", "name": "Simone", "type": "文章"},
    {"url": "https://timsh.org/rss/", "category": "科技", "name": "timsh", "type": "文章"},
    {"url": "https://buttondown.com/hillelwayne/rss", "category": "科技", "name": "Hillel Wayne", "type": "文章"},

    # ===== 安全 =====
    {"url": "https://rsshub.app/freebuf/articles/new", "category": "安全", "name": "FreeBuf", "type": "简讯"},
    {"url": "https://rsshub.app/seebug/latest", "category": "安全", "name": "Seebug", "type": "简讯"},
    {"url": "https://krebsonsecurity.com/feed/", "category": "安全", "name": "Krebs on Security", "type": "文章"},
    {"url": "https://micahflee.com/feed/", "category": "安全", "name": "Micah Lee", "type": "文章"},
    {"url": "https://www.troyhunt.com/rss/", "category": "安全", "name": "Troy Hunt", "type": "文章"},
    {"url": "https://computer.rip/rss.xml", "category": "安全", "name": "computer.rip", "type": "文章"},
    {"url": "https://mjg59.dreamwidth.org/data/rss", "category": "安全", "name": "Matthew Garrett", "type": "文章"},
    {"url": "https://brutecat.com/rss.xml", "category": "安全", "name": "brutecat", "type": "文章"},
    {"url": "https://keygen.sh/blog/feed.xml", "category": "安全", "name": "Keygen", "type": "文章"},

    # ===== 金融 =====
    {"url": "https://awealthofcommonsense.com/feed/", "category": "金融", "name": "A Wealth of Common Sense", "type": "文章"},
    {"url": "https://noahpinion.substack.com/feed", "category": "金融", "name": "Noahpinion", "type": "文章"},
    {"url": "https://diff.substack.com/feed", "category": "金融", "name": "The Diff (Byrne Hobart)", "type": "文章"},
    {"url": "https://abnormalreturns.com/feed/", "category": "金融", "name": "Abnormal Returns", "type": "简讯"},
    {"url": "https://klementoverinvesting.substack.com/feed", "category": "金融", "name": "Klement on Investing", "type": "文章"},
    {"url": "https://www.notboring.co/feed", "category": "金融", "name": "Not Boring", "type": "文章"},

    # ===== 商业 =====
    {"url": "https://rsshub.app/36kr/newsflashes", "category": "商业", "name": "36氪快讯", "type": "简讯"},
    {"url": "https://steveblank.com/feed/", "category": "商业", "name": "Steve Blank", "type": "文章"},
    {"url": "https://www.dwarkeshpatel.com/feed", "category": "商业", "name": "Dwarkesh Patel", "type": "文章"},
    {"url": "https://www.construction-physics.com/feed", "category": "商业", "name": "Construction Physics", "type": "文章"},
    {"url": "https://anildash.com/feed.xml", "category": "商业", "name": "Anil Dash", "type": "文章"},
    {"url": "https://joanwestenberg.com/rss", "category": "商业", "name": "Joan Westenberg", "type": "文章"},

    # ===== 文化 =====
    {"url": "https://rsshub.app/douban/explore", "category": "文化", "name": "豆瓣精选", "type": "简讯"},
    {"url": "https://www.experimental-history.com/feed", "category": "文化", "name": "Experimental History", "type": "文章"},
    {"url": "https://feed.tedium.co/", "category": "文化", "name": "Tedium", "type": "文章"},
    {"url": "https://www.wheresyoured.at/rss/", "category": "文化", "name": "Ed Zitron", "type": "文章"},
]

CATEGORIES = ["全部", "AI", "科技", "金融", "商业", "安全", "文化"]
CONTENT_TYPES = ["全部", "文章", "简讯"]

HOTSPOT_PLATFORMS = ["全部", "微博", "知乎", "小红书", "抖音"]
