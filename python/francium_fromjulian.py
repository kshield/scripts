# Code adapted from Julian Rees's Ac225/Ac227 analysis code
# The original code can be found here:
# https://github.com/julianrees/raddaughters/blob/master/2018-4-4-18%20Francium.R

library(reshape2)
library(plyr)
library(dplyr)
library(drc)
library(drfit)
library(ggplot2)
library(deSolve)
library(emdbook)
library(stats)
library(plotly)
library(cowplot)
library(gridExtra)

#Forces scientific notation only for >> numbers
#options(scipen=defaults)

#not acounting for alpha recoil effects, which is 4 au / mass of parent isotope * alpha energy


#Specific activity constants in uCi/ng
#k10 is Lu-177, k11 is Hf-177


# k1 = ac225
# k2 = fr221
# k3 = at217
# k4 = bi213
# k5 = po213
# k6 = pb209
# k7 = bi209
# k8 = rn217
# k9 = tl209
# k10 = lu177
# k11 = hf177
# k12 = ac227
# k13 = th227
# k14 = fr223
# k15 = ra223
# k16 = rn219
# k17 = po215
# k18 = pb211
# k19 = bi211
# k20 = tl207
# k21 = pb207


  #activity in Ci/mg
activity = c(k1 = 58, k2 = 176026.2, k3 = 1609541800, k4 = 20000, k5 = 1.3*10^13, k6 = 4613, k7 = 0, k8 = 96216216216, k9 = 410000, k10 = 110, k11 = 0,
             k12 = 0.072, k13 = 31, k14 = 38926.9, k15 = 51.2, k16 = 13008438.4, k17 = 29461992937, k18 = 24639.1739, k19 = 416405.3549, k20 = 190584.9219, k21 = 0)

#initial activity in uCi
uciac225 =  0.17/1000 #0.1 nCi = 220 CPM  ->>>> divide by #major species (5) if in transient equilibrium, don't include minor species.
ucilu177 = 21/1000
uciac227 = 0.002 #/8 divide by # starting @EQ (8) to get total dose equivalency, don't include minor species.

#Initial nmoles of actinium-225
#use the mol ratios #agged out to start at transient equilibiurm - but change the uciac225 starting activity accordingly as well.
#for ac-225, initial stock activity should be roughly 6x the expected amount if perfect. However, it would be tough for
  #LANL to measure it so quickly, so it is only ~3.5-4.5x the stock value. However, since these half lifes are so short, if
  #ac-225 destructions blow out of DOTA, then upon washing the mAb-DOTA complex, it is basically a pure ac-225 separation.
  #For ac-227, however, there are several long lived isotopes (Th-227, Fr-223, Ra-223) which last at least 11 days. A 227 conjugation will have these isotopes
  #on the antibody as well (probably - have to look at dota efficiency for Ra-223)

#3 day equilibrium numbers
EQnum = c(1.057009e-08,3.616078e-12,3.972766e-16,3.402997e-11,5.068525e-20,1.461998e-10,2.270190e-09,5.114168e-21,3.341722e-14,7.889644e-07)
EQratio = EQnum/1.057009e-08

#assume Ac-225 only upon mAb metallation / washing.
nmolesac225 = uciac225/58/225
nmolesfr221 = 1*EQratio[2]*nmolesac225
nmolesat217 = EQratio[3]*nmolesac225
nmolesbi213 = EQratio[4]*nmolesac225
nmolespo213 = EQratio[5]*nmolesac225
nmolespb209 = EQratio[6]*nmolesac225
nmolesbi209 = EQratio[7]*nmolesac225 #starting with 1 day equilibrium
nmolesrn217 = EQratio[8]*nmolesac225
nmolestl209 = EQratio[9]*nmolesac225






nmoleslu177 = ucilu177/110/177

#divide by mole ratio if starting at EQ (200 days), otherwise create initial non-steady state mol ratio set to start halfway in or whatever

nmolesac227 = 0#uciac227/0.072/227
nmolesth227 = uciac227/31/227#0.002323661*nmolesac227
nmolesfr223 = 0#3.77269E-05*nmolesac227 #isn't chelated by dota
nmolesra223 = 0#0.00144379*nmolesac227 #isn't chelated by dota
nmolesrn219 = 0#5.78948E-09*nmolesac227
nmolespo215 = 0#2.6038E-12*nmolesac227
nmolespb211 = 0#3.17247E-06*nmolesac227
nmolesbi211 = 0#1.8772E-07*nmolesac227
nmolestl207 = 0#4.18072E-07*nmolesac227
nmolespb207 = 0#1/100*nmolesac227






#initial DPM of ac-225
dpmac225 = uciac225*2220000
dpmlu177 = ucilu177*2220000
dpmac227 = uciac227*2220000


#lambda values are ln(2)/t(1/2) with t1/2 in days
parameters = c(l1 = 0.069663033, l2 = 206.5115, l3 = 1854115, l4 = 21.69852043, l5 = 14259027714, l6 = 5.118625333, l7 = 8.75554E-19, l8 = 110903548.9, l9 = 461.8842851, l10 = 0.104232659, l11 = 0,
               l12 = 8.72237E-05,l13 = 0.03710638,l14 = 46.08181,l15 = 0.060642798,l16 = 15123.21121,l17 = 33626005.84,l18 = 27.59862689,l19 = 466.4167944,l20 = 209.4275997,l21 = 0)


#probabilities of the destruction to a certain species
#using beta 1/3 average energy rule from beta max

#2nd row starts at #15
probabilities = c(ac2fr = 1, fr2at = 1, at2bi = 0.99923, bi2po = 0.978, po2pb = 1, pb2bi = 1, at2rn = 0.00077, bi2tl = 0.0209, rn2po = 1, tl2pb = 1, bi2tl205 = 1, lu2hfbeta = 0.79, lu2hfgamma1 = 0.11, lu2hfgamma2 = 0.064,
                  ac2th227 = 0.9862, ac2fr223 = 0.0138, fr2ra223 = 1, th2ra223 = 1, ra2rn219 = 1, rn2po215 = 1, po2pb211 = 1, pb2bi211 = 1, bi2tl207 = 1, tl2pb207 = 1, pb2stable = 1 )
energies = c(eac2fr = 5.935, efr2at = 6.46, eat2bi = 7.20, ebi2po = 1.4227/3, epo2pb = 8.536, epb2bi = 0.644/3, eat2rn = 0.737/3, ebi2tl = 5.98, ern2po = 7.88, etl2pb = 3.976/3, ebi2tl205 = 3.137, elu2hfbeta = 0.497/3, elu2hfgamma1 = 0.208, elu2hfgamma2 = 0.113,
             eac2th227 = 0.044/3, eac2fr227 = 5.04, efr2ra223 = 1.149/3, eth2ra223 = 6.1466, era2rn219 = 5.97899, ern2po215 = 6.94612, epo2pb211 = 7.52626, epb2bi211 = 1.36697/3, ebi2tl207 = 6.75033, etl2pb207 = 1.41824, epb2stable = 0)
checktable = data.frame(probabilities, energies)

#these numbers are in nmoles
state = c(A = nmolesac225, B = nmolesfr221, C = nmolesat217, D = nmolesbi213, E = nmolespo213, f = nmolespb209, G = nmolesbi209, H = nmolesrn217, I = nmolestl209, J = nmoleslu177, K = 0,
          L = nmolesac227, M = nmolesth227, N = nmolesfr223, O = nmolesra223, P = nmolesrn219, Q = nmolespo215, R = nmolespb211, S = nmolesbi211, t = nmolestl207, U = nmolespb207)


#For TLC calc
#state = c(A = 0, B = out[out$time==0.083,"Fr221"], C = out[out$time==0.083,"At217"], D = out[out$time==0.083,"Bi213"], E = out[out$time==0.083,"Po213"], f = out[out$time==0.083,"Pb209"], G = out[out$time==0.083,"Bi209"], H = out[out$time==0.083,"Rn217"], I = out[out$time==0.083,"Tl209"],J = nmoleslu177, K = 0, L = nmolesac227, M = nmolesth227, N = nmolesfr223, O = nmolesra223, P = nmolesrn219, Q = nmolespo215, R = nmolespb211, S = nmolesbi211, t = nmolestl207, U = nmolespb207)
masses = c('Ac225' = 225, 'Fr221' = 221, 'At217' = 217, 'Bi213' = 213, 'Po213' = 213, 'Pb209' = 209, 'Bi209' = 209, 'Rn217' = 217, 'Tl209' = 209, 'Lu177' = 177, 'Hf177' = 177, j12 = 227, j13 = 227, j14 = 223, j15 = 223, j16 = 219, j17 = 215, j18 = 211, j19 = 211, j20 = 207, j21 = 207)


#calculate nmoles of species
#probabilities only matter for the species input, not output

daughters = function(t, state, parameters, probabilities) {with(as.list(c(state, parameters, probabilities)),{
  dA = -l1*A
  dB = l1*ac2fr*A-l2*B
  dC = l2*fr2at*B-l3*C
  dH = l3*at2rn*C-l8*H
  dD = l3*at2bi*C-l4*D
  dI = l4*bi2tl*D-l9*I
  dE = l4*bi2po*D+l8*rn2po*H-l5*E
  df = l5*po2pb*E+l9*tl2pb*I-l6*f
  dG = l6*pb2bi*f-l7*G
  dJ = -l10*J
  dK = l10*J

  dL = -l12*L
  dM = l12*ac2th227*L-l13*M
  dN = l12*ac2fr223*L-l14*N
  dO = l13*th2ra223*M+l14*fr2ra223*N-l15*O
  dP = l15*ra2rn219*O-l16*P
  dQ = l16*rn2po215*P-l17*Q
  dR = l17*po2pb211*Q-l18*R
  dS = l18*pb2bi211*R-l19*S
  dt = l19*bi2tl207*S-l20*t
  dU = l20*tl2pb207*t-l21*U


  list(c(dA, dB, dC, dD, dE, df, dG, dH, dI, dJ, dK, dL, dM, dN, dO, dP, dQ, dR, dS, dt, dU))
})}

