def CalculateVelocityForces(angularVelocityX, angularVelocityY, angularVelocityZ):
    wx = angularVelocityX**2
    wy = angularVelocityY**2
    wz = angularVelocityZ**2
    wxwz = angularVelocityX * angularVelocityZ
    wywz = angularVelocityY * angularVelocityZ
    xTable = [
        [0, 0, 191876.5377],
        [0, -123.3163147, 191835.2446],
        [0, -163.1143914, 191793.9501],
        [0, -202.9124755, 191752.6555],
        [0, -242.7105595, 191711.361],
        [0, 0, 191678.6127],
        [0, 0, 191891.0492],
        [0, -103.417995, 191849.7546],
        [0, -143.2160718, 191808.4601],
        [0, -183.0142069, 191767.1655],
        [0, -222.8107441, 191725.8725],
        [0, 0, 191684.5779],
        [0, -37.08835595, 191912.4418],
        [0, -83.51971547, 191864.2646],
        [0, -123.3163147, 191822.9715],
        [0, -163.1143914, 191781.677],
        [0, -202.9124755, 191740.3824],
        [0, -242.7105595, 191699.0879],
        [0, 0, 191672.182],
        [0, -63.61991095, 191878.776],
        [0, -103.417995, 191837.4815],
        [0, -143.2160718, 191796.1869],
        [0, -183.01266, 191754.8939],
        [0, -222.8107441, 191713.5993],
        [0, 0, 191677.5638],
        [0, -37.08835595, 191900.1687],
        [0, -83.51971547, 191851.9914],
        [0, 0, 191810.6984],
        [0, -163.1143914, 191769.4039],
        [0, -202.9124755, 191728.1093],
        [0, 0, 191691.522],
        [0, -63.61991095, 191866.5029],
        [0, -103.417995, 191825.2083],
        [0, -143.2160718, 191783.9138],
        [0, 0, 191742.6208],
        [0, 0, 191713.1953],
        [0, -50.35489321, 191874.1302],
        [0, -90.15146595, 191832.8372],
        [0, 0, 191793.5882],
        [0, 0, 191758.5344],
        [0, 0, 191859.4054],
        [0, 0, 191816.2],
        [0, 0, 191785.9311],
        [0, 0, 191946.1076],
        [0, 29.24158227, 191987.4024],
        [0, 69.03965902, 192028.697],
        [0, 108.8377431, 192069.9915],
        [0, 148.6340322, 192111.2842],
        [0, 0, 192152.5788],
        [0, 9.343018168, 191960.6191],
        [0, 49.13971951, 192001.9122],
        [0, 88.93779627, 192043.2068],
        [0, 128.7358803, 192084.5013],
        [0, 168.5339644, 192125.7959],
        [0, 0, 192156.012],
        [0, -10.55680095, 191933.8344],
        [0, 29.24158227, 191975.1293],
        [0, 69.03965902, 192016.4238],
        [0, 108.8359481, 192057.7165],
        [0, 148.6340322, 192099.0111],
        [0, 0, 192139.5561],
        [0, 9.343018168, 191948.346],
        [0, 0, 191989.6391],
        [0, 88.93779627, 192030.9337],
        [0, 128.7358803, 192072.2282],
        [0, 0, 192111.774],
        [0, -10.55680095, 191921.5613],
        [0, 29.24158227, 191962.8561],
        [0, 69.03965902, 192004.1507],
        [0, 0, 192045.4434],
        [0, 0, 192077.8028],
        [0, -23.82183055, 191901.661],
        [0, 15.97475405, 191942.954],
        [0, 0, 191986.294],
        [0, 0, 192017.7512],
        [0, 0, 191904.7722],
        [0, 0, 191950.7978],
        [0, 0, 191984.8974],
        [0, 0, 191972.8922],
        [0, 49.13971951, 192014.1853],
        [0, 88.93779627, 192055.4799],
        [0, 128.7358803, 192096.7744],
        [0, 168.5339644, 192138.069],
        [0, 0, 192170.817],
        [0, 0, 191958.3807],
        [0, 29.24158227, 191999.6755],
        [0, 69.03965902, 192040.9701],
        [0, 108.8377431, 192082.2647],
        [0, 148.6340322, 192123.5574],
        [0, 0, 192164.8519],
        [0, -37.08835595, 191936.9881],
        [0, 9.343018168, 191985.1653],
        [0, 49.13971951, 192026.4584],
        [0, 88.93779627, 192067.753],
        [0, 128.7358803, 192109.0476],
        [0, 168.5339644, 192150.3421],
        [0, 0, 192177.2479],
        [0, -10.55680095, 191970.6538],
        [0, 29.24158227, 192011.9487],
        [0, 69.03965902, 192053.2432],
        [0, 108.8359481, 192094.5359],
        [0, 148.6340322, 192135.8305],
        [0, 0, 192171.866],
        [0, -37.08835595, 191949.2612],
        [0, 9.343018168, 191997.4384],
        [0, 0, 192038.7316],
        [0, 88.93779627, 192080.0261],
        [0, 128.7358803, 192121.3207],
        [0, 0, 192157.9075],
        [0, -10.55680095, 191982.9269],
        [0, 29.24158227, 192024.2218],
        [0, 69.03965902, 192065.5163],
        [0, 0, 192106.809],
        [0, 0, 192136.2343],
        [0, -23.82183055, 191975.2997],
        [0, 15.97475405, 192016.5927],
        [0, 0, 192055.8417],
        [0, 0, 192090.8952],
        [0, 0, 191990.0245],
        [0, 0, 192033.23],
        [0, 0, 192063.4987],
        [0, 0, 191903.3223],
        [0, -103.417995, 191862.0277],
        [0, -143.2160718, 191820.7332],
        [0, -183.0142069, 191779.4386],
        [0, -222.8107441, 191738.1456],
        [0, 0, 191696.851],
        [0, -83.51971547, 191888.8108],
        [0, -123.3163147, 191847.5178],
        [0, -163.1143914, 191806.2232],
        [0, -202.9124755, 191764.9287],
        [0, -242.7105595, 191723.6341],
        [0, 0, 191693.4179],
        [0, -63.61991095, 191915.5954],
        [0, -103.417995, 191874.3009],
        [0, -143.2160718, 191833.0063],
        [0, -183.01266, 191791.7133],
        [0, -222.8107441, 191750.4187],
        [0, 0, 191709.8736],
        [0, -83.51971547, 191901.0839],
        [0, 0, 191859.7909],
        [0, -163.1143914, 191818.4963],
        [0, -202.9124755, 191777.2018],
        [0, 0, 191737.6556],
        [0, -63.61991095, 191927.8685],
        [0, -103.417995, 191886.574],
        [0, -143.2160718, 191845.2794],
        [0, 0, 191803.9864],
        [0, 0, 191771.6268],
        [0, -50.35489321, 191947.7689],
        [0, -90.15146595, 191906.4759],
        [0, 0, 191863.1358],
        [0, 0, 191831.6784],
        [0, 0, 191944.6576],
        [0, 0, 191898.6322],
        [0, 0, 191864.5324],
    ]
    yTable = [
        [0, 0, 191882.4661],
        [0, 86.22802385, 191846.2543],
        [0, 126.026103, 191810.0413],
        [0, 165.8241895, 191773.8282],
        [0, 205.622276, 191737.6151],
        [0, 0, 191708.8966],
        [0, 0, 191896.3331],
        [0, 66.32970298, 191860.12],
        [0, 106.1277822, 191823.9069],
        [0, 145.9259197, 191787.6938],
        [0, 185.7224593, 191751.4821],
        [1584.113903, 0, 191715.2689],
        [0, 0.000059887, 191916.2345],
        [0, 46.43142224, 191873.9856],
        [0, 86.22802385, 191837.7739],
        [0, 126.026103, 191801.5608],
        [0, 165.8241895, 191765.3477],
        [0, 205.622276, 191729.1346],
        [0, 0, 191705.2318],
        [0, 26.5316165, 191887.8526],
        [0, 66.32970298, 191851.6395],
        [0, 106.1277822, 191815.4264],
        [0, 145.9243728, 191779.2147],
        [0, 185.7224593, 191743.0016],
        [0, 0, 191710.981],
        [0, 0.000059887, 191907.754],
        [0, 46.43142224, 191865.5052],
        [1584.113903, 0, 191829.2934],
        [0, 126.026103, 191793.0803],
        [0, 165.8241895, 191756.8672],
        [0, 0, 191724.507],
        [0, 26.5316165, 191879.3721],
        [0, 66.32970298, 191843.159],
        [0, 106.1277822, 191806.946],
        [1584.113903, 0, 191770.7342],
        [0, 0, 191744.6569],
        [0, 13.26659796, 191887.2021],
        [0, 53.06317312, 191850.9903],
        [0, 0, 191816.1906],
        [0, 0, 191785.7848],
        [0, 0, 191875.369],
        [0, 0, 191837.2181],
        [0, 0, 191810.3177],
        [0, 0, 191944.6163],
        [0, -66.32988236, 191980.8297],
        [0, -106.1279615, 192017.0428],
        [0, -145.926048, 192053.2558],
        [0, -185.7223395, 192089.4673],
        [1584.113903, 0, 192125.6804],
        [0, -46.43131705, 191958.4833],
        [0, -86.22802082, 191994.6952],
        [0, -126.0261, 192030.9083],
        [0, -165.8241865, 192067.1213],
        [0, -205.6222729, 192103.3344],
        [0, 0, 192129.5245],
        [0, -26.53149673, 191936.1358],
        [0, -66.32988236, 191972.3492],
        [0, -106.1279615, 192008.5623],
        [0, -145.924253, 192044.7737],
        [0, -185.7223395, 192080.9868],
        [0, 0, 192116.1233],
        [0, -46.43131705, 191950.0029],
        [1584.113903, 0, 191986.2147],
        [0, -126.0261, 192022.4278],
        [0, -165.8241865, 192058.6409],
        [0, 0, 192093.0452],
        [0, -26.53149673, 191927.6553],
        [0, -66.32988236, 191963.8687],
        [0, -106.1279615, 192000.0818],
        [1584.113903, 0, 192036.2933],
        [0, 0, 192064.3979],
        [0, -13.26646632, 191911.345],
        [0, -53.06305334, 191947.5568],
        [0, 0, 191985.1833],
        [0, 0, 192013.1039],
        [0, 0, 191915.1533],
        [0, 0, 191955.253],
        [0, 0, 191984.8004],
        [0, 0, 191966.9638],
        [0, -86.22802082, 192003.1756],
        [0, -126.0261, 192039.3887],
        [0, -165.8241865, 192075.6018],
        [0, -205.6222729, 192111.8149],
        [0, 0, 192140.5331],
        [0, 0, 191953.0968],
        [0, -66.32988236, 191989.3101],
        [0, -106.1279615, 192025.5232],
        [0, -145.926048, 192061.7363],
        [0, -185.7223395, 192097.9478],
        [1584.113903, 0, 192134.1609],
        [0, 0.000059887, 191933.1954],
        [0, -46.43131705, 191975.4443],
        [0, -86.22802082, 192011.6561],
        [0, -126.0261, 192047.8692],
        [0, -165.8241865, 192084.0823],
        [0, -205.6222729, 192120.2954],
        [0, 0, 192144.198],
        [0, -26.53149673, 191961.5772],
        [0, -66.32988236, 191997.7906],
        [0, -106.1279615, 192034.0037],
        [0, -145.924253, 192070.2151],
        [0, -185.7223395, 192106.4282],
        [0, 0, 192138.4487],
        [0, 0.000059887, 191941.6759],
        [0, -46.43131705, 191983.9247],
        [1584.113903, 0, 192020.1366],
        [0, -126.0261, 192056.3496],
        [0, -165.8241865, 192092.5627],
        [0, 0, 192124.9226],
        [0, -26.53149673, 191970.0577],
        [0, -66.32988236, 192006.2711],
        [0, -106.1279615, 192042.4842],
        [1584.113903, 0, 192078.6956],
        [0, 0, 192104.7728],
        [0, -13.26646632, 191962.2278],
        [0, -53.06305334, 191998.4395],
        [0, 0, 192033.2392],
        [0, 0, 192063.6448],
        [0, 0, 191974.0608],
        [0, 0, 192012.2119],
        [0, 0, 192039.1122],
        [0, 0, 191904.8136],
        [0, 66.32970298, 191868.6005],
        [0, 106.1277822, 191832.3874],
        [0, 145.9259197, 191796.1742],
        [0, 185.7224593, 191759.9626],
        [1584.113903, 0, 191723.7494],
        [0, 46.43142224, 191890.9466],
        [0, 86.22802385, 191854.7348],
        [0, 126.026103, 191818.5217],
        [0, 165.8241895, 191782.3086],
        [0, 205.622276, 191746.0955],
        [0, 0, 191719.9054],
        [0, 26.5316165, 191913.294],
        [0, 66.32970298, 191877.0809],
        [0, 106.1277822, 191840.8678],
        [0, 145.9243728, 191804.6561],
        [0, 185.7224593, 191768.443],
        [0, 0, 191733.3064],
        [0, 46.43142224, 191899.427],
        [1584.113903, 0, 191863.2153],
        [0, 126.026103, 191827.0022],
        [0, 165.8241895, 191790.7891],
        [0, 0, 191756.3844],
        [0, 26.5316165, 191921.7745],
        [0, 66.32970298, 191885.5614],
        [0, 106.1277822, 191849.3483],
        [1584.113903, 0, 191813.1366],
        [0, 0, 191785.0318],
        [0, 13.26659796, 191938.0848],
        [0, 53.06317312, 191901.8731],
        [0, 0, 191864.2466],
        [0, 0, 191836.3258],
        [0, 0, 191934.2766],
        [0, 0, 191894.177],
        [0, 0, 191864.6295],
    ]
    zTable = [
        [0, 0, 5.928441158],
        [0, -37.08829942, 11.00974079],
        [0, -37.08830096, 16.09122908],
        [0, -37.08830251, 21.17271831],
        [0, -37.08830406, 26.25420753],
        [0, 0, 30.28403849],
        [0, 0, 1.491224132],
        [0, -37.08829864, 6.572713354],
        [0, -37.08830019, 11.65420165],
        [0, -37.08830174, 16.73569739],
        [0, -37.08830328, 21.8169891],
        [1584.113903, 0, 26.89848578],
        [0, -37.08829606, -3.792746435],
        [0, -37.08829787, 2.135691042],
        [0, -37.08829942, 7.216990674],
        [0, -37.08830096, 12.29847897],
        [0, -37.08830251, 17.37996819],
        [0, -37.08830406, 22.46145741],
        [0, 0, 26.48752064],
        [0, -37.08829709, -2.301542445],
        [0, -37.08829864, 2.779946777],
        [0, -37.08830019, 7.861435068],
        [0, -37.08830174, 12.9427333],
        [0, -37.08830328, 18.02422253],
        [0, 0, 23.43284815],
        [0, -37.08829606, -7.585496552],
        [0, -37.08829787, -1.657059075],
        [1584.113903, 0, 3.424240557],
        [0, -37.08830096, 8.505728848],
        [0, -37.08830251, 13.58721807],
        [0, 0, 18.72869075],
        [0, -37.08829709, -6.094292964],
        [0, -37.08829864, -1.012803741],
        [0, -37.08830019, 4.06868455],
        [1584.113903, 0, 9.149982785],
        [0, 0, 13.40482639],
        [0, -37.08829658, -9.684351907],
        [0, -37.08829813, -4.603055652],
        [0, 0, 1.11055297],
        [0, 0, 4.647119799],
        [0, 0, -10.38141561],
        [0, 0, -4.455539773],
        [0, 0, 0.096823423],
        [0, 0, -5.283966886],
        [0, -37.08829348, -10.36549431],
        [0, -37.08829194, -15.4469826],
        [0, -37.08829039, -20.52847182],
        [0, -37.08828884, -25.60973186],
        [1584.113903, 0, -30.69121922],
        [0, -37.08829426, -9.721185776],
        [0, -37.08829271, -14.80249845],
        [0, -37.08829116, -19.88398674],
        [0, -37.08828962, -24.96547597],
        [0, -37.08828807, -30.04696519],
        [0, 0, -33.05002602],
        [0, -37.08829503, -9.076733463],
        [0, -37.08829348, -14.15826088],
        [0, -37.08829194, -19.23974917],
        [0, -37.08829039, -24.32100921],
        [0, -37.08828884, -29.40249843],
        [0, 0, -33.41747872],
        [0, -37.08829426, -13.51393589],
        [1584.113903, 0, -18.59524857],
        [0, -37.08829116, -23.67673686],
        [0, -37.08828962, -28.75822608],
        [0, 0, -32.98528229],
        [0, -37.08829503, -12.86948398],
        [0, -37.08829348, -17.9510114],
        [0, -37.08829194, -23.03249969],
        [1584.113903, 0, -28.11375973],
        [0, 0, -31.46183322],
        [0, -37.08829555, -13.07213992],
        [0, -37.088294, -18.15343769],
        [0, 0, -22.60280751],
        [0, 0, -27.25071701],
        [0, 0, -15.9640209],
        [0, 0, -21.01842564],
        [0, 0, -24.38691476],
        [0, 0, -5.928435659],
        [0, -37.08829271, -11.00974834],
        [0, -37.08829116, -16.09123663],
        [0, -37.08828962, -21.17272585],
        [0, -37.08828807, -26.25421507],
        [0, 0, -30.28400876],
        [0, 0, -1.491215364],
        [0, -37.08829348, -6.572742784],
        [0, -37.08829194, -11.65423108],
        [0, -37.08829039, -16.7357203],
        [0, -37.08828884, -21.81698034],
        [1584.113903, 0, -26.89846769],
        [0, -37.08829606, 3.792757411],
        [0, -37.08829426, -2.135681929],
        [0, -37.08829271, -7.216994605],
        [0, -37.08829116, -12.2984829],
        [0, -37.08828962, -17.37997212],
        [0, -37.08828807, -22.46146134],
        [0, 0, -26.48751468],
        [0, -37.08829503, 2.301536961],
        [0, -37.08829348, -2.779990459],
        [0, -37.08829194, -7.86147875],
        [0, -37.08829039, -12.94273879],
        [0, -37.08828884, -18.02422801],
        [0, 0, -23.43280196],
        [0, -37.08829606, 7.585511141],
        [0, -37.08829426, 1.657071801],
        [1584.113903, 0, -3.424240875],
        [0, -37.08829116, -8.505729166],
        [0, -37.08828962, -13.58721839],
        [0, 0, -18.72866134],
        [0, -37.08829503, 6.094290691],
        [0, -37.08829348, 1.012763271],
        [0, -37.08829194, -4.06872502],
        [1584.113903, 0, -9.149985058],
        [0, 0, -13.404786],
        [0, -37.08829555, 9.68436801],
        [0, -37.088294, 4.603070241],
        [0, 0, -1.110542395],
        [0, 0, -4.647078609],
        [0, 0, 10.38141995],
        [0, 0, 4.455541865],
        [0, 0, -0.096819272],
        [0, 0, 5.283975654],
        [0, -37.08829864, 10.36546488],
        [0, -37.08830019, 15.44695317],
        [0, -37.08830174, 20.52844891],
        [0, -37.08830328, 25.60974063],
        [1584.113903, 0, 30.6912373],
        [0, -37.08829787, 9.721194888],
        [0, -37.08829942, 14.80249452],
        [0, -37.08830096, 19.88398281],
        [0, -37.08830251, 24.96547204],
        [0, -37.08830406, 30.04696126],
        [0, 0, 33.05003197],
        [0, -37.08829709, 9.076727978],
        [0, -37.08829864, 14.1582172],
        [0, -37.08830019, 19.23970549],
        [0, -37.08830174, 24.32100373],
        [0, -37.08830328, 29.40249295],
        [0, 0, 33.4175249],
        [0, -37.08829787, 13.51394862],
        [1584.113903, 0, 18.59524825],
        [0, -37.08830096, 23.67673654],
        [0, -37.08830251, 28.75822577],
        [0, 0, 32.98531169],
        [0, -37.08829709, 12.86948171],
        [0, -37.08829864, 17.95097093],
        [0, -37.08830019, 23.03245922],
        [1584.113903, 0, 28.11375746],
        [0, 0, 31.46187361],
        [0, -37.08829658, 13.07215602],
        [0, -37.08829813, 18.15345228],
        [0, 0, 22.60281809],
        [0, 0, 27.2507582],
        [0, 0, 15.96402524],
        [0, 0, 21.01842773],
        [0, 0, 24.38691891],
    ]
    xzTable = [
        [0, 0, 96851.94476],
        [0, 20.35460762, 179968.7245],
        [0, 29.74916695, 263088.5903],
        [0, 39.143728, 346208.4713],
        [0, 48.53828906, 429328.3522],
        [0, 0, 495245.853],
        [0, 0, 55272.44624],
        [0, 15.65749762, 138392.3272],
        [0, 25.05205695, 221512.193],
        [0, 34.44663005, 304632.1806],
        [0, 43.84082595, 387748.8309],
        [-2495021.294, 0, 470868.8338],
        [0, 0.000014137, -157.7268321],
        [0, 10.96039708, 96816.01372],
        [0, 20.35460762, 179932.7935],
        [0, 29.74916695, 263052.6592],
        [0, 39.143728, 346172.5402],
        [0, 48.53828906, 429292.4212],
        [0, 0, 486786.4367],
        [0, 6.262936565, 55236.51505],
        [0, 15.65749762, 138356.396],
        [0, 25.05205695, 221476.2618],
        [0, 34.4462649, 304593.0187],
        [0, 43.84082595, 387712.8997],
        [0, 0, 464792.4638],
        [0, 0.000014137, -193.6578747],
        [0, 10.96039708, 96780.08268],
        [-2495021.294, 0, 179896.8625],
        [0, 29.74916695, 263016.7282],
        [0, 39.143728, 346136.6092],
        [0, 0, 422763.6432],
        [0, 6.262936565, 55200.584],
        [0, 15.65749762, 138320.465],
        [0, 25.05205695, 221440.3307],
        [-2495021.294, 0, 304557.0876],
        [0, 0, 366743.5516],
        [0, 3.131654697, 27478.10165],
        [0, 12.52585899, 110594.8262],
        [0, 0, 193720.6956],
        [0, 0, 260653.9946],
        [0, 0, 45411.8012],
        [0, 0, 135220.1763],
        [0, 0, 200008.1256],
        [0, 0, -55551.96887],
        [0, -15.65753996, -138672.4747],
        [0, -25.05209929, -221792.3404],
        [0, -34.44666034, -304912.2214],
        [0, -43.84079768, -388028.3535],
        [-2495021.294, 0, -471148.204],
        [0, -10.96037225, -97131.49786],
        [0, -20.35460691, -180248.491],
        [0, -29.74916624, -263368.3567],
        [0, -39.14372729, -346488.2377],
        [0, -48.53828834, -429608.1187],
        [0, 0, -487092.199],
        [0, -6.262908292, -55587.90006],
        [0, -15.65753996, -138708.4059],
        [0, -25.05209929, -221828.2716],
        [0, -34.44623663, -304944.4037],
        [0, -43.84079768, -388064.2847],
        [0, 0, -465130.2804],
        [0, -10.96037225, -97167.4289],
        [-2495021.294, 0, -180284.422],
        [0, -29.74916624, -263404.2878],
        [0, -39.14372729, -346524.1688],
        [0, 0, -423141.7785],
        [0, -6.262908292, -55623.83111],
        [0, -15.65753996, -138744.3369],
        [0, -25.05209929, -221864.2026],
        [-2495021.294, 0, -304980.3348],
        [0, 0, -367157.7209],
        [0, -3.131623625, -27937.25472],
        [0, -12.52583072, -111054.004],
        [0, 0, -194167.8966],
        [0, 0, -261111.2366],
        [0, 0, -45905.02879],
        [0, 0, -135705.3421],
        [0, 0, -200481.8321],
        [0, 0, -97095.56682],
        [0, -20.35460691, -180212.56],
        [0, -29.74916624, -263332.4257],
        [0, -39.14372729, -346452.3067],
        [0, -48.53828834, -429572.1877],
        [0, 0, -495489.0788],
        [0, 0, -55516.03781],
        [0, -15.65753996, -138636.5436],
        [0, -25.05209929, -221756.4093],
        [0, -34.44666034, -304876.2903],
        [0, -43.84079768, -387992.4224],
        [-2495021.294, 0, -471112.2729],
        [0, 0.000014137, -85.86471267],
        [0, -10.96037225, -97059.63574],
        [0, -20.35460691, -180176.6289],
        [0, -29.74916624, -263296.4946],
        [0, -39.14372729, -346416.3756],
        [0, -48.53828834, -429536.2566],
        [0, 0, -487030.0283],
        [0, -6.262908292, -55480.10675],
        [0, -15.65753996, -138600.6125],
        [0, -25.05209929, -221720.4783],
        [0, -34.44623663, -304836.6104],
        [0, -43.84079768, -387956.4914],
        [0, 0, -465035.6895],
        [0, 0.000014137, -49.93363583],
        [0, -10.96037225, -97023.70467],
        [-2495021.294, 0, -180140.6978],
        [0, -29.74916624, -263260.5635],
        [0, -39.14372729, -346380.4445],
        [0, 0, -423006.7168],
        [0, -6.262908292, -55444.17567],
        [0, -15.65753996, -138564.6815],
        [0, -25.05209929, -221684.5472],
        [-2495021.294, 0, -304800.6793],
        [0, 0, -366986.6555],
        [0, -3.131623625, -27721.6684],
        [0, -12.52583072, -110838.4177],
        [0, 0, -193964.2872],
        [0, 0, -260897.0985],
        [0, 0, -45655.44231],
        [0, 0, -135464.0116],
        [0, 0, -200251.7172],
        [0, 0, 55308.3773],
        [0, 15.65749762, 138428.2583],
        [0, 25.05205695, 221548.124],
        [0, 34.44663005, 304668.1117],
        [0, 43.84082595, 387784.7619],
        [-2495021.294, 0, 470904.7648],
        [0, 10.96039708, 96887.87584],
        [0, 20.35460762, 180004.6556],
        [0, 29.74916695, 263124.5214],
        [0, 39.143728, 346244.4023],
        [0, 48.53828906, 429364.2833],
        [0, 0, 486848.6074],
        [0, 6.262936565, 55344.30836],
        [0, 15.65749762, 138464.1893],
        [0, 25.05205695, 221584.0551],
        [0, 34.4462649, 304700.812],
        [0, 43.84082595, 387820.693],
        [0, 0, 464887.0548],
        [0, 10.96039708, 96923.80692],
        [-2495021.294, 0, 180040.5867],
        [0, 29.74916695, 263160.4524],
        [0, 39.143728, 346280.3334],
        [0, 0, 422898.7049],
        [0, 6.262936565, 55380.23944],
        [0, 15.65749762, 138500.1204],
        [0, 25.05205695, 221619.9862],
        [-2495021.294, 0, 304736.7431],
        [0, 0, 366914.617],
        [0, 3.131654697, 27693.68798],
        [0, 12.52585899, 110810.4125],
        [0, 0, 193924.305],
        [0, 0, 260868.1327],
        [0, 0, 45661.38768],
        [0, 0, 135461.5068],
        [0, 0, 200238.2405],
    ]
    yzTable = [
        [0, 0, 47.91959834],
        [0, -299230.5421, 68.61227411],
        [0, -299151.1504, 89.30571816],
        [0, -299071.7586, 109.999166],
        [0, -298992.3668, 130.6926138],
        [0, 0, 147.1033732],
        [0, 0, -72036.84567],
        [0, -299270.2366, -72016.15222],
        [0, -299190.8448, -71995.45878],
        [0, -299111.4529, -71974.7653],
        [0, -299032.0643, -71954.07266],
        [0, 0, -71933.37918],
        [0, -299402.5552, -144125.0592],
        [0, -299309.9309, -144100.9167],
        [0, -299230.5421, -144080.224],
        [0, -299151.1504, -144059.5306],
        [0, -299071.7586, -144038.8371],
        [0, -298992.3668, -144018.1437],
        [0, 0, -124563.7874],
        [0, -299349.6284, -216186.3076],
        [0, -299270.2366, -216165.6141],
        [0, -299190.8448, -216144.9207],
        [0, -299111.456, -216124.228],
        [0, -299032.0643, -216103.5346],
        [0, 0, -189601.0397],
        [0, -299402.5552, -288273.8955],
        [0, -299309.9309, -288249.753],
        [0, 0, -288229.0603],
        [0, -299151.1504, -288208.3669],
        [0, -299071.7586, -288187.6734],
        [0, 0, -270792.6367],
        [0, -299349.6284, -360335.1591],
        [0, -299270.2366, -360314.4657],
        [0, -299190.8448, -360293.7722],
        [0, 0, -360273.0796],
        [0, 0, -343026.6245],
        [0, -299376.0903, -432415.8337],
        [0, -299296.7015, -432395.141],
        [0, 0, -408349.8552],
        [0, 0, -429452.8324],
        [0, 0, -500612.7397],
        [0, 0, -484029.4101],
        [0, 0, -461516.1603],
        [0, 0, -72064.43641],
        [0, -299534.8744, -72085.13002],
        [0, -299614.2662, -72105.82346],
        [0, -299693.658, -72126.51691],
        [0, -299773.0462, -72147.20942],
        [0, 0, -72167.90286],
        [0, -299495.1795, -144149.2017],
        [0, -299574.5685, -144169.8944],
        [0, -299653.9603, -144190.5879],
        [0, -299733.3521, -144211.2813],
        [0, -299812.7438, -144231.9748],
        [0, 0, -124806.2434],
        [0, -299455.4821, -216213.8983],
        [0, -299534.8744, -216234.5919],
        [0, -299614.2662, -216255.2854],
        [0, -299693.6544, -216275.9779],
        [0, -299773.0462, -216296.6713],
        [0, 0, -189832.5524],
        [0, -299495.1795, -288298.038],
        [0, 0, -288318.7307],
        [0, -299653.9603, -288339.4242],
        [0, -299733.3521, -288360.1176],
        [0, 0, -271003.2325],
        [0, -299455.4821, -360362.7499],
        [0, -299534.8744, -360383.4435],
        [0, -299614.2662, -360404.1369],
        [0, 0, -360424.8294],
        [0, 0, -343209.3359],
        [0, -299429.0201, -432429.6299],
        [0, -299508.4089, -432450.3225],
        [0, 0, -408446.4235],
        [0, 0, -429582.7306],
        [0, 0, -500635.4738],
        [0, 0, -484096.8594],
        [0, 0, -461615.8659],
        [0, 0, -0.365392789],
        [0, -299574.5685, -21.05812168],
        [0, -299653.9603, -41.75156573],
        [0, -299733.3521, -62.44501357],
        [0, -299812.7438, -83.13846142],
        [0, 0, -99.549069],
        [0, 0, 72084.45329],
        [0, -299534.8744, 72063.75969],
        [0, -299614.2662, 72043.06624],
        [0, -299693.658, 72022.37279],
        [0, -299773.0462, 72001.68028],
        [0, 0, 71980.98684],
        [0, -299402.5552, 144172.7507],
        [0, -299495.1795, 144148.6082],
        [0, -299574.5685, 144127.9155],
        [0, -299653.9603, 144107.2221],
        [0, -299733.3521, 144086.5286],
        [0, -299812.7438, 144065.8352],
        [0, 0, 124611.2882],
        [0, -299455.4821, 216233.3735],
        [0, -299534.8744, 216212.6799],
        [0, -299614.2662, 216191.9865],
        [0, -299693.6544, 216171.2939],
        [0, -299773.0462, 216150.6005],
        [0, 0, 189649.2196],
        [0, -299402.5552, 288321.7244],
        [0, -299495.1795, 288297.5819],
        [0, 0, 288276.8891],
        [0, -299653.9603, 288256.1957],
        [0, -299733.3521, 288235.5022],
        [0, 0, 270839.8248],
        [0, -299455.4821, 360382.3471],
        [0, -299534.8744, 360361.6535],
        [0, -299614.2662, 360340.9601],
        [0, 0, 360320.2676],
        [0, 0, 343074.3009],
        [0, -299429.0201, 432463.6626],
        [0, -299508.4089, 432442.9699],
        [0, 0, 408397.5314],
        [0, 0, 429500.5393],
        [0, 0, 500660.2939],
        [0, 0, 484077.3304],
        [0, 0, 461563.5924],
        [0, 0, 72112.04403],
        [0, -299270.2366, 72132.73748],
        [0, -299190.8448, 72153.43092],
        [0, -299111.4529, 72174.1244],
        [0, -299032.0643, 72194.81704],
        [0, 0, 72215.51052],
        [0, -299309.9309, 144196.8932],
        [0, -299230.5421, 144217.5859],
        [0, -299151.1504, 144238.2793],
        [0, -299071.7586, 144258.9728],
        [0, -298992.3668, 144279.6662],
        [0, 0, 124853.7442],
        [0, -299349.6284, 216260.9643],
        [0, -299270.2366, 216281.6577],
        [0, -299190.8448, 216302.3511],
        [0, -299111.456, 216323.0438],
        [0, -299032.0643, 216343.7373],
        [0, 0, 189880.7323],
        [0, -299309.9309, 288345.8668],
        [0, 0, 288366.5595],
        [0, -299151.1504, 288387.253],
        [0, -299071.7586, 288407.9464],
        [0, 0, 271050.4206],
        [0, -299349.6284, 360409.9379],
        [0, -299270.2366, 360430.6313],
        [0, -299190.8448, 360451.3248],
        [0, 0, 360472.0174],
        [0, 0, 343257.0123],
        [0, -299376.0903, 432477.4587],
        [0, -299296.7015, 432498.1514],
        [0, 0, 408494.0998],
        [0, 0, 429630.4375],
        [0, 0, 500683.028],
        [0, 0, 484144.7798],
        [0, 0, 461663.298],
    ]
    xForces = []
    yForces = []
    zForces = []
    for i in range(len(xTable)):
        xForce = (
            wx * xTable[i][0]
            + wy * yTable[i][0]
            + wz * zTable[i][0]
            + wxwz * xzTable[i][0]
            + wywz * yzTable[i][0]
        ) / 1000.0
        yForce = (
            wx * xTable[i][1]
            + wy * yTable[i][1]
            + wz * zTable[i][1]
            + wxwz * xzTable[i][1]
            + wywz * yzTable[i][1]
        ) / 1000.0
        zForce = (
            wx * xTable[i][2]
            + wy * yTable[i][2]
            + wz * zTable[i][2]
            + wxwz * xzTable[i][2]
            + wywz * yzTable[i][2]
        ) / 1000.0
        xForces.append(xForce)
        yForces.append(yForce)
        zForces.append(zForce)

    return xForces, yForces, zForces
