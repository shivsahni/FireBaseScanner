# FireBase Scanner
Firebase is one of the widely used data stores for mobile applications. In 2018, Appthority Mobile Threat Team (MTT) discovered a misconfiguration in Firebase instance also called HospitalGown vulnerability. The following are some of the key highlights taken from the [ research paper](https://cdn2.hubspot.net/hubfs/436053/Appthority%20Q2-2018%20MTR%20Unsecured%20Firebase%20Databases.pdf) published by Appthority Mobile Threat Team (MTT):

* The research was performed on total of 2,705,987 apps and 27,227 Android apps and 1,275 iOS apps were found to be connected to a Firebase database. Of those connected apps, it was observed that: 
* 1 In 11 Android apps (9%) and almost half of iOS apps (47%) that connect to a Firebase database were vulnerable
* More than 3,000 apps were leaking data from 2,300 unsecured servers. Of these, 975 apps were in active customer environments.
* 1 in 10 Firebase databases (10.34%) are vulnerable
* Vulnerable Android apps alone were downloaded over 620 million times
* Over 100 million records (113 gigabytes) of data was exposed

## Getting Started

### Prerequisites
* Support for Python 2.7

### Installing

Say what the step will be

```
git clone https://github.com/shivsahni/FireBaseScanner.git
```
Once the script is downloaded, run the script with the required arguments. We can either provide the APK file as an input as shown below:
```
python FirebaseMisconfig.py --path /home/shiv/TestAPK/test.apk
or
python FirebaseMisconfig.py -p /home/shiv/TestAPK/test.apk
```
Or we can provide the comma sperated firebase project names as shown below:
```
python FirebaseMisconfig.py --firebase project1,project2,project3
or
python FirebaseMisconfig.py -f project1,project2,project3
```

## Authors

* **Shiv Sahni** - [LinkedIn](https://www.linkedin.com/in/shivsahni/)
