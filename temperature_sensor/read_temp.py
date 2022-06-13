
from machine import Pin
from machine import ADC
from math import log
import constant


class TemperatureSensor:

    adc_V_lookup = [0.01852941, 0.04941176, 0.05352941, 0.05764706, 0.06176471, 0.06588235, 0.06999999, 0.07411765, 0.07720589, 0.08029412, 0.08338234, 0.08647058, 0.09058824, 0.09470588, 0.09882353, 0.1019118, 0.105, 0.1080882, 0.1111765, 0.1152941, 0.1194118, 0.1235294, 0.1266176, 0.1297059, 0.1327941, 0.1358824, 0.14, 0.1441176, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882, 0.1636765, 0.1667647, 0.1698529, 0.1729412, 0.1770588, 0.1811765, 0.1852941, 0.1894118, 0.1935294, 0.197647, 0.2007353, 0.2038235, 0.2069118, 0.21, 0.2130882, 0.2161765, 0.2192647, 0.2223529, 0.2264706, 0.2305882, 0.2347059, 0.2388235, 0.2429412, 0.2470588, 0.2501471, 0.2532353, 0.2563235, 0.2594118, 0.2625, 0.2655882, 0.2686765, 0.2717647, 0.2748529, 0.2779412, 0.2810294, 0.2841177, 0.2872059, 0.2902941, 0.2933824, 0.2964706, 0.3005882, 0.3047059, 0.3088235, 0.3119118, 0.315, 0.3180882, 0.3211765, 0.3252941, 0.3294117, 0.3335294, 0.3376471, 0.3417647, 0.3458823, 0.3489706, 0.3520588, 0.355147, 0.3582353, 0.3623529, 0.3664706, 0.3705882, 0.3736764, 0.3767647, 0.3798529, 0.3829412, 0.3860294, 0.3891176, 0.3922059, 0.3952941, 0.3994117, 0.4035294, 0.407647, 0.4107353, 0.4138235, 0.4169117, 0.42, 0.4230882, 0.4261765, 0.4292647, 0.4323529, 0.4364706, 0.4405882, 0.4447059, 0.4477941, 0.4508823, 0.4539706, 0.4570588, 0.4611764, 0.4652941, 0.4694118, 0.4735294, 0.4776471, 0.4817647, 0.4842353, 0.4867059, 0.4891764, 0.4916471, 0.4941176, 0.4972058, 0.5002941, 0.5033823, 0.5064706, 0.5105882, 0.5147059, 0.5188235, 0.5219117, 0.525, 0.5280882, 0.5311765, 0.5342647, 0.5373529, 0.5404411, 0.5435294, 0.547647, 0.5517647, 0.5558824, 0.5589705, 0.5620588, 0.565147, 0.5682353, 0.5723529, 0.5764706, 0.5805882, 0.5836764, 0.5867647, 0.5898529, 0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6094117, 0.6135294, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6341176, 0.6382353, 0.642353, 0.6454412, 0.6485294, 0.6516176, 0.6547059, 0.6577941, 0.6608823, 0.6639705, 0.6670588, 0.6711764, 0.6752941, 0.6794117, 0.6824999, 0.6855882, 0.6886764, 0.6917646, 0.6958823, 0.7, 0.7041176, 0.7065882, 0.7090588, 0.7115294, 0.714, 0.7164705, 0.7205882, 0.7247059, 0.7288235, 0.7329412, 0.7370588, 0.7411764, 0.7442647, 0.7473529, 0.7504411, 0.7535294, 0.757647, 0.7617647, 0.7658823, 0.7689705, 0.7720588, 0.775147, 0.7782352, 0.7797794, 0.7813235, 0.7828676, 0.7844117, 0.7859559, 0.7875, 0.7890441, 0.7905882, 0.7947059, 0.7988235, 0.8029411, 0.8054117, 0.8078823, 0.8103529, 0.8128235, 0.8152941, 0.8194118, 0.8235293, 0.827647, 0.8307353, 0.8338235, 0.8369118, 0.84, 0.8441176, 0.8482352, 0.8523529, 0.8548235, 0.8572941, 0.8597647, 0.8622353, 0.8647058, 0.8708823, 0.8770588, 0.8801471, 0.8832353, 0.8863235, 0.8894117, 0.8935294, 0.897647, 0.9017647, 0.9042353, 0.9067059, 0.9091764, 0.911647, 0.9141176, 0.9172059, 0.9202941, 0.9233823, 0.9264706, 0.9305882, 0.9347058, 0.9388235, 0.9419117, 0.9449999, 0.9480882, 0.9511765, 0.9542646, 0.9573528, 0.9604411, 0.9635294, 0.9676471, 0.9717647, 0.9758823, 0.9789705, 0.9820587, 0.985147, 0.9882353, 0.9913235, 0.9944117, 0.9974999, 1.000588, 1.003676, 1.006765, 1.009853, 1.012941, 1.017059, 1.021176, 1.025294, 1.029412, 1.033529, 1.037647, 1.040735, 1.043823, 1.046912, 1.05, 1.053088, 1.056176, 1.059265, 1.062353, 1.065441, 1.068529, 1.071618, 1.074706, 1.078824, 1.082941, 1.087059, 1.090147, 1.093235, 1.096323, 1.099412, 1.1025, 1.105588, 1.108676, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.128235, 1.132353, 1.136471, 1.140588, 1.144706, 1.148823, 1.151294, 1.153765, 1.156235, 1.158706, 1.161176, 1.165294, 1.169412, 1.173529, 1.177647, 1.181765, 1.185882, 1.188971, 1.192059, 1.195147, 1.198235, 1.202353, 1.20647, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.226029, 1.229118, 1.232206, 1.235294, 1.238382, 1.241471, 1.244559, 1.247647, 1.251765, 1.255882, 1.26, 1.263088, 1.266176, 1.269265, 1.272353, 1.276471, 1.280588, 1.284706, 1.287794, 1.290882, 1.293971, 1.297059, 1.301176, 1.305294, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.325882, 1.33, 1.334118, 1.336588, 1.339059, 1.341529, 1.344, 1.34647, 1.349559, 1.352647, 1.355735, 1.358823, 1.361912, 1.365, 1.368088, 1.371176, 1.375294, 1.379412, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.4, 1.404118, 1.408235, 1.411323, 1.414412, 1.4175, 1.420588, 1.423676, 1.426765, 1.429853, 1.432941, 1.437059, 1.441176, 1.445294, 1.448382, 1.45147, 1.454559, 1.457647, 1.461765, 1.465882, 1.47, 1.473088, 1.476176, 1.479265, 1.482353, 1.485441, 1.488529, 1.491618, 1.494706, 1.498824, 1.502941, 1.507059, 1.510147, 1.513235, 1.516323, 1.519412, 1.523529, 1.527647, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.548235, 1.552353, 1.55647, 1.558941, 1.561412, 1.563882, 1.566353, 1.568823, 1.581176, 1.585294, 1.589412, 1.593529, 1.596618, 1.599706, 1.602794, 1.605882, 1.61, 1.614118, 1.618235, 1.621323, 1.624412, 1.6275, 1.630588, 1.634706, 1.638824, 1.642941, 1.646029, 1.649118, 1.652206, 1.655294, 1.659412, 1.663529, 1.667647, 1.670735, 1.673823, 1.676912, 1.68, 1.683088, 1.686176, 1.689265, 1.692353, 1.69647, 1.700588, 1.704706, 1.707176, 1.709647, 1.712118, 1.714588, 1.717059, 1.721176, 1.725294, 1.729412, 1.733529, 1.737647, 1.741765, 1.744853, 1.747941, 1.751029, 1.754118, 1.757206, 1.760294, 1.763382, 1.766471, 1.770588, 1.774706, 1.778823, 1.781294, 1.783765, 1.786235, 1.788706, 1.791176, 1.795294, 1.799412, 1.803529, 1.806618, 1.809706, 1.812794, 1.815882, 1.82, 1.824118, 1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.843676, 1.846765, 1.849853, 1.852941, 1.856029, 1.859118, 1.862206, 1.865294, 1.87147, 1.877647, 1.880735, 1.883823, 1.886912, 1.89, 1.893088, 1.896176, 1.899265, 1.902353, 1.90647, 1.910588, 1.914706, 1.917794, 1.920882, 1.92397, 1.927059, 1.931176, 1.935294, 1.939412, 1.9425, 1.945588, 1.948676, 1.951765, 1.954853, 1.957941, 1.961029, 1.964118, 1.968235, 1.972353, 1.97647, 1.979559, 1.982647, 1.985735, 1.988823, 1.992941, 1.997059, 2.001176, 2.004265, 2.007353, 2.010441, 2.013529, 2.017647, 2.021765, 2.025882, 2.02897, 2.032059, 2.035147, 2.038235, 2.041323, 2.044412, 2.0475, 2.050588, 2.053676, 2.056765, 2.059853, 2.062941, 2.067059, 2.071177, 2.075294, 2.079412, 2.083529, 2.087647, 2.090735, 2.093823, 2.096912, 2.1, 2.104117, 2.108235, 2.112353, 2.114823, 2.117294, 2.119765, 2.122235, 2.124706, 2.128823, 2.132941, 2.137059, 2.140147, 2.143235, 2.146323, 2.149412, 2.153529, 2.157647, 2.161765, 2.164853, 2.167941, 2.171029, 2.174118, 2.177206, 2.180294, 2.183382, 2.186471, 2.189559, 2.192647, 2.195735, 2.198823, 2.202941, 2.207059, 2.211176, 2.214265, 2.217353, 2.220441, 2.223529, 2.226618, 2.229706, 2.232794, 2.235882, 2.238971, 2.242059, 2.245147, 2.248235, 2.251323, 2.254412, 2.2575, 2.260588, 2.264706, 2.268823, 2.272941, 2.276029, 2.279118, 2.282206, 2.285294, 2.288382, 2.291471, 2.294559, 2.297647, 2.301764, 2.305882, 2.31, 2.313088, 2.316176, 2.319265, 2.322353, 2.325441, 2.328529, 2.331618, 2.334706, 2.338823, 2.342941, 2.347059, 2.349529, 2.352, 2.35447, 2.356941, 2.359412, 2.360956, 2.3625, 2.364044, 2.365588, 2.367132, 2.368676, 2.37022, 2.371765, 2.375882, 2.38, 2.384118, 2.386588, 2.389059, 2.391529, 2.394, 2.396471, 2.400588, 2.404706, 2.408823, 2.412941, 2.417059, 2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.436, 2.43847, 2.440941, 2.443412, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.462353, 2.46647, 2.470588, 2.473676, 2.476765, 2.479853, 2.482941, 2.485412, 2.487882, 2.490353, 2.492823, 2.495294, 2.498382, 2.501471, 2.504559, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.534823, 2.537294, 2.539765, 2.542235, 2.544706, 2.547794, 2.550882, 2.553971, 2.557059, 2.560147, 2.563235, 2.566324, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.584235, 2.586706, 2.589176, 2.591647, 2.594118, 2.597206, 2.600294, 2.603382, 2.606471, 2.608235, 2.61, 2.611765, 2.613529, 2.615294, 2.617059, 2.618824, 2.621912, 2.625, 2.628088, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.646, 2.64847, 2.650941, 2.653412, 2.655882, 2.65897, 2.662059, 2.665147, 2.668235, 2.670294, 2.672353, 2.674412, 2.676471, 2.678529, 2.680588, 2.683059, 2.685529, 2.688, 2.69047, 2.692941, 2.695412, 2.697882, 2.700353, 2.702823, 2.705294, 2.707765, 2.710235, 2.712706, 2.715176, 2.717647, 2.720735, 2.723823, 2.726912, 2.73, 2.732059, 2.734118, 2.736176, 2.738235, 2.740294, 2.742353, 2.744823, 2.747294, 2.749765, 2.752235, 2.754706, 2.757176, 2.759647, 2.762118, 2.764588, 2.767059, 2.769118, 2.771176, 2.773235, 2.775294, 2.777353, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791764, 2.793823, 2.795882, 2.797941, 2.8, 2.802059, 2.804117, 2.806588, 2.809059, 2.811529, 2.814, 2.81647, 2.818529, 2.820588, 2.822647, 2.824706, 2.826765, 2.828823, 2.830882, 2.832941, 2.835, 2.837059, 2.839118, 2.841176, 2.843647, 2.846117, 2.848588, 2.851059, 2.853529, 2.855588, 2.857647, 2.859706, 2.861765, 2.863823, 2.865882, 2.867941, 2.87, 2.872059, 2.874118, 2.876176, 2.878235, 2.880706, 2.883176, 2.885647, 2.888118, 2.890588, 2.893059, 2.895529, 2.898, 2.900471, 2.902941, 2.904485, 2.906029, 2.907574, 2.909118, 2.910662, 2.912206, 2.91375, 2.915294, 2.917764, 2.920235, 2.922706, 2.925176, 2.927647, 2.929412, 2.931176, 2.932941, 2.934706, 2.93647, 2.938235, 2.94, 2.941544, 2.943088, 2.944632, 2.946176, 2.947721, 2.949265, 2.950809, 2.952353, 2.954823, 2.957294, 2.959765, 2.962235, 2.964706, 2.966471, 2.968235, 2.97, 2.971765, 2.973529, 2.975294, 2.977059, 2.979118, 2.981176, 2.983235, 2.985294, 2.987353, 2.989412, 2.991882, 2.994353, 2.996824, 2.999294, 3.001765, 3.003137, 3.00451, 3.005882, 3.007255, 3.008627, 3.01, 3.011372, 3.012745, 3.014117, 3.015882, 3.017647, 3.019412, 3.021176, 3.022941, 3.024706, 3.02647, 3.028015, 3.029559, 3.031103, 3.032647, 3.034191, 3.035735, 3.037279, 3.038823, 3.040882, 3.042941, 3.045, 3.047059, 3.049118, 3.051176, 3.052941, 3.054706, 3.05647, 3.058235, 3.06, 3.061765, 3.063529, 3.065588, 3.067647, 3.069706, 3.071765, 3.073823, 3.075882, 3.077426, 3.07897, 3.080515, 3.082059, 3.083603, 3.085147, 3.086691, 3.088235, 3.09, 3.091765, 3.093529, 3.095294, 3.097059, 3.098824, 3.100588, 3.102647, 3.104706, 3.106765, 3.108824, 3.110882, 3.112941, 3.114485, 3.116029, 3.117573, 3.119117, 3.120662, 3.122206, 3.12375, 3.125294, 3.127353, 3.129411, 3.13147, 3.133529, 3.135588, 3.137647, 3.15, 3.15]

    NOM_RES = 10000
    SER_RES = 9820
    TEMP_NOM = 25
    NUM_SAMPLES = 25
    THERM_B_COEFF = 3950
    ADC_MAX = 1023
    ADC_Vmax = 3.15
    feedname = "Temperature"
    
    def __init__(self, period):
        self.period = period
        adc = ADC(Pin(constant.TENP_SENS_ADC_PIN_NO))
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_10BIT)
        self.temp_sens = adc


    def read_value(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, self.NUM_SAMPLES+1):
            raw_read.append(self.temp_sens.read())

        # Average of the NUM_SAMPLES and look it up in the table
        raw_average = sum(raw_read)/self.NUM_SAMPLES
        # print('raw_avg = ' + str(raw_average))
        # print('V_measured = ' + str(self.adc_V_lookup[round(raw_average)]))

        # Convert to resistance
        raw_average = self.ADC_MAX * self.adc_V_lookup[round(raw_average)]/self.ADC_Vmax
        resistance = (self.SER_RES * raw_average) / (self.ADC_MAX - raw_average)
        # print('Thermistor resistance: {} ohms'.format(resistance))

        # Convert to temperature
        steinhart = log(resistance / self.NOM_RES) / self.THERM_B_COEFF
        steinhart += 1.0 / (self.TEMP_NOM + 273.15)
        steinhart = (1.0 / steinhart) - 273.15
        # print('Thermistor temperature: ' + str(steinhart))
        return steinhart
