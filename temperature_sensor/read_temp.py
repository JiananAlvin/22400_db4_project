from machine import Pin
from machine import ADC
from math import log
import constant


class TemperatureSensor():
    adc_V_lookup = [0.03705883, 0.02161765, 0.0432353, 0.06485295, 0.08647059, 0.09264707, 0.09882354, 0.1012941,
                    0.1037647, 0.1062353, 0.1087059, 0.1111765, 0.1152941, 0.1194118, 0.1235294, 0.1276471, 0.1317647,
                    0.1358824, 0.1389706, 0.1420588, 0.1451471, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882,
                    0.1647059, 0.1688235, 0.1729412, 0.1754118, 0.1778824, 0.180353, 0.1828235, 0.1852941, 0.1894118,
                    0.1935294, 0.1976471, 0.2007353, 0.2038235, 0.2069118, 0.21, 0.2130883, 0.2161765, 0.2192647,
                    0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2388236, 0.2429412, 0.2470588, 0.2501471, 0.2532353,
                    0.2563236, 0.2594118, 0.2625, 0.2655883, 0.2686765, 0.2717647, 0.2758824, 0.28, 0.2841177,
                    0.2872059, 0.2902942, 0.2933824, 0.2964706, 0.3005883, 0.3047059, 0.3088235, 0.3119118, 0.315,
                    0.3180882, 0.3211765, 0.3242647, 0.327353, 0.3304412, 0.3335294, 0.3366177, 0.3397059, 0.3427941,
                    0.3458824, 0.35, 0.3541177, 0.3582353, 0.3613235, 0.3644118, 0.3675, 0.3705883, 0.3736765,
                    0.3767647, 0.379853, 0.3829412, 0.3891177, 0.3952941, 0.3994118, 0.4035295, 0.4076471, 0.4101177,
                    0.4125883, 0.4150588, 0.4175294, 0.42, 0.4241177, 0.4282353, 0.432353, 0.4354412, 0.4385294,
                    0.4416177, 0.4447059, 0.4477942, 0.4508824, 0.4539706, 0.4570589, 0.4601471, 0.4632353, 0.4663236,
                    0.4694118, 0.4735294, 0.4776471, 0.4817647, 0.4858823, 0.4900001, 0.4941177, 0.4972059, 0.5002942,
                    0.5033824, 0.5064706, 0.5089412, 0.5114118, 0.5138824, 0.5163529, 0.5188236, 0.5219118, 0.525,
                    0.5280883, 0.5311765, 0.5342648, 0.537353, 0.5404412, 0.5435295, 0.547647, 0.5517647, 0.5558824,
                    0.56, 0.5641177, 0.5682353, 0.5713236, 0.5744118, 0.5775001, 0.5805883, 0.5847059, 0.5888236,
                    0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6094118, 0.6135294, 0.6176471, 0.6207353,
                    0.6238235, 0.6269117, 0.63, 0.6330882, 0.6361765, 0.6392647, 0.642353, 0.6454412, 0.6485294,
                    0.6516176, 0.6547059, 0.6588235, 0.6629412, 0.6670588, 0.6695294, 0.672, 0.6744706, 0.6769412,
                    0.6794118, 0.6855883, 0.6917647, 0.6942353, 0.6967059, 0.6991765, 0.701647, 0.7041177, 0.7102942,
                    0.7164706, 0.7189412, 0.7214118, 0.7238824, 0.7263529, 0.7288236, 0.7329412, 0.7370589, 0.7411765,
                    0.7442647, 0.747353, 0.7504412, 0.7535295, 0.7566176, 0.7597059, 0.7627941, 0.7658824, 0.77,
                    0.7741177, 0.7782353, 0.78, 0.7817647, 0.7835294, 0.7852942, 0.7870589, 0.7888236, 0.7905883,
                    0.7936765, 0.7967648, 0.7998529, 0.8029412, 0.8070589, 0.8111765, 0.8152942, 0.8177647, 0.8202353,
                    0.8227058, 0.8251765, 0.8276471, 0.8317648, 0.8358824, 0.8400001, 0.8430882, 0.8461765, 0.8492647,
                    0.852353, 0.8564707, 0.8605883, 0.8647059, 0.8677941, 0.8708824, 0.8739706, 0.8770589, 0.8811766,
                    0.8852942, 0.8894118, 0.8925, 0.8955883, 0.8986765, 0.9017648, 0.904853, 0.9079412, 0.9110294,
                    0.9141177, 0.9182354, 0.9223529, 0.9264707, 0.9289412, 0.9314118, 0.9338823, 0.936353, 0.9388236,
                    0.9419118, 0.9450001, 0.9480883, 0.9511765, 0.9542647, 0.957353, 0.9604412, 0.9635295, 0.9666177,
                    0.969706, 0.9727942, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9923531, 0.9964705,
                    1.000588, 1.003677, 1.006765, 1.009853, 1.012941, 1.017059, 1.021176, 1.025294, 1.028382, 1.031471,
                    1.034559, 1.037647, 1.040735, 1.043824, 1.046912, 1.05, 1.053088, 1.056177, 1.059265, 1.062353,
                    1.065441, 1.068529, 1.071618, 1.074706, 1.078824, 1.082941, 1.087059, 1.091177, 1.095294, 1.099412,
                    1.1025, 1.105588, 1.108677, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.128235, 1.132353,
                    1.136471, 1.138941, 1.141412, 1.143882, 1.146353, 1.148824, 1.152941, 1.157059, 1.161177, 1.164265,
                    1.167353, 1.170441, 1.17353, 1.177647, 1.181765, 1.185882, 1.188971, 1.192059, 1.195147, 1.198235,
                    1.202353, 1.206471, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.226029, 1.229118, 1.232206,
                    1.235294, 1.238382, 1.241471, 1.244559, 1.247647, 1.251765, 1.255882, 1.26, 1.263088, 1.266176,
                    1.269265, 1.272353, 1.275441, 1.278529, 1.281618, 1.284706, 1.288824, 1.292941, 1.297059, 1.300147,
                    1.303235, 1.306324, 1.309412, 1.313529, 1.317647, 1.321765, 1.324853, 1.327941, 1.331029, 1.334118,
                    1.337206, 1.340294, 1.343382, 1.346471, 1.348941, 1.351412, 1.353882, 1.356353, 1.358824, 1.361912,
                    1.365, 1.368088, 1.371176, 1.375294, 1.379412, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882,
                    1.398971, 1.402059, 1.405147, 1.408235, 1.412353, 1.416471, 1.420588, 1.423676, 1.426765, 1.429853,
                    1.432941, 1.436029, 1.439118, 1.442206, 1.445294, 1.448382, 1.451471, 1.454559, 1.457647, 1.460735,
                    1.463824, 1.466912, 1.47, 1.476177, 1.482353, 1.484824, 1.487294, 1.489765, 1.492235, 1.494706,
                    1.498824, 1.502941, 1.507059, 1.510147, 1.513235, 1.516324, 1.519412, 1.5225, 1.525588, 1.528677,
                    1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.548235, 1.552353, 1.556471, 1.559559, 1.562647,
                    1.565735, 1.568824, 1.571912, 1.575, 1.578088, 1.581177, 1.583647, 1.586118, 1.588588, 1.591059,
                    1.593529, 1.596618, 1.599706, 1.602794, 1.605882, 1.61, 1.614118, 1.618235, 1.622353, 1.626471,
                    1.630588, 1.633677, 1.636765, 1.639853, 1.642941, 1.646029, 1.649118, 1.652206, 1.655294, 1.658382,
                    1.661471, 1.664559, 1.667647, 1.671765, 1.675882, 1.68, 1.684118, 1.688235, 1.692353, 1.694824,
                    1.697294, 1.699765, 1.702235, 1.704706, 1.708824, 1.712941, 1.717059, 1.720147, 1.723235, 1.726324,
                    1.729412, 1.733529, 1.737647, 1.741765, 1.744853, 1.747941, 1.751029, 1.754118, 1.758235, 1.762353,
                    1.766471, 1.769559, 1.772647, 1.775735, 1.778824, 1.781294, 1.783765, 1.786235, 1.788706, 1.791177,
                    1.794265, 1.797353, 1.800441, 1.80353, 1.807647, 1.811765, 1.815882, 1.818971, 1.822059, 1.825147,
                    1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.843677, 1.846765, 1.849853, 1.852941, 1.857059,
                    1.861177, 1.865294, 1.869412, 1.87353, 1.877647, 1.880735, 1.883824, 1.886912, 1.89, 1.893088,
                    1.896177, 1.899265, 1.902353, 1.90647, 1.910588, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059,
                    1.930147, 1.933235, 1.936324, 1.939412, 1.9425, 1.945588, 1.948677, 1.951765, 1.955882, 1.96,
                    1.964118, 1.968235, 1.972353, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.992941, 1.997059,
                    2.001177, 2.005294, 2.009412, 2.01353, 2.016, 2.018471, 2.020941, 2.023412, 2.025882, 2.028971,
                    2.032059, 2.035147, 2.038235, 2.042353, 2.046471, 2.050588, 2.054706, 2.058824, 2.062941, 2.06603,
                    2.069118, 2.072206, 2.075294, 2.079412, 2.083529, 2.087647, 2.090735, 2.093824, 2.096912, 2.1,
                    2.103088, 2.106177, 2.109265, 2.112353, 2.116471, 2.120588, 2.124706, 2.127177, 2.129647, 2.132118,
                    2.134588, 2.137059, 2.141176, 2.145294, 2.149412, 2.153529, 2.157647, 2.161765, 2.164853, 2.167941,
                    2.17103, 2.174118, 2.176588, 2.179059, 2.18153, 2.184, 2.186471, 2.190588, 2.194706, 2.198824,
                    2.201294, 2.203765, 2.206235, 2.208706, 2.211177, 2.215294, 2.219412, 2.22353, 2.226, 2.228471,
                    2.230941, 2.233412, 2.235883, 2.24, 2.244118, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588,
                    2.264706, 2.268824, 2.272941, 2.277059, 2.281177, 2.285294, 2.287765, 2.290235, 2.292706, 2.295177,
                    2.297647, 2.300735, 2.303824, 2.306912, 2.31, 2.313088, 2.316177, 2.319265, 2.322353, 2.326471,
                    2.330588, 2.334706, 2.337177, 2.339647, 2.342118, 2.344588, 2.347059, 2.351177, 2.355294, 2.359412,
                    2.361471, 2.363529, 2.365588, 2.367647, 2.369706, 2.371765, 2.374235, 2.376706, 2.379177, 2.381647,
                    2.384118, 2.388235, 2.392353, 2.396471, 2.398941, 2.401412, 2.403883, 2.406353, 2.408823, 2.415,
                    2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.436618, 2.439706, 2.442794, 2.445882, 2.448353,
                    2.450824, 2.453294, 2.455765, 2.458235, 2.462353, 2.466471, 2.470588, 2.473676, 2.476765, 2.479853,
                    2.482941, 2.485412, 2.487882, 2.490353, 2.492824, 2.495294, 2.499412, 2.50353, 2.507647, 2.510735,
                    2.513824, 2.516912, 2.52, 2.522471, 2.524941, 2.527412, 2.529882, 2.532353, 2.536471, 2.540588,
                    2.544706, 2.546765, 2.548824, 2.550882, 2.552941, 2.555, 2.557059, 2.561177, 2.565294, 2.569412,
                    2.571882, 2.574353, 2.576824, 2.579294, 2.581765, 2.584235, 2.586706, 2.589177, 2.591647, 2.594118,
                    2.596588, 2.599059, 2.60153, 2.604, 2.606471, 2.608941, 2.611412, 2.613883, 2.616353, 2.618824,
                    2.621294, 2.623765, 2.626235, 2.628706, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.646618,
                    2.649706, 2.652794, 2.655882, 2.658353, 2.660824, 2.663294, 2.665765, 2.668235, 2.670706, 2.673177,
                    2.675647, 2.678118, 2.680588, 2.683059, 2.685529, 2.688, 2.690471, 2.692941, 2.695412, 2.697882,
                    2.700353, 2.702824, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720118, 2.722588,
                    2.725059, 2.72753, 2.73, 2.732471, 2.734941, 2.737412, 2.739882, 2.742353, 2.744824, 2.747294,
                    2.749765, 2.752235, 2.754706, 2.757176, 2.759647, 2.762118, 2.764588, 2.767059, 2.769529, 2.772,
                    2.774471, 2.776941, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.793824, 2.795882,
                    2.797941, 2.8, 2.802059, 2.804118, 2.806588, 2.809059, 2.81153, 2.814, 2.816471, 2.818235, 2.82,
                    2.821765, 2.823529, 2.825294, 2.827059, 2.828824, 2.831294, 2.833765, 2.836236, 2.838706, 2.841177,
                    2.843235, 2.845294, 2.847353, 2.849412, 2.851471, 2.853529, 2.856, 2.858471, 2.860941, 2.863412,
                    2.865882, 2.868353, 2.870824, 2.873294, 2.875765, 2.878235, 2.88, 2.881765, 2.883529, 2.885294,
                    2.887059, 2.888824, 2.890588, 2.892133, 2.893677, 2.895221, 2.896765, 2.898309, 2.899853, 2.901397,
                    2.902941, 2.905, 2.907059, 2.909118, 2.911177, 2.913235, 2.915294, 2.917353, 2.919412, 2.921471,
                    2.92353, 2.925588, 2.927647, 2.929412, 2.931177, 2.932941, 2.934706, 2.936471, 2.938235, 2.94,
                    2.942059, 2.944118, 2.946177, 2.948236, 2.950294, 2.952353, 2.954118, 2.955883, 2.957647, 2.959412,
                    2.961176, 2.962941, 2.964706, 2.966765, 2.968824, 2.970882, 2.972941, 2.975, 2.977059, 2.979118,
                    2.981177, 2.983235, 2.985294, 2.987353, 2.989412, 2.991177, 2.992941, 2.994706, 2.996471, 2.998235,
                    3.0, 3.001765, 3.00353, 3.005294, 3.007059, 3.008824, 3.010588, 3.012353, 3.014118, 3.015882,
                    3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.028015, 3.029559, 3.031103, 3.032647,
                    3.034191, 3.035735, 3.03728, 3.038824, 3.040588, 3.042353, 3.044118, 3.045882, 3.047647, 3.049412,
                    3.051177, 3.053236, 3.055294, 3.057353, 3.059412, 3.061471, 3.063529, 3.065294, 3.067059, 3.068824,
                    3.070588, 3.072353, 3.074118, 3.075882, 3.077647, 3.079412, 3.081177, 3.082941, 3.084706, 3.086471,
                    3.088235, 3.09, 3.091765, 3.093529, 3.095294, 3.097059, 3.098824, 3.100588, 3.101961, 3.103333,
                    3.104706, 3.106079, 3.107451, 3.108824, 3.110196, 3.111569, 3.112941, 3.115, 3.117059, 3.119118,
                    3.121177, 3.123235, 3.125294, 3.131471, 3.143824]

    NOM_RES = 10000
    SER_RES = 9820
    TEMP_NOM = 25
    NUM_SAMPLES = 25
    THERM_B_COEFF = 3950
    ADC_MAX = 1023
    ADC_Vmax = 3.15
    feedname = constant.FEEDNAME_TEMP
    logger = None

    def __init__(self, period, logger):
        self.period = period
        adc = ADC(Pin(constant.TENP_SENS_ADC_PIN_NO))
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_10BIT)
        self.temp_sens = adc
        self.logger = logger

    def read_value(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, self.NUM_SAMPLES + 1):
            raw_read.append(self.temp_sens.read())

        # Average of the NUM_SAMPLES and look it up in the table
        raw_average = sum(raw_read) / self.NUM_SAMPLES
        self.logger.log('raw_avg = ' + str(raw_average))
        self.logger.log('V_measured = ' + str(self.adc_V_lookup[round(raw_average)]))

        # Convert to resistance
        raw_average = self.ADC_MAX * self.adc_V_lookup[round(raw_average)] / self.ADC_Vmax
        resistance = (self.SER_RES * raw_average) / (self.ADC_MAX - raw_average)
        self.logger.log('Thermistor resistance: {} ohms'.format(resistance))

        # Convert to temperature
        steinhart = log(resistance / self.NOM_RES) / self.THERM_B_COEFF
        steinhart += 1.0 / (self.TEMP_NOM + 273.15)
        steinhart = (1.0 / steinhart) - 273.15
        self.logger.log('Thermistor temperature: ' + str(steinhart), self.feedname)
        return steinhart
