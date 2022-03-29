# Polygon Zone(다각형 영역) for HA

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version][version-shield]

Polygon Zone for Home Assistant 입니다.<br>
HA의 device_tracker 정보를 기준으로 다각형(Polygon) 영역(Zone)의 안/밖을 상태로 나타냅니다.<br>
현재는 HA에서 원으로만 영역을 지정할 수 있는 것을 보완을 목적으로 합니다.<br>
위도, 경도를 한쌍으로 해서 포인터를 구성하고, 여러개의 포인터로 영역을 설정합니다.<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2022.03.30  | First version  |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components에 polygon_zone폴더 안의 전체 파일을 복사해줍니다.<br>
  `<config directory>/custom_components/polygon_zone/`<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/miumida/polygon_zone' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, Polygon Zone 검색하여 설치

<br>

## Usage
### Custom Integration
- 구성 > 통합구성요소 > 통합구성요소 추가하기 > Polygon Zone > 정보 입력후, 확인.
<br>

### 기본 설정값

|옵션|내용|
|--|--|
|zone_name| (필수) 다각형 영역 이름 |
|zone_path| (필수) 다각형 영역 Path / (위도, 경도)를 한쌍으로 3개 이상으로 구성 |
|zone_type| (필수) 다각형 영역 타입 |
|tracker| (필수) HA 내 device_tracker |

<br>

### zone_path 설정값
다각형 영역을 구성하기 위한 (위도, 경도)의 집합.<br>
위도1, 경도1, 위도2, 경도2, 위도3, 경도3, ... 형태로 입력하면 됩니다.<br>
구글지도(<https://www.google.co.kr/maps/?hl=ko>)로 가서, 영역을 구성하기 원하는 좌표들을 복사합니다.<br>

<br>

## 참고사이트
[1] community.home-assistant.io | Zones that are not circles (<https://community.home-assistant.io/t/zones-that-are-not-circles/175914/24>)<br>

[version-shield]: https://img.shields.io/badge/version-v1.0.0-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
