clear all;
good_tracks_length = [13.352466618426725, 42.62911316712797, 52.795292247275825, 40.41000605101012, 23.461660318225277, 27.36934202478655, 53.408001048694736, 21.156174408610475, 39.348690598336034, 39.23810171321091, 54.0781306062251, 44.681731301300346, 40.183554937511566, 22.90004512748593, 23.961338103309508, 39.74483339686308, 39.673280975798576, 54.81237102587586, 52.375073397805515, 33.672439353463695, 39.01295100858388];
bad_tracks_length = [25.855971556037716, 29.615350409317827, 24.68908070835026, 20.275060595900968, 16.2796393517303, 15.624138829890398, 40.13734076910081, 25.20260089340659, 28.536350578923823, 14.98323438396217, 37.78015598405953, 17.251005021920008, 13.493904796813503, 14.62553998873252, 10.003021304171007, 13.405642334295756, 18.15660735589485, 25.321566874807026, 41.68099107864938, 37.74141597911486, 16.246944286613555, 25.162376578319808, 14.012336621467604, 29.318829570004354, 18.15968767321445, 33.674233227968884, 25.165158960705426, 16.93706356058984, 18.215055514137852, 10.277825902758728, 13.18751567349662, 26.3552168500554, 12.713912813885521, 23.233505076893206, 30.43354348438622, 14.18090135505247, 12.253535294008486, 12.350473459112207, 28.29371117668704, 24.716440242576518, 40.880209752029174, 17.294498563382767, 33.21963570052396, 25.62735896320212, 32.108405631239705, 17.453164466348703, 36.457953363626245, 14.333747979064185, 19.302312675861884, 15.152907991083012, 15.583678192720257, 17.34783501672014, 12.769800944916177, 23.780331624208465, 23.416531353690047, 44.48695139500977, 38.82846111238432, 38.181997874538, 15.009983897435802, 24.28405307188813, 20.633763632063364, 38.978284779884916, 54.5991041742649, 14.035707748519695, 18.763542177547187, 28.66748650177358, 31.748114667638802, 37.036153465811864, 30.29183822629024, 14.675551004057795, 25.973492772052424, 10.395345727137425, 30.977363477734798, 22.146948183475946, 28.474492631590522, 26.3746920846544, 15.195043514163018, 36.21827134878087, 25.012340988643558, 18.28311315354304, 18.374446710344913, 21.40156813566205, 26.944338507701975, 34.163530525093734, 24.390644680850478, 19.244378249142443, 19.948796682352253, 19.691005797946808, 18.68003153846761, 28.587838525275046, 15.57861419849246, 10.08181737936404, 11.621389413654121, 24.965707356122905, 53.25829802955366, 26.047892353378188, 34.57205025980537, 39.12462638360855, 31.32870365347945, 24.271284722911734, 18.98879183230916, 13.540729679346516, 14.253429814391552, 25.104350227239717, 41.37742289512576, 23.779500709604896, 26.726593174978305, 26.06345608360199, 47.19602942291724, 14.695595176206588, 35.19285315321938, 25.616369369803394, 40.05759490614429, 33.77027269558103, 18.180792520581377, 29.717639459891934, 18.665535472960514, 12.171564586629689, 30.548950851026504, 12.138948835597073, 17.57726338118698, 13.203560933709376, 38.14231527528466, 33.78597879244455, 30.184515619230474, 12.419763021808858, 15.149667656599092, 16.2767382901832, 11.667888731064412, 17.45364534007064, 23.85302957545241, 21.354402399806265, 20.015325118624375, 22.604890718749694, 30.24498727117284, 45.74369810371896, 37.92925706680627, 17.972853870392413, 29.758825125558715, 16.23828616858775, 30.0356089853367, 25.784627129082708, 28.418826670058223, 17.245673731914607, 41.55722166134773, 20.129475801433358, 22.629611515608943, 36.202136067128095, 34.139894263389664, 33.15829590653583, 44.91326967063912, 37.67867019330026, 42.38105524510331, 30.566150210524654, 33.88090977166627, 18.361343349768113, 13.381701995436224, 28.303379448641856, 10.082801143678026, 17.692720282129166, 17.165516831216166, 18.853307590040416, 31.513412362602907, 18.72818505618097, 39.83505216805767, 16.380942734644748, 22.348021771074187, 18.750305828228353, 18.6745939817918, 34.54615844962146, 17.217763277132462, 13.636955955354772, 39.03030151205677, 29.12841322781356, 17.10566238292718, 27.2605453530137, 18.60178234502727, 11.405296629957245, 28.526668289123883, 22.61569578122142, 39.99493820616229, 27.675756590231487, 31.278235480506027, 26.029028573852095, 33.365439961091724, 36.93165765317153, 19.263851191718345, 12.07469469322588, 34.92389866336153, 20.635331343033755, 28.851695464204322, 44.04329581074765, 40.397572385646676, 30.717057240026257, 34.59688150603898, 28.65118450797729, 31.90082955630878];
good_tracks_rho = [44.905577181743624, 82.014862711544438, 100.32816315764865, 66.058853074809065, 62.557945980761296, 93.091246430529026, 87.735554592104165, 85.810873771922687, 63.008162714408662, 63.710611274768404, 83.069878206016625, 80.32181667799577, 65.577361984141632, 55.452522434371865, 66.136466551021741, 58.737874312553146, 63.233737593073279, 81.784530550006224, 85.988729542477827, 68.732192570900352, 81.922838053425735];
bad_tracks_rho = [23.52213269041637, 49.637532598246977, 54.044411536056465, 51.908668052714376, 71.94924545194479, 47.84270309314028, 51.045580394842602, 51.536846992214414, 43.369643903244103, 68.971867667147308, 60.462778659852077, 16.214027391973705, 16.789114026539877, 25.082960697640345, 111.64877308655305, 54.358199343765769, 109.10811408352566, 64.63033482491484, 52.767336634123886, 93.433842372427776, 91.332438380482571, -2.5500975884734665, 21.639707518167022, 5.5193180826251336, 71.608271288236878, 78.833629251039412, 39.044260380278935, 78.795353967608122, 21.080610934495024, 57.448313242504859, -16.030598408474457, 32.322020293434853, -6.1351783284312509, 98.08618399666463, 25.413844077741324, 13.111725826713837, 96.03231641565857, 99.012722079332661, 23.919874452246624, 40.079445645948482, 37.272047198269178, 81.541123944252973, 103.1037764876761, 97.643413592020735, 21.034211914457597, 33.726920889728063, 41.648605844050124, 24.980081903008458, 60.512342792331239, 37.95306709696883, 45.084108030702637, 23.782591444443227, 45.112679329283424, 66.150532812925277, 56.018408710008543, 90.119732830268617, 57.485883580356635, 90.482261639881486, 47.347656079321915, 83.808827475066096, 71.547769042644632, 43.88945576272144, 101.6460770278905, 98.132294526710226, 29.649851301399217, -13.358692434470365, 18.027895449605349, 38.877219235999718, 98.636048263441694, 99.233772930396341, 81.161270993681981, 0.79955105536574445, 0.48588807447935084, 91.142017537434057, 7.1897879056544687, 52.540510503173529, 76.050430828228556, 11.754488912851501, 50.45530153361802, 40.848758845027824, 35.023749203639078, 61.117689907594709, 67.267304468142314, 49.50126483173166, 81.316410494148698, 89.027870109320432, 104.51022667269058, 90.772248546667527, 56.544796204489352, 29.404164315141081, 92.846541332645998, 32.766995989413047, 106.07982363318563, 99.621784314766032, 74.341455267180933, 69.242661698942385, 52.340381186530429, 58.050491674790152, 100.51713529062478, 63.875329561026774, 61.520517933132119, 50.060378238565335, 58.601187514426094, 55.388024910176014, 57.832135577994165, 22.514878151843874, 85.336464548652188, 21.578343061883668, 63.428706653431142, 32.379233499722851, 57.231622489251428, -16.93417551823218, 46.548248005978202, 67.301821876856394, 50.864228024604181, 70.697546266758891, 101.47582209791339, 98.882416882068881, 24.977540745337425, 69.191227483010096, 55.534338746845016, 30.313964948102431, 87.555648491934889, 63.809851430620505, 75.6572524935779, 67.526753099972268, 84.370691192975343, 80.085626012827689, 62.182980093494322, 84.352394074959378, 66.881168769752691, 46.114559210890818, 63.212036988247213, 35.319294598207534, 57.058824343311834, 99.201093075242511, 56.658374484836948, 54.864149122144802, 30.382597785018298, 43.619654395226739, 33.794537190840401, 86.133636051962199, 7.2297483379918663, 111.43687371824936, 60.379158105893225, 58.513737608990489, 46.878985341565375, 43.923559200290256, 40.346444321486139, 45.848149916591083, 59.939174781035376, 45.636418746262059, 53.078392301981722, -0.047047646882056669, 36.805199986035753, 43.528731759419912, 33.930222735779907, 44.024239113461441, 64.526322787657534, 97.287893321867202, 4.3056551966239631, 57.732242036994577, 63.893386780320725, 44.719606204511749, 100.46017193021625, 36.064575771547183, 62.659952692132762, 49.528104135935763, 24.227652700606725, 55.906738753327183, 45.688022971010056, 36.912413788120041, 64.193595599472459, 64.037313353432893, 31.208628891266734, 62.848474472517275, 49.082188545192594, 49.839991714268407, 98.599693085264775, 29.431783987768345, 82.425963281282549, 102.13889509864954, 10.071389530647346, 16.599968568401501, 56.369983910668545, 104.67221757191885, 77.779178912957818, 2.4931062433967774, 40.173561003155299, 48.520477468784591, 63.023167497609229, 57.017734240692519, 40.622303177641363, 53.342892776378847, 28.233651093471199, -12.193546830615874, 49.094280233564291];
good_tracks_theta = [0.61054512892607138, 0.0089378039663598283, 0.13193637522295323, -0.10222188055032619, -0.31731548294624934, 0.30472230891184332, 0.054683365603341631, 0.14293962482160993, 0.014393062498314981, 0.043717729450788077, 0.036363935779708915, 0.05403018004469038, 0.028772724680649824, 0.0041445746599256747, 0.55911664655234916, -0.0261548382378138, -0.11294164560543897, 0.18147520074099574, 0.12957368036681638, -0.11415847820018302, 0.23496929367146863];
bad_tracks_theta = [1.13167226192047, -0.18704173142856104, 0.51919484719487374, 0.40352781585482628, -0.15742645140381475, 0.51426628622775972, -0.073554333837951333, -0.28810481662857118, 0.39755021643378041, -0.92686510245814713, 0.73673858848613205, 0.59355827851192355, 0.99288167399520777, 0.85302726689586073, -0.72170286696302843, 0.84078929596439178, -0.29430237766482409, -0.42407504939228824, 0.72054556665561353, 0.18921820294789954, -0.17587177428800393, 1.2638498586737781, 0.84659509208205408, 1.1899756707605871, 0.34626015670052063, 0.098863928566037346, -1.5145301079089732, 0.087785645139891066, 0.3845232076945288, -0.21256076565294355, 1.2470697569850098, 0.49018406540126291, 1.2412840241973253, -0.1843549403829636, 0.42424187115548045, 1.1434577799229273, -0.356592589340678, -0.085863531572616891, 1.2486370992913782, 0.55220044540249047, 0.18617920908820029, 0.26375577151572588, -0.37232657848961276, -0.71930036703936029, 0.92676435987170913, 0.62776487887139254, 0.73326757693974853, 0.94151489046746573, 0.67540868115413089, 0.9484435014119672, 0.61397201961528869, 0.81986160850278789, 0.58585379279981797, 0.33922853319390961, 0.48881252536147313, 0.18797430144596153, 0.55042367569969741, 0.20461211062562862, 0.8979654741124784, -0.68770803587734741, -0.14379833745121764, 0.71437356969618271, -0.40897189409752988, 0.21265211231194556, 0.75015570401439957, 1.2519286881420595, 0.99807874766826843, 0.77472988963794909, 0.21397641109378884, -0.39449628454728242, 0.50699193903405959, 1.1701349176858988, 1.0009052511325671, 0.084538132860892221, 0.91228231589470776, 0.90890008237629194, -0.73215757365437062, 0.82616188933566359, 0.30441780610364266, 0.49300295674930694, 0.52366992984994787, -0.22234019619212372, -0.026471569774435606, -0.16471040775490284, 0.30501229296337995, 0.45264539249463126, 0.07818180911021344, 0.11006915809047672, 0.25157622818306108, 0.49317981364427993, -0.94081864398621595, 0.75947216107353621, -0.36271098248209876, -0.81032246469952929, 0.46718270892835384, 0.52702849133399643, 0.81518853675624836, 0.75117750884411305, 0.050119576733395253, -0.21328265475641361, -0.075697203194725615, -0.32224044392802009, -0.043659351119966321, 0.00037258985994033513, 0.70511773703898395, 0.50856888168635694, 0.29679160655507086, 0.47979403737252024, 0.60652260439920291, 0.38381960582959068, 0.79228495585873449, 1.3874986328851155, 0.07661164656551446, 0.67334523603104002, 0.84223752425220699, 0.61599044398826608, -0.90337585169582324, 0.21894612440618286, 0.94613652521704372, -0.30014407766706519, 0.11594603653954416, 0.27589592625243781, 0.1401392045800797, 0.07256997945994674, 0.35980277233854763, -0.19885057437469997, -0.26298568822791113, 0.24960620710218603, 0.056537196433893364, -0.049581146076695032, -0.18571566882731144, 0.41913251231442, -1.4590043173774605, 0.58890500220364117, -1.0959398957296416, 0.14622315158961435, -0.016124310901845948, -0.22720739327224837, 0.46537515068833352, 0.72585486944599276, 0.49499568746065797, 0.11426639637491647, 1.1793330004451024, -0.10109127746757589, 0.52872776640166108, 0.41713227112907497, 0.49262689500371709, 0.69823053284659586, 0.76173322330373439, 0.65717773974894733, 0.55282701392139966, 0.76473506951394377, 0.66158472936823087, 1.1532924002377354, 0.13562097485259092, 0.52661494541132325, 0.44937912280326692, 0.49212335409071001, 0.28830336136746659, 0.31131907338839321, 0.72061976213625656, -0.37358348349510406, 0.44090162090242851, 0.063972002504068967, -0.17108687797183297, 0.3644142721401204, -0.1197824350611824, -0.24316495112604827, 0.76046375480735695, 0.2380686511482934, -1.0884411737051631, 0.69621026890386961, -0.57633395711286517, 0.7488903482017828, 0.55572925360413217, -0.019946472021562987, 0.37499379900815927, -0.7677365901268608, 0.21775635516505676, 0.25263056659158706, 0.41664299423635909, 0.070862618733629645, 1.0526966514417466, 0.841670179906157, 0.54445488891293481, -0.026874245426947958, -1.0741043448863365, 0.6514878562960208, 0.85896306162989045, 0.26196336996601705, -0.26370632593360405, 0.6348680448055265, 0.023062240244444403, -0.1298631758500991, 0.8562701533337479, 1.260483472898452, 0.26610874277855878];
good_tracks_x0 = [8.45727, 12.8432, 1.29191, 8.40215, 8.62263, 1.62264, 1.92924, 1.43315, 8.788, 8.788, 1.37803, 10.3628, 8.67775, 8.45727, 3.74823, 8.51239, 8.56751, 1.21266, 1.37803, 9.78018, 1.43315];
bad_tracks_x0 = [11.6857, 22.5131, 31.9082, 8.84312, 31.3566, 8.29191, 21.6863, 21.5761, 22.1514, 16.6707, 1.48827, 30.5608, 16.3396, 16.8357, 46.1777, 1.37803, 37.9957, 39.5697, 11.4652, 2.06361, 1.43315, 29.2624, 21.8207, 26.4271, 30.0341, 21.5765, 33.3104, 19.3165, 45.0267, 8.67776, 44.059, 21.6312, 26.0099, 2.61482, 28.1355, 10.1109, 8.40253, 1.29191, 1.76388, 13.3079, 21.9619, 14.9068, 6.74889, 36.1767, 35.1604, 21.7105, 27.0886, 10.1109, 23.4747, 11.3549, 41.1135, 18.8752, 8.788, 32.9004, 33.3414, 10.4179, 22.1828, 18.0728, 3.19702, 14.9309, 27.7187, 26.372, 5.42599, 1.18167, 15.7333, 41.2237, 31.0814, 27.4744, 1.40215, 40.0662, 4.54406, 33.3414, 25.9858, 1.76388, 25.9307, 1.43315, 1.07142, 21.7966, 23.0334, 17.3318, 25.8445, 41.1682, 21.8758, 21.9068, 31.9875, 1.56751, 5.64647, 1.37803, 19.5366, 22.0171, 36.2869, 11.2684, 42.7051, 36.8381, 2.37021, 26.1205, 3.58287, 1.819, 2.89042, 23.1436, 9.0636, 21.8517, 34.1127, 8.34703, 5.56723, 27.5843, 19.6162, 32.3798, 5.29162, 31.3325, 1.37803, 25.2141, 22.2927, 1.43315, 15.5131, 1.26779, 43.7524, 1.18167, 28.9868, 37.0582, 23.1987, 36.979, 1.15754, 13.804, 1.37803, 8.12654, 9.59107, 5.01602, 8.45727, 1.37803, 25.0177, 8.5124, 52.1859, 19.5366, 29.0967, 9.61519, 8.40215, 22.6234, 21.6312, 43.1461, 22.1273, 29.5931, 25.3798, 38.1059, 17.3873, 36.814, 8.56752, 28.3254, 29.2073, 29.0971, 16.5604, 19.2063, 18.6551, 35.7116, 28.5765, 8.34703, 36.507, 9.06361, 45.5473, 1.40215, 40.6721, 35.9868, 21.3009, 21.8517, 1.45727, 23.0092, 25.6241, 22.5683, 22.9231, 8.45727, 16.1742, 8.40215, 20.2532, 1.21266, 30.2542, 21.49, 8.45727, 21.6863, 2.8353, 40.3414, 1.32291, 1.40215, 34.1131, 21.521, 26.7027, 17.1909, 31.3811, 50.6731, 16.7258, 28.3801, 8.56751, 13.6149, 21.8517, 21.7966, 32.7351, 38.6881, 14.4655];
good_tracks_y0 = [60.18, 81.75, 101.44, 65.735, 62.71, 97.92, 87.8, 87.03, 63.59, 64.195, 83.29, 80.65, 66.01, 55.56, 80.925, 58.86, 62.82, 83.235, 86.315, 67.99, 84.335];
bad_tracks_y0 = [80.98, 46.265, 81.145, 60.455, 67.88, 59.3, 49.62, 47.31, 56.0, 93.245, 82.52, 40.875, 55.01, 57.21, 107.82, 83.455, 102.76, 53.085, 81.035, 95.225, 93.135, 83.95, 57.76, 80.925, 86.865, 81.09, 107.765, 81.035, 41.37, 56.825, 81.365, 48.025, 55.45, 99.405, 41.095, 55.175, 98.965, 99.075, 80.705, 54.955, 42.415, 88.68, 107.655, 98.25, 81.915, 57.815, 81.2, 56.44, 95.61, 81.035, 84.335, 55.12, 59.905, 81.42, 81.365, 93.355, 81.585, 95.885, 80.76, 96.655, 68.045, 81.2, 108.48, 100.395, 55.23, 80.98, 80.705, 81.42, 101.22, 90.715, 95.17, 81.145, 41.205, 91.595, 45.385, 86.865, 102.1, 41.535, 59.96, 55.45, 55.285, 53.305, 67.055, 46.54, 95.555, 99.515, 105.565, 91.265, 63.315, 45.22, 107.875, 55.505, 97.645, 106.225, 84.5, 95.28, 80.925, 80.87, 101.22, 60.18, 60.84, 45.88, 56.935, 55.67, 80.98, 41.535, 95.39, 41.59, 81.42, 47.915, 82.355, 40.985, 48.465, 86.59, 94.07, 87.525, 107.985, 101.66, 83.07, 60.73, 58.695, 41.865, 88.68, 65.46, 81.42, 67.605, 84.5, 84.005, 62.49, 84.28, 62.82, 54.845, 107.875, 54.955, 67.935, 101.275, 56.66, 50.885, 45.0, 96.27, 50.61, 90.055, 81.145, 107.93, 80.32, 80.87, 57.155, 80.705, 82.905, 80.595, 81.035, 81.805, 81.53, 80.485, 41.645, 55.065, 55.065, 54.955, 81.09, 102.1, 41.315, 47.695, 81.035, 46.045, 101.715, 47.035, 59.52, 45.715, 55.065, 59.245, 67.935, 54.845, 63.7, 87.8, 55.45, 62.05, 55.45, 49.015, 101.385, 41.095, 90.33, 102.265, 81.09, 48.63, 82.3, 103.86, 105.345, 41.975, 81.09, 57.925, 62.93, 80.98, 41.59, 50.83, 80.65, 80.705, 54.9];
good_tracks_Nhits = [78, 269, 148, 99, 69, 149, 227, 58, 89, 112, 199, 160, 179, 78, 79, 116, 111, 171, 213, 92, 129];
bad_tracks_Nhits = [98, 120, 115, 73, 68, 26, 140, 103, 111, 104, 147, 98, 61, 58, 77, 307, 137, 76, 130, 135, 71, 154, 90, 175, 26, 230, 128, 52, 101, 24, 273, 148, 49, 76, 110, 98, 141, 140, 94, 108, 153, 36, 126, 153, 45, 54, 124, 76, 133, 38, 42, 60, 60, 142, 55, 155, 169, 136, 408, 126, 89, 101, 102, 40, 44, 22, 28, 53, 139, 55, 157, 64, 58, 29, 21, 92, 197, 199, 80, 84, 49, 52, 313, 97, 57, 169, 179, 61, 39, 85, 199, 35, 121, 166, 170, 152, 107, 55, 317, 42, 36, 72, 76, 58, 177, 187, 93, 72, 69, 64, 160, 274, 106, 97, 112, 37, 62, 314, 22, 241, 332, 176, 137, 417, 147, 105, 57, 107, 51, 58, 211, 158, 65, 124, 154, 122, 146, 28, 168, 180, 104, 121, 71, 26, 133, 110, 211, 70, 44, 30, 48, 36, 38, 28, 218, 41, 30, 130, 63, 79, 76, 337, 197, 164, 417, 137, 176, 103, 125, 319, 148, 62, 157, 106, 167, 210, 215, 147, 84, 72, 89, 90, 236, 169, 153, 91, 66, 31, 108, 90, 73, 244, 328, 68, 25, 22, 98];
good_tracks_R2 = [4.1842939642602532, 13.711992687143928, 7.487738934725928, 4.8720923085322259, 2.1053584332955406, 1.8985614909768249, 12.674075724955971, 1.2888694040209825, 6.632244670266048, 6.8726961684780505, 11.855902274292841, 3.7001700470765044, 8.4991103593993671, 2.4443329584303548, 2.4875656967249187, 10.341217157618491, 5.8952841210927511, 5.2971888278197996, 14.728037908934404, 1.2878714338797477, 3.9429266992772258];
bad_tracks_R2 = [3.5684129140851248, 6.1591872996039285, 6.6875319496181653, 3.290555103618916, 1.263039827018839, 0.85361116972746076, 6.4938160732341412, 0.77725943173665513, 2.2267679121318338, 6.6620067607005664, 9.2414576178373338, 2.9569983618671332, 4.9832113555210178, 2.7076261623988715, 3.9518795323623745, 20.127308985428897, 7.7729616168222799, 0.38003830630375385, 8.9512932862427785, 9.2480107246919552, 5.8185960477585441, 4.0815699229951736, 1.4116680263580326, 6.88621843410714, 0.75403536485651479, 13.75329511013009, 3.8327086996668585, 1.5080136844507599, 2.3468116295105363, 0.50394805898241157, 28.715181230673899, 4.5551477995549412, 2.462607667729289, 2.1495486765347533, 7.6373928050072522, 6.1278183474000754, 4.3839053311885348, 5.2590034912951955, 4.9514863017553736, 7.5909304359820844, 6.4869846469665013, 0.88185069949135231, 8.0592087525541007, 5.915509336672514, 1.8722450903644727, 3.1771240935874494, 7.1130049764454597, 4.1828317459057969, 8.6597048327165513, 0.57395717829789905, 1.437511147368876, 3.9187458336310148, 3.1036630260581712, 13.804472464224396, 2.2196020769047378, 5.5494089684688914, 12.159807597946145, 5.3309238016549285, 36.020775711515448, 5.7722556442934279, 6.3666136540802798, 5.8063604419937427, 3.0829207958755918, 0.77579316876990723, 2.6727878254589386, 2.2256384859613854, 2.0419707751873486, 3.9782864486977836, 4.1834967591324457, 1.6091903609887224, 3.3043434295983936, 0.75599878410442045, 3.1942345270236117, 1.0428343148668653, 0.81199558618694145, 6.8474935615317776, 9.3718370695284516, 11.172501453122811, 4.4807426445346739, 6.0312699107088488, 0.8597529705801461, 2.6168880380501607, 18.312450100056978, 2.612305059434215, 1.1250303576397542, 12.709384386668798, 15.49518235325495, 3.4691209759180599, 0.33778908692514142, 3.7567743495011277, 11.920133338283934, 0.44348166133677819, 4.570954565118801, 4.5047789521366903, 7.6920749084683058, 8.663782768773542, 2.0506187764348152, 0.85764770249120736, 20.522375946482647, 0.18509767903935814, 0.42673838532483699, 4.7200704307634522, 2.5966770944387578, 3.9347870520855217, 14.174805387236736, 12.726951863915611, 3.4214238540741428, 3.5014544595219621, 3.65700469542183, 4.2150730904127984, 4.7902807028144947, 20.619595190749529, 2.2031982380048292, 3.2990029409214019, 5.2672367989672084, 1.2351065240341714, 2.3200253856407973, 23.245896323642501, 2.1566180068727103, 15.484312689434976, 24.353433391960401, 9.8576047163905809, 11.054215914784642, 21.594764209275972, 8.3081646291104665, 6.8301451281378824, 1.9955413558467605, 4.2316936920321648, 2.4600531394267824, 1.3826250247474394, 11.403788957740899, 12.984062208815773, 4.933357858323701, 2.3869762577458764, 11.542368988493477, 7.7679528984131823, 7.5281808347466779, 0.74841575018256878, 9.6998595620286601, 8.6783573918075501, 4.7893726402312344, 3.9865249924472899, 6.4226399224557991, 1.6379338164108472, 8.3874518730230712, 4.4355561443707829, 8.2859636983829432, 4.7787571769829542, 4.0059373587590494, 2.6258381215111215, 3.5529161086695713, 1.8596205724156682, 3.5428202489819798, 1.79413820118727, 17.782864940403723, 1.7278501326127673, 0.59825536853560612, 6.6649877928429566, 1.5696449948991442, 3.1442327474261149, 3.0651124349504859, 13.863645123104225, 12.176789440480965, 10.836353015842437, 24.992145652708842, 7.0551246377347665, 9.8675772849387045, 1.8890429414259557, 9.1934943355159273, 12.729104422568717, 6.8454498763314513, 1.6592826056311121, 9.0360932396783262, 5.0673966353493567, 9.4007597389691551, 12.810144270628864, 12.717450455697255, 4.214345346469818, 1.1320786503153446, 3.24473305557117, 6.9178345655749824, 1.923427228034597, 6.0764892656610883, 11.361902255843209, 5.7814561170729792, 2.035984759065729, 2.1271318039431417, 1.7184224706420439, 4.5929499559207434, 1.9076579893646226, 0.68880146992691238, 13.9437878087725, 26.609123717241516, 3.4741867897854046, 1.5113754646527273, 1.2780985420114825, 7.9449159484488501];
save('Run26.mat')
