# WIZ-CLI
![windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![maintaining](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/{infinityInfinite }/{philips-wiz-cli}.svg)

## control your wiz light in your PC !!!
**wiz light can only be controlled with wiz mobile app , this cli tools gives you access for your wiz light in pc !!**

## INSTALLATION
+ clone the repo
`git clone https://github.com/infinityInfinite/philips-wiz-cli.git`
+ install the requirements file
`pip3 install -r requirements.txt`

## USAGE
+ `python3 wizcli.py --help`

## EXAMPLES
+ **default port is already set to 38899**
+ `python3 wizcli.py [IP ADDRESS] [PORT] --turnoff` 
+ `python3 wizcli.py [IP ADDRESS] [PORT] --turnon`
+ `python3 wizcli.py [IP ADDRESS] [PORT] --changecolor`
+ `python3 wizcli.py [IP ADDRESS] [PORT] --setscene`


### OPTIONS
+ changecolor
+ turnoff
+ turnon
+ setscene
+ dimming
### *more options comming soon*

#### get ip address of your wiz light from your wiz mobile app !!


![made with python](http://ForTheBadge.com/images/badges/made-with-python.svg)
![made with love](http://ForTheBadge.com/images/badges/built-with-love.svg)
![made by infinityInfinite](https://img.shields.io/badge/Made%20By-infinityInfinite-red)