#Ac-227 timefame
#timedays = 365*21.772                                     #total days for plot
timedays = 3
timestep = 0.001                                   #step size
timestepout = 1/timestep                           #to make a timesout match starting at 1

times = seq(0, timedays, by = timestep)     #list all points
timesout = seq(1, timedays*timestepout+1, by = 1)  #number of points sequentially





#MODEL INTEGRATION

out = ode(y = state, times = times, func = daughters, parms = parameters, prob=probabilities)

#head(out)


#calculate activity produces over time
#daughtersactiv = function(t, activity, masses, out) {with(as.list(c(activity, masses, out)),{

#multiply to get DPM from uCi and divide by initial ac-225 DPM to get Fraction Activity Remaining
Ac225 = masses[1]*activity[1]*out[timesout,2]*2220000/dpmac225
Fr221 = masses[2]*activity[2]*out[timesout,3]*2220000/dpmac225
At217 = masses[3]*activity[3]*out[timesout,4]*2220000/dpmac225
Bi213 = masses[4]*activity[4]*out[timesout,5]*2220000/dpmac225
Po213 = masses[5]*activity[5]*out[timesout,6]*2220000/dpmac225
Pb209 = masses[6]*activity[6]*out[timesout,7]*2220000/dpmac225
Bi209 = masses[7]*activity[7]*out[timesout,8]*2220000/dpmac225
Rn217 = masses[8]*activity[8]*out[timesout,9]*2220000/dpmac225
Tl209 = masses[9]*activity[9]*out[timesout,10]*2200000/dpmac225
SUM = (Ac225+Fr221+At217+Bi213+Po213+Pb209+Bi209+Rn217+Tl209)
SUMoverac225 = SUM/Ac225
Lu177 = masses[10]*activity[10]*out[timesout,11]*2220000/dpmlu177
Hf177 = masses[11]*activity[11]*out[timesout,12]*2220000/dpmlu177


Ac227 = masses[12]*activity[12]*out[timesout,13]*2220000/dpmac227
Th227 = masses[13]*activity[13]*out[timesout,14]*2220000/dpmac227
Fr223 = masses[14]*activity[14]*out[timesout,15]*2220000/dpmac227
Ra223 = masses[15]*activity[15]*out[timesout,16]*2220000/dpmac227
Rn219 = masses[16]*activity[16]*out[timesout,17]*2220000/dpmac227
Po215 = masses[17]*activity[17]*out[timesout,18]*2220000/dpmac227
Pb211 = masses[18]*activity[18]*out[timesout,19]*2220000/dpmac227
Bi211 = masses[19]*activity[19]*out[timesout,20]*2220000/dpmac227
Tl207 = masses[20]*activity[20]*out[timesout,21]*2220000/dpmac227
Pb207 = masses[21]*activity[21]*out[timesout,22]*2220000/dpmac227
Ac227SUM = (Ac227+Th227+Fr223+Ra223+Rn219+Po215+Pb211+Bi211+Tl207+Pb207)


daughtersdata = data.frame(times)
daughtersdata = cbind(daughtersdata, Ac225, Fr221, At217, Bi213, Po213, Pb209, Bi209, Rn217, Tl209, SUM, SUMoverac225, Lu177, Hf177, Ac227, Th227, Fr223, Ra223, Rn219, Po215, Pb211, Bi211, Tl207, Pb207, Ac227SUM)
colnames(daughtersdata) = c("times", "Ac-225", "Fr-221", "At-217", "Bi-213", "Po-213", "Pb-209", "Bi-209", "Rn-217", "Tl-209", "SUM Ac-225", "Ac-225 SUM / Ac-225", "Lu-177", "Hf-177", "Ac-227", "Th227", "Fr223", "Ra223", "Rn219", "Po215", "Pb211", "Bi211", "Tl207", "Pb207", "Ac-227 SUM")


#melt this first
#mdaughtersdata = melt(daughtersdata, id="times")

plotrows = unique(round(lseq(1, length(timesout), 1000)))
plottimes <- times[plotrows]


#choose your columns: Lu-177 and Hf-177 are 13 and 14
#Ac-225 are c(1:11)
#Ac-227 are c(1,15,16,17,18,19,20,21,22,23,24,25)

#Ac-225&Lu-177/Hf-177 *****#8 is Bi-209 final product
plotout <- daughtersdata[plotrows, c(1,2,3,8)]#,4,5,6,7,9,10,8,11)]#,13,14)]

#Ac-227
#plotout <- daughtersdata[plotrows, c(1,15,16,17,18,19,20,21,22,23,24,25)]
plotout = plotout[-1,] #remove first row

mplotout <- melt(plotout, id="times")
colnames(mplotout) <- c("times","Species","value")

#---- new section ----
#plot the indivudual activities produced

ggplot(mplotout, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "b", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_continuous(labels = scales::percent, breaks=c(0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))+
  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  labs(x = "Time (day)", y = "% Activity(t) / Ac-225(0)", color="Species")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+
  guides(shape=guide_legend(override.aes = list(size=3)))
#  guides(color=guide_legend(title=""))



#melt the masses
#choose columns
out = data.frame(out[plotrows, 1:10])
#out = data.frame(out[plotrows, c(1,13,14,15,16,17,18,19,20,21,22)])


colnames(out) = c("time", "Ac225", "Fr221", "At217", "Bi213", "Po213", "Pb209", "Bi209", "Rn217", "Tl209")
#colnames(out) = c("")

mout = melt(out, id="time")
colnames(mout) <- c("time","Species","value")

#plot the masses

ggplot(mout, aes(x=time, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17))+

    scale_x_log10(breaks=c(0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "b", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+
  scale_y_log10()+#breaks=c(10^(-20), 10^(-15), 10^(-10), 10^(-5)))+ #'s are for 0.1 nmol starting
  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+

  #annotation_logticks(base = 10, sides = "l", scaled = TRUE,
                      #short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      #colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+
  labs(x = "Time (day)", y = "Amount (nmoles/min)")+
  theme(text = element_text(size=18))+
  guides(shape=guide_legend(override.aes = list(size=3)))
#  guides(color=guide_legend(title=""))



#####test#####µ
################
#Total energy produced from starting amount of metal

#energies in MeV/destruction * probability of destruction occuring

energiesprobabilities = energies*probabilities


#multiply by initial activity in CPM to get CPM due to mass of element initially, and then by energy per destruction, *1440 to convert to energy per days from CPM
eAc225 = Ac225*dpmac225*(energiesprobabilities[1])*1440
eFr221 = Fr221*dpmac225*(energiesprobabilities[2])*1440
eAt217 = At217*dpmac225*(energiesprobabilities[3]+energiesprobabilities[7])*1440
eBi213 = Bi213*dpmac225*(energiesprobabilities[4]+energiesprobabilities[8])*1440
ePo213 = Po213*dpmac225*(energiesprobabilities[5])*1440
ePb209 = Pb209*dpmac225*(energiesprobabilities[6])*1440
eBi209 = Bi209*dpmac225*(energiesprobabilities[11])*1440
eRn217 = Rn217*dpmac225*(energiesprobabilities[9])*1440
eTl209 = Tl209*dpmac225*(energiesprobabilities[10])*1440
eSUM = (eAc225+eFr221+eAt217+eBi213+ePo213+ePb209+eBi209+eRn217+eTl209)
eSUMoverac225 = eSUM/eAc225
eLu177 = Lu177*dpmlu177*(energiesprobabilities[12]+energiesprobabilities[13]+energiesprobabilities[14])*1440
eAlpha = (eAc225+eFr221+At217*dpmac225*(energiesprobabilities[3])*1440+Bi213*dpmac225*(energiesprobabilities[8])*1440+ePo213+eBi209+eRn217)
eBeta = At217*dpmac225*(energiesprobabilities[7])*1440+Bi213*dpmac225*(energiesprobabilities[4])*1440+ePb209+eTl209


eAc227 = Ac227*dpmac227*(energiesprobabilities[15]+energiesprobabilities[16])*1440
eTh227 = Th227*dpmac227*(energiesprobabilities[18])*1440
eFr223 = Fr223*dpmac227*(energiesprobabilities[17])*1440
eRa223 = Ra223*dpmac227*(energiesprobabilities[19])*1440
eRn219 = Rn219*dpmac227*(energiesprobabilities[20])*1440
ePo215 = Po215*dpmac227*(energiesprobabilities[21])*1440
ePb211 = Pb211*dpmac227*(energiesprobabilities[22])*1440
eBi211 = Bi211*dpmac227*(energiesprobabilities[23])*1440
eTl207 = Tl207*dpmac227*(energiesprobabilities[24])*1440
ePb207 = Pb207*dpmac227*(energiesprobabilities[25])*1440
eAc227SUM = (eAc227+eTh227+eFr223+eRa223+eRn219+ePo215+ePb211+eBi211+eTl207+ePb207)



edaughtersdata = data.frame(times)
edaughtersdata = cbind(edaughtersdata, eAc225, eFr221, eAt217, eBi213, ePo213, ePb209, eBi209, eRn217, eTl209, eSUM, eSUMoverac225, eLu177, eAlpha, eBeta, eAc227, eTh227, eFr223, eRa223, eRn219, ePo215, ePb211, eBi211, eTl207, ePb207, eAc227SUM)
colnames(edaughtersdata) = c("times", "Ac-225 (0.2 µCi)", "Fr-221", "At-217", "Bi-213", "Po-213", "Pb-209", "Bi-209", "Rn-217", "Tl-209", "Ac-225 SUM", "SUM / Ac-225", "Lu-177 (20 µCi)", "Ac-225 SUM Alpha", "Ac-225 SUM Beta", "Ac-227 (0.2 ?Ci)", "Th-227", "Fr-223", "Ra-223", "Rn-219", "Po-215", "Pb-211", "Bi-211", "Tl-207", "Pb-207", "Ac-227 SUM")

eplotrows = unique(round(lseq(1, length(timesout), 1000)))
eplottimes <- times[eplotrows]

#
##
######
#############  Add in spatial coordinates! Each destruction is one atom, so that works out. Each destruction starts steady state
######         Add in vertical weighting based on cell interactions, kd's etc.
##
#

#tester create cylinder randowm points
# plus scaling tot he 10th order
 # nn <- 1e4
 # rho <- sqrt(runif(nn, 0, 3.175))
 # theta <- runif(nn, 0, 2*pi)
 # nz = runif(1e4, 0, 3.16)
 # nz = nz^10
 # nz = nz/3.16^10*3.16
 # nx <- rho * cos(theta)
 # ny <- rho * sin(theta)
 # nall = data.frame(nx,ny,nz)
 #
 # plot_ly(nall, x = ~nx, y = ~ny, z = ~nz, color = ~nz, colors = c('#BF382A', '#0C4B8E'),
 #         mode = 'markers', #symbols = c('circle','x','o'),
 #         marker = list(size = 3)) #,color = I('black'), )



##### dE/dx calculations per isotope

# constants


sol = 299792458 #m/s
malpha = 6.64884*10^-27 #kg

zbeta = 1
e0 = 8.85419*10^-12 #C^2/(N m^2)
echarge = 1.60218*10^-19 #C
ion = 1.248*10^-17 #J is 78 eV for water
Z = 6.6 #average charge for water
Na = 6.022*10^23 #atoms/mole
densitywater = 993333 #g/m^3
A = 14.3333333 #atomic mass average water
Mu = 1  #g/mol molar mass constant
me = 9.10938*10^-31 #kg electron mass
mwater = 2.99003*10^-36 #kg mass water
joulesperev = 1.6*10^-19 #J/eV
mmpermeter = 1000 #mm/m



maximumdistances = data.frame("Ac225" = 0.065, "Fr221" = 1, "At217" = 1, "Bi213" = 10, "Po213" = 1, "Pb209" = 10, "Bi209" = 10, "Rn217" = 10, "Tl209" = 10, "Lu177" = 0.41202 )
#Initial kinetic energy
#alpha

#j numbers, 1=Ac225, 2=Fr221, 3=at217, 4=bi213, 5=po213, 6=pb209, 7=bi209, 8=rn217, 9=tl209, 10=lu177, 11=
imasses = data.frame('Ac225' = 225, 'Fr221' = 221, 'At217' = 217, 'Bi213' = 213, 'Po213' = 213, 'Pb209' = 209, 'Bi209' = 209, 'Rn217' = 217, 'Tl209' = 209, 'Lu177' = 177, 'Hf177' = 177, j12 = 227, j13 = 227, j14 = 223, j15 = 223, j16 = 219, j17 = 215, j18 = 211, j19 = 211, j20 = 207, j21 = 207)
ienergies = data.frame(eac2fr = 5.935, efr2at = 6.46, eat2bi = 7.20, ebi2po = 1.4227/3, epo2pb = 8.536, epb2bi = 0.644/3, eat2rn = 0.737/3, ebi2tl = 5.98, ern2po = 7.88, etl2pb = 3.976/3, ebi2tl205 = 3.137, elu2hfbeta = 0.497/3, elu2hfgamma1 = 0.208, elu2hfgamma2 = 0.113, eac2th227 = 0.044/3, eac2fr227 = 5.04, efr2ra223 = 1.149/3, eth2ra223 = 6.1466, era2rn219 = 5.97899, ern2po215 = 6.94612, epo2pb211 = 7.52626, epb2bi211 = 1.36697/3, ebi2tl207 = 6.75033, etl2pb207 = 1.41824, epb2stable = 0)


#alpha inital
#write either  -> ke(1000000,1,1) or ke(1000000,'eac2fr','Ac225') etc.
v0alpha = function(e,j){((2*ienergies[,e]*(10^6)*joulesperev)/(malpha+(malpha^2)/((imasses[,j])/1000/Na)))^0.5} #ienergy is in MeV, so multiply by 10^6 and convert to J
e0alpha = function(v){0.5*malpha*v^2}


#beta initial
lorentz0 = function(e){ienergies[,e]/0.511+1} #12 is Lu1772Hf
v0beta = function(lorentz){sol*(1-(1/lorentz)^2)^0.5}

e0beta = function(lorentz){(lorentz-1)*me*sol^2}

#Alpha dE/dx
astepsize = 0.00005 #mm
adistances = NULL

  #zalpha is the charge as a function of velocity due to picking up electrons, starts at 2, goes to 0 eventually when slow enough.
zalpha = function(v){0.0094*(v*100/10^9)^5-0.2591*(v*100/10^9)^4+1.6336*(v*100/10^9)^3-4.2678*(v*100/10^9)^2+5.0412*(v*100/10^9)-0.2426} #v is in m/s
dEadx = function(v){(((4*pi*zalpha(v)^2)/(me*v^2))*((Na*Z*densitywater)/(A*Mu))*(echarge^2/(4*pi*e0))^2*(LN((2*me*v^2)/ion)))/mmpermeter}

Exa = Ex[i-1]-dExadx[i-1]*astepsize

via = function(Exa){(2*Exa/malpha)^0.5}


#Beta dE/dx
bstepsize = 0.0001 #mm
bdistances = NULL

lorentzi = function()








wellheight = 3.16 #mm
wellradius = 3.175^2 #mm
cellheight = 0.02 #mm -> the interaction zone, phi = 0-2*pi still for rho = well radius


#maximum distance travelled for vector (mm)


pmaximumb = 2 #runif(length(times), 0, maximumdistances[,'Lu177'])


Lu177pathlength =  #mm on average
Lu177halfdistance = maximumdistances[,'Lu177']

#point coordinates used for ALL destructions
rho = sqrt(runif(length(times), 0, wellradius))
phi = runif(length(times), 0, 2*pi) #lowercase phi is the point location
pz = runif(length(times), 0, wellheight)

#scaling factor -- check how close to kD it is?
pz = pz^4
pz = pz/wellheight^4*wellheight
#end scaling factor

px <- rho*cos(phi)
py <- rho*sin(phi)

theta = runif(length(times), 0, 2*pi)
Phi = runif(length(times), 0, 2*pi) #capital Phi is the point trajectory
pc = cellheight/cos(theta) #->>pc is the path length of particle interacting through cells
pr = pz-cellheight  #radius from particle to cell surface
pb = pr/cos(theta)

########################## choose if alpha or beta distance, capital Rho is point magnitude
Rho = pmaximumb*sin(theta) #data.frame('Ac225' = maximumdistances[,'Ac225']*sin(theta))

#Vector coordinates
Px = px - Rho*cos(Phi)
Py = py - Rho*sin(Phi)
Pz = pz - Rho/tan(theta)



#create an exclusionary zone for particle angles at certain positions
#theta must be between 0 -> pi/2, and 3*pi/2 to 2*pi
#maximum distance of b+c

#test vector magnitude
pmag = ((Px-px)^2+(Py-py)^2+(Pz-pz)^2)^0.5


#still using 1/3 max beta energy since it's a distribution and most aren't that energenic, most are 1/3 as energetic as the max.

#beta using ionization depletion from - http://www.physics.smu.edu/~scalise/emmanual/radioactivity/lab.html
Lu177intensity = function(raylength){(energies['elu2hfbeta']/Lu177pathlength) * 2^(-raylength/(Lu177pathlength/1.5))} #if you use this, you have to remove the 1/3 max intensity rule to beta since this is more accurate
#alpha from Bethe equation - https://en.wikipedia.org/wiki/Bethe_formula










Ac225intensity = function(raylength){(energies['eac2fr']/maximumdistances[,'Ac225'])}



#Ac225intensity = function(raylength){(energies['eac2fr']/Ac225pathlength) * (raylength^0.05)-((energies['eac2fr']/Ac225pathlength))/(1+(raylength/Ac225pathlength)^(-10))}
#betaintensity = function(raylength){energies['elu2hfbeta']/betapathlength-((energies['elu2hfbeta']/betapathlength))/(1+(raylength/(betapathlength/4))^(-1))} #MeV/mm
#alphaintensity = function(raylength){energies['eac2fr']/alphapathlength-((energies['eac2fr']/alphapathlength))/(1+(raylength/alphapathlength)^(-10))} #MeV/mm

distancesalpha = c(lseq(0.001,1,1000))
intensityAc225 = data.frame(distancesalpha,Ac225intensity(distancesalpha))
colnames(intensityAc225) = c("Distances","Ac-225")

distancesbeta = c(lseq(0.001,20,500))
intensityLu177 = data.frame(distancesbeta,Lu177intensity(distancesbeta))
colnames(intensityLu177) = c("Distances","Lu-177")

mintensityAc225 = melt(intensityAc225[1:600,], id="Distances")
colnames(mintensityAc225) = c("Distances","Species", "LET")

mintensityLu177 = melt(intensityLu177[1:384,], id="Distances")
colnames(mintensityLu177) = c("Distances","Species", "LET")




AcLET = ggplot(mintensityAc225, aes(x=Distances, y=LET, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17))+
  scale_x_continuous(breaks=c(0, 0.02, 0.04, 0.06, 0.08, 0.1))+
  scale_y_continuous(breaks=c(0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140))+
  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  labs(x = "Distance (mm)", y = "LET (MeV/mm)", color="Species")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+
  guides(shape=guide_legend(override.aes = list(size=3)))

LuLET = ggplot(mintensityLu177, aes(x=Distances, y=LET, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17))+
  scale_x_continuous(breaks=c(0.0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4))+#0.4, 0.8, 1.2, 1.6))+
  scale_y_continuous(breaks=c(0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4))+
  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  labs(x = "Distance (mm)", y = "LET (MeV/mm)", color="Species")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+
  guides(shape=guide_legend(override.aes = list(size=3)))

grid.arrange(AcLET, LuLET, nrow = 1)

write.csv(intensitytestbeta, "intensitybetarecent.csv", sep="\t")


positions = data.frame(times, px, py, pz)
vectors = data.frame(times, Px, Py, Pz)
positions1 = cbind(positions, 0)
vectors1 = cbind(vectors, 1)

colnames(positions1) = c('times', 'px', 'py', 'pz', 'zz')
colnames(vectors1) = c('times', 'px', 'py', 'pz', 'zz')


positionlinevector = rbind(positions1, vectors1)
positionlinevector1 = positionlinevector[order(positionlinevector$times),]
positionlinevector2 = do.call(rbind, by(positionlinevector1, positionlinevector1$times, rbind, NA))

#control surface
rhocirc = sqrt(wellradius)
phicirc = runif(length(times), 0, 2*pi) #lowercase phi is the point location
pzcirc = matrix(runif(length(times), 0, 0))
pxcirc = rhocirc*cos(phicirc)
pycirc = rhocirc*sin(phicirc)

controlsurface = data.frame(times, pxcirc, pycirc, pzcirc)

plot_ly() %>%
  add_trace(data = positionlinevector2, x = ~px, y = ~py, z = ~pz, type = 'scatter3d', mode = 'lines+markers', name = 'Beta',
            line = list(color = 'orange', width = 0.5),
            marker = list(color = ~zz, colorscale = 'RdBu', size = 2, showscale = TRUE))%>%
  add_trace(data = controlsurface, x = controlsurface$pxcirc, y = controlsurface$pycirc, z = controlsurface$pzcirc, type="mesh3d")


plot_ly(positions) %>%
  add_trace(x = ~px, y = ~py, z = ~pz, type = 'scatter3d', mode = 'markers', name = 'vectorend',
            marker = list(color = 'blue', size = 3)) #%>%
 # add_trace(x = ~px, y = ~py, z = pz, type = 'scatter3d', mode = 'markers', name = 'metal location',
  #          marker = list(color = '#0C4B8E', size = 3))



plot_ly(vectors, x = ~Px, y = ~Py, z = ~Pz, color = ~Pz, colors = c('#BF382A', '#0C4B8E'),
      type = 'scatter3d',
      mode = 'markers', #symbols = c('circle','x','o'),
      marker = list(size = 3))#,color = I('black'), )








#exclusion test -> this removes points that are x^2+y^2 < 1, for all columns
#positions2 = positions[positions$px^2+positions$py^2<1,]



#write inclusionary conditions for each point hitting the control surface

#################positionsinclusive = positions[positions$  +  positions$  <  ,]


# for x,y,z positions
#x^2+y^2 <= wellradius  #this is already squared!
#z < cellheight
#z >= 0


#equation of each vector -> end - start

# <Px,Py,Pz> - <px,py,pz> -> (Px-px,Py-py,Pz-pz)

vectorsline = data.frame(Px-px,Py-py,Pz-pz)
vx = Px-px
vy = Py-py
vz = Pz-pz



#r = c(Px, Py, Pz) + t*vectorsline
#or parametricly
rx = Px+t*vx
ry = Py+t*vy
yz = Pz+t*vz


#myfunction = function(x){2*x+1}

#test = myfunction(2)


#########################################################################################################
#Example vector intersecting a 3D circle

v0 = c(2,2,2)
v1 = c(-2,-2,-2)
vv = data.frame(v0,v1)

#circle
rhoc = sqrt(runif(length(times), 0, wellradius))
phic = runif(length(times), 0, 2*pi) #lowercase phi is the point location
pzc = runif(length(times), 0, cellheight)
pxc = rhoc*cos(phic)
pyc = rhoc*sin(phic)

circle = data.frame(pxc,pyc,pzc)
#vertical line
ax = c(0,0)
ay = c(0,0)
az = c(1,-1)

#test line

#pointAA
cc = c(2,2,2)
dd = c(-2,-2,-2)

#or
cx = 2
cy = 3
cz = 4
Cx = -2
Cy = -2
Cz = -2

cpoints = c(cx,cy,cz)
Cpoints = c(Cx,Cy,Cz)

Ccpoints = t(matrix(Cpoints-cpoints))


#equation of the line
#r = c(Px, Py, Pz) + t*vectorsline
pointseq = function(tt){tt*Ccpoints+cpoints}

#parametric
ppx = function(t){cx+t*(Ccpoints[,1])}
ppy = function(t){cy+t*(Ccpoints[,2])}
ppz = function(t){cz+t*(Ccpoints[,3])}

#when ppz = 0, that is the intersection point. just see if x^2 + y^2 are => cellradius^0.5

setz0 = -cz/Ccpoints[,3]

intersection0 = c(ppx(setz0), ppy(setz0), ppz(setz0))

setzh = (cellheight-cz)/Ccpoints[,3]

intersectionh = c(ppx(setzh), ppy(setzh), ppz(setzh))

#ray length of intersection - magnitude from intersectionh to intersection0
raymagh = ((intersectionh[1]-intersection0[1])^2+(intersectionh[2]-intersection0[2])^2+(intersectionh[3]-intersection0[3])^2)^0.5


#ray distance from start = magnitude from point a (lowercase) to intersection h
raymag = ((cpoints[1]-intersectionh[1])^2+(cpoints[2]-intersectionh[2])^2+(cpoints[3]-intersectionh[3])^2)^0.5

#ray energy at that distance

rayintensity = betaintensity(raymag) - betaintensity(raymagh+raymag)


#equation of the lower circle at z=0
#x^2+y^2 = wellradius @ z = 0 to z = cellheight

# aaaa = (Ccpoints[,1])^2+(Ccpoints[,2])^2
# bbbb = 2*(cx*Ccpoints[,1]+cy*Ccpoints[,2])
# cccc = cx^2+cy^2-wellradius
#
# tol1 = (-(bbbb)+(bbbb^2-4*aaaa*cccc)^0.5)/(2*aaaa)
# tol2 = (-(bbbb)-(bbbb^2-4*aaaa*cccc)^0.5)/(2*aaaa)
#




#what values of tt do I even choose?

pointslineout = data.frame(t(pointseq(1)), t(pointseq(0.75)), t(pointseq(0.5)), t(pointseq(0.25)), t(pointseq(0)))
pointslineoutt = data.frame(t(pointslineout))
colnames(pointslineoutt) = c("x","y","z")

pointsx = pointslineoutt$x[]
pointsy = pointslineoutt$y[]
pointsz = pointslineoutt$z[]

plot_ly() %>%
  add_trace(x = ~pxc, y = ~pyc, z = ~pzc, type = 'scatter3d', mode = 'markers', name = 'vectorend',
            marker = list(color = '#BF382A', size = 1)) %>%
  add_trace(x = ~ax, y = ~ay, z = ~az, type = 'scatter3d', mode = 'lines', name = 'metal location',
            line = list(color = '#0C4B8E', size = 3)) %>%
  add_trace(x = ~pointsx, y = ~pointsy, z = ~pointsz, type = 'scatter3d', mode = 'lines', name = 'metal location',
          line = list(color = 'green', size = 3))

#now predict the intersection of the plane








########################################################################################################################

#example to rbind and create blanks after each group for line segmentation plot

# tester1 = data.frame(aaa = c(0,1,2,3), bbb = c(1,2,3,4), ccc = c(2,3,5,6), groupss = c('a','a','b','b'))
#
# #transform to characters
# tester1new <- as.data.frame(lapply(tester1, as.character), stringsAsFactors = FALSE)
#
# tester1new1 = do.call(rbind, by(tester1new, tester1new$groupss, rbind, ""))
#
#
#
# plot_ly(tester1new1) %>%
#   add_trace(x = ~aaa, y = ~bbb, z = ~ccc, type = 'scatter3d', mode = 'lines', name = 'vectorend',
#             line = list(color = '#BF382A', size = 3))
#





#now add a vector from each point?
#with vector, see hwo far away from 10 micron surface, yes or no and assign a yes or no
#then add into energies data array
#then run many times to take average energy
#or should I run this many times ahead of time







#Comapre activities of Ac-225 vs Lu-177 with the starting activities used at the top uciac225, ucilu177
#Lutetium-177 activity calculator

#colnames(edaughtersdata)[c(2,13,14,15)] = c("Ac-225 (0.X ?Ci)", "Lu-177 (20 ?Ci)", "Ac-225 SUM Alpha", "Ac-225 SUM Beta")

#no PK
eploto <- edaughtersdata[eplotrows, c(1,2,11,14,15,13,3,4,5,6,7,8,9,10,16,17,18,19,20,21,22,23,24,25,26)]

##################################
################################## <<<<<<<<<<<<<<<------ eplotout PK half life from here out
####################
#PK elimination
#human, 29 days
#mouse, 10 days
#No PK = 1000000 is effectivy multiplying by 1

PK = 1000000

####################


#with PK
eplotout <- edaughtersdata[eplotrows, c(1,2,11,14,15,13,3,4,5,6,7,8,9,10,16,17,18,19,20,21,22,23,24,25,26)]

eplottimesdf = data.frame(plottimes)
eplotoutpk = (0.5^(plottimes/PK))*eplotout[,2:ncol(eplotout)]
eplotout = cbind(eplottimesdf,eplotoutpk)
colnames(eplotout)[1] = "times"




#testerr = by(eploto, 1:nrow(eploto), function(this) newenergy = oldenergy*2)

# for (i in 1:(length(eploto[,1]))){
# eplotout[i] = eploto[i,2:(length(eploto[1,]))]*0.5
# }
#



#PKadjust = function(timee,energy) {
#  energyout = energy*0.5^((timee)/PK)
#}

#Aaaa = PKadjust(10,10)

#apply test

#apply(thearray, a vector giving where function is applied over, function to be applied)

#for(i in 1:(length(eploto[,1])))
#{eplotout[i] = PKadjust(eploto[i,2],eploto[i,1])
#}

#for(i in 1:(length(eploto[,1])))
#{eplotout[i] = ((eploto[i,2])*0.5^((eploto[i,1])/PK))
#}


#no PK
#eplotout2 <- edaughtersdata[eplotrows, c(1,2,11,14,15,13,3,4,5,6,7,8,9,10)]
#eplotout2 <- edaughtersdata[eplotrows, c(1,2,11,13)]

# for Ac-227 series, 16:26

#with PK
eplotout2 <- eplotout[, c(1,2,3,6)]

meplotout <- melt(eplotout, id="times")
meplotout2 <- melt(eplotout2, id="times")

colnames(meplotout) <- c("times","Species","value")
colnames(meplotout2) <- c("times","Species","value")

#compare the two
eplotoutcompare <- cbind((edaughtersdata[eplotrows, c(1,2,11,13)]),eplotout2[,2:4])
colnames(eplotoutcompare)[5:7] = cbind("Ac-225 (0.2 ?Ci) PK","Ac-225 SUM PK","Lu-177 (20 ?Ci) PK")

meplotoutcompare = melt(eplotoutcompare, id="times")
colnames(meplotoutcompare) <- c("times","Species","value")

ggplot(meplotout2, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=2, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-5), 10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4), 10^(5), 10^(6), 10^(7), 10^(8), 10^(9), 10^(10), 10^(11), 10^(12), 10^(13)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.title.align = 0.5, text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+

  labs(x = "Time (day)", y = "Power (MeV/day)")+
  theme(text = element_text(size=18, face = "bold"),

      legend.position = c(.05, .05),
      legend.justification = c("left", "bottom"),
      legend.box.just = c("left"),
      legend.margin = margin(4, 4, 4, 4))+


  guides(shape=guide_legend(override.aes = list(size=3)))




ggplot(meplotoutcompare, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=2, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-5), 10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4), 10^(5), 10^(6), 10^(7), 10^(8), 10^(9), 10^(10), 10^(11), 10^(12), 10^(13)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.title.align = 0.5, text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"))+

  labs(x = "Time (day)", y = "Power (MeV/day)")+
  #theme(text = element_text(size=18, face = "bold"))+

  #theme(legend.position = #c(.95, .95),
  #     legend.justification = c("right", "top"),
  #    legend.box.just = "right")+
  #    legend.margin = margin(6, 6, 6, 6))+


  guides(shape=guide_legend(override.aes = list(size=3)))





#Integrate to get sum of energy vs time isnteaf of instantaneous.

Ac225gs = NULL
Ac225gsi = NULL
Ac225SUMgs = NULL
Ac225SUMgsi = NULL
Lu177gs = NULL
Lu177gsi = NULL
AlphaSUMgs = NULL
AlphaSUMgsi = NULL
BetaSUMgs = NULL
BetaSUMgsi = NULL

Fr221gs = NULL
Fr221gsi = NULL
At217gs = NULL
At217gsi = NULL
Bi213gs = NULL
Bi213gsi = NULL
Po213gs = NULL
Po213gsi = NULL
Pb209gs = NULL
Pb209gsi = NULL
Bi209gs = NULL
Bi209gsi = NULL
Rn217gs = NULL
Rn217gsi = NULL
Tl209gs = NULL
Tl209gsi = NULL

Ac227gs = NULL
Ac227gsi = NULL
Th227gs = NULL
Th227gsi = NULL
Fr223gs = NULL
Fr223gsi = NULL
Ra223gs = NULL
Ra223gsi = NULL
Rn219gs = NULL
Rn219gsi = NULL
Po215gs = NULL
Po215gsi = NULL
Pb211gs = NULL
Pb211gsi = NULL
Bi211gs = NULL
Bi211gsi = NULL
Tl207gs = NULL
Tl207gsi = NULL
Pb207gs = NULL
Pb207gsi = NULL
Ac227SUMgs = NULL
Ac227SUMgsi = NULL


for(i in 1:(length(eplotout[,1])))
{Ac225gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,2]+3*((2*eplotout[i,2]+eplotout[i+1,2])/3)+3*((eplotout[i,2]+2*eplotout[i+1,2])/3)+eplotout[i+1,2])
Ac225gsi[i] = sum(Ac225gs[1:i-1])

Ac225SUMgs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,3]+3*((2*eplotout[i,3]+eplotout[i+1,3])/3)+3*((eplotout[i,3]+2*eplotout[i+1,3])/3)+eplotout[i+1,3])
Ac225SUMgsi[i] = sum(Ac225SUMgs[1:i-1])

Lu177gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,6]+3*((2*eplotout[i,6]+eplotout[i+1,6])/3)+3*((eplotout[i,6]+2*eplotout[i+1,6])/3)+eplotout[i+1,6])
Lu177gsi[i] = sum(Lu177gs[1:i-1])

AlphaSUMgs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,4]+3*((2*eplotout[i,4]+eplotout[i+1,4])/3)+3*((eplotout[i,4]+2*eplotout[i+1,4])/3)+eplotout[i+1,4])
AlphaSUMgsi[i] = sum(AlphaSUMgs[1:i-1])

BetaSUMgs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,5]+3*((2*eplotout[i,5]+eplotout[i+1,5])/3)+3*((eplotout[i,5]+2*eplotout[i+1,5])/3)+eplotout[i+1,5])
BetaSUMgsi[i] = sum(BetaSUMgs[1:i-1])

Fr221gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,7]+3*((2*eplotout[i,7]+eplotout[i+1,7])/3)+3*((eplotout[i,7]+2*eplotout[i+1,7])/3)+eplotout[i+1,7])
Fr221gsi[i] = sum(Fr221gs[1:i-1])

At217gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,8]+3*((2*eplotout[i,8]+eplotout[i+1,8])/3)+3*((eplotout[i,8]+2*eplotout[i+1,8])/3)+eplotout[i+1,8])
At217gsi[i] = sum(At217gs[1:i-1])

Bi213gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,9]+3*((2*eplotout[i,9]+eplotout[i+1,9])/3)+3*((eplotout[i,9]+2*eplotout[i+1,9])/3)+eplotout[i+1,9])
Bi213gsi[i] = sum(Bi213gs[1:i-1])

Po213gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,10]+3*((2*eplotout[i,10]+eplotout[i+1,10])/3)+3*((eplotout[i,10]+2*eplotout[i+1,10])/3)+eplotout[i+1,10])
Po213gsi[i] = sum(Po213gs[1:i-1])

Pb209gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,11]+3*((2*eplotout[i,11]+eplotout[i+1,11])/3)+3*((eplotout[i,11]+2*eplotout[i+1,11])/3)+eplotout[i+1,11])
Pb209gsi[i] = sum(Pb209gs[1:i-1])

Bi209gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,12]+3*((2*eplotout[i,12]+eplotout[i+1,12])/3)+3*((eplotout[i,12]+2*eplotout[i+1,12])/3)+eplotout[i+1,12])
Bi209gsi[i] = sum(Bi209gs[1:i-1])

Rn217gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,13]+3*((2*eplotout[i,13]+eplotout[i+1,13])/3)+3*((eplotout[i,13]+2*eplotout[i+1,13])/3)+eplotout[i+1,13])
Rn217gsi[i] = sum(Rn217gs[1:i-1])

Tl209gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,14]+3*((2*eplotout[i,14]+eplotout[i+1,14])/3)+3*((eplotout[i,14]+2*eplotout[i+1,14])/3)+eplotout[i+1,14])
Tl209gsi[i] = sum(Tl209gs[1:i-1])


Ac227gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,15]+3*((2*eplotout[i,15]+eplotout[i+1,15])/3)+3*((eplotout[i,15]+2*eplotout[i+1,15])/3)+eplotout[i+1,15])
Ac227gsi[i] = sum(Ac227gs[1:i-1])
Th227gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,16]+3*((2*eplotout[i,16]+eplotout[i+1,16])/3)+3*((eplotout[i,16]+2*eplotout[i+1,16])/3)+eplotout[i+1,16])
Th227gsi[i] = sum(Th227gs[1:i-1])
Fr223gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,17]+3*((2*eplotout[i,17]+eplotout[i+1,17])/3)+3*((eplotout[i,17]+2*eplotout[i+1,17])/3)+eplotout[i+1,17])
Fr223gsi[i] = sum(Fr223gs[1:i-1])
Ra223gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,18]+3*((2*eplotout[i,18]+eplotout[i+1,18])/3)+3*((eplotout[i,18]+2*eplotout[i+1,18])/3)+eplotout[i+1,18])
Ra223gsi[i] = sum(Ra223gs[1:i-1])
Rn219gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,19]+3*((2*eplotout[i,19]+eplotout[i+1,19])/3)+3*((eplotout[i,19]+2*eplotout[i+1,19])/3)+eplotout[i+1,19])
Rn219gsi[i] = sum(Rn219gs[1:i-1])
Po215gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,20]+3*((2*eplotout[i,20]+eplotout[i+1,20])/3)+3*((eplotout[i,20]+2*eplotout[i+1,20])/3)+eplotout[i+1,20])
Po215gsi[i] = sum(Po215gs[1:i-1])
Pb211gs[i]=  ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,21]+3*((2*eplotout[i,21]+eplotout[i+1,21])/3)+3*((eplotout[i,21]+2*eplotout[i+1,21])/3)+eplotout[i+1,21])
Pb211gsi[i] = sum(Pb211gs[1:i-1])
Bi211gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,22]+3*((2*eplotout[i,22]+eplotout[i+1,22])/3)+3*((eplotout[i,22]+2*eplotout[i+1,22])/3)+eplotout[i+1,22])
Bi211gsi[i] = sum(Bi211gs[1:i-1])
Tl207gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,23]+3*((2*eplotout[i,23]+eplotout[i+1,23])/3)+3*((eplotout[i,23]+2*eplotout[i+1,23])/3)+eplotout[i+1,23])
Tl207gsi[i] = sum(Tl207gs[1:i-1])
Pb207gs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,24]+3*((2*eplotout[i,24]+eplotout[i+1,24])/3)+3*((eplotout[i,24]+2*eplotout[i+1,24])/3)+eplotout[i+1,24])
Pb207gsi[i] = sum(Pb207gs[1:i-1])
Ac227SUMgs[i] = ((eplotout[i+1,1]-eplotout[i,1])/8)*(eplotout[i,25]+3*((2*eplotout[i,25]+eplotout[i+1,25])/3)+3*((eplotout[i,25]+2*eplotout[i+1,25])/3)+eplotout[i+1,25])
Ac227SUMgsi[i] = sum(Ac227SUMgs[1:i-1])
}

Allgsim = data.frame(cbind(eplotout[,1],Ac225gsi,Ac225SUMgsi,BetaSUMgsi,Lu177gsi,Fr221gsi,At217gsi,Bi213gsi,Po213gsi,Pb209gsi,Bi209gsi,Rn217gsi,Tl209gsi,Ac227gsi,Th227gsi,Fr223gsi,Ra223gsi,Rn219gsi,Po215gsi,Pb211gsi,Bi211gsi,Tl207gsi,Pb207gsi,Ac227SUMgsi))
#Allgsim = Allgsim[-1,] #remove first row
colnames(Allgsim) = c("times", "Ac-225 (0.17 µCi)","Ac-225 (0.17 µCi) SUM","Ac-225 Beta SUM","Lu-177 (21 µCi)","Fr-221", "At-217", "Bi-213", "Po-213", "Pb-209", "Bi-209", "Rn-217", "Tl-209", "Ac-227 (0.X ?Ci)", "Th-227", "Fr-223", "Ra-223", "Rn-219", "Po-215", "Pb-211", "Bi-211", "Tl-207", "Pb-207", "Ac-227 SUM")

#select columns
#for Ac-225
Allgsim2 = Allgsim[,cbind(1,3,5)]

#For Ac-227
#Allgsim2 = Allgsim[, c(1,14,24,15,16,17,18,19,20,21,22,23)]
#colnames(Allgsim2) = c("times", "Ac-227 (0.X ?Ci)", "Ac-227 SUM)", "Th-227", "Fr-223", "Ra-223", "Rn-219", "Po-215", "Pb-211", "Bi-211", "Tl-207", "Pb-207")


#can change all these to mAllgsim si mAllgsim2

mAllgsim2 <- melt(Allgsim2, id="times")
colnames(mAllgsim2) <- c("times","Species","value")



ggplot(mAllgsim2, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-5), 10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0),10^(1), 10^(2), 10^(3), 10^(4), 10^(5), 10^(6), 10^(7), 10^(8), 10^(9), 10^(10), 10^(11), 10^(12), 10^(13)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Cumulative Energy (MeV)")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.05, .95),
        legend.justification = c("left", "top"),
        legend.box.just = "left",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))





#Choose the radius of effect, or directly the volume affected



#  **********************
#  **************************
#Fraction ID, not per gram
ID = 1
#  **************************
#  **********************

#per kilogram

alphadistance = #0.5 #cm
volalphatissue = 0.1 #4/3*pi*alphadistance^3 #cm^3
tissuedensity = 1#1.04 #g/cm^3 #cite Nuclear Medicine Therapy: Principles and Clinical Applications - Aktolun, Goldsmith
massalphatissue = volalphatissue*tissuedensity/1000 #kg

betadistance = #0.5 #cm
volbetatissue = 0.1 #4/3*pi*betadistance^3 #cm^3
tissuedensity = 1#1.04 #g/cm^3 #cite Nuclear Medicine Therapy: Principles and Clinical Applications - Aktolun, Goldsmith
massbetatissue = volbetatissue*tissuedensity/1000 #kg

Gy = 6.242E12 #MeV/J & 1 J/kg is 1 Gy, so also units of #(MeV/kg)/Gy which is 1 Gy = 6.242E12 MeV/kg since 1 J = 6.242E12 MeV

#ac225dose = (2.5E6/massalphatissue)/Gy #(MeV/kg)/6.242E12(MeV/kg)/Gy = #Gy


gAc225 = ID*Allgsim[,2]*(probabilities[1]/massalphatissue)/Gy
gFr221 = ID*Allgsim[,6]*(probabilities[2]/massalphatissue)/Gy
gAt217 = ID*Allgsim[,7]*(probabilities[3]/massalphatissue+probabilities[7]/massbetatissue)/Gy
gBi213 = ID*Allgsim[,8]*(probabilities[4]/massalphatissue+probabilities[8]/massbetatissue)/Gy
gPo213 = ID*Allgsim[,9]*(probabilities[5]/massalphatissue)/Gy
gPb209 = ID*Allgsim[,10]*(probabilities[6]/massbetatissue)/Gy
gBi209 = ID*Allgsim[,11]*(probabilities[11]/massalphatissue)/Gy
gRn217 = ID*Allgsim[,12]*(probabilities[9]/massalphatissue)/Gy
gTl209 = ID*Allgsim[,13]*(probabilities[10]/massbetatissue)/Gy
gAc225SUM = (gAc225+gFr221+gAt217+gBi213+gPo213+gPb209+gBi209+gRn217+gTl209)
gSUMoverac225 = gAc225SUM/gAc225
gLu177 = ID*Allgsim[,5]/massbetatissue/Gy
gAlpha = gAc225 +
         gFr221 +
         ID*Allgsim[,7]*(probabilities[3]/massalphatissue)/Gy +
         ID*Allgsim[,8]*(probabilities[4]/massalphatissue)/Gy +
         gPo213 +
         gBi209 +
         gRn217

gBeta =  ID*Allgsim[,7]*(probabilities[7]/massbetatissue)/Gy +
         ID*Allgsim[,8]*(probabilities[8]/massbetatissue)/Gy +
         gPb209 +
         gTl209

gAc225n = gAc225/gAc225SUM
gLu177n = gLu177/gAc225SUM
gAlphan = gAlpha/gAc225SUM
gBetan = gBeta/gAc225SUM


gAc227 = ID*Allgsim[,14]*(probabilities[15]/massbetatissue+probabilities[16]/massalphatissue)/Gy
gTh227 = ID*Allgsim[,15]*(probabilities[18]/massalphatissue)/Gy
gFr223 = ID*Allgsim[,16]*(probabilities[17]/massbetatissue)/Gy
gRa223 = ID*Allgsim[,17]*(probabilities[19]/massalphatissue)/Gy
gRn219 = ID*Allgsim[,18]*(probabilities[20]/massalphatissue)/Gy
gPo215 = ID*Allgsim[,19]*(probabilities[21]/massalphatissue)/Gy
gPb211 = ID*Allgsim[,20]*(probabilities[22]/massbetatissue)/Gy
gBi211 = ID*Allgsim[,21]*(probabilities[23]/massalphatissue)/Gy
gTl207 = ID*Allgsim[,22]*(probabilities[24]/massbetatissue)/Gy
gPb207 = ID*Allgsim[,23]*(probabilities[25]/massalphatissue)/Gy
gAc227SUM = (gAc227+gTh227+gFr223+gRa223+gRn219+gPo215+gPb211+gBi211+gTl207+gPb207)

gAc227n = gAc227/gAc227SUM
gAcvsn = gAc227SUM/gAc225SUM




gdaughtersdata = data.frame(Allgsim[,1])
gdaughtersdata = cbind(gdaughtersdata, gAc225, gFr221, gAt217, gBi213, gPo213, gPb209, gBi209, gRn217, gTl209, gAc225SUM, gSUMoverac225, gLu177, gAlpha, gBeta, gAc225n, gLu177n, gAlphan, gBetan, gAc227,gTh227,gFr223,gRa223,gRn219,gPo215,gPb211,gBi211,gTl207,gPb207,gAc227SUM, gAc227n, gAcvsn)
colnames(gdaughtersdata) = c("times", "Ac-225 (0.00018 ?Ci)", "Fr-221", "At-217", "Bi-213", "Po-213", "Pb-209", "Bi-209", "Rn-217", "Tl-209", "Ac-225 SUM (0.17 µCi)", "Ac-225 SUM / Ac-225", "Lu-177 (21 µCi)", "Ac-225 SUM Alpha", "Ac-225 SUM Beta", "Ac-225 SUM / Ac-225 SUM", "Lu-177 / Ac-225 SUM", "Alpha SUM / Ac-225 SUM", "Beta SUM / Ac-225 SUM", "Ac-227 (2 nCi)", "Th-227", "Fr-223", "Ra-223", "Rn-219", "Po-215", "Pb-211", "Bi-211", "Tl-207", "Pb-207", "Ac-227 SUM", "Ac-227 / Ac-227 SUM", "Ac-225 SUM / Ac-227 SUM")



#no longer necessary to parse since integrated parsed
# gplotrows = seq(1, length(timesout), 1))
# gplottimes <- times[gplotrows]

#choose columns


# gplotout <- gdaughtersdata[gplotrows, c(1:11,13,14,15,12,17,18,19)]
# mgplotout <- melt(gplotout, id="times")
# colnames(mgplotout) <- c("times","Species","value")

gplotout <- gdaughtersdata[,c(1:11,13,14,15,12,17,18,19)]
#gplotout <- gdaughtersdata[,c(1,11,13)]
mgplotout <- melt(gplotout, id="times")
colnames(mgplotout) <- c("times","Species","value")

gplotout2 <- gdaughtersdata[,c(1,20,21,22,23,24,25,26,27,28,29,30)]
mgplotout2 <- melt(gplotout2, id="times")
colnames(mgplotout2) <- c("times","Species","value")





ggplot(mgplotout, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-13), 10^(-12), 10^(-11), 10^(-10), 10^(-9), 10^(-8), 10^(-7), 10^(-6), 10^(-5),10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Dose (Gy)")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.05, .95),
        legend.justification = c("left", "top"),
        legend.box.just = "left",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))



#Just the ones that matter


gplotout <- gdaughtersdata[, c(1,11,13)]
mgplotout <- melt(gplotout, id="times")
colnames(mgplotout) <- c("times","Species","value")



ggplot(mgplotout, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-10), 10^(-9), 10^(-8), 10^(-7), 10^(-6), 10^(-5),10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Dose (Gy)")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.01, .99),
        legend.justification = c("left", "top"),
        legend.box.just = "left",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))


#to compare two doses, run first at low dose, create gplotoutlowdose from gplotout,
  #then run again with new numbers into gplotouthighdose, add them into BOTH, and reorder columns

#gplotoutlowdose = gplotout
#gplotouthighdose = gplotout
gplotoutboth = cbind(gplotoutlowdose[,],gplotouthighdose[,2:3])
gplotoutbothordered = gplotoutboth[,c(1,2,4,3,5)]

#plot out final figure




mgplotout <- melt(gplotoutbothordered, id="times")
colnames(mgplotout) <- c("times","Species","value")



ggplot(mgplotout, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(10^(-10), 10^(-9), 10^(-8), 10^(-7), 10^(-6), 10^(-5),10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Dose (Gy)")+
  theme(text = element_text(size=18, face = "bold"),
        legend.title.align = 0,
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.99, 0.01),
        legend.justification = c("right", "bottom"),
        legend.box.just = "left",
        legend.margin = margin(1, 1, 1, 1))+
  guides(shape=guide_legend(override.aes = list(size=3)))



#at thsi point, add an IgG elimination rate to get more realistic dose.








#Plot as a fraction of Ac-225 dose

# gplotout <- gdaughtersdata[gplotrows, c(1,12,18,19,17)]
# mgplotout <- melt(gplotout, id="times")
# colnames(mgplotout) <- c("times","Species","value")
#
#
#
# ggplot(mgplotout, aes(x=times, y=value, by=Species))+
#   geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
#   scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+
#
#   scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100))+
#   annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
#                       short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
#                       colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+
#
#   scale_y_log10(breaks=c(10^(-4), 10^(-3), 10^(-2), 10^(-1), 10^(0), 10^(1), 10^(2), 10^(3), 10^(4)))+
#
#   theme_bw() +
#   theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
#
#   labs(x = "Time (days)", y = "Dose x / Ac-225 only Dose")+
#   theme(text = element_text(size=18, face = "bold"))+
#   guides(shape=guide_legend(override.aes = list(size=3)))
#
#




#Integrate to find total dose from instantaneous dose
#Fit gElements

#working prototype
#Simpsons 3/8 rule
#from a to b, f(x) dx = ((b-a)/8)*(f(a)+3*f((2a+b)/3)+3*f((a+2*b)/3)+f(b))


#___________________________
# #vv = seq(0,10,0.1)
# xx = seq(0,10,0.1)
# yy = seq(0,10,0.1)
# zz = data.frame(xx,yy)
# usw = NULL
# usr = NULL
# usq = NULL
#
# for(i in 1:(length(zz[,1])))
# {usw[i] = ((zz[i+1,1]-zz[i,1])/8)*(zz[i,2]+3*((2*zz[i,2]+zz[i+1,2])/3)+3*((zz[i,2]+2*zz[i+1,2])/3)+zz[i+1,2])
#     usr[i] = sum(usw[1:i-1])}
#
# usq = data.frame(cbind(xx,usw,usr))
#
# plot(xx^2/2,usr)
#___________________________
#OK!
#Now with gdaughtersdata


#1,2,11,13,14,15

#Ac225g = data.frame(gdaughtersdata[,1],gdaughtersdata[,2])
#colnames(Ac225g) = c("times","Ac-225")






#now do fractional cumulative dose compared to Ac-225



fAllgsim = data.frame(cbind(gplotout[,1],gAc225n,gAc225n/gAc225n,gLu177n,gAcvsn))
#fAllgsim = fAllgsim[-1,] #remove first row
colnames(fAllgsim) = c("times", "Ac-225 0.2 ?Ci","Ac-225 0.2 ?Ci + Daughters","Lu-177 20 ?Ci", "Ac-227 2 nCi + Daughters")



mfAllgsim <- melt(fAllgsim, id="times")
colnames(mfAllgsim) <- c("times","Species","value")


saa=10
ggplot(mfAllgsim, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(saa^(-4), saa^(-3), saa^(-2), saa^(-1), saa^(0), saa^(1), saa^(2), saa^(3), saa^(4), saa^(5)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Dose of Species(x) / Ac-225 SUM")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.01, .3),
        legend.justification = c("left", "bottom"),
        legend.box.just = "left",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))



#Now add in equivalent dose and convert to Sieverts
#equivalent dose = SUM(absorbed dose * weighting factor)
# 1 Gy alpha = 20 Sv, 1 Gy beta = 1 Sv

#alpha weighting factor
AF = 20


eqAllgsim = data.frame(cbind(gplotout[,1],gAc225*AF,gAc225SUM*AF,gLu177))
#eqAllgsim = eqAllgsim[-1,] #remove first row
colnames(eqAllgsim) = c("times", "Ac-225 0.51 ?Ci","Ac-225 0.51 ?Ci + Daughters","Lu-177 64 ?Ci")



meqAllgsim <- melt(eqAllgsim, id="times")
colnames(meqAllgsim) <- c("times","Species","value")


sb=10
ggplot(meqAllgsim, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(sb^(-4), sb^(-3), sb^(-2), sb^(-1), sb^(-0), sb^(1), sb^(2), sb^(3), sb^(4), sb^(5), sb^(6), sb^(7)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Cumulative \n Equivalent Dose (Sv)")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.97, .02),
        legend.justification = c("right", "bottom"),
        legend.box.just = "right",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))





#now do fractional cumulative equivalent dose compared to Ac-225

eqfAllgsim = data.frame(cbind(gplotout[,1],(gAc225*AF)/(gAc225SUM*AF),(gAc225SUM*AF)/(gAc225SUM*AF),gLu177/(gAc225SUM*AF)))
#eqfAllgsim = eqfAllgsim[-1,] #remove first row
colnames(eqfAllgsim) = c("times", "Ac-225 0.2 ?Ci","Ac-225 0.2 ?Ci + Daughters","Lu-177 20 ?Ci")



meqfAllgsim <- melt(eqfAllgsim, id="times")
colnames(meqfAllgsim) <- c("times","Species","value")


sc=2
ggplot(meqfAllgsim, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(sc^(-3), sc^(-2), sc^(-1), sc^(0), sc^(1), sc^(2), sc^(3), sc^(4), sc^(5), sc^(6)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Equivolume Bolus Cumulative Equivalent \n Dose Normalized to Ac-225 + Daughters")+
  theme(text = element_text(size=18, face = "bold"))+
  guides(shape=guide_legend(override.aes = list(size=3)))+
  theme(legend.position = c(.97, .78),
      legend.justification = c("right", "top"),
      legend.box.just = "right",
      legend.margin = margin(6, 6, 6, 6),
      axis.text.y=element_text(colour="black"),
      axis.text.x=element_text(colour="black"))





#Now if you know counts per organ, can multiply by tissue weighting factor to get Biological Effective Dose
#And compartmental model IgG biodistribution for organ dosing


#Choose your tissue factor:

# Organ/Tissue Number of
# tissues


# Lung, stomach, colon,
# bone marrow, breast,
# remainder
# 0.12

# Gonads
#0.08

# Thyroid, oesophagus,
# bladder, liver
# 0.04

# Bone surface, skin, brain,
# salivary glands
# 0.01

WT = 0.1

eqtAllgsim = data.frame(cbind(gplotout[,1],gAc225*AF*WT,gAc225SUM*AF*WT,gLu177*WT))
#eqAllgsim = eqAllgsim[-1,] #remove first row
colnames(eqtAllgsim) = c("times", "Ac-225 0.2 ?Ci","Ac-225 0.2 ?Ci + Daughters","Lu-177 20 ?Ci")



meqtAllgsim <- melt(eqtAllgsim, id="times")
colnames(meqtAllgsim) <- c("times","Species","value")


sb=10
ggplot(meqtAllgsim, aes(x=times, y=value, by=Species))+
  geom_point(aes(color=Species, shape=Species), size=1.25, alpha=1, stroke = 1.25)+
  scale_shape_manual(values = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))+

  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(breaks=c(sb^(-4), sb^(-3), sb^(-2), sb^(-1), sb^(-0), sb^(1), sb^(2), sb^(3), sb^(4), sb^(5), sb^(6), sb^(7)))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "Bolus Tissue Weighted \n Equivalent Dose (Sv)")+
  theme(text = element_text(size=18, face = "bold"),
        axis.text.y=element_text(colour="black"),
        axis.text.x=element_text(colour="black"),
        legend.position = c(0.97, .02),
        legend.justification = c("right", "bottom"),
        legend.box.just = "right",
        legend.margin = margin(6, 6, 6, 6))+
  guides(shape=guide_legend(override.aes = list(size=3)))













#######################################################################################################
#PK analysis
#######################################################################################################

# ?Ci injected dose
injdose = 0.1


#in days
timepoints = c(1/24,6/24,24/24,72/24,144/24,288/24)

#Tissues ---> a=group; 1=tissue number, 1=replicate #
# fraction ID/g per tissue, per timepoint

#gamma
pkac225 = data.frame(cbind(timepoints,

a.1.1.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.1.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.1.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.1.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.1.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.2.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.2.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.2.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.2.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.2.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.3.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.3.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.3.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.3.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.3.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.4.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.4.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.4.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.4.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.4.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.5.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.5.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.5.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.5.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.5.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.6.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.6.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.6.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.6.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.6.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.7.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.7.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.7.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.7.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.7.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.8.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.8.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.8.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.8.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.8.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.9.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.9.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.9.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.9.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.9.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

a.1.10.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
a.1.10.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.10.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
a.1.10.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
a.1.10.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14)

))


