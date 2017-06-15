# Boring Tetris
Tetris made with pygame
원본
# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

![](http://postfiles14.naver.net/MjAxNzA2MTFfMTEy/MDAxNDk3MTc0ODY4MzM3.EBXP_7YmC6960HLE69e75aIqG9RfuupGpvBtteBOsmog.nPiIGDex5dCrteibrL8LBaRISwnO-Mct4MBpXSaRGqAg.GIF.chbkk123/playthrough1.gif?type=w3)
![](http://postfiles2.naver.net/MjAxNzA2MTFfNTAg/MDAxNDk3MTc0ODY5MDUz.P_HTHtvUOJOkphxrM9KZqrLLSHCz7Twk0_ZucAkoaZAg.KyTNzbO2jBCOwRuciUAIaZcaXrGf4qsxuQ1mXvQXBWMg.GIF.chbkk123/playthrough3.gif?type=w3)

[실행 영상](https://youtu.be/ZzF_0WL0gog)


## 게임 진행
### 조작법

| 명령  | 버튼 |
| :------------ | -----------: |
| 좌로 이동 | ← |
| 우로 이동 | → |
| 회전 | ↑ |
| 빠르게 추락 | ↓ |
| 완전히 떨어뜨리기 | Space |
| 일시정지 | P |
| 게임 종료 | ESC |

자세한 내용은 [이곳](https://github.com/chbkk123/Project-2/wiki/How-to-Play)




## 동작
* [시작 화면](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EC%8B%9C%EC%9E%91-%ED%99%94%EB%A9%B4)
* [블럭 무작위 생성](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EB%B8%94%EB%9F%AD-%EB%AC%B4%EC%9E%91%EC%9C%84-%EC%83%9D%EC%84%B1)
* [화면](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%ED%99%94%EB%A9%B4)
* [레벨](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EB%A0%88%EB%B2%A8-1)
* [블럭 이동/회전 제한](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EB%B8%94%EB%9F%AD-%EC%9D%B4%EB%8F%99%ED%9A%8C%EC%A0%84-%EC%A0%9C%ED%95%9C)
* [블럭 저장(홀드)](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EB%B8%94%EB%9F%AD-%EC%A0%80%EC%9E%A5%ED%99%80%EB%93%9C)
* [일시 정지](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EC%9D%BC%EC%8B%9C-%EC%A0%95%EC%A7%80)
* [꼭대기에 도달하면 게임 오버](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EA%BC%AD%EB%8C%80%EA%B8%B0%EC%97%90-%EB%8F%84%EB%8B%AC%ED%95%98%EB%A9%B4-%EA%B2%8C%EC%9E%84-%EC%98%A4%EB%B2%84)
* [배경음악 / 효과음](https://github.com/chbkk123/Project-2/wiki/Sucessed-works#%EB%B0%B0%EA%B2%BD%EC%9D%8C%EC%95%85--%ED%9A%A8%EA%B3%BC%EC%9D%8C)

## 동작하지 않는 것
 저장한 블럭이 없는 상태로 처음 블럭을 저장할때 무작위하게 오류가 발생해 게임이 중단됩니다. 오류 발생 코드를 되짚어가니 처음 블럭을 저장할때 fallingPiece를 savedPiece에 저장하고 fallingPiece를 None으로 만드는데, 그 후 프로그램이 fallingPiece의 현재 위치를 읽는 코드를 먼저 실행하면 오류가 발생해 게임이 중단되는데, fallingPiece가 None이여서 다음 Piece를 가져오는 코드가 먼저 실행된다면 오류가 발생하지 않습니다. 이 부분을 어떻게 수정해야 할지 몰라서 수정하지 못했습니다.

## 추가하고 싶은 것
* [T 스핀](https://github.com/chbkk123/Project-2/wiki/Plans#t-%EC%8A%A4%ED%95%80)
* [하이스코어](https://github.com/chbkk123/Project-2/wiki/Plans#%ED%95%98%EC%9D%B4%EC%8A%A4%EC%BD%94%EC%96%B4)
* [레벨에 따른 배경음 전환](https://github.com/chbkk123/Project-2/wiki/Plans#%EB%A0%88%EB%B2%A8%EC%97%90-%EB%94%B0%EB%A5%B8-%EB%B0%B0%EA%B2%BD%EC%9D%8C-%EC%A0%84%ED%99%98)

## 스크린샷
 
 ![](http://postfiles4.naver.net/MjAxNzA2MTFfMTE1/MDAxNDk3MTc0ODY3Njc1.kUbMOmOBRqvy5z0cH5RkZ_E64b-8ixCzDGzWU_hjLV4g.v3qhSIFetOdhumEJ_eGDICmoezgF7XNuYRDDE7xDLYEg.PNG.chbkk123/%EC%BA%A1%EC%B2%983.PNG?type=w3)
 ![](http://postfiles2.naver.net/MjAxNzA2MTFfMjYx/MDAxNDk3MTc0ODY3NDM1.GOrFccTGAEG_AWRxLY6IbK1JrhM6OS0ZrPDc6ZteymUg.PWN8Act0MouTOvwSO2Mky1EMSqkkf6VeHoMa5oXE1-8g.PNG.chbkk123/%EC%BA%A1%EC%B2%982.PNG?type=w3)


 자세한 정보는 [Boring Tetris Wiki](https://github.com/chbkk123/Project-2/wiki)에