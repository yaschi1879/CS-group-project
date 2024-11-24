from api_functions import get_club_players

club_id = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

meta_player_list = []

for club in club_id:
    meta_player_list.extend(get_club_players(club))
# dauert lange, darum nicht mehr ausgeführt und unten die liste einfach manuell kopiert

player_list = ['238223', '85941', '14555', '258004', '284730', '177476', '186590', '475959', '576121', '701057', '95424', '357565', '601883', '51471', '53622', '241641', '88755', '583199', '486049', '203460', '406635', '743591', '661207', '418560', '108390', '404839', '401530', '86202', '59016', '251896', '291417', '341264', '138927', '221316', '413112', '369081', '640428', '27992', '319745', '581678', '314678', '371998', '412363', '861410', '342229', '971570', '17259', '468539', '40680', '344695', '503482', '353892', '175722', '744729', '424204', '170986', '938146', '483046', '475413', '161056', '257455', '792380', '223967', '153084', '580195', '159471', '243714', '801734', '744728', '566723', '192565', '956920', '58358', '132098', '105470', '340918', '486604', '357119', '139208', '256178', '632349', '234803', '338070', '314353', '624258', '146310', '618494', '534033', '478573', '433188', '565822', '451276', '480692', '434675', '148455', '341092', '546543', '340950', '338670', '128969', '1041614', '371149', '256448', '281769', '39728', '277179', '605396', '251075', '631927', '962125', '199248', '166237', '624690', '633992', '813137', '550108', '286297', '641537', '94529', '668951', '381950', '206050', '343537', '358166', '315858', '318470', '466783', '181767', '661171', '872171', '204069', '282041', '616341', '281963', '398073', '1047097', '670681', '810092', '487469', '350219', '903693', '810093', '557149', '708265', '914562', '288230', '296622', '1185888', '550550', '487969', '257814', '453737', '76158', '388198', '193004', '166601', '284732', '884820', '627228', '370789', '119296', '406640', '106987', '82873', '884810', '187492', '504215', '496094', '670882', '819215', '326029', '866579', '270541', '578392', '403151', '585323', '116648', '490606', '614258', '386047', '463603', '475411', '258878', '805714', '284857', '316125', '472423', '620322', '687626', '628451', '648195', '475188', '659459', '622380', '568177', '344381', '537860', '401173', '487465', '503987', '462250', '776890', '1082850', '938158', '388516', '42205', '303657', '70580', '315853', '353366', '441986', '111196', '993645', '131075', '198116', '585982', '321528', '54906', '126414', '543771', '255942', '394300', '181136', '55735', '638793', '227081', '406625', '318528', '307058', '41384', '712107', '341713', '547248', '484988', '780630', '286384', '15452', '678406', '356197', '126719', '480763', '76467', '485963', '783396', '380598', '59561', '165007', '548111', '568157', '709969', '343052', '937941', '177467', '246968', '550829', '48015', '85543', '810826', '564545', '659813', '196357', '919515', '644613', '193082', '348026', '977464', '111455', '159088', '401578', '261504', '944582', '484547', '340322', '598577', '7161', '532776', '442891', '656681', '242086', '234509', '336077', '34130', '326031', '923831', '480762', '177907', '184573', '42412', '183288', '339340', '357147', '340456', '476701', '16306', '654253', '820374', '69633', '747153', '240306', '346483', '258923', '811779', '536835', '602105', '610442', '435648', '888639', '74857', '283170', '44058', '709955', '480267', '962110', '196948', '466794', '158863', '741258', '636688', '705395', '411975', '937955', '636695', '1018920', '646740', '683840', '326330', '636703', '293385', '720038', '411295', '466810', '937958', '398184', '38253', '707572', '537844', '504072', '670710', '650568', '504087', '582987', '54781', '342967', '811778', '452607', '649452', '357162', '454567', '223367', '357233', '258027', '164913', '382528', '670103', '1000674', '491704', '479638', '45320', '324503', '390638', '548729', '357153', '155396', '284701', '491693', '420465', '818495', '406151', '57723', '478365', '228433', '544784', '537602', '935480', '756990', '222813', '466805', '512913', '537598', '957653', '610335', '575716', '448470', '520662', '454121', '479649', '991268', '284883', '392767', '1063292', '121483', '242359', '930415', '351809', '250845', '182904', '35047', '57500', '240692', '448628', '424042', '488362', '255901', '775605', '74229', '282411', '205562', '694928', '461617', '612496', '266807', '576024', '125781', '238407', '742201', '566036', '486046', '57071', '160971', '618472', '787912', '93740', '215599', '318204', '420210', '202591', '926694', '223979', '402008', '404950', '897424', '53418', '566931', '324278', '400489', '894914', '368887', '627442', '157635', '198008', '120629', '61697', '29692', '525247', '605184', '415912', '845321', '181778', '92571', '477758', '157672', '401356', '283628', '342385', '372246', '430310', '444523', '474701', '543499', '314875', '991800', '75489', '134294', '104124', '459763', '45026', '126634', '571604', '644771', '503075', '343475', '165513', '94005', '72441', '546880', '133179', '982267', '607854', '528833', '205938', '459128', '357992', '173859', '895937', '91970', '616631', '435772', '392085', '406040', '315867', '554903', '262749', '111819', '495666', '435338', '420243', '425918', '502821', '203853', '300716', '335721', '331560', '357662', '230784', '102017', '890721', '338424', '316264', '890719', '655488', '144028', '134425', '433177', '309400', '363205', '301238', '110923', '75411', '516716', '509022', '585949', '145707', '459658', '686965', '741090', '708072', '265088', '362842', '447661', '463618', '332697', '432090', '122153', '360518', '944570', '845654', '654991', '486031', '487474', '370846', '357498', '191891', '182906', '199976', '939745', '303254', '521964', '574671', '323167', '339808', '476344', '262523', '631007', '741257', '130365', '569598', '351816', '460939', '202886', '503991', '883349', '357164', '346890', '315779', '401922', '331726', '128223', '257462', '448705', '480453', '25520', '371001', '662131', '748601', '162959', '559327', '765743', '904802', '339328', '557407', '701055', '510310', '787907', '470394', '203938', '61651', '182932', '559333', '694186', '748804', '704773', '131996', '129554', '610429', '473169', '197642', '228645', '720799', '240414', '421873', '250683', '724099', '386446', '257732', '662261', '121985', '376514', '118689', '87884', '169880', '250153', '192735', '423744', '315969', '354361', '377042', '502670', '433584', '469822', '165895', '358032', '405885', '96341', '282388', '50219', '250543', '559320', '893661', '741142', '743381', '236168', '88262', '1067903', '429915', '594227', '981196', '578680', '743122', '699783', '608172', '499758', '148365', '137576', '451677', '393565', '432982', '564489', '743384', '320440', '599231', '708454', '197929', '481675', '538079', '918957', '618341', '197747', '276896', '126729', '1110645', '535955', '346567', '239802', '200056', '525704', '465830', '303116', '143812', '334835', '170481', '331401', '530742', '601577', '834468', '283735', '462823', '457736', '607226', '873981', '65278', '522784', '626913', '45672', '997861', '40034', '368891', '328784', '546213', '635645', '684315', '591193', '691892', '369684', '49723', '290587', '951957', '931838', '191422', '846310', '536482', '855015', '816585', '74842', '933217', '939964', '429874', '445939', '709726', '605268', '453704', '73517', '730581', '766583', '439022', '538996', '849410', '501418', '676042', '402733', '711625', '15956', '569384', '74294', '381967', '212723', '148928', '766723', '610238', '743387', '500067', '303259', '111961', '639733', '687609', '295330', '128899', '208772', '235767', '202788', '633650', '910175', '56100', '477930', '851595', '643097', '62094', '346315', '503640', '633649', '422763', '658531', '567151', '633624', '390177', '229970', '282076', '258916', '633753', '975689', '404384', '242063', '624266', '519731', '317806', '885445', '315121', '196829', '859218', '746973', '404418', '593862', '825199', '59145', '856068', '514285', '374212', '698678', '313094', '257987', '997903', '416660', '571149', '420213', '683620', '365394', '409344', '1057565', '653610', '1110406', '387105', '917911', '552955', '589128', '491707', '212862', '625657', '361914', '355628', '580560', '229804', '1018938', '517842', '568158', '297070', '661145', '280730', '423440', '625651', '634431', '502722', '625660', '309110', '555143', '907813', '625655', '616369', '188888', '405398', '366930', '351478', '660438', '337715', '296802', '333640', '723005', '318508', '586429', '800976', '339337', '654918', '323910', '539665', '361104', '205006', '347900', '408574', '702869', '816974', '467437', '372267', '813437', '575367', '339332', '316889', '593837', '42460', '565424', '627207', '72522', '429070', '492319', '848875', '670711', '549006', '974982', '548193', '504073', '288253', '379249', '946883', '139395', '461496', '524315', '461943', '426620', '290391', '572675', '412669', '314367', '701979', '1138758', '325443', '807386', '725912', '242089', '240536', '189630', '567738', '534568', '544149', '216278', '944827', '765094', '129655', '343558', '728635', '928023', '401475', '580978', '147555', '493758', '486054', '234153', '1111589', '504189', '292779', '321195', '1066142', '552059', '726714', '108416', '405855', '198614', '666268', '229604', '315253', '199321', '575998', '485960', '203348', '807165', '328609', '557613', '192616', '354482', '298975', '167799', '127189', '182913', '921655', '332889', '659520', '955358', '787618', '372711', '1170286', '691316', '672381', '1075589', '532826', '1027216', '1183719', '659542', '217115', '599663', '463600', '33781', '205465', '810789', '463605', '648020', '126540', '80293', '744074', '361065', '362108', '124028', '816580', '100986', '327863', '245537', '84301', '1016015', '221025', '1097139', '903666', '392770', '113707', '652275', '580657', '496857', '533738', '724129', '594991', '293185', '234187', '131310', '590554', '946969', '676266', '631222', '324819', '240106', '331840', '60603', '665276', '946957', '292666', '492730', '709970', '410185', '104466', '294778', '668207', '227035', '71542', '1009485', '317482', '580451', '846545', '205940', '557614', '403290', '458367', '665266', '316047', '960057', '256358', '59377', '96254', '471936', '934159', '373373', '282144', '346561', '746712', '1144700', '273132', '547985', '124555', '823486', '401529', '395236', '308279', '199733', '562049', '893675', '392959', '337725', '386455', '324690', '305947', '628366', '364135', '704772', '116471', '595935', '79045', '635371', '646707', '479643', '112052', '646704', '661427', '315254', '733438', '577394', '507223', '361074', '104223', '595940', '859035', '747017', '801031', '578804', '735701', '543501', '795274', '718303', '747720', '552655', '678546', '728864', '286047', '52570', '428016', '282823', '355915', '557459', '568559', '192765', '556385', '282429', '553875', '922693', '483348', '410425', '354362', '568693', '866246', '294057', '431755', '91845', '170527', '1011147', '470607', '743498', '258889', '378710', '879768']