#gamma
pkac227 = data.frame(cbind(timepoints,

b.1.1.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.1.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.1.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.1.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.1.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.2.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.2.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.2.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.2.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.2.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.3.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.3.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.3.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.3.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.3.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.4.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.4.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.4.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.4.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.4.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.5.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.5.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.5.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.5.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.5.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.6.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.6.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.6.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.6.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.6.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.7.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.7.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.7.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.7.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.7.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.8.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.8.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.8.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.8.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.8.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.9.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.9.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.9.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.9.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.9.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

b.1.10.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
b.1.10.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.10.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
b.1.10.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
b.1.10.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14)

))

#alpha/beta
pktotal = data.frame(cbind(timepoints,

t.1.1.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.1.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.1.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.1.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.1.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.2.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.2.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.2.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.2.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.2.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.3.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.3.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.3.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.3.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.3.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.4.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.4.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.4.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.4.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.4.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.5.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.5.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.5.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.5.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.5.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.6.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.6.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.6.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.6.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.6.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.7.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.7.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.7.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.7.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.7.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.8.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.8.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.8.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.8.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.8.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.9.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.9.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.9.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.9.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.9.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14),

t.1.10.1 = c(0.03, 0.06, 0.075, 0.16, 0.2, 0.17),
t.1.10.2 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.10.3 = c(0.03, 0.07, 0.07, 0.18, 0.22, 0.18),
t.1.10.4 = c(0.04, 0.05, 0.08, 0.15, 0.24, 0.18),
t.1.10.5 = c(0.04, 0.06, 0.07, 0.15, 0.19, 0.14)
))

#units are fraction injected dose / g * uCi total = uCi/g
pktotalinj = pktotal*injdose

#what fracton CPM from gamma comes from Ac-225 vs Ac-227?? 1 out of 5 for instance?

























#couldnt get close enough guess, whatever, just numerically integrate

#fitAc225 = data.frame(gdaughtersdata[,1],gdaughtersdata[,2])
#colnames(fitAc225) = c("times", "Ac225f")

#A1 = 200; lrc1 = 0.05; A2 = 1; lrc2 = 0.1
#SSbiexp(fitAc225$times, A1, lrc1, A2, lrc2)
#print(getInitial(Ac225f ~ SSbiexp(times, A1, lrc1, A2, lrc2)),
#      digits = 5)
#fitAc225nls = nls(Ac225f ~ SSbiexp(times, A1, lrc1, A2, lrc2), data = fitAc225)
#summary(fitAc225nls)



#plot(gdaughtersdata[,1], A1*exp(-lrc1*gdaughtersdata[,1]) + A2*exp(-lrc2*gdaughtersdata[,1]))
#par(new=TRUE)
#plot(fitAc225)





#convert these energies into realistic dosages

#Ac-225 penetration is 0.05 mm in water
#Alpha weighting factor WR = 20

#Lu-177 penetration is 1.6 mm in water
#Beta weighting factor WR = 1

#1 Gy = 1 joule/kg
#1 J = 6.242E18 eV
#1 J = 6.242E12 eV


#Distance travelled by alpha particle in matter mass 3D
##100 microns max radius, how about
##V=4/3*pi*100^3 = 4188790.204 micron^3 = 0.004188790204 #cm^3


#Where equivalent dose = sum (absorbed dose * weighting factor ) -> 1 Gy alpha = 20 Sv equivalent dose

#Tissue weighting factor WT = 0.05 for liver, 0.2 gonads

#and effective dose = sum (absorbed dose * weighting factor * tissue weighting factor)


#1) Energy per distance (consistant distance)
#2) Biological effectiveness per distance
#3)












#old style plot

#ggplot(medaughtersdata, aes(x=times, y=value, by=variable))+
#  geom_point(aes(color=variable), size = 1.25)+


#  scale_x_log10(breaks=c(0.0001, 0.001, 0.01, 0.1, 1, 10, 100))+
#  annotation_logticks(base = 10, sides = "b", scaled = TRUE,
#                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
#                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  #scale_y_continuous()+#breaks=c(0, 1000, 2000, 3000, 4000, 5000, 6000, 7000))+
 # scale_y_log10(breaks=c(10^(1), 10^(2), 10^(3), 10^(4), 10^(5), 10^(6), 10^(7)))+

#  labs(x = "Time (days)", y = "Energy (MeV)")+
#  theme(text = element_text(size=18))+
#  guides(color=guide_legend(title=""))


##












#
##
####
#######
###############
################################
###################################################################################################################################################
################################
###############
#######
####
##
#

#what if start out with actinium, do TLC plate, and now the daughters are separated? Start initial amounts @ time = 2/24, or 2 hours after blotting





#These values for 'state' are using 'out' from the above calcualtion, so need to run everything!
parameters = c(l1 = 0.002888113*24, l2 = 8.487516497*24, l3 = 77254.79412*24, l4 = 0.904105018*24, l5 = 594126154.8*24, l6 = 0.213276056*24, l7 = 3.64*10^-20*24, l8 = 4620981.204*24, l9 = 19.24517854*24)
state = c(A = 0, B = out[out$time==0.083,"Fr221"], C = out[out$time==0.083,"At217"], D = out[out$time==0.083,"Bi213"], E = out[out$time==0.083,"Po213"], f = out[out$time==0.083,"Pb209"], G = out[out$time==0.083,"Bi209"], H = out[out$time==0.083,"Rn217"], I = out[out$time==0.083,"Tl209"]) #these numbers are in nmoles
activity = c(k1 = 58, k2 = 180000, k3 = 1600000000, k4 = 20000, k5 = 1.3*10^13, k6 = 4700, k7 = 0, k8 = 96216216216, k9 = 410000)
masses = c(j1 = 225, j2 = 221, j3 = 217, j4 = 213, j5 = 213, j6 = 209, j7 = 209, j8 = 217, j9 = 209)
#initmassng = c(i1 = 1, i2 = 0,  i3 = 0,  i4 = 0,  i5 = 0,  i6 = 0,  i7 = 0)

#calculate nmoles of species
daughters = function(t, state, parameters, probabilities) {with(as.list(c(state, parameters, probabilities)),{
  dA = -l1*A
  dB = l1*ac2fr*A-l2*B
  dC = l2*fr2at*B-l3*C
  dH = l3*at2rn*C-l8*H
  dD = l3*at2bi*C-l4*D
  dI = l4*bi2tl*D-l9*I
  dE = l4*bi2po*D+l8*rn2po*H-l5*E
  df = l5*po2pb*E+l9*tl2pb*I-l6*f
  dG = l6*pb2bi*f-l7*G


  list(c(dA, dB, dC, dD, dE, df, dG, dH, dI))
})}

#timedays = 10
#timestep = 0.001
#timestepout = 1/timestep

#times = seq(0, timedays, by = timestep)
#timesout = seq(1, timedays*timestepout+1, by = 1)

#MODEL INTEGRATION

out = ode(y = state, times = times, func = daughters, parms = parameters, prob=probabilities)
#head(out)


#calculate activity produces over time
#daughtersactiv = function(t, activity, masses, out) {with(as.list(c(activity, masses, out)),{

Ac225 = masses[1]*activity[1]*out[timesout,2]*2200000/dpmac225
Fr221 = masses[2]*activity[2]*out[timesout,3]*2200000/dpmac225
At217 = masses[3]*activity[3]*out[timesout,4]*2200000/dpmac225
Bi213 = masses[4]*activity[4]*out[timesout,5]*2200000/dpmac225
Po213 = masses[5]*activity[5]*out[timesout,6]*2200000/dpmac225
Pb209 = masses[6]*activity[6]*out[timesout,7]*2200000/dpmac225
Bi209 = masses[7]*activity[7]*out[timesout,8]*2200000/dpmac225
Rn217 = masses[8]*activity[8]*out[timesout,9]*2200000/dpmac225
Tl209 = masses[9]*activity[9]*out[timesout,10]*2200000/dpmac225
SUM = (Ac225+Fr221+At217+Bi213+Po213+Pb209+Bi209+Rn217+Tl209)
#SUMoverac225 = SUM/Ac225

daughtersdata = data.frame(times)
daughtersdata = cbind(daughtersdata, Ac225, Fr221, At217, Bi213, Po213, Pb209, Bi209, Rn217, Tl209, SUM)#, SUMoverac225)
#colnames(daughtersdata)[12] = "SUM / Ac225"

#melt this first
mdaughtersdata = melt(daughtersdata, id="times")


plotout <- daughtersdata[plotrows, ]
mplotout <- melt(plotout, id="times")





#plot the indivudual activities produced

ggplot(mplotout, aes(x=times, y=value, by=variable))+
  geom_point(aes(color=variable), size=1.25)+
  scale_x_log10(breaks=c(0.001, 0.01, 0.1, 1, 10, 100))+
  annotation_logticks(base = 10, sides = "bl", scaled = TRUE,
                      short = unit(0.1, "cm"), mid = unit(0.2, "cm"), long = unit(0.3, "cm"),
                      colour = "black", size = 0.5, linetype = 1, alpha = 1, color = NULL)+

  scale_y_log10(labels = scales::percent, breaks=c(10^(-4):1 %o% 10^(1:4)), limits = c(2*10^(-4),1))+

  theme_bw() +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+

  labs(x = "Time (days)", y = "% Activity(t) / Ac225(2 hr), w/o Ac225 Present")+
  theme(text = element_text(size=18, face = "bold"))+

  # theme(legend.position = c(.95, .95),
  #   legend.justification = c("right", "top"),
  #   legend.box.just = "right",
  #   legend.margin = margin(6, 6, 6, 6))+



  guides(color=guide_legend(title="Species"))
