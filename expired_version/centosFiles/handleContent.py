#!/usr/bin/python
# -*- coding: UTF-8 -*-
#@filename:handleContent.py
#@author: wheee/RenjiaLu
#@time:2018.04.20
#@description:  handle content (save openId,config ) from msg and return a msg

import ConfigParser
import time
import random
import json
import os,sys
import requests
reload(sys) 
sys.setdefaultencoding('utf-8')



#类
class GlobalValue :

	#[座位标号：坐标],不同学校的座位表不同
	R1_BJTU={
	#第一自习室座位编码 		252 个
	 '1':'39,20','10':'37,23','100':'7,21','101':'8,21','102':'10,21','103':'10,20','104':'8,20','105':'7,20','106':'5,20','107':'7,13','108':'8,12','109':'9,11','11':'36,23','110':'10,10','111':'11,9','112':'16,6','113':'16,8','114':'16,9','115':'16,11','116':'16,12','117':'16,14','118':'17,14','119':'17,12','12':'34,23','120':'17,11','121':'17,9','122':'17,8','123':'17,6','124':'19,6','125':'19,8','126':'19,9','127':'19,11','128':'19,12','129':'19,14','13':'34,24','130':'20,14','131':'20,12','132':'20,11','133':'20,9','134':'20,8','135':'20,6','136':'22,6','137':'22,8','138':'22,9','139':'22,11','14':'36,24','140':'22,12','141':'22,14','142':'23,14','143':'23,12','144':'23,11','145':'23,9','146':'23,8','147':'23,6','148':'25,6','149':'25,8','15':'37,24','150':'25,9','151':'25,11','152':'25,12','153':'25,14','154':'26,14','155':'26,12','156':'26,11','157':'26,9','158':'26,8','16':'39,24','160':'31,20','161':'29,20','162':'28,20','163':'26,20','164':'25,20','165':'23,20','166':'22,20','167':'20,20','168':'17,20','169':'15,20','17':'39,26','170':'14,20','171':'12,20','172':'12,21','173':'14,21','174':'15,21','175':'17,21','176':'20,21','177':'22,21','178':'23,21','179':'25,21','18':'37,26','180':'26,21','181':'28,21','182':'29,21','183':'31,21','184':'31,23','185':'29,23','186':'28,23','187':'26,23','188':'25,23','189':'23,23','19':'36,26','190':'22,23','191':'20,23','192':'17,23','193':'15,23','194':'14,23','195':'12,23','196':'12,24','197':'14,24','198':'15,24','199':'17,24','2':'37,20','20':'34,26','200':'20,24','201':'22,24','202':'23,24','203':'25,24','204':'26,24','205':'28,24','206':'29,24','207':'31,24','208':'31,26','209':'29,26','21':'34,27','210':'28,26','211':'26,26','212':'25,26','213':'23,26','214':'22,26','215':'20,26','216':'17,26','217':'15,26','218':'14,26','219':'12,26','22':'36,27','220':'12,27','221':'14,27','222':'15,27','223':'17,27','224':'20,27','225':'22,27','226':'23,27','227':'25,27','228':'26,27','229':'28,27','23':'37,27','230':'29,27','231':'31,27','232':'31,29','233':'29,29','234':'28,29','235':'26,29','236':'25,29','237':'23,29','238':'22,29','239':'20,29','24':'39,27','240':'17,29','241':'15,29','242':'14,29','243':'12,29','244':'14,30','245':'15,30','246':'17,30','247':'20,30','248':'22,30','249':'23,30','25':'39,29','250':'25,30','251':'26,30','252':'28,30','253':'29,30','26':'37,29','27':'36,29','28':'34,29','29':'34,30','3':'36,20','30':'36,30','31':'37,30','32':'39,30','33':'37,37','34':'36,38','35':'35,39','36':'34,40','37':'33,41','38':'26,44','39':'26,42','4':'34,20','40':'26,41','41':'26,39','42':'25,39','43':'25,41','44':'25,42','45':'25,44','46':'23,44','47':'23,42','48':'23,41','49':'23,39','5':'34,21','50':'22,39','51':'22,41','52':'22,42','53':'22,44','54':'20,44','55':'20,42','56':'20,41','57':'20,39','58':'19,39','59':'19,41','6':'36,21','60':'19,42','61':'19,44','62':'17,44','63':'17,42','64':'17,41','65':'17,39','66':'16,39','67':'16,41','68':'16,42','69':'16,44','7':'37,21','70':'11,41','71':'10,40','72':'9,39','73':'8,38','74':'7,37','75':'5,30','76':'7,30','77':'8,30','78':'10,30','79':'10,29','8':'39,21','80':'8,29','81':'7,29','82':'5,29','83':'5,27','84':'7,27','85':'8,27','86':'10,27','87':'10,26','88':'8,26','89':'7,26','9':'39,23','90':'5,26','91':'5,24','92':'7,24','93':'8,24','94':'10,24','95':'10,23','96':'8,23','97':'7,23','98':'5,23','99':'5,21'
	}
	R2_BJTU={
		#第二自习室座位编码		203  个 
		'1':'33,24','10':'29,25','100':'9,30','101':'9,31','102':'7,24','103':'7,25','104':'7,26','105':'7,27','106':'7,28','107':'7,29','108':'7,30','109':'7,31','11':'29,26','110':'4,28','111':'3,28','112':'3,26','113':'4,26','114':'4,24','115':'3,24','116':'3,22','117':'4,22','118':'4,20','119':'3,20','12':'29,27','120':'3,18','121':'4,18','122':'7,20','123':'7,19','124':'7,18','125':'7,17','126':'7,16','127':'7,15','128':'9,15','129':'9,16','13':'29,28','130':'9,17','131':'9,18','132':'9,19','133':'9,20','134':'11,20','135':'11,19','136':'11,18','137':'11,17','138':'11,16','139':'11,15','14':'29,29','140':'13,15','141':'13,16','142':'13,17','143':'13,18','144':'13,19','145':'13,20','146':'19,20','147':'19,19','148':'19,18','149':'19,17','15':'29,30','150':'19,16','151':'19,15','152':'19,14','153':'19,13','154':'19,12','155':'19,11','156':'21,11','157':'21,12','158':'21,13','159':'21,14','16':'29,31','160':'21,15','161':'21,16','162':'21,17','163':'21,18','164':'21,19','165':'21,20','166':'23,20','167':'23,19','168':'23,18','169':'23,17','17':'29,32','170':'23,16','171':'23,15','172':'23,14','173':'23,13','174':'23,12','175':'23,11','176':'25,11','177':'25,12','178':'25,13','179':'25,14','18':'29,33','180':'25,15','181':'25,16','182':'25,17','183':'25,18','184':'25,19','185':'25,20','186':'27,20','187':'27,19','188':'27,18','189':'27,17','19':'27,33','190':'27,16','191':'27,15','192':'29,15','193':'29,16','194':'29,17','195':'29,18','196':'29,19','197':'29,20','198':'31,20','199':'31,19','2':'33,25','20':'27,32','200':'33,19','201':'33,20','202':'21,24','203':'19,24','21':'27,31','22':'27,30','23':'27,29','24':'27,28','25':'27,27','26':'27,26','27':'27,25','28':'27,24','29':'25,24','3':'33,28','30':'25,25','31':'25,26','32':'25,27','33':'25,28','34':'25,29','35':'25,30','36':'25,31','37':'25,32','38':'25,34','39':'25,35','4':'33,29','40':'23,35','41':'23,34','42':'23,33','43':'23,32','44':'23,31','45':'23,30','46':'23,29','47':'23,28','48':'23,27','49':'23,26','5':'31,29','50':'23,25','51':'23,24','52':'21,25','53':'21,26','54':'21,27','55':'21,28','56':'21,29','57':'21,30','58':'21,31','59':'21,32','6':'31,28','60':'21,33','61':'21,34','62':'21,35','63':'19,35','64':'19,34','65':'19,33','66':'19,32','67':'19,31','68':'19,30','69':'19,29','7':'31,25','70':'19,28','71':'19,27','72':'19,26','73':'19,25','74':'13,24','75':'13,25','76':'13,26','77':'13,27','78':'13,28','79':'13,29','8':'31,24','80':'13,30','81':'13,31','82':'13,32','83':'13,33','84':'11,33','85':'11,32','86':'11,31','87':'11,30','88':'11,29','89':'11,28','9':'29,24','90':'11,27','91':'11,26','92':'11,25','93':'11,24','94':'9,24','95':'9,25','96':'9,26','97':'9,27','98':'9,28','99':'9,29'
	}
		#[自习室编号:服务器代号]
	#DICT_ROOMKV_BJTU={"ROOM_1":"323","ROOM_2":"324"}
	DICT_ROOMKV_BJTU={"1":"323","2":"324"}

	#蚌埠医学院
	R1_BMC = {
	'344':'28,43', '345':'30,41', '346':'30,42', '347':'30,43', '340':'26,42', '341':'26,43', '342':'28,41', '343':'28,42', '348':'32,41', '349':'32,42', '298':'46,33', '299':'48,30', '296':'46,31', '297':'46,32', '294':'44,33', '295':'46,30', '292':'44,31', '293':'44,32', '290':'42,33', '291':'44,30', '199':'10,34', '198':'10,33', '195':'10,30', '194':'8,34', '197':'10,32', '196':'10,31', '191':'8,31', '190':'8,30', '193':'8,33', '192':'8,32', '270':'34,35', '271':'36,30', '272':'36,31', '273':'36,32', '274':'36,33', '275':'36,34', '276':'36,35', '277':'38,30', '278':'38,31', '279':'38,32', '108':'7,21', '109':'9,19', '102':'54,12', '103':'5,19', '100':'53,12', '101':'54,10', '106':'7,19', '107':'7,20', '104':'5,20', '105':'5,21', '39':'52,6', '38':'37,8', '33':'35,6', '32':'33,8', '31':'33,6', '30':'32,8', '37':'37,6', '36':'36,8', '35':'36,6', '34':'35,8', '339':'26,41', '338':'24,43', '335':'22,43', '334':'22,42', '337':'24,42', '336':'24,41', '331':'20,42', '330':'20,41', '333':'22,41', '332':'20,43', '6':'13,8', '99':'53,10', '98':'52,12', '91':'48,11', '90':'46,13', '93':'48,13', '92':'48,12', '95':'50,12', '94':'50,11', '97':'52,10', '96':'50,13', '238':'24,33', '239':'24,34', '234':'22,35', '235':'24,30', '236':'24,31', '237':'24,32', '230':'22,31', '231':'22,32', '232':'22,33', '233':'22,34', '1':'5,7', '146':'41,20', '147':'41,21', '144':'39,21', '145':'41,19', '142':'39,19', '143':'39,20', '140':'37,20', '141':'37,21', '148':'43,19', '149':'43,20', '133':'31,19', '132':'29,20', '131':'29,19', '130':'27,19', '137':'35,19', '136':'33,20', '135':'33,19', '134':'31,20', '139':'37,19', '138':'35,20', '24':'28,8', '25':'29,6', '26':'29,8', '27':'30,6', '20':'25,8', '21':'26,6', '22':'26,8', '23':'28,6', '28':'30,8', '29':'32,6', '379':'52,42', '378':'52,41', '371':'46,43', '370':'46,42', '373':'48,42', '372':'48,41', '375':'50,41', '374':'48,43', '377':'50,43', '376':'50,42', '88':'44,13', '89':'46,12', '82':'37,13', '83':'39,12', '80':'35,13', '81':'37,12', '86':'41,13', '87':'44,12', '84':'39,13', '85':'41,12', '7':'14,6', '245':'26,34', '244':'26,33', '247':'28,30', '246':'26,35', '241':'26,30', '240':'24,35', '243':'26,32', '242':'26,31', '249':'28,32', '248':'28,31', '179':'4,30', '178':'3,32', '177':'3,30', '176':'2,32', '175':'2,30', '174':'54,16', '173':'54,14', '172':'53,16', '171':'53,14', '170':'52,16', '182':'3,36', '183':'4,34', '180':'4,32', '181':'3,34', '186':'6,31', '187':'6,32', '184':'4,36', '185':'6,30', '188':'6,33', '189':'6,34', '11':'18,6', '10':'15,8', '13':'19,6', '12':'18,8', '15':'21,6', '14':'19,8', '17':'22,6', '16':'21,8', '19':'25,6', '18':'22,8', '62':'19,12', '322':'14,42', '323':'14,43', '320':'12,43', '321':'14,41', '326':'16,43', '327':'18,41', '324':'16,41', '325':'16,42', '328':'18,42', '329':'18,43', '201':'12,30', '200':'10,35', '203':'12,32', '202':'12,31', '205':'12,34', '204':'12,33', '207':'14,30', '206':'12,35', '209':'14,32', '208':'14,31', '77':'33,12', '76':'31,13', '75':'31,12', '74':'29,13', '73':'29,12', '72':'27,13', '71':'27,12', '70':'25,13', '79':'35,12', '78':'33,13', '2':'5,8', '8':'14,8', '68':'23,13', '120':'17,20', '121':'19,19', '122':'19,20', '123':'21,19', '124':'21,20', '125':'23,19', '126':'23,20', '127':'25,19', '128':'25,20', '129':'27,20', '69':'25,12', '319':'12,42', '318':'12,41', '313':'8,42', '312':'8,41', '311':'6,43', '310':'6,42', '317':'10,43', '316':'10,42', '315':'10,41', '314':'8,43', '3':'7,7', '368':'44,43', '369':'46,41', '366':'44,41', '367':'44,42', '364':'42,42', '365':'42,43', '362':'40,43', '363':'42,41', '360':'40,41', '361':'40,42', '380':'52,43', '381':'54,41', '382':'54,42', '383':'54,43', '384':'56,41', '385':'56,42', '386':'56,43', '60':'17,13', '61':'17,14', '258':'30,35', '259':'32,30', '64':'19,14', '65':'21,12', '66':'21,13', '67':'23,12', '252':'28,35', '253':'30,30', '250':'28,33', '251':'28,34', '256':'30,33', '257':'30,34', '254':'30,31', '255':'30,32', '168':'50,21', '169':'52,14', '164':'48,20', '165':'48,21', '166':'50,19', '167':'50,20', '160':'50,15', '161':'50,16', '162':'50,17', '163':'48,19', '9':'15,6', '357':'38,41', '356':'36,43', '355':'36,42', '354':'36,41', '353':'34,43', '352':'34,42', '351':'34,41', '350':'32,43', '359':'38,43', '358':'38,42', '216':'16,33', '217':'16,34', '214':'16,31', '215':'16,32', '212':'14,35', '213':'16,30', '210':'14,33', '211':'14,34', '218':'16,35', '219':'18,30', '289':'42,32', '288':'42,31', '4':'7,8', '281':'38,34', '280':'38,33', '283':'40,31', '282':'40,30', '285':'40,33', '284':'40,32', '287':'42,30', '286':'40,34', '263':'32,34', '262':'32,33', '261':'32,32', '260':'32,31', '267':'34,32', '266':'34,31', '265':'34,30', '264':'32,35', '269':'34,34', '268':'34,33', '59':'17,12', '58':'15,14', '55':'13,14', '54':'13,13', '57':'15,13', '56':'15,12', '51':'11,13', '50':'9,14', '53':'13,12', '52':'11,14', '柱':'23,7', '63':'19,13', '115':'13,21', '114':'13,20', '117':'15,20', '116':'15,19', '111':'11,19', '110':'9,20', '113':'13,19', '112':'11,20', '119':'17,19', '118':'15,21', '308':'4,40', '309':'6,41', '300':'48,31', '301':'48,32', '302':'48,33', '303':'2,38', '304':'2,40', '305':'3,38', '306':'3,40', '307':'4,38', '229':'22,30', '228':'20,34', '227':'20,33', '226':'20,32', '225':'20,31', '224':'20,30', '223':'18,34', '222':'18,33', '221':'18,32', '220':'18,31', '151':'45,19', '150':'43,21', '153':'45,21', '152':'45,20', '155':'47,20', '154':'47,19', '157':'48,15', '156':'47,21', '159':'48,17', '158':'48,16', '48':'7,14', '49':'9,13', '46':'5,14', '47':'7,13', '44':'54,8', '45':'5,13', '42':'53,8', '43':'54,6', '40':'52,8', '41':'53,6', '5':'13,6'
	}
	R2_BMC = {
	'216':'12,33', '217':'12,34', '214':'10,40', '215':'10,41', '212':'10,38', '213':'10,39', '210':'10,36', '211':'10,37', '264':'22,36', '265':'22,37', '218':'12,35', '219':'12,36', '133':'6,21', '132':'6,20', '131':'6,19', '130':'6,18', '137':'8,19', '136':'8,18', '135':'8,17', '134':'6,22', '95':'30,4', '139':'8,21', '138':'8,20', '225':'14,33', '24':'12,6', '25':'12,7', '250':'18,40', '224':'12,41', '20':'10,11', '21':'10,12', '22':'12,4', '23':'12,5', '223':'12,40', '28':'12,10', '29':'12,11', '222':'12,39', '289':'28,34', '288':'28,33', '221':'12,38', '281':'26,35', '280':'26,34', '283':'26,37', '220':'12,37', '285':'26,39', '284':'26,38', '287':'26,41', '286':'26,40', '87':'26,10', '227':'14,35', '120':'38,7', '121':'38,8', '122':'38,9', '123':'40,4', '124':'40,5', '125':'40,6', '126':'40,7', '127':'40,8', '128':'40,9', '129':'6,17', '269':'22,41', '268':'22,40', '66':'20,12', '91':'28,7', '59':'20,5', '58':'20,4', '55':'18,10', '54':'18,9', '57':'18,12', '56':'18,11', '51':'18,6', '276':'24,39', '53':'18,8', '52':'18,7', '柱':'17,23', '63':'20,9', '298':'30,34', '299':'30,35', '296':'28,41', '297':'30,33', '294':'28,39', '295':'28,40', '292':'28,37', '293':'28,38', '290':'28,35', '291':'28,36', '85':'26,8', '201':'8,36', '319':'34,37', '318':'34,36', '199':'8,34', '198':'8,33', '200':'8,35', '195':'6,39', '194':'6,38', '197':'6,41', '196':'6,40', '191':'6,35', '190':'6,34', '193':'6,37', '192':'6,36', '115':'36,6', '114':'36,5', '117':'38,4', '116':'36,7', '111':'34,6', '110':'34,5', '113':'36,4', '112':'34,7', '278':'24,41', '205':'8,40', '313':'32,40', '5':'6,10', '119':'38,6', '118':'38,5', '84':'26,7', '204':'8,39', '251':'18,41', '207':'10,33', '256':'20,37', '206':'8,41', '226':'14,34', '257':'20,38', '27':'12,9', '3':'6,8', '254':'20,35', '7':'8,6', '312':'32,39', '92':'28,8', '255':'20,36', '308':'32,35', '309':'32,36', '300':'30,36', '301':'30,37', '302':'30,38', '303':'30,39', '304':'30,40', '26':'12,8', '306':'32,33', '305':'30,41', '245':'18,35', '244':'18,34', '108':'32,10', '109':'34,4', '241':'16,40', '240':'16,39', '243':'18,33', '242':'16,41', '102':'32,4', '103':'32,5', '100':'30,9', '101':'30,10', '106':'32,8', '107':'32,9', '104':'32,6', '105':'32,7', '39':'14,12', '38':'14,11', '33':'14,6', '32':'14,5', '270':'24,33', '30':'12,12', '37':'14,10', '247':'18,37', '35':'14,8', '34':'14,7', '246':'18,36', '88':'28,4', '窗':'40,50', '8':'8,7', '282':'26,36', '252':'20,33', '72':'22,9', '271':'24,34', '86':'26,9', '70':'22,7', '330':'40,41', '60':'20,6', '61':'20,7', '258':'20,39', '259':'20,40', '64':'20,10', '65':'20,11', '179':'34,21', '178':'34,20', '177':'34,19', '176':'32,22', '175':'32,21', '174':'32,20', '173':'30,22', '172':'30,21', '171':'30,20', '170':'28,22', '203':'8,38', '96':'30,5', '69':'22,6', '249':'18,39', '253':'20,34', '248':'18,38', '182':'36,20', '183':'36,21', '180':'34,22', '181':'36,19', '186':'38,20', '187':'40,19', '184':'36,22', '185':'38,19', '188':'40,20', '189':'6,33', '311':'32,38', '202':'8,37', '4':'6,9', '310':'32,37', '97':'30,6', '83':'26,6', '317':'34,35', '6':'6,11', '315':'34,33', '316':'34,34', '99':'30,8', '98':'30,7', '168':'28,20', '169':'28,21', '229':'14,37', '228':'14,36', '164':'24,22', '165':'26,20', '166':'26,21', '167':'26,22', '160':'22,21', '161':'22,22', '162':'24,20', '163':'24,21', '11':'8,10', '10':'8,9', '13':'10,4', '12':'8,11', '15':'10,6', '14':'10,5', '17':'10,8', '16':'10,7', '19':'10,10', '18':'10,9', '314':'32,41', '272':'24,35', '93':'28,9', '273':'24,36', '274':'24,37', '31':'14,4', '275':'24,38', '151':'16,21', '150':'16,20', '153':'18,20', '152':'16,22', '155':'18,22', '154':'18,21', '157':'20,21', '156':'20,20', '159':'22,20', '158':'20,22', '62':'20,8', '277':'24,40', '36':'14,9', '82':'26,5', '322':'36,34', '90':'28,6', '238':'16,37', '239':'16,38', '279':'26,33', '234':'16,33', '235':'16,34', '236':'16,35', '237':'16,36', '230':'14,38', '231':'14,39', '232':'14,40', '233':'14,41', '81':'26,4', '48':'16,12', '49':'18,4', '46':'16,10', '47':'16,11', '44':'16,8', '45':'16,9', '42':'16,6', '43':'16,7', '40':'16,4', '41':'16,5', '1':'6,6', '323':'36,35', '320':'34,38', '321':'36,33', '326':'36,38', '327':'38,40', '324':'36,36', '325':'36,37', '9':'8,8', '328':'38,41', '329':'40,40', '146':'12,22', '147':'14,20', '144':'12,20', '145':'12,21', '142':'10,21', '143':'10,22', '140':'8,22', '141':'10,20', '209':'10,35', '208':'10,34', '307':'32,34', '148':'14,21', '149':'14,22', '77':'24,7', '76':'24,6', '75':'24,5', '74':'24,4', '73':'22,10', '50':'18,5', '71':'22,8', '68':'22,5', '94':'28,10', '79':'24,9', '78':'24,8', '2':'6,7', '263':'22,35', '80':'24,10', '262':'22,34', '261':'22,33', '89':'28,5', '260':'20,41', '267':'22,39', '67':'22,4', '266':'22,38' 
	}
	DICT_ROOMKV_BMC={"1":"176","2":"175"}

	DICT_SCHOOL={"BJTU":{
					"1":{"ROOMVALUE":"323","SEATVALUE":R1_BJTU},
					"2":{"ROOMVALUE":"324","SEATVALUE":R2_BJTU}
					},
				"BBMC":{
					"1":{"ROOMVALUE":"176","SEATVALUE":R1_BMC},
					"2":{"ROOMVALUE":"175","SEATVALUE":R2_BMC}
					}
				}

	def __init__(self):
		pass

mheaders =  {
'Host':	'wechat.v2.traceint.com',
'User-Agent':	'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.5.1280(0x26060536) NetType/WIFI Language/zh_CN',
'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
'Accept-Encoding':	'gzip, deflate',
'Accept-Language':	'zh-CN,en-US;q=0.8'
}
mcookies = dict(FROM_TYPE="weixin" ,wechatSESS_ID="35421io3v7cobh00d0cmu315p7",
	Hm_lvt_7ecd21a13263a714793f376c18038a87="1521734275,1524209281",
	Hm_lpvt_7ecd21a13263a714793f376c18038a87=str(int(time.time())))

ADMINOPENID = "qwertsfdadfghdsadfghgfdgsfad"

CONFIG_NAME = "RSconf.ini"
#section标签为：[openIdConf_2018-04-08]
LST_INSTR = ["#抢座","#取消任务","#CONFIG","#帮助","抢座","取消任务","CONFIG","帮助"]
HELP_INFO = "按以下格式发送消息添加任务即可帮您在开放预约的那一刻完成抢座! \
\n(以中/英文逗号或空格分隔)指令格式：\
\n#抢座，[sessid]，[学校英文简称],[几号自习室]，[几号座位]，... \
\n例如：\n#抢座，1u68vgH892ugal3P，BBMC,1，80,2,81  \
\n\n表示的意思：蚌埠医学院的1号自习室80号座位，备选是2号自习室的81号座位了\n回复[#取消任务]即可取消添加的任务 \
\n\n注意：sessionid时间越长越容易失效，建议在抢座时间前30分钟获取sessionid\
\n其他帮助：[sessid是什么？怎么获取？] http://mp.weixin.qq.com/s/3kxk4ByEAbHxb5bfz45MHA\n[代码已开源,项目地址]https://github.com/RenjiaLu9527/igotolibrary"

#返回信息
def replyMsg(str_flg,str_info):
	if str_flg == "ROBOT" :
		if str_info.find("抢座") >= 0 or str_info.find("帮助") >= 0  :
			return HELP_INFO
		#图灵机器人
		api_url = 'http://www.tuling123.com/openapi/api'
		apikey = 'APIKey'
		data = {'key': '3869ab82cc41ffa457e7799c88609',
					'info': str_info}
		req = requests.post(api_url, data=data).text
		replys = json.loads(req,encoding="UTF-8")['text']

		return replys
	elif str_flg == "RIGHT" :
		return str_info
	elif str_flg == "ERROR" :
		return str_info
	else:
		return u"#[E]: 致命错误!"



#保存用户添加的任务信息
def addTask(openId,list_content):

	gv = GlobalValue()
	try:

		#验证 MsgContent 长度是否为偶数 list_content =[35421io3v7cobh00d0cmu315p7,bbmc,2,33,1,181]
		if len(list_content) % 2 !=0 :
			#消息格式不正确
			return replyMsg("ERROR",u"#指令格式不正确.")
 
		#验证学校名称是否存在
		schoolname = list_content[1].upper()
		if gv.DICT_SCHOOL.has_key(schoolname) :
			pass
		else:
			print(u"[I]: 学校名称 %s 不匹配或不支持该学校."%schoolname)
			return replyMsg("ERROR",u"学校名称 %s 不匹配或不支持该学校."%schoolname)

		mcookies["wechatSESS_ID"] = list_content[0]
		rs = requests.Session()
		
		url_zuowei ="http://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat"
		try:
			respone=rs.get(url_zuowei,timeout=1,headers=mheaders,cookies=mcookies)
		except Exception as e:
			print(u"#[E]: sessId验证出错 %s"%repr(e))
			return replyMsg("ERROR",u"#sessId验证出错，请重试.")
		else:
			if (respone.status_code == 200 ) :
				print(u"#[I]:  sessId验证成功-状态码：%5d"% respone.status_code+"\n")
			else:
				print(u"#[I]:  sessId验证失败-状态码：%5d"% respone.status_code+"\n")
				# print(respone.text)
				# print(respone.url)
				return replyMsg("ERROR",u"#sessId无效，请重试！")

		conf=ConfigParser.ConfigParser()
		conf.read(CONFIG_NAME)
		#验证配置文件格式
		todaySection = "openIdConf_%s"%time.strftime('%Y-%m-%d',time.localtime(time.time()))
		if todaySection not in conf.sections() :
			conf.add_section(todaySection)
		#若此openid已经添加过任务了，则会覆盖原来的任务
		conf.set(todaySection, openId, ",".join(list_content)) # 修改指定section 的option
		conf.write(open(CONFIG_NAME, 'w+'))

	except Exception as e:
		print(u"#[E]: addTask()函数出错 %s"%repr(e))
		return replyMsg("ERROR",u"#系统出错,[I]: addTask.请联系管理员反馈.")
	else:
		i=0
		tmpstr = ""
		list_content.remove(list_content[0]) #移除sessionid
		list_content.remove(list_content[0]) #移除学校简称
		for xstr in list_content:
			tmpstr = tmpstr + (("第"+xstr+"自习室") if i % 2 == 0 else (xstr+"号座位 - "))
			i = i + 1
		tmpstr = schoolname+" 的"+tmpstr
		return replyMsg("RIGHT",u"#抢座任务信息:\n[%s] \n\n预定任务添加成功."%tmpstr)
	finally:
		pass

#取消某个用户的任务
def cancelTask(openId):
	todaySection = "openIdConf_%s"%time.strftime('%Y-%m-%d',time.localtime(time.time()))
	try:
		#准备时间-读取配置文件
		conf = ConfigParser.ConfigParser()
		conf.read(CONFIG_NAME)
		if openId in conf.options(todaySection) : # 某个域下的所有key
			conf.remove_option(todaySection,openId) #删除某个section下面的某个key和value
			conf.write(open(CONFIG_NAME, 'w+'))
			return replyMsg("RIGHT",u"#好的，任务已取消.")
		else:
			return replyMsg("ERROR",u"#任务取消失败，您还未添加过任务.")
	except Exception as e:
		print(u"#[E]: cancelTask()函数出错 %s"%repr(e))
		return replyMsg("ERROR",u"#系统出错,[I]: cancelTask.请联系管理员反馈.")

#返回当前配置信息
def getAdminConfig():
	todaySection = "openIdConf_%s"%time.strftime('%Y-%m-%d',time.localtime(time.time()))
	try:
		#准备时间-读取配置文件
		conf = ConfigParser.ConfigParser()
		conf.read(CONFIG_NAME)       # 文件路径
		list_tmp = conf.items(todaySection)# 返回openId_wechatSESS_ID标签项下面的键值对 list
		dict_openID_SESSID = dict(list_tmp)#user1openid = 35421io3v7cobh00d0cmu315p7,bbmc,2,33,1,181
		return replyMsg("RIGHT",u"当前共 %d 个任务\n列表如下：%s"%(len(dict_openID_SESSID),str(dict_openID_SESSID)))
	except Exception as e:
		print(u"#[E]: getAdminConfig()函数出错 %s"%repr(e))
		return replyMsg("ERROR",u"#系统出错,[I]: getAdminConfig.请联系管理员反馈.")


#分析原始的Content，判断是否为指令，再调用相应的函数
#MsgContent 的格式：" #抢座 ，sessid , 1    ，123 ,     2    ，189  "
def parseContent(openId,MsgContent):
	#由于配置文件内容全部为小写
	openId = openId.lower()
	try:
		#抢座，35421io3v7cobh00d0cmu315p7, bbMc,2，33, 1，   181
		list_content = (MsgContent.replace(","," ").replace("，"," ").replace("."," ")\
			.replace(":"," ").replace("一","1").replace("二","2").replace("坐","座").strip()).split()
		if len(list_content) < 1 or list_content[0] not in LST_INSTR:
			#不是指令，调用图灵机器人
			return replyMsg("ROBOT",MsgContent)
		else:
			#删除'#抢座' 、 '#取消任务'等指令字符串
			instr_flg = list_content[0]
			list_content.remove(list_content[0])
			if instr_flg.find("抢座") >= 0 :
				return addTask(openId,list_content)

			elif instr_flg.find("取消任务") >= 0 :
				return cancelTask(openId)
			elif instr_flg.find("帮助") >= 0 :
				return HELP_INFO

			elif instr_flg.find("CONFIG") >= 0 and openId == ADMINOPENID :
				#指令来至管理员 :
				return getAdminConfig()
			else:
				#理论上这里 会运行
				return replyMsg("ROBOT",MsgContent)
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass

