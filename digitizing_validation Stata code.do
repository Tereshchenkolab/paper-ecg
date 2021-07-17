***Analysis of the validation dataset for paper-ecg digitizing manuscript
***by Larisa Tereshchenko <tereshch@ohsu.edu>
***June-July 2021
***use STATA 17.0

concord peakQRSTAngle_10s peakQRSTAngle_1b, sum
egen pQRSTa10s_1b = rowmean ( peakQRSTAngle_10s peakQRSTAngle_1b)
di  100-(6.449/pQRSTa10s_1b)*100
alpha peakQRSTAngle_10s peakQRSTAngle_1b, std

concord peakQRSTAngle_scan peakQRSTAngle_1b, sum
egen pQRSTascan_1b = rowmean ( peakQRSTAngle_scan peakQRSTAngle_1b)
di  100-(7.040/ pQRSTascan_1b)*100
alpha peakQRSTAngle_scan peakQRSTAngle_1b, std

concord areaQRSTAngle_10s areaQRSTAngle_1b , sum
egen aQRSTa10s_1b = rowmean ( areaQRSTAngle_10s areaQRSTAngle_1b )
di  100-(1.420/ aQRSTa10s_1b)*100
alpha areaQRSTAngle_10s areaQRSTAngle_1b, std

concord areaQRSTAngle_scan areaQRSTAngle_1b , sum
egen aQRSTascan_1b = rowmean ( areaQRSTAngle_scan areaQRSTAngle_1b )
di  100-(2.818/ aQRSTascan_1b)*100
alpha areaQRSTAngle_scan areaQRSTAngle_1b, std

concord peakQRSTAngle_scan peakQRSTAngle_10s, sum
egen pQRSTa10s_scan = rowmean ( peakQRSTAngle_scan peakQRSTAngle_10s )
di  100-(0.591/ pQRSTa10s_scan )*100
alpha peakQRSTAngle_scan peakQRSTAngle_10s, std

concord areaQRSTAngle_scan areaQRSTAngle_10s, sum
egen aQRSTa10s_scan = rowmean (  areaQRSTAngle_scan areaQRSTAngle_10s)
di  100-(1.398 / aQRSTa10s_scan )*100
alpha areaQRSTAngle_scan areaQRSTAngle_10s, std

concord peakSVGElevation_10s peakSVGElevation_1b , sum
egen pSVGel10s_1b = rowmean ( peakSVGElevation_10s peakSVGElevation_1b  )
di  100-( 3.464/ pSVGel10s_1b)*100
alpha peakSVGElevation_10s peakSVGElevation_1b , std

concord peakSVGElevation_scan peakSVGElevation_1b , sum
egen pSVGelscan_1b = rowmean ( peakSVGElevation_scan peakSVGElevation_1b  )
di  100-( 1.494/pSVGelscan_1b)*100
alpha peakSVGElevation_scan peakSVGElevation_1b , std

concord peakSVGElevation_scan peakSVGElevation_10s , sum
egen pSVGelscan_10s = rowmean ( peakSVGElevation_scan peakSVGElevation_10s  )
di  100-( 1.970/pSVGelscan_10s)*100
alpha peakSVGElevation_scan peakSVGElevation_10s , std

concord areaSVGElevation_10s areaSVGElevation_1b , sum
egen aSVGel10s_1b = rowmean (areaSVGElevation_10s areaSVGElevation_1b  )
di  100-( 14.464/aSVGel10s_1b)*100
alpha areaSVGElevation_10s areaSVGElevation_1b , std

concord areaSVGElevation_scan areaSVGElevation_1b , sum
egen aSVGelscan_1b = rowmean (areaSVGElevation_scan areaSVGElevation_1b  )
di  100-(2.530  /aSVGelscan_1b)*100
alpha areaSVGElevation_scan areaSVGElevation_1b , std

concord areaSVGElevation_scan areaSVGElevation_10s , sum
egen aSVGelscan_10s = rowmean (areaSVGElevation_scan areaSVGElevation_10s)
di  100-(11.934/aSVGelscan_10s)*100
alpha areaSVGElevation_scan areaSVGElevation_10s , std

concord PRinterval_10s PRinterval_1b , sum
egen PR10s_1b = rowmean (PRinterval_10s PRinterval_1b )
di  100-(16.350 /PR10s_1b )*100
alpha PRinterval_10s PRinterval_1b, std

concord PRinterval_scan PRinterval_1b , sum
egen PRscan_1b = rowmean (PRinterval_scan PRinterval_1b )
di  100-(3.373 /PRscan_1b )*100
alpha PRinterval_scan PRinterval_1b, std

concord PRinterval_scan PRinterval_10s , sum
egen PRscan_10s = rowmean (PRinterval_scan PRinterval_10s )
di  100-(19.723/PRscan_10s )*100
alpha PRinterval_scan PRinterval_10s, std

concord QRSduration_10s QRSduration_1b , sum
egen QRS10s_1b = rowmean (QRSduration_10s QRSduration_1b )
di  100-(8.9/QRS10s_1b)*100
alpha QRSduration_10s QRSduration_1b , std

concord QRSduration_scan QRSduration_1b , sum
egen QRSscan_1b = rowmean (QRSduration_scan QRSduration_1b )
di  100-(2.633/QRSscan_1b)*100
alpha QRSduration_scan QRSduration_1b, std

concord QRSduration_scan QRSduration_10s , sum
egen QRSscan_10s = rowmean (QRSduration_scan QRSduration_10s )
di  100-(6.267/QRSscan_10s)*100
alpha QRSduration_scan QRSduration_10s, std

concord QTInterval_10s QTInterval_1b , sum
egen QT10s_1b = rowmean (QTInterval_10s QTInterval_1b)
di  100-(18/QT10s_1b)*100
alpha QTInterval_10s QTInterval_1b , std

concord QTInterval_scan QTInterval_1b , sum
egen QTscan_1b = rowmean (QTInterval_scan QTInterval_1b)
di  100-(3.726/QTscan_1b)*100
alpha QTInterval_scan QTInterval_1b , std

concord QTInterval_scan QTInterval_10s , sum
egen QTscan_10s = rowmean (QTInterval_scan QTInterval_10s)
di  100-( 21.726/QTscan_10s)*100
alpha QTInterval_scan QTInterval_10s , std

replace SAIQRST_1b = SAIQRST_1b/1000
replace SAIQRST_10s = SAIQRST_10s/1000
replace SAIQRST_scan = SAIQRST_scan/1000

concord SAIQRST_10s SAIQRST_1b , sum
egen SAI10s_1b = rowmean ( SAIQRST_10s SAIQRST_1b )
di  100-( 8.406/SAI10s_1b)*100
alpha SAIQRST_10s SAIQRST_1b , std

concord SAIQRST_scan SAIQRST_1b , sum
egen SAIscan_1b = rowmean ( SAIQRST_scan SAIQRST_1b )
di  100-( 12.264/SAIscan_1b)*100
alpha SAIQRST_scan SAIQRST_1b , std

concord SAIQRST_scan SAIQRST_10s , sum
egen SAIscan_10s = rowmean ( SAIQRST_scan SAIQRST_10s )
di  100-( 3.859/SAIscan_10s)*100
alpha SAIQRST_scan SAIQRST_10s , std

replace AUCofQTVM_1b = AUCofQTVM_1b/1000
replace AUCofQTVM_10s =AUCofQTVM_10s/1000
replace AUCofQTVM_scan = AUCofQTVM_scan/1000

concord AUCofQTVM_10s AUCofQTVM_1b , sum
egen VMQTi10s_1b = rowmean ( AUCofQTVM_10s AUCofQTVM_1b )
di  100-( 5.538/VMQTi10s_1b)*100
alpha  AUCofQTVM_10s AUCofQTVM_1b  , std

concord AUCofQTVM_scan AUCofQTVM_1b , sum
egen VMQTiscan_1b = rowmean ( AUCofQTVM_scan AUCofQTVM_1b )
di  100-( 6.398/VMQTiscan_1b)*100
alpha  AUCofQTVM_scan AUCofQTVM_1b  , std

concord AUCofQTVM_scan AUCofQTVM_10s , sum
egen VMQTiscan_10s = rowmean ( AUCofQTVM_scan AUCofQTVM_10s )
di  100-( 0.86/VMQTiscan_10s)*100
alpha  AUCofQTVM_scan AUCofQTVM_10s  , std

replace peakSVGMagnitude_10s = peakSVGMagnitude_10s/1000
replace peakSVGMagnitude_1b = peakSVGMagnitude_1b/1000
replace peakSVGMagnitude_scan = peakSVGMagnitude_scan/1000

concord peakSVGMagnitude_10s peakSVGMagnitude_1b , sum
egen pSVGmag10s_1b = rowmean ( peakSVGMagnitude_10s peakSVGMagnitude_1b )
di  100-(  0.042/ pSVGmag10s_1b)*100
alpha  peakSVGMagnitude_10s peakSVGMagnitude_1b, std

concord peakSVGMagnitude_scan peakSVGMagnitude_1b , sum
egen pSVGmagscan_1b = rowmean ( peakSVGMagnitude_scan peakSVGMagnitude_1b )
di  100-(  0.307/ pSVGmagscan_1b)*100
alpha  peakSVGMagnitude_scan peakSVGMagnitude_1b, std

concord peakSVGMagnitude_scan peakSVGMagnitude_10s, sum
egen pSVGmagscan_10s = rowmean ( peakSVGMagnitude_scan peakSVGMagnitude_10s )
di  100-(  0.349/ pSVGmagscan_10s)*100
alpha  peakSVGMagnitude_scan peakSVGMagnitude_10s, std

replace WilsonSVG_10s = WilsonSVG_10s/1000
replace WilsonSVG_1b = WilsonSVG_1b/1000
replace WilsonSVG_scan = WilsonSVG_scan/1000

concord WilsonSVG_10s WilsonSVG_1b , sum
egen SVGmag10s_1b = rowmean ( WilsonSVG_10s WilsonSVG_1b )
di  100-( 1.392/ SVGmag10s_1b)*100
alpha  WilsonSVG_10s WilsonSVG_1b    , std

concord WilsonSVG_scan WilsonSVG_1b , sum
egen SVGmagscan_1b = rowmean ( WilsonSVG_scan WilsonSVG_1b )
di  100-(  0.275/ SVGmagscan_1b)*100
alpha   WilsonSVG_scan WilsonSVG_1b, std

concord WilsonSVG_scan WilsonSVG_10s , sum
egen SVGmagscan_10s = rowmean ( WilsonSVG_scan WilsonSVG_10s )
di  100-( 1.667/ SVGmagscan_10s)*100
alpha   WilsonSVG_scan WilsonSVG_10s, std

circcomp peakSVGAzimuth_10s peakSVGAzimuth_1b peakSVGAzimuth_scan , det
concord peakSVGAzimuth_10s peakSVGAzimuth_1b  , sum
alpha   peakSVGAzimuth_10s peakSVGAzimuth_1b, std
***to calculate relative bias, azimuth must be transformed (*2+360)
gen trpSVGaz10s = ( peakSVGAzimuth_10s*2)+360
gen trpSVGaz1b = ( peakSVGAzimuth_1b*2)+360
gen trpSVGazscan = ( peakSVGAzimuth_scan*2)+360
gen traSVGaz10s = ( areaSVGAzimuth_10s*2)+360
gen traSVGaz1b = ( areaSVGAzimuth_1b*2)+360
gen traSVGazscan = ( areaSVGAzimuth_scan*2)+360

circcomp areaSVGAzimuth_10s areaSVGAzimuth_1b areaSVGAzimuth_scan , det
concord peakSVGAzimuth_scan peakSVGAzimuth_1b  , sum
alpha   peakSVGAzimuth_scan peakSVGAzimuth_1b, std
concord peakSVGAzimuth_scan peakSVGAzimuth_10s  , sum
alpha   peakSVGAzimuth_scan peakSVGAzimuth_10s, std
concord areaSVGAzimuth_10s areaSVGAzimuth_1b  , sum
alpha areaSVGAzimuth_10s areaSVGAzimuth_1b  , std
concord areaSVGAzimuth_scan areaSVGAzimuth_1b  , sum
alpha areaSVGAzimuth_scan areaSVGAzimuth_1b  , std
concord areaSVGAzimuth_scan areaSVGAzimuth_10s, sum
alpha areaSVGAzimuth_scan areaSVGAzimuth_10s  , std
concord trpSVGaz10s trpSVGaz1b , sum
egen trpSVGaz10s_1b = rowmean ( trpSVGaz10s trpSVGaz1b  )
di  100-(38.744/ trpSVGaz10s_1b )*100
concord trpSVGazscan trpSVGaz1b , sum
egen trpSVGazscan_1b = rowmean ( trpSVGazscan trpSVGaz1b  )
di  100-( 4.645/ trpSVGazscan_1b )*100
concord trpSVGazscan trpSVGaz10s , sum
egen trpSVGazscan_10s = rowmean ( trpSVGazscan trpSVGaz10s  )
di  100-(34.099/ trpSVGazscan_10s )*100
concord traSVGaz10s traSVGaz1b , sum
egen traSVGaz10s_1b = rowmean ( traSVGaz10s traSVGaz1b  )
di  100-(7.230/ traSVGaz10s_1b )*100
concord traSVGazscan traSVGaz1b , sum
egen traSVGazscan_1b = rowmean ( traSVGazscan traSVGaz1b  )
di  100-(1.560/ traSVGazscan_1b )*100
concord traSVGazscan traSVGaz10s , sum
egen traSVGazscan_10s = rowmean ( traSVGazscan traSVGaz10s  )
di  100-(8.791/ traSVGazscan_10s )*100

gen QTc_10s = QTInterval_10s*1000/sqrt( RRinterval_10s*1000)
gen QTc_scan = QTInterval_scan*1000/sqrt( RRinterval_scan*1000)
gen QTc_1b = QTInterval_1b*1000/sqrt( RRinterval_1b*1000)

gen HR_10s = 60000/RRinterval_10s
gen HR_1b = 60000/RRinterval_1b
gen HR_scan = 60000/RRinterval_scan

concord HR_10s HR_1b, sum
egen HR10s_1b = rowmean ( HR_10s HR_1b  )
di  100-(12.709/ HR10s_1b )*100
alpha HR_10s HR_1b , std
concord HR_scan HR_1b, sum
egen HRscan_1b = rowmean ( HR_scan HR_1b  )
di  100-(0.777/ HRscan_1b )*100
alpha HR_scan HR_1b , std
concord HR_scan HR_10s, sum
egen HRscan_10s = rowmean ( HR_scan HR_10s  )
di  100-(11.932/ HRscan_10s )*100
alpha HR_scan HR_10s , std

concord QTc_10s QTc_1b , sum
egen QTc10s_1b = rowmean ( QTc_10s QTc_1b )
di  100-(54.280/ QTc10s_1b )*100
alpha QTc_10s QTc_1b  , std
concord QTc_scan QTc_1b , sum
egen QTcscan_1b = rowmean ( QTc_scan QTc_1b )
di  100-(1.975/ QTcscan_1b )*100
alpha QTc_scan QTc_1b  , std
concord QTc_scan QTc_10s , sum
egen QTcscan_10s = rowmean ( QTc_scan QTc_10s )
di  100-( 56.255  / QTcscan_10s )*100
alpha QTc_scan QTc_10s  , std

