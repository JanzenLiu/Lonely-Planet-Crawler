from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from json import dumps, JSONEncoder
import re

# poiByCity = [
# {'cityPath': 'china/sichuan/chengdu', 'pois': [{'path': '/china/sichuan/chengdu/attractions/chengdu-museum/a/poi-sig/1543456/356085', 'name': 'Chéngdū Museum'}, {'path': '/china/sichuan/chengdu/attractions/tomb-of-wang-jian/a/poi-sig/472738/356085', 'name': 'Tomb of Wáng Jiàn'}]},
# {'cityPath': 'china/zhejiang/hangzhou', 'pois': [{'path': '/china/zhejiang/hangzhou/attractions/west-lake/a/poi-sig/473520/356175', 'name': 'West Lake'}, {'path': '/china/zhejiang/hangzhou/attractions/lingy-n-temple/a/poi-sig/1096625/356175', 'name': 'Língyǐn Temple'}, {'path': '/china/zhejiang/hangzhou/attractions/dragon-well-tea-village/a/poi-sig/1437342/356175', 'name': 'Dragon Well Tea Village'}, {'path': '/china/zhejiang/hangzhou/attractions/jingci-temple/a/poi-sig/473504/356175', 'name': 'Jìngcí Temple'}, {'path': '/china/zhejiang/hangzhou/attractions/sunrise-terrace/a/poi-sig/1418425/356175', 'name': 'Sunrise Terrace'}, {'path': '/china/zhejiang/hangzhou/attractions/six-harmonies-pagoda/a/poi-sig/473516/356175', 'name': 'Six Harmonies Pagoda'}, {'path': '/china/zhejiang/hangzhou/attractions/qinghefang-old-street/a/poi-sig/473530/356175', 'name': 'Qīnghéfāng Old Street'}, {'path': '/china/zhejiang/hangzhou/attractions/huqingyu-tang-chinese-medicine-museum/a/poi-sig/473502/356175', 'name': 'Húqìngyú Táng Chinese Medicine Museum'}, {'path': '/china/zhejiang/hangzhou/attractions/china-national-silk-museum/a/poi-sig/1096638/356175', 'name': 'China National Silk Museum'}]},
# {'cityPath': 'china/shandong/qingdao', 'pois': [{'path': '/china/shandong/qingdao/attractions/han-dynasty-brick-museum/a/poi-sig/1499195/356071', 'name': 'Han Dynasty Brick Museum'}, {'path': '/china/shandong/qingdao/attractions/st-michael-s-cathedral/a/poi-sig/473134/356071', 'name': 'St Michael’s Cathedral'}, {'path': '/china/shandong/qingdao/attractions/zhongshan-park/a/poi-sig/473148/356071', 'name': 'Zhōngshān Park'}, {'path': '/china/shandong/qingdao/attractions/governor-s-house-museum/a/poi-sig/1436974/356071', 'name': 'Governor’s House Museum'}, {'path': '/china/shandong/qingdao/attractions/tsingtao-beer-museum/a/poi-sig/1238017/356071', 'name': 'Tsingtao Beer Museum'}, {'path': '/china/shandong/qingdao/attractions/tianhou-temple/a/poi-sig/473138/356071', 'name': 'Tiānhòu Temple'}, {'path': '/china/shandong/qingdao/attractions/little-qingd-o/a/poi-sig/473120/356071', 'name': 'Little Qīngdǎo'}, {'path': '/china/shandong/qingdao/attractions/shil-oren-beach/a/poi-sig/1499400/356071', 'name': 'Shílǎorén Beach'}, {'path': '/china/shandong/qingdao/attractions/protestant-church/a/poi-sig/473128/356071', 'name': 'Protestant Church'}]},
# {'cityPath': 'china/shandong/taian', 'pois': [{'path': '/china/shandong/taian/attractions/dai-temple/a/poi-sig/1237755/356073', 'name': 'Dài Temple'}, {'path': '/china/shandong/taian/attractions/pervading-light-temple/a/poi-sig/1436921/356073', 'name': 'Pervading Light Temple'}, {'path': '/china/shandong/taian/attractions/azure-clouds-temple/a/poi-sig/1238826/356073', 'name': 'Azure Clouds Temple'}, {'path': '/china/shandong/taian/attractions/north-pointing-rock/a/poi-sig/1454452/356073', 'name': 'North Pointing Rock'}, {'path': '/china/shandong/taian/attractions/red-gate-palace/a/poi-sig/1238824/356073', 'name': 'Red Gate Palace'}, {'path': '/china/shandong/taian/attractions/yaocan-pavilion/a/poi-sig/1237749/356073', 'name': 'Yáocān Pavilion'}, {'path': '/china/shandong/taian/attractions/tai-shan/a/poi-sig/1016914/356073', 'name': 'Tài Shān'}, {'path': '/china/shandong/taian/attractions/d-um-hall/a/poi-sig/1499027/356073', 'name': 'Dǒumǔ Hall'}, {'path': '/china/shandong/taian/attractions/hall-of-heavenly-blessing/a/poi-sig/1237742/356073', 'name': 'Hall of Heavenly Blessing'}]},
# {'cityPath': 'china/shaanxi-shanxi/xian', 'pois': [{'path': '/china/shaanxi-shanxi/xian/attractions/army-of-terracotta-warriors/a/poi-sig/1016918/356065', 'name': 'Army of Terracotta Warriors'}, {'path': '/china/shaanxi-shanxi/xian/attractions/xi-an-city-walls/a/poi-sig/475738/356065', 'name': 'Xī’ān City Walls'}, {'path': '/china/shaanxi-shanxi/xian/attractions/big-goose-pagoda/a/poi-sig/475736/356065', 'name': 'Big Goose Pagoda'}, {'path': '/china/shaanxi-shanxi/xian/attractions/tomb-of-emperor-jingdi/a/poi-sig/1239657/356065', 'name': 'Tomb of Emperor Jingdi'}, {'path': '/china/shaanxi-shanxi/xian/attractions/f-men-temple/a/poi-sig/1239678/356065', 'name': 'Fǎmén Temple'}, {'path': '/china/shaanxi-shanxi/xian/attractions/gu-ngren-temple/a/poi-sig/1535996/356065', 'name': 'Guǎngrén Temple'}, {'path': '/china/shaanxi-shanxi/xian/attractions/imperial-tombs/a/poi-sig/1239677/356065', 'name': 'Imperial Tombs'}, {'path': '/china/shaanxi-shanxi/xian/attractions/great-mosque/a/poi-sig/475748/356065', 'name': 'Great Mosque'}, {'path': '/china/shaanxi-shanxi/xian/attractions/tomb-of-qin-shi-huang/a/poi-sig/1239391/356065', 'name': 'Tomb of Qin Shi Huang'}]},
# {'cityPath': 'egypt/cairo', 'pois': [{'path': '/egypt/cairo/attractions/pyramids-of-giza/a/poi-sig/1432031/355225', 'name': 'Pyramids of Giza'}, {'path': '/egypt/cairo/attractions/egyptian-museum/a/poi-sig/1021384/355225', 'name': 'Egyptian Museum'}, {'path': '/egypt/cairo/attractions/khan-al-khalili/a/poi-sig/406432/355225', 'name': 'Khan al-Khalili'}, {'path': '/egypt/cairo/attractions/al-azhar-mosque/a/poi-sig/406208/355225', 'name': 'Al-Azhar Mosque'}, {'path': '/egypt/cairo/attractions/mosque-madrassa-of-sultan-hassan/a/poi-sig/406356/355225', 'name': 'Mosque-Madrassa of Sultan Hassan'}, {'path': '/egypt/cairo/attractions/coptic-museum/a/poi-sig/406474/355225', 'name': 'Coptic Museum'}, {'path': '/egypt/cairo/attractions/mosque-of-qaitbey/a/poi-sig/1431130/355225', 'name': 'Mosque of Qaitbey'}, {'path': '/egypt/cairo/attractions/mahmoud-mukhtar-museum/a/poi-sig/1076128/355225', 'name': 'Mahmoud Mukhtar Museum'}, {'path': '/egypt/cairo/attractions/agricultural-museum/a/poi-sig/406204/355225', 'name': 'Agricultural Museum'}]},
# {'cityPath': 'egypt/red-sea-coast/hurghada', 'pois': [{'path': '/egypt/red-sea-coast/hurghada/attractions/gota-abu-ramada/a/poi-sig/1426644/355257', 'name': 'Gota Abu Ramada'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/umm-qamar/a/poi-sig/1426639/355257', 'name': 'Umm Qamar'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/giftun-islands/a/poi-sig/1426640/355257', 'name': 'Giftun Islands'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/hurghada-public-beach/a/poi-sig/1427048/355257', 'name': 'Hurghada Public Beach'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/shedwan-island-lighthouse/a/poi-sig/1453534/355257', 'name': 'Shedwan Island Lighthouse'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/ashrafi-island-lighthouse/a/poi-sig/1453535/355257', 'name': 'Ashrafi Island Lighthouse'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/stingray-station/a/poi-sig/1453531/355257', 'name': 'Stingray Station'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/alternatives/a/poi-sig/1453532/355257', 'name': 'Alternatives'}, {'path': '/egypt/red-sea-coast/hurghada/attractions/siyul-kebira/a/poi-sig/1426637/355257', 'name': 'Siyul Kebira'}]},
# {'cityPath': 'italy/rome', 'pois': [{'path': '/italy/rome/attractions/vatican-museums/a/poi-sig/1256585/359975', 'name': 'Vatican Museums'}, {'path': '/italy/rome/attractions/roman-forum/a/poi-sig/389047/359975', 'name': 'Roman Forum'}, {'path': '/italy/rome/attractions/st-peter-s-basilica/a/poi-sig/1256581/359975', 'name': "St Peter's Basilica"}, {'path': '/italy/rome/attractions/palatino/a/poi-sig/1090383/359975', 'name': 'Palatino'}, {'path': '/italy/rome/attractions/museo-e-galleria-borghese/a/poi-sig/389101/359975', 'name': 'Museo e Galleria Borghese'}, {'path': '/italy/rome/attractions/colosseum/a/poi-sig/1160430/359975', 'name': 'Colosseum'}, {'path': '/italy/rome/attractions/capitoline-museums/a/poi-sig/389381/359975', 'name': 'Capitoline Museums'}, {'path': '/italy/rome/attractions/pantheon/a/poi-sig/389093/359975', 'name': 'Pantheon'}, {'path': '/italy/rome/attractions/basilica-di-san-giovanni-in-laterano/a/poi-sig/389103/359975', 'name': 'Basilica di San Giovanni in Laterano'}]},
# {'cityPath': 'italy/venice', 'pois': [{'path': '/italy/venice/attractions/palazzo-ducale/a/poi-sig/399883/360029', 'name': 'Palazzo Ducale'}, {'path': '/italy/venice/attractions/gallerie-dell-accademia/a/poi-sig/399885/360029', 'name': "Gallerie dell'Accademia"}, {'path': '/italy/venice/attractions/basilica-di-san-marco/a/poi-sig/1097875/360029', 'name': 'Basilica di San Marco'}, {'path': '/italy/venice/attractions/peggy-guggenheim-collection/a/poi-sig/399959/360029', 'name': 'Peggy Guggenheim Collection'}, {'path': '/italy/venice/attractions/basilica-di-santa-maria-della-salute/a/poi-sig/399961/360029', 'name': 'Basilica di Santa Maria della Salute'}, {'path': '/italy/venice/attractions/the-ghetto/a/poi-sig/400345/360029', 'name': 'The Ghetto'}, {'path': '/italy/venice/attractions/scuola-grande-di-san-rocco/a/poi-sig/400371/360029', 'name': 'Scuola Grande di San Rocco'}, {'path': '/italy/venice/attractions/ca-rezzonico/a/poi-sig/399933/360029', 'name': "Ca' Rezzonico"}, {'path': '/italy/venice/attractions/fondazione-giorgio-cini/a/poi-sig/400323/360029', 'name': 'Fondazione Giorgio Cini'}]},
# {'cityPath': 'italy/florence', 'pois': [{'path': '/italy/florence/attractions/galleria-degli-uffizi/a/poi-sig/1157282/360059', 'name': 'Galleria degli Uffizi'}, {'path': '/italy/florence/attractions/basilica-di-santa-maria-novella/a/poi-sig/388407/360059', 'name': 'Basilica di Santa Maria Novella'}, {'path': '/italy/florence/attractions/palazzo-vecchio/a/poi-sig/1255748/360059', 'name': 'Palazzo Vecchio'}, {'path': '/italy/florence/attractions/museo-di-san-marco/a/poi-sig/1213653/360059', 'name': 'Museo di San Marco'}, {'path': '/italy/florence/attractions/duomo/a/poi-sig/388337/360059', 'name': 'Duomo'}, {'path': '/italy/florence/attractions/grande-museo-del-duomo/a/poi-sig/388799/360059', 'name': 'Grande Museo del Duomo'}, {'path': '/italy/florence/attractions/cupola-del-brunelleschi/a/poi-sig/1343900/360059', 'name': 'Cupola del Brunelleschi'}, {'path': '/italy/florence/attractions/galleria-dell-accademia/a/poi-sig/1087169/360059', 'name': "Galleria dell'Accademia"}, {'path': '/italy/florence/attractions/museo-novecento/a/poi-sig/1511850/360059', 'name': 'Museo Novecento'}]},
# {'cityPath': 'italy/milan', 'pois': [{'path': '/italy/milan/attractions/the-last-supper/a/poi-sig/1215052/359947', 'name': 'The Last Supper'}, {'path': '/italy/milan/attractions/duomo/a/poi-sig/1137450/359947', 'name': 'Duomo'}, {'path': '/italy/milan/attractions/cimitero-monumentale/a/poi-sig/405548/359947', 'name': 'Cimitero Monumentale'}, {'path': '/italy/milan/attractions/museo-nazionale-della-scienza-e-della-tecnologia/a/poi-sig/405580/359947', 'name': 'Museo Nazionale della Scienza e della Tecnologia'}, {'path': '/italy/milan/attractions/pinacoteca-di-brera/a/poi-sig/1137628/359947', 'name': 'Pinacoteca di Brera'}, {'path': '/italy/milan/attractions/museo-poldi-pezzoli/a/poi-sig/405600/359947', 'name': 'Museo Poldi Pezzoli'}, {'path': '/italy/milan/attractions/chiesa-di-san-maurizio/a/poi-sig/405620/359947', 'name': 'Chiesa di San Maurizio'}, {'path': '/italy/milan/attractions/quadrilatero-d-oro/a/poi-sig/1256164/359947', 'name': "Quadrilatero d'Oro"}, {'path': '/italy/milan/attractions/castello-sforzesco/a/poi-sig/1137618/359947', 'name': 'Castello Sforzesco'}]},
# {'cityPath': 'italy/sicily', 'pois': [{'path': '/italy/sicily/attractions/valley-of-the-temples/a/poi-sig/1374041/359993', 'name': 'Valley of the Temples'}, {'path': '/italy/sicily/attractions/cattedrale-di-monreale/a/poi-sig/1137549/359993', 'name': 'Cattedrale di Monreale'}, {'path': '/italy/sicily/attractions/cappella-palatina/a/poi-sig/458749/359993', 'name': 'Cappella Palatina'}, {'path': '/italy/sicily/attractions/parco-archeologico-della-neapolis/a/poi-sig/471856/359993', 'name': 'Parco Archeologico della Neapolis'}, {'path': '/italy/sicily/attractions/villa-romana-del-casale/a/poi-sig/1408603/359993', 'name': 'Villa Romana del Casale'}, {'path': '/italy/sicily/attractions/piazza-del-duomo/a/poi-sig/1372278/359993', 'name': 'Piazza del Duomo'}, {'path': '/italy/sicily/attractions/stromboli-crater/a/poi-sig/1372147/359993', 'name': 'Stromboli Crater'}, {'path': '/italy/sicily/attractions/ragusa-ibla/a/poi-sig/1372407/359993', 'name': 'Ragusa Ibla'}, {'path': '/italy/sicily/attractions/tempio-della-concordia/a/poi-sig/471572/359993', 'name': 'Tempio della Concordia'}]},
# {'cityPath': 'italy/puglia/otranto', 'pois': []},
# {'cityPath': 'italy/puglia/taranto', 'pois': []},
# {'cityPath': 'italy/puglia/trani', 'pois': []},
# {'cityPath': 'italy/puglia/alberobello', 'pois': []},
# {'cityPath': 'italy/puglia/cisternino', 'pois': []},
# {'cityPath': 'spain/madrid', 'pois': [{'path': '/spain/madrid/attractions/museo-del-prado/a/poi-sig/399599/360770', 'name': 'Museo del Prado'}, {'path': '/spain/madrid/attractions/museo-thyssen-bornemisza/a/poi-sig/399601/360770', 'name': 'Museo Thyssen-Bornemisza'}, {'path': '/spain/madrid/attractions/parque-del-buen-retiro/a/poi-sig/399603/360770', 'name': 'Parque del Buen Retiro'}, {'path': '/spain/madrid/attractions/centro-de-arte-reina-sofia/a/poi-sig/399591/360770', 'name': 'Centro de Arte Reina Sofía'}, {'path': '/spain/madrid/attractions/museo-lazaro-galdiano/a/poi-sig/1094855/360770', 'name': 'Museo Lázaro Galdiano'}, {'path': '/spain/madrid/attractions/real-academia-de-bellas-artes-de-san-fernando/a/poi-sig/1094815/360770', 'name': 'Real Academia de Bellas Artes de San Fernando'}, {'path': '/spain/madrid/attractions/plaza-mayor/a/poi-sig/399605/360770', 'name': 'Plaza Mayor'}, {'path': '/spain/madrid/attractions/plaza-de-toros-museo-taurino/a/poi-sig/1205219/360770', 'name': 'Plaza de Toros & Museo Taurino'}, {'path': '/spain/madrid/attractions/basilica-de-san-francisco-el-grande/a/poi-sig/1094816/360770', 'name': 'Basílica de San Francisco El Grande'}]},
# {'cityPath': 'france/paris', 'pois': [{'path': '/france/paris/attractions/musee-du-louvre/a/poi-sig/372123/359279', 'name': 'Musée du Louvre'}, {'path': '/france/paris/attractions/cathedrale-notre-dame-de-paris/a/poi-sig/372127/359279', 'name': 'Cathédrale Notre Dame de Paris'}, {'path': '/france/paris/attractions/jardin-du-luxembourg/a/poi-sig/372163/359279', 'name': 'Jardin du Luxembourg'}, {'path': '/france/paris/attractions/centre-pompidou/a/poi-sig/372153/359279', 'name': 'Centre Pompidou'}, {'path': '/france/paris/attractions/les-catacombes/a/poi-sig/372143/359279', 'name': 'Les Catacombes'}, {'path': '/france/paris/attractions/musee-d-orsay/a/poi-sig/372151/359279', 'name': 'Musée d’Orsay'}, {'path': '/france/paris/attractions/cimetiere-du-pere-lachaise/a/poi-sig/372157/359279', 'name': 'Cimetière du Père Lachaise'}, {'path': '/france/paris/attractions/pantheon/a/poi-sig/1264241/359279', 'name': 'Panthéon'}, {'path': '/france/paris/attractions/musee-rodin/a/poi-sig/372149/359279', 'name': 'Musée Rodin'}]},
# {'cityPath': 'france/nice', 'pois': [{'path': '/france/nice/attractions/vieux-nice/a/poi-sig/1196834/1322981', 'name': 'Vieux Nice'}, {'path': '/france/nice/attractions/promenade-des-anglais/a/poi-sig/1196798/1322981', 'name': 'Promenade des Anglais'}, {'path': '/france/nice/attractions/parc-du-chateau/a/poi-sig/410076/1322981', 'name': 'Parc du Château'}, {'path': '/france/nice/attractions/musee-massena/a/poi-sig/410144/1322981', 'name': 'Musée Masséna'}, {'path': '/france/nice/attractions/musee-d-art-moderne-et-d-art-contemporain/a/poi-sig/1188487/1322981', 'name': 'Musée d’Art Moderne et d’Art Contemporain'}, {'path': '/france/nice/attractions/musee-matisse/a/poi-sig/1196791/1322981', 'name': 'Musée Matisse'}, {'path': '/france/nice/attractions/port-lympia/a/poi-sig/1196848/1322981', 'name': 'Port Lympia'}, {'path': '/france/nice/attractions/musee-national-marc-chagall/a/poi-sig/1196793/1322981', 'name': 'Musée National Marc Chagall'}, {'path': '/france/nice/attractions/cathedrale-orthodoxe-russe-st-nicolas/a/poi-sig/410074/1322981', 'name': 'Cathédrale Orthodoxe Russe St-Nicolas'}]},
# {'cityPath': 'france/provence/marseille', 'pois': [{'path': '/france/provence/marseille/attractions/musee-des-civilisations-de-l-europe-et-de-la-mediterranee/a/poi-sig/1226376/359286', 'name': 'Musée des Civilisations de l’Europe et de la Méditerranée'}, {'path': '/france/provence/marseille/attractions/le-panier/a/poi-sig/1195462/359286', 'name': 'Le Panier'}, {'path': '/france/provence/marseille/attractions/villa-mediterranee/a/poi-sig/1496147/359286', 'name': 'Villa Méditerranée'}, {'path': '/france/provence/marseille/attractions/basilique-notre-dame-de-la-garde/a/poi-sig/399731/359286', 'name': 'Basilique Notre Dame de la Garde'}, {'path': '/france/provence/marseille/attractions/vieux-port/a/poi-sig/1195435/359286', 'name': 'Vieux Port'}, {'path': '/france/provence/marseille/attractions/centre-de-la-vieille-charite/a/poi-sig/399733/359286', 'name': 'Centre de la Vieille Charité'}, {'path': '/france/provence/marseille/attractions/chateau-d-if/a/poi-sig/399735/359286', 'name': 'Château d’If'}, {'path': '/france/provence/marseille/attractions/musee-cantini/a/poi-sig/399743/359286', 'name': 'Musée Cantini'}, {'path': '/france/provence/marseille/attractions/la-cite-radieuse/a/poi-sig/1227036/359286', 'name': 'La Cité Radieuse'}]},
# {'cityPath': 'france/burgundy-and-the-rhone/lyon', 'pois': [{'path': '/france/burgundy-and-the-rhone/lyon/attractions/musee-des-beaux-arts/a/poi-sig/417298/359234', 'name': 'Musée des Beaux-Arts'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/basilique-notre-dame-de-fourviere/a/poi-sig/417258/359234', 'name': 'Basilique Notre Dame de Fourvière'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/lyon-confluence/a/poi-sig/417276/359234', 'name': 'Lyon Confluence'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/musee-des-confluences/a/poi-sig/417300/359234', 'name': 'Musée des Confluences'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/place-des-terreaux/a/poi-sig/417316/359234', 'name': 'Place des Terreaux'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/musees-gadagne/a/poi-sig/1192297/359234', 'name': 'Musées Gadagne'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/parc-de-la-tete-d-or/a/poi-sig/417312/359234', 'name': "Parc de la Tête d'Or"}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/opera-de-lyon/a/poi-sig/417248/359234', 'name': 'Opéra de Lyon'}, {'path': '/france/burgundy-and-the-rhone/lyon/attractions/centre-d-histoire-de-la-resistance-et-de-la-deportation/a/poi-sig/417262/359234', 'name': "Centre d'Histoire de la Résistance et de la Déportation"}]},
# {'cityPath': 'france/provence/avignon', 'pois': [{'path': '/france/provence/avignon/attractions/palais-des-papes/a/poi-sig/418483/359285', 'name': 'Palais des Papes'}, {'path': '/france/provence/avignon/attractions/pont-st-benezet/a/poi-sig/1193710/359285', 'name': 'Pont St-Bénezet'}, {'path': '/france/provence/avignon/attractions/musee-du-petit-palais/a/poi-sig/418475/359285', 'name': 'Musée du Petit Palais'}, {'path': '/france/provence/avignon/attractions/musee-angladon/a/poi-sig/418471/359285', 'name': 'Musée Angladon'}, {'path': '/france/provence/avignon/attractions/place-du-palais/a/poi-sig/1196146/359285', 'name': 'Place du Palais'}, {'path': '/france/provence/avignon/attractions/musee-lapidaire/a/poi-sig/1536129/359285', 'name': 'Musée Lapidaire'}, {'path': '/france/provence/avignon/attractions/collection-lambert/a/poi-sig/1265295/359285', 'name': 'Collection Lambert'}, {'path': '/france/provence/avignon/attractions/musee-calvet/a/poi-sig/418473/359285', 'name': 'Musée Calvet'}, {'path': '/france/provence/avignon/attractions/basilique-st-pierre/a/poi-sig/1512559/359285', 'name': 'Basilique St-Pierre'}]},
# {'cityPath': 'france/southwestern-france/bordeaux', 'pois': [{'path': '/france/southwestern-france/bordeaux/attractions/la-cite-du-vin/a/poi-sig/1537668/359293', 'name': 'La Cité du Vin'}, {'path': '/france/southwestern-france/bordeaux/attractions/miroir-d-eau/a/poi-sig/1537398/359293', 'name': "Miroir d'Eau"}, {'path': '/france/southwestern-france/bordeaux/attractions/musee-du-vin-et-du-negoce/a/poi-sig/1537490/359293', 'name': 'Musée du Vin et du Négoce'}, {'path': '/france/southwestern-france/bordeaux/attractions/musee-d-aquitaine/a/poi-sig/452933/359293', 'name': "Musée d'Aquitaine"}, {'path': '/france/southwestern-france/bordeaux/attractions/musee-des-beaux-arts/a/poi-sig/452937/359293', 'name': 'Musée des Beaux-Arts'}, {'path': '/france/southwestern-france/bordeaux/attractions/musee-d-art-contemporain/a/poi-sig/452923/359293', 'name': "Musée d'Art Contemporain"}, {'path': '/france/southwestern-france/bordeaux/attractions/cathedrale-st-andre/a/poi-sig/1196013/359293', 'name': 'Cathédrale St-André'}, {'path': '/france/southwestern-france/bordeaux/attractions/tour-pey-berland/a/poi-sig/1193620/359293', 'name': 'Tour Pey Berland'}, {'path': '/france/southwestern-france/bordeaux/attractions/musee-des-arts-decoratifs-et-du-design/a/poi-sig/452935/359293', 'name': 'Musée des Arts Décoratifs et du Design'}]},
# {'cityPath': 'france/cote-dazur/cannes', 'pois': [{'path': '/france/cote-dazur/cannes/attractions/la-croisette/a/poi-sig/1227608/359252', 'name': 'La Croisette'}, {'path': '/france/cote-dazur/cannes/attractions/iles-de-lerins/a/poi-sig/1270506/359252', 'name': 'Îles de Lérins'}, {'path': '/france/cote-dazur/cannes/attractions/palais-des-festivals-et-des-congres/a/poi-sig/1188653/359252', 'name': 'Palais des Festivals et des Congrès'}, {'path': '/france/cote-dazur/cannes/attractions/la-malmaison/a/poi-sig/428884/359252', 'name': 'La Malmaison'}, {'path': '/france/cote-dazur/cannes/attractions/vieux-port/a/poi-sig/428900/359252', 'name': 'Vieux Port'}, {'path': '/france/cote-dazur/cannes/attractions/le-suquet/a/poi-sig/1196940/359252', 'name': 'Le Suquet'}, {'path': '/france/cote-dazur/cannes/attractions/hotel-de-ville/a/poi-sig/1251682/359252', 'name': 'Hôtel de Ville'}]},
# {'cityPath': 'france/alsace-and-lorraine/strasbourg', 'pois': [{'path': '/france/alsace-and-lorraine/strasbourg/attractions/cathedrale-notre-dame/a/poi-sig/417553/359225', 'name': 'Cathédrale Notre-Dame'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/palais-rohan/a/poi-sig/417575/359225', 'name': 'Palais Rohan'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/grande-ile/a/poi-sig/417559/359225', 'name': 'Grande Île'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/petite-france/a/poi-sig/417579/359225', 'name': 'Petite France'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/musee-de-l-oeuvre-notre-dame/a/poi-sig/417569/359225', 'name': 'Musée de l’Œuvre Notre-Dame'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/musee-d-art-moderne-et-contemporain/a/poi-sig/1400306/359225', 'name': 'Musée d’Art Moderne et Contemporain'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/grande-mosquee-de-strasbourg/a/poi-sig/1489262/359225', 'name': 'Grande Mosquée de Strasbourg'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/barrage-vauban/a/poi-sig/1262509/359225', 'name': 'Barrage Vauban'}, {'path': '/france/alsace-and-lorraine/strasbourg/attractions/jardin-des-deux-rives/a/poi-sig/417561/359225', 'name': 'Jardin des Deux Rives'}]},
# {'cityPath': 'france/provence/aix-en-provence', 'pois': [{'path': '/france/provence/aix-en-provence/attractions/musee-granet/a/poi-sig/475694/359282', 'name': 'Musée Granet'}, {'path': '/france/provence/aix-en-provence/attractions/caumont-centre-d-art/a/poi-sig/1536084/359282', 'name': 'Caumont Centre d’Art'}, {'path': '/france/provence/aix-en-provence/attractions/cours-mirabeau/a/poi-sig/1229369/359282', 'name': 'Cours Mirabeau'}, {'path': '/france/provence/aix-en-provence/attractions/vieil-aix/a/poi-sig/1195975/359282', 'name': 'Vieil Aix'}, {'path': '/france/provence/aix-en-provence/attractions/camp-des-milles/a/poi-sig/1227619/359282', 'name': 'Camp des Milles'}, {'path': '/france/provence/aix-en-provence/attractions/bastide-du-jas-de-bouffan/a/poi-sig/1227638/359282', 'name': 'Bastide du Jas de Bouffan'}, {'path': '/france/provence/aix-en-provence/attractions/carrieres-de-bibemus/a/poi-sig/1227646/359282', 'name': 'Carrières de Bibemus'}, {'path': '/france/provence/aix-en-provence/attractions/atelier-cezanne/a/poi-sig/475684/359282', 'name': 'Atelier Cézanne'}, {'path': '/france/provence/aix-en-provence/attractions/cathedrale-st-sauveur/a/poi-sig/475686/359282', 'name': 'Cathédrale St-Sauveur'}]},
# {'cityPath': 'france/toulouse', 'pois': [{'path': '/france/toulouse/attractions/cite-de-l-espace/a/poi-sig/1192993/1003054', 'name': 'Cité de l’Espace'}, {'path': '/france/toulouse/attractions/couvent-des-jacobins/a/poi-sig/1192995/1003054', 'name': 'Couvent des Jacobins'}, {'path': '/france/toulouse/attractions/basilique-st-sernin/a/poi-sig/1065219/1003054', 'name': 'Basilique St-Sernin'}, {'path': '/france/toulouse/attractions/place-du-capitole/a/poi-sig/1065217/1003054', 'name': 'Place du Capitole'}, {'path': '/france/toulouse/attractions/musee-des-augustins/a/poi-sig/1065216/1003054', 'name': 'Musée des Augustins'}, {'path': '/france/toulouse/attractions/capitole/a/poi-sig/1065224/1003054', 'name': 'Capitole'}, {'path': '/france/toulouse/attractions/fondation-bemberg/a/poi-sig/1457533/1003054', 'name': 'Fondation Bemberg'}, {'path': '/france/toulouse/attractions/les-abattoirs/a/poi-sig/1065232/1003054', 'name': 'Les Abattoirs'}, {'path': '/france/toulouse/attractions/canal-du-midi/a/poi-sig/1065221/1003054', 'name': 'Canal du Midi'}]}
# ]

