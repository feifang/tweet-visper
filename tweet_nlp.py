#!/usr/bin/env python

# Written by Karen Fang - karen.feifang@gmail.com
# A tool for parsing tweets, part-of-speech tagging and performing sentiment analysis on tweets

# Revision history: 
# 2016/04/11 - tokenization, extract some Emoji and save as entities
# 2016/04/12 - added more Emoji and sentiment functionality

import json
import string
import re
from pattern.en import tag
from pattern.en import sentiment
from twokenize import normalizeTextForTagger, tokenizeRawTweetText, squeezeWhitespace
from tweet_reducer import save_json_to_file
from tweet_trending import load_json_from_file


filename = 'Springbreak_All_0303_0405_sim'
data = '../pro_data/Springbreak_All_0303_0405_sim.json'
outpath = '../pro_data/'

# Todo: add all other emoji to the list
# emoji retrieved from https://www.piliapp.com/twitter-symbols/
people1 = u"😄😃😀😊😉😍😘😚😗😙😜😝😛😳😁😔😌😒😞😣😢😂😭😪😥😰😅😓😩😫😨😱😠😡😤😖😆😋😷😎😴😵😲😟😦😧😈👿😮😬😐😕😯😶😇😏😑👲👳"
people2 = u"👮👷💂👶👦👧👨👩👴👵👱👼👸😺😸😻😽😼🙀😿😹😾👹👺🙈🙉🙊💀👽💩🔥🌟💫💥💢💦💧💤💨👂👀👃👅👄👍👎👌👊👋👐👆👇👉👈🙌🙏"
people3 = u"👏💪🚶🏃💃👫👪👬👭💏💑👯🙆🙅💁🙋💆💇💅👰🙎🙍🙇🎩👑👒👟👞👡👠👢👕👔👚👗🎽👖👘👙💼👜👝👛👓🎀🌂💄💛💙💜💚💔💗💓💕💖💞💘💌💋💍💎👤👥💬👣💭🖖"
people_8 = u"👨‍👩‍👦👨‍👩‍👧👩‍👩‍👦👩‍👩‍👧👨‍👨‍👦👨‍👨‍👧👩‍❤️‍👩👨‍❤️‍👨"
people_11 = "👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👩‍👧‍👦👩‍👩‍👦‍👦👩‍👩‍👧‍👧👨‍👨‍👧‍👦👨‍👨‍👦‍👦👨‍👨‍👧‍👧👩‍❤️‍💋‍👩👨‍❤️‍💋‍👨"
people_single = u"☺✨✊✌✋☝❤"
animals = u"🐶🐺🐱🐭🐹🐰🐸🐯🐨🐻🐷🐽🐮🐗🐵🐒🐴🐑🐘🐼🐧🐦🐤🐥🐣🐔🐍🐢🐛🐝🐜🐞🐌🐙🐚🐠🐟🐬🐳🐋🐄🐏🐀🐃🐅🐇🐉🐎🐐🐓🐕🐖🐁🐂🐲🐡🐊🐫🐪🐆🐈🐩🐾"
nature = u"💐🌸🌷🍀🌹🌻🌺🍁🍃🍂🌿🌾🍄🌵🌴🌲🌳🌰🌱🌼🌐🌞🌝🌚🌑🌒🌓🌔🌕🌖🌗🌘🌜🌛🌙🌍🌎🌏🌋🌌🌠🌀🌁🌈🌊"
nature_single = u"⭐☀⛅☁⚡☔❄⛄"
colors = u"🏻🏼🏽🏾🏿"
object1 = u"🎍💝🎎🎒🎓🎏🎆🎇🎐🎑🎃👻🎅🎄🎁🎋🎉🎊🎈🎌🔮🎥📷📹📼💿📀💽💾💻📱📞📟📠📡📺📻🔊🔉🔈🔇🔔🔕📢📣🔓🔒🔏🔐🔑🔎💡🔦🔆🔅"
object2 = u"🔌🔋🔍🛁🛀🚿🚽🔧🔩🔨🚪🚬💣🔫🔪💊💉💰💴💵💷💶💳💸📲📧📥📤📩📨📯📫📪📬📭📮📦📝📄📃📑📊📈📉📜📋📅📆📇📁📂📌📎📏📐📕"
object3 = u"📗📘📙📓📔📒📚📖🔖📛🔬🔭📰🎨🎬🎤🎧🎼🎵🎶🎹🎻🎺🎷🎸👾🎮🃏🎴🀄🎲🎯🏈🏀🎾🎱🏉🎳🚵🚴🏁🏇🏆🎿🏂🏊🏄🎣🍵🍶🍼🍺🍻🍸🍹🍷"
object_single = u"☎⏳⌛⏰⌚✉✂✒✏⚽⚾⛳☕"
food = u"🍴🍕🍔🍟🍗🍖🍝🍛🍤🍱🍣🍥🍙🍘🍚🍜🍲🍢🍡🍳🍩🍞🍮🍦🍨🍧🎂🍰🍪🍫🍬🍭🍯🍎🍏🍊🍋🍇🍉🍓🍑🍈🍌🍐🍍🍠🍆🍅🌽"
place1 = u"🏠🏡🏫🏢🏣🏥🏦🏪🏩🏨💒🏬🏤🌇🌆🏯🏰🏭🗼🗾🗻🌄🌅🌃🗽🌉🎠🎡🎢🚢🚤🚣💺🚁🚂🚊🚉🚞🚆🚄🚅🚈🚇🚝🚋🚃🚎🚌🚍🚙🚘🚗🚕"
place2 = u"🚖🚛🚚🚨🚓🚔🚒🚑🚐🚲🚡🚟🚠🚜💈🚏🎫🚦🚥🚧🔰🏮🎰🗿🎪🎭📍🚩"
place_single = u"⛪⛺⛲⛵⚓✈⚠⛽♨"
flag_4 = u"🇯🇵🇰🇷🇩🇪🇨🇳🇺🇸🇫🇷🇪🇸🇮🇹🇷🇺🇬🇧"
symbol1 = u"1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣0⃣🔟🔢#⃣🔣🔠🔡🔤🔄🔼🔽🆗🔀🔁🔂🆕🆙🆒🆓🆖📶🎦🈁🈯🈳🈵🈴🈲🉐🈹"
symbol2 = u"🈺🈶🈚🚻🚹🚺🚼🚾🚰🚮🅿🚭🈷🈸🈂🛂🛄🛅🛃🉑🆑🆘🆔🚫🔞📵🚯🚱🚳🚷🚸💟🆚📳📴🅰🅱🆎🅾💠"
symbol3 = u"🔯🏧💹💲💱🔝🔚🔙🔛🔜🔃🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕖🕗🕘🕙🕚🕡🕢🕣🕤🕥🕦💮💯🔘🔗🔱🔹🔸🔷🔶🔻🔵🔴🔳🔲🔺"
symbol_single = u"⬆⬇⬅➡↗↖↘↙↔↕◀▶↩↪ℹ⏪⏩⏫⏬⤵⤴⛔✳❇❎✅✴♻➿♈♉♊♋♌♍♎♏♐♑♒♓⛎‼❌⁉❗❓❕❔⭕✖➕➖➗♠♥♣♦⬛⬜⚪⚫▫▪◽◾◻◼"


# some of the following lists contain two list (double and single) or more (8)
people_u = [u'\U0001f604', u'\U0001f603', u'\U0001f600', u'\U0001f60a', u'\U0001f609', u'\U0001f60d', u'\U0001f618', u'\U0001f61a', u'\U0001f617', u'\U0001f619', u'\U0001f61c', u'\U0001f61d', u'\U0001f61b', u'\U0001f633', u'\U0001f601', u'\U0001f614', u'\U0001f60c', u'\U0001f612', u'\U0001f61e', u'\U0001f623', u'\U0001f622', u'\U0001f602', u'\U0001f62d', u'\U0001f62a', u'\U0001f625', u'\U0001f630', u'\U0001f605', u'\U0001f613', u'\U0001f629', u'\U0001f62b', u'\U0001f628', u'\U0001f631', u'\U0001f620', u'\U0001f621', u'\U0001f624', u'\U0001f616', u'\U0001f606', u'\U0001f60b', u'\U0001f637', u'\U0001f60e', u'\U0001f634', u'\U0001f635', u'\U0001f632', u'\U0001f61f', u'\U0001f626', u'\U0001f627', u'\U0001f608', u'\U0001f47f', u'\U0001f62e', u'\U0001f62c', u'\U0001f610', u'\U0001f615', u'\U0001f62f', u'\U0001f636', u'\U0001f607', u'\U0001f60f', u'\U0001f611', u'\U0001f472', u'\U0001f473', u'\U0001f46e', u'\U0001f477', u'\U0001f482', u'\U0001f476', u'\U0001f466', u'\U0001f467', u'\U0001f468', u'\U0001f469', u'\U0001f474', u'\U0001f475', u'\U0001f471', u'\U0001f47c', u'\U0001f478', u'\U0001f63a', u'\U0001f638', u'\U0001f63b', u'\U0001f63d', u'\U0001f63c', u'\U0001f640', u'\U0001f63f', u'\U0001f639', u'\U0001f63e', u'\U0001f479', u'\U0001f47a', u'\U0001f648', u'\U0001f649', u'\U0001f64a', u'\U0001f480', u'\U0001f47d', u'\U0001f4a9', u'\U0001f525', u'\U0001f31f', u'\U0001f4ab', u'\U0001f4a5', u'\U0001f4a2', u'\U0001f4a6', u'\U0001f4a7', u'\U0001f4a4', u'\U0001f4a8', u'\U0001f442', u'\U0001f440', u'\U0001f443', u'\U0001f445', u'\U0001f444', u'\U0001f44d', u'\U0001f44e', u'\U0001f44c', u'\U0001f44a', u'\U0001f44b', u'\U0001f450', u'\U0001f446', u'\U0001f447', u'\U0001f449', u'\U0001f448', u'\U0001f64c', u'\U0001f64f', u'\U0001f44f', u'\U0001f4aa', u'\U0001f6b6', u'\U0001f3c3', u'\U0001f483', u'\U0001f46b', u'\U0001f46a', u'\U0001f46c', u'\U0001f46d', u'\U0001f48f', u'\U0001f491', u'\U0001f46f', u'\U0001f646', u'\U0001f645', u'\U0001f481', u'\U0001f64b', u'\U0001f486', u'\U0001f487', u'\U0001f485', u'\U0001f470', u'\U0001f64e', u'\U0001f64d', u'\U0001f647', u'\U0001f3a9', u'\U0001f451', u'\U0001f452', u'\U0001f45f', u'\U0001f45e', u'\U0001f461', u'\U0001f460', u'\U0001f462', u'\U0001f455', u'\U0001f454', u'\U0001f45a', u'\U0001f457', u'\U0001f3bd', u'\U0001f456', u'\U0001f458', u'\U0001f459', u'\U0001f4bc', u'\U0001f45c', u'\U0001f45d', u'\U0001f45b', u'\U0001f453', u'\U0001f380', u'\U0001f302', u'\U0001f484', u'\U0001f49b', u'\U0001f499', u'\U0001f49c', u'\U0001f49a', u'\U0001f494', u'\U0001f497', u'\U0001f493', u'\U0001f495', u'\U0001f496', u'\U0001f49e', u'\U0001f498', u'\U0001f48c', u'\U0001f48b', u'\U0001f48d', u'\U0001f48e', u'\U0001f464', u'\U0001f465', u'\U0001f4ac', u'\U0001f463', u'\U0001f4ad', u'\U0001f596']+[u'\U0001f468\u200d\U0001f469\u200d\U0001f466', u'\U0001f468\u200d\U0001f469\u200d\U0001f467', u'\U0001f469\u200d\U0001f469\u200d\U0001f466', u'\U0001f469\u200d\U0001f469\u200d\U0001f467', u'\U0001f468\u200d\U0001f468\u200d\U0001f466', u'\U0001f468\u200d\U0001f468\u200d\U0001f467', u'\U0001f469\u200d\u2764\ufe0f\u200d\U0001f469', u'\U0001f468\u200d\u2764\ufe0f\u200d\U0001f468']+[u'\U0001f468\u200d\U0001f469\u200d\U0001f466', u'\U0001f468\u200d\U0001f469\u200d\U0001f467', u'\U0001f469\u200d\U0001f469\u200d\U0001f466', u'\U0001f469\u200d\U0001f469\u200d\U0001f467', u'\U0001f468\u200d\U0001f468\u200d\U0001f466', u'\U0001f468\u200d\U0001f468\u200d\U0001f467', u'\U0001f469\u200d\u2764\ufe0f\u200d\U0001f469', u'\U0001f468\u200d\u2764\ufe0f\u200d\U0001f468']+[u'\u263a', u'\u2728', u'\u270a', u'\u270c', u'\u270b', u'\u261d', u'\u2764']
animals_u = [u'\U0001f436', u'\U0001f43a', u'\U0001f431', u'\U0001f42d', u'\U0001f439', u'\U0001f430', u'\U0001f438', u'\U0001f42f', u'\U0001f428', u'\U0001f43b', u'\U0001f437', u'\U0001f43d', u'\U0001f42e', u'\U0001f417', u'\U0001f435', u'\U0001f412', u'\U0001f434', u'\U0001f411', u'\U0001f418', u'\U0001f43c', u'\U0001f427', u'\U0001f426', u'\U0001f424', u'\U0001f425', u'\U0001f423', u'\U0001f414', u'\U0001f40d', u'\U0001f422', u'\U0001f41b', u'\U0001f41d', u'\U0001f41c', u'\U0001f41e', u'\U0001f40c', u'\U0001f419', u'\U0001f41a', u'\U0001f420', u'\U0001f41f', u'\U0001f42c', u'\U0001f433', u'\U0001f40b', u'\U0001f404', u'\U0001f40f', u'\U0001f400', u'\U0001f403', u'\U0001f405', u'\U0001f407', u'\U0001f409', u'\U0001f40e', u'\U0001f410', u'\U0001f413', u'\U0001f415', u'\U0001f416', u'\U0001f401', u'\U0001f402', u'\U0001f432', u'\U0001f421', u'\U0001f40a', u'\U0001f42b', u'\U0001f42a', u'\U0001f406', u'\U0001f408', u'\U0001f429', u'\U0001f43e']
nature_u = [u'\U0001f490', u'\U0001f338', u'\U0001f337', u'\U0001f340', u'\U0001f339', u'\U0001f33b', u'\U0001f33a', u'\U0001f341', u'\U0001f343', u'\U0001f342', u'\U0001f33f', u'\U0001f33e', u'\U0001f344', u'\U0001f335', u'\U0001f334', u'\U0001f332', u'\U0001f333', u'\U0001f330', u'\U0001f331', u'\U0001f33c', u'\U0001f310', u'\U0001f31e', u'\U0001f31d', u'\U0001f31a', u'\U0001f311', u'\U0001f312', u'\U0001f313', u'\U0001f314', u'\U0001f315', u'\U0001f316', u'\U0001f317', u'\U0001f318', u'\U0001f31c', u'\U0001f31b', u'\U0001f319', u'\U0001f30d', u'\U0001f30e', u'\U0001f30f', u'\U0001f30b', u'\U0001f30c', u'\U0001f320', u'\U0001f300', u'\U0001f301', u'\U0001f308', u'\U0001f30a']+[u'\u2b50', u'\u2600', u'\u26c5', u'\u2601', u'\u26a1', u'\u2614', u'\u2744', u'\u26c4']
colors_u = [u'\U0001f3fb', u'\U0001f3fc', u'\U0001f3fd', u'\U0001f3fe', u'\U0001f3ff']
object_u = [u'\U0001f38d', u'\U0001f49d', u'\U0001f38e', u'\U0001f392', u'\U0001f393', u'\U0001f38f', u'\U0001f386', u'\U0001f387', u'\U0001f390', u'\U0001f391', u'\U0001f383', u'\U0001f47b', u'\U0001f385', u'\U0001f384', u'\U0001f381', u'\U0001f38b', u'\U0001f389', u'\U0001f38a', u'\U0001f388', u'\U0001f38c', u'\U0001f52e', u'\U0001f3a5', u'\U0001f4f7', u'\U0001f4f9', u'\U0001f4fc', u'\U0001f4bf', u'\U0001f4c0', u'\U0001f4bd', u'\U0001f4be', u'\U0001f4bb', u'\U0001f4f1', u'\U0001f4de', u'\U0001f4df', u'\U0001f4e0', u'\U0001f4e1', u'\U0001f4fa', u'\U0001f4fb', u'\U0001f50a', u'\U0001f509', u'\U0001f508', u'\U0001f507', u'\U0001f514', u'\U0001f515', u'\U0001f4e2', u'\U0001f4e3', u'\U0001f513', u'\U0001f512', u'\U0001f50f', u'\U0001f510', u'\U0001f511', u'\U0001f50e', u'\U0001f4a1', u'\U0001f526', u'\U0001f506', u'\U0001f505', u'\U0001f50c', u'\U0001f50b', u'\U0001f50d', u'\U0001f6c1', u'\U0001f6c0', u'\U0001f6bf', u'\U0001f6bd', u'\U0001f527', u'\U0001f529', u'\U0001f528', u'\U0001f6aa', u'\U0001f6ac', u'\U0001f4a3', u'\U0001f52b', u'\U0001f52a', u'\U0001f48a', u'\U0001f489', u'\U0001f4b0', u'\U0001f4b4', u'\U0001f4b5', u'\U0001f4b7', u'\U0001f4b6', u'\U0001f4b3', u'\U0001f4b8', u'\U0001f4f2', u'\U0001f4e7', u'\U0001f4e5', u'\U0001f4e4', u'\U0001f4e9', u'\U0001f4e8', u'\U0001f4ef', u'\U0001f4eb', u'\U0001f4ea', u'\U0001f4ec', u'\U0001f4ed', u'\U0001f4ee', u'\U0001f4e6', u'\U0001f4dd', u'\U0001f4c4', u'\U0001f4c3', u'\U0001f4d1', u'\U0001f4ca', u'\U0001f4c8', u'\U0001f4c9', u'\U0001f4dc', u'\U0001f4cb', u'\U0001f4c5', u'\U0001f4c6', u'\U0001f4c7', u'\U0001f4c1', u'\U0001f4c2', u'\U0001f4cc', u'\U0001f4ce', u'\U0001f4cf', u'\U0001f4d0', u'\U0001f4d5', u'\U0001f4d7', u'\U0001f4d8', u'\U0001f4d9', u'\U0001f4d3', u'\U0001f4d4', u'\U0001f4d2', u'\U0001f4da', u'\U0001f4d6', u'\U0001f516', u'\U0001f4db', u'\U0001f52c', u'\U0001f52d', u'\U0001f4f0', u'\U0001f3a8', u'\U0001f3ac', u'\U0001f3a4', u'\U0001f3a7', u'\U0001f3bc', u'\U0001f3b5', u'\U0001f3b6', u'\U0001f3b9', u'\U0001f3bb', u'\U0001f3ba', u'\U0001f3b7', u'\U0001f3b8', u'\U0001f47e', u'\U0001f3ae', u'\U0001f0cf', u'\U0001f3b4', u'\U0001f004', u'\U0001f3b2', u'\U0001f3af', u'\U0001f3c8', u'\U0001f3c0', u'\U0001f3be', u'\U0001f3b1', u'\U0001f3c9', u'\U0001f3b3', u'\U0001f6b5', u'\U0001f6b4', u'\U0001f3c1', u'\U0001f3c7', u'\U0001f3c6', u'\U0001f3bf', u'\U0001f3c2', u'\U0001f3ca', u'\U0001f3c4', u'\U0001f3a3', u'\U0001f375', u'\U0001f376', u'\U0001f37c', u'\U0001f37a', u'\U0001f37b', u'\U0001f378', u'\U0001f379', u'\U0001f377']+[u'\u260e', u'\u23f3', u'\u231b', u'\u23f0', u'\u231a', u'\u2709', u'\u2702', u'\u2712', u'\u270f', u'\u26bd', u'\u26be', u'\u26f3', u'\u2615']
food_u = [u'\U0001f374', u'\U0001f355', u'\U0001f354', u'\U0001f35f', u'\U0001f357', u'\U0001f356', u'\U0001f35d', u'\U0001f35b', u'\U0001f364', u'\U0001f371', u'\U0001f363', u'\U0001f365', u'\U0001f359', u'\U0001f358', u'\U0001f35a', u'\U0001f35c', u'\U0001f372', u'\U0001f362', u'\U0001f361', u'\U0001f373', u'\U0001f369', u'\U0001f35e', u'\U0001f36e', u'\U0001f366', u'\U0001f368', u'\U0001f367', u'\U0001f382', u'\U0001f370', u'\U0001f36a', u'\U0001f36b', u'\U0001f36c', u'\U0001f36d', u'\U0001f36f', u'\U0001f34e', u'\U0001f34f', u'\U0001f34a', u'\U0001f34b', u'\U0001f347', u'\U0001f349', u'\U0001f353', u'\U0001f351', u'\U0001f348', u'\U0001f34c', u'\U0001f350', u'\U0001f34d', u'\U0001f360', u'\U0001f346', u'\U0001f345', u'\U0001f33d']
place_u = [u'\U0001f3e0', u'\U0001f3e1', u'\U0001f3eb', u'\U0001f3e2', u'\U0001f3e3', u'\U0001f3e5', u'\U0001f3e6', u'\U0001f3ea', u'\U0001f3e9', u'\U0001f3e8', u'\U0001f492', u'\U0001f3ec', u'\U0001f3e4', u'\U0001f307', u'\U0001f306', u'\U0001f3ef', u'\U0001f3f0', u'\U0001f3ed', u'\U0001f5fc', u'\U0001f5fe', u'\U0001f5fb', u'\U0001f304', u'\U0001f305', u'\U0001f303', u'\U0001f5fd', u'\U0001f309', u'\U0001f3a0', u'\U0001f3a1', u'\U0001f3a2', u'\U0001f6a2', u'\U0001f6a4', u'\U0001f6a3', u'\U0001f4ba', u'\U0001f681', u'\U0001f682', u'\U0001f68a', u'\U0001f689', u'\U0001f69e', u'\U0001f686', u'\U0001f684', u'\U0001f685', u'\U0001f688', u'\U0001f687', u'\U0001f69d', u'\U0001f68b', u'\U0001f683', u'\U0001f68e', u'\U0001f68c', u'\U0001f68d', u'\U0001f699', u'\U0001f698', u'\U0001f697', u'\U0001f695', u'\U0001f696', u'\U0001f69b', u'\U0001f69a', u'\U0001f6a8', u'\U0001f693', u'\U0001f694', u'\U0001f692', u'\U0001f691', u'\U0001f690', u'\U0001f6b2', u'\U0001f6a1', u'\U0001f69f', u'\U0001f6a0', u'\U0001f69c', u'\U0001f488', u'\U0001f68f', u'\U0001f3ab', u'\U0001f6a6', u'\U0001f6a5', u'\U0001f6a7', u'\U0001f530', u'\U0001f3ee', u'\U0001f3b0', u'\U0001f5ff', u'\U0001f3aa', u'\U0001f3ad', u'\U0001f4cd', u'\U0001f6a9']+[u'\u26ea', u'\u26fa', u'\u26f2', u'\u26f5', u'\u2693', u'\u2708', u'\u26a0', u'\u26fd', u'\u2668']
flag_u = [u'\U0001f1ef\U0001f1f5', u'\U0001f1f0\U0001f1f7', u'\U0001f1e9\U0001f1ea', u'\U0001f1e8\U0001f1f3', u'\U0001f1fa\U0001f1f8', u'\U0001f1eb\U0001f1f7', u'\U0001f1ea\U0001f1f8', u'\U0001f1ee\U0001f1f9', u'\U0001f1f7\U0001f1fa', u'\U0001f1ec\U0001f1e7']
symbol_u = [u'1\u20e3', u'2\u20e3', u'3\u20e3', u'4\u20e3', u'5\u20e3', u'6\u20e3', u'7\u20e3', u'8\u20e3', u'9\u20e3', u'0\u20e3', u'\U0001f51f', u'\U0001f522', u'#\u20e3', u'\U0001f523', u'\U0001f520', u'\U0001f521', u'\U0001f524', u'\U0001f504', u'\U0001f53c', u'\U0001f53d', u'\U0001f197', u'\U0001f500', u'\U0001f501', u'\U0001f502', u'\U0001f195', u'\U0001f199', u'\U0001f192', u'\U0001f193', u'\U0001f196', u'\U0001f4f6', u'\U0001f3a6', u'\U0001f201', u'\U0001f22f', u'\U0001f233', u'\U0001f235', u'\U0001f234', u'\U0001f232', u'\U0001f250', u'\U0001f239', u'\U0001f23a', u'\U0001f236', u'\U0001f21a', u'\U0001f6bb', u'\U0001f6b9', u'\U0001f6ba', u'\U0001f6bc', u'\U0001f6be', u'\U0001f6b0', u'\U0001f6ae', u'\U0001f17f', u'\U0001f6ad', u'\U0001f237', u'\U0001f238', u'\U0001f202', u'\U0001f6c2', u'\U0001f6c4', u'\U0001f6c5', u'\U0001f6c3', u'\U0001f251', u'\U0001f191', u'\U0001f198', u'\U0001f194', u'\U0001f6ab', u'\U0001f51e', u'\U0001f4f5', u'\U0001f6af', u'\U0001f6b1', u'\U0001f6b3', u'\U0001f6b7', u'\U0001f6b8', u'\U0001f49f', u'\U0001f19a', u'\U0001f4f3', u'\U0001f4f4', u'\U0001f170', u'\U0001f171', u'\U0001f18e', u'\U0001f17e', u'\U0001f4a0', u'\U0001f52f', u'\U0001f3e7', u'\U0001f4b9', u'\U0001f4b2', u'\U0001f4b1', u'\U0001f51d', u'\U0001f51a', u'\U0001f519', u'\U0001f51b', u'\U0001f51c', u'\U0001f503', u'\U0001f55b', u'\U0001f567', u'\U0001f550', u'\U0001f55c', u'\U0001f551', u'\U0001f55d', u'\U0001f552', u'\U0001f55e', u'\U0001f553', u'\U0001f55f', u'\U0001f554', u'\U0001f560', u'\U0001f555', u'\U0001f556', u'\U0001f557', u'\U0001f558', u'\U0001f559', u'\U0001f55a', u'\U0001f561', u'\U0001f562', u'\U0001f563', u'\U0001f564', u'\U0001f565', u'\U0001f566', u'\U0001f4ae', u'\U0001f4af', u'\U0001f518', u'\U0001f517', u'\U0001f531', u'\U0001f539', u'\U0001f538', u'\U0001f537', u'\U0001f536', u'\U0001f53b', u'\U0001f535', u'\U0001f534', u'\U0001f533', u'\U0001f532', u'\U0001f53a']+[u'\u2b06', u'\u2b07', u'\u2b05', u'\u27a1', u'\u2197', u'\u2196', u'\u2198', u'\u2199', u'\u2194', u'\u2195', u'\u25c0', u'\u25b6', u'\u21a9', u'\u21aa', u'\u2139', u'\u23ea', u'\u23e9', u'\u23eb', u'\u23ec', u'\u2935', u'\u2934', u'\u26d4', u'\u2733', u'\u2747', u'\u274e', u'\u2705', u'\u2734', u'\u267b', u'\u27bf', u'\u2648', u'\u2649', u'\u264a', u'\u264b', u'\u264c', u'\u264d', u'\u264e', u'\u264f', u'\u2650', u'\u2651', u'\u2652', u'\u2653', u'\u26ce', u'\u203c', u'\u274c', u'\u2049', u'\u2757', u'\u2753', u'\u2755', u'\u2754', u'\u2b55', u'\u2716', u'\u2795', u'\u2796', u'\u2797', u'\u2660', u'\u2665', u'\u2663', u'\u2666', u'\u2b1b', u'\u2b1c', u'\u26aa', u'\u26ab', u'\u25ab', u'\u25aa', u'\u25fd', u'\u25fe', u'\u25fb', u'\u25fc']

Emoji_list = people_u + animals_u + nature_u + colors_u + object_u + food_u + place_u + flag_u + symbol_u
# sep should be the length of each emoji, usually 2
def sep_emoji(str, sep):
	emoji_list = []
	i = 0
	while i < len(str):
		emoji_list.append(str[i:i+sep])
		i += sep
	print emoji_list
	return emoji_list
    
def tokenize(text):
	return tokenizeRawTweetText(text)

# In nlp process, we only care about terms, rather than sentences, so sentences may not be readable
def normalize(text):
	# for easier comparison 
	text = text.lower()
	# to avoid IndexError: string index out of range (usually too much indent)
	text = squeezeWhitespace(text)
	# replace common abbreviation or unreadable characters 
	text = text.replace("&gt;", ">")
	text = text.replace("&amp;", "&")
	text = text.replace("w/", "with")
	text = text.replace('\u2019', "'")
	text = text.replace('\u2026', "...")
	# remove urls
	text = re.sub(r'http\S+', '', text)    #replace URL links with the term 'URL'
	# remove keyword 'springbreak'
	text = text.replace('springbreak', '')
	text = text.replace('spring', '')
	text = text.replace('break', '')
	return normalizeTextForTagger(text)
	
# standalone function
# input a string that needs to extract emoji, a list of emoji that needs to be extracted
def extract_emoji(text, Emoji_list):
	#print "Before:", text
	emojis = []
	for emoji in Emoji_list:
		if emoji in text:
			text = text.replace(emoji, "")
			emojis.append(emoji)
			print "Extracted", emoji
	print "After:", text
	return text, emojis

def tag_pos(text, pos_wanted):
	t = tag(text)
	pos_list = {}
	for p in pos_wanted:
		pos_list[p] = [word for word, pos in t if pos == p]
	return pos_list
	
# input : a string
# output: a dict
def sentiment_pattern(text):
	test_result = sentiment(text)
	# (polarity, subjectivity)-tuple, e.g.(0.4083333333333334, 0.4666666666666666)
	return {'polarity': test_result[0], 'subjectivity': test_result[1]}
	
# standalone function: input a tweet(JSON) and output a tweet(JSON) with nlp data 
def add_nlp_data(tweet):
	# copy tweet data
	nlp_tweet = tweet
	# we focus on the tweet itself now, so remove the retweeted status
	nlp_tweet.pop("retweeted_status", None)
	
	# STEP 1: update text and entities after extracting emoji
	text = normalize(nlp_tweet['text'])
	nlp_tweet['text'], nlp_tweet['entities']['emoji'] = extract_emoji(text, Emoji_list)
	nlp_tweet['tokens'] = tokenize(nlp_tweet['text'])
	# STEP 2: tag part_of_speech and save useful ones, use text from STEP 1
	pos_wanted = ['JJ', 'RB', 'VB', 'VBD', 'VBG', 'VBN']    # adjective, adverb, verb(take, took, taking, taken)
	nlp_tweet['pos'] = tag_pos(nlp_tweet['text'], pos_wanted)
	# STEP 3: add sentiment score 
	nlp_tweet['sentiment'] = sentiment_pattern(nlp_tweet['text'])
	return nlp_tweet

# process tweets in batch 
def nlp_tweet(tweets):
	for tweet in tweets:
		tweet = add_nlp_data(tweet)
	return tweets

# process tweets from file to file
def get_nlp_tweet(data):
	tweets = load_json_from_file(data)
	nlp_tweets = nlp_tweet(tweets)
	save_json_to_file(nlp_tweets, '\n', outpath, filename+'_nlp.json')
	
	
if __name__ == '__main__':
	get_nlp_tweet(data)
	