def makeUrl(path):
	return ("https://www.lonelyplanet.com" + path)

def getBS(url):
	browser.get(url)
	src = browser.page_source
	bs = BeautifulSoup(src, "lxml")
	return bs

def findOne(bs, tag, className):
	res = bs.find(tag, class_=className)
	return res

def findAll(bs, tag, className):
	res = bs.find_all(tag, class_=className)
	return res

def getInfo(bs):
	Info = {
		"Contact": "",
		"Location": "",
		"Price": "",
		"Hours": "",
	}
	info = findOne(bs, "div", "EssentialInfo")
	if(info):
		items = findAll(info, "section", "SidebarSection")
		for item in items:
			title = item.header.text
			if(title != "Contact"):
				# may have list
				content = item.div.text
			else:
				content = []
				for a in item.find_all("a"):
					content.append(a.text)
			Info[title] = content
	return Info

def getImage(bs):
	img = findOne(bs, "div", "ImageHero")
	imgUrl = ""
	if(img):
		style = img["style"]
		# to parse the image url out of the style
		matchObj = re.search(pattern, style)
		imgUrl = matchObj.group()
	return imgUrl

def getPara(bs):
	res = []
	paras = bs.find_all("p")
	for para in paras:
		res.append(para.text)
	return res

def getSingleInfo(path):
	bs = getBS(makeUrl(path))
	Info = getInfo(bs)
	return Info

def saveJson(fileName, object):
	JSONEncoder().encode(object)
	with open(fileName,"a") as file:
		file.write(dumps(object, file, indent=4))

pois = []

def crawlAll():
	for city in poiByCity:
		try:
			for poi in city["pois"]:
				try:
					print("Getting poi", poi["name"], "...")
					path = poi["path"]
					url = makeUrl(path)
					bs = getBS(url)
					info = getInfo(bs)
					newPoi = {
						"name": poi["name"],
						"cityPath": city["cityPath"],
						"introduction": getPara(bs),
						"imageUrl": getImage(bs),
						"contact": info["Contact"],
						"location": info["Location"],
						"ticket": info["Price"],
						"openTime": info["Hours"]
					}
					saveJson("pois.json", newPoi)
					city["pois"].remove(poi)
				except TimeoutException: # also catch other exception
					continue
				except WebDriverException:
					browser = webdriver.Firefox()
					continue
			#poiByCity.remove(city) # remove city when all pois are crawled
		except TimeoutException:
			continue
		except WebDriverException:
			browser = webdriver.Firefox()
			continue

pattern = 'lonelyplanetimages\.imgix\.net\/.*\.jpg'


browser = webdriver.Firefox()
crawlAll()