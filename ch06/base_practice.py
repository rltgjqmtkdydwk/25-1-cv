import os
import sys
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                          QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout,
                          QWidget)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class VisionAgentGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("비전 에이전트")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # 공통 UI 요소
        self.label = QLabel("Welcome!", self)
        self.layout.addWidget(self.label)

        self.initial_button_layout = QHBoxLayout()  # 초기 버튼 레이아웃
        self.layout.addLayout(self.initial_button_layout)

        self.function_button_layout = QHBoxLayout()  # 기능별 버튼 레이아웃
        self.layout.addLayout(self.function_button_layout)  # 메인 레이아웃에 추가

        self.create_buttons()

        self.show()

    def create_buttons(self):
        # 기능 선택 버튼
        self.orim_button = QPushButton("오림", self)
        self.traffic_button = QPushButton("교통약자 보호구역 알림", self)
        self.panorama_button = QPushButton("파노라마", self)
        self.effect_button = QPushButton("특수 효과", self)
        self.quit_button = QPushButton("종료", self)

        self.initial_button_layout.addWidget(self.orim_button)
        self.initial_button_layout.addWidget(self.traffic_button)
        self.initial_button_layout.addWidget(self.panorama_button)
        self.initial_button_layout.addWidget(self.effect_button)
        self.initial_button_layout.addWidget(self.quit_button)

        # 버튼 연결
        self.orim_button.clicked.connect(self.orim_function)
        self.traffic_button.clicked.connect(self.traffic_function)
        self.panorama_button.clicked.connect(self.panorama_function)
        self.effect_button.clicked.connect(self.effect_function)
        self.quit_button.clicked.connect(self.quit_program)

    def clear_function_button_layout(self):
        """기능별 버튼 레이아웃을 지웁니다."""
        while self.function_button_layout.count():
            item = self.function_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # --- 오림 기능 ---
    def orim_function(self):
        self.label.setText("오림 기능 선택됨")
        self.clear_function_button_layout()  # 기능별 버튼 지우기
        self.orim_ui()

    def orim_ui(self):
        # 함수 범위 내에 버튼 생성
        self.file_button = QPushButton("파일", self)
        self.paint_button = QPushButton("페인트", self)
        self.cut_button = QPushButton("자르기", self)
        self.inc_button = QPushButton("+", self)
        self.dec_button = QPushButton("-", self)
        self.save_button = QPushButton("저장", self)

        self.function_button_layout.addWidget(self.file_button)
        self.function_button_layout.addWidget(self.paint_button)
        self.function_button_layout.addWidget(self.cut_button)
        self.function_button_layout.addWidget(self.inc_button)
        self.function_button_layout.addWidget(self.dec_button)
        self.function_button_layout.addWidget(self.save_button)

        # 버튼 연결
        self.file_button.clicked.connect(self.file_open_function)
        self.paint_button.clicked.connect(self.paint_function)
        self.cut_button.clicked.connect(self.cut_function)
        self.inc_button.clicked.connect(self.inc_function)
        self.dec_button.clicked.connect(self.dec_function)
        self.save_button.clicked.connect(self.save_function)

        self.BrushSiz = 5
        self.LColor, self.RColor = (255,0,0), (0,0,255)

    def file_open_function(self):
        fname = QFileDialog.getOpenFileName(self, '사진 읽기', './')
        self.img = cv.imread(fname[0])
        if self.img is None: sys.exit("파일을 찾을 수 없습니다.")
        
        self.img_show=np.copy(self.img) # 표시용 영상
        cv.imshow('Painting', self.img_show)

        self.mask = np.zeros((self.img.shape[0], self.img.shape[1]), np.uint8)
        self.mask[:,:] = cv.GC_PR_BGD # 모든 화소를 배경으로 초기화

    def paint_function(self):
        cv.setMouseCallback('Painting', self.painting)

    def painting(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            cv.circle(self.img_show, (x, y), self.BrushSiz, self.LColor, -1)
            cv.circle(self.mask, (x, y), self.BrushSiz, cv.GC_FGD, -1)

        elif event == cv.EVENT_RBUTTONDOWN:
            cv.circle(self.img_show, (x, y), self.BrushSiz, self.RColor, -1)
            cv.circle(self.mask, (x, y), self.BrushSiz, cv.GC_BGD, -1)

        elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
            cv.circle(self.img_show, (x, y), self.BrushSiz, self.LColor, -1)
            cv.circle(self.mask, (x, y), self.BrushSiz, cv.GC_FGD, -1)

        elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
            cv.circle(self.img_show, (x, y), self.BrushSiz, self.RColor, -1)
            cv.circle(self.mask, (x, y), self.BrushSiz, cv.GC_BGD, -1)

        cv.imshow('Painting', self.img_show)

    def cut_function(self):
        background = np.zeros((1, 65), np.float64)
        foreground = np.zeros((1, 65), np.float64)

        cv.grabCut(self.img, self.mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype('uint8')
        self.grabImg = self.img * mask2[:, :, np.newaxis]

        cv.imshow('Scissoring', self.grabImg)

    def inc_function(self):
        self.BrushSiz = min(20, self.BrushSiz + 1)

    def dec_function(self):
        self.BrushSiz = max(1, self.BrushSiz - 1)

    def save_function(self):
        fname = QFileDialog.getSaveFileName(self, '파일 저장', './')
        cv.imwrite(fname[0], self.grabImg)

    # --- 교통약자 보호구역 알림 기능 ---
    def traffic_function(self):
        self.label.setText("교통약자 보호구역 알림 기능 선택됨")
        self.clear_function_button_layout()  # 기능별 버튼 지우기
        self.traffic_ui()

    def traffic_ui(self):
        # 함수 범위 내에 버튼 생성
        self.sign_button = QPushButton("표지판", self)
        self.road_button = QPushButton("도로", self)
        self.recognition_button = QPushButton("인식", self)

        self.function_button_layout.addWidget(self.sign_button)
        self.function_button_layout.addWidget(self.road_button)
        self.function_button_layout.addWidget(self.recognition_button)

        # 버튼 연결
        self.sign_button.clicked.connect(self.sign_function)
        self.road_button.clicked.connect(self.road_function)
        self.recognition_button.clicked.connect(self.recognition_function)

        self.signFiles=[['img/child.png', '어린이'],['img/elder.png', '노인'],['img/disabled.png','장애인']]
        self.signImgs=[]

    # 소리
    def play_warning_sound():
        os.system("afplay/System/Library/Sounds/Funk.aiff")

    def sign_function(self):
        self.label.clear()
        self.label.setText('교통약자 표지판을 등록합니다.')

        for fname,_ in self.signFiles:
            self.signImgs.append(cv.imread(fname))
            cv.imshow(fname, self.signImgs[-1])

    def road_function(self):
        if self.signImgs == []:
            self.label.setText("먼저 표지판을 등록하세요.")
        else:
            fname = QFileDialog.getOpenFileName(self, '파일 읽기', './')
            self.roadImg = cv.imread(fname[0])
            if self.roadImg is None:
                sys.exit("파일을 찾을 수 없습니다.")
            cv.imshow('Road scene', self.roadImg)

    def recognition_function(self):
        if self.roadImg is None:
            self.label.setText("먼저 도로 영상을 입력하세요.")
        else:
            sift = cv.SIFT_create()
            KD = []

            for img in self.signImgs:
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                KD.append(sift.detectAndCompute(gray, None))
                kp, des = sift.detectAndCompute(gray, None)

            grayRoad = cv.cvtColor(self.roadImg, cv.COLOR_BGR2GRAY)
            road_kp, road_des = sift.detectAndCompute(grayRoad, None)

            matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
            GM = []

            for sign_kp, sign_des in KD:
                knn_match = matcher.knnMatch(sign_des, road_des, 2)

                T = 0.7
                good_match = []
                for nearest1, nearest2 in knn_match:
                    if nearest1.distance / nearest2.distance < T:
                        good_match.append(nearest1)

                GM.append(good_match)

            if GM:  # 매칭 결과가 있는 경우에만 진행
                best_index = GM.index(max(GM, key=len))
                match_count = len(GM[best_index])

                if match_count > 10:
                    self.label.setText("표지판이 감지되었습니다.")
                    # play_warning_sound()
                else:
                    self.label.setText("표지판이 감지되지 않았습니다.")
            else:
                self.label.setText("표지판이 감지되지 않았습니다.")

            best = GM.index(max(GM, key=len))


    # --- 파노라마 기능 ---
    def panorama_function(self):
        self.label.setText("파노라마 기능 선택됨")
        self.clear_function_button_layout()  # 기능별 버튼 지우기
        self.panorama_ui()

    def panorama_ui(self):
        # 함수 범위 내에 버튼 생성
        self.load_video_button = QPushButton("비디오 로드", self)
        self.collect_from_video_button = QPushButton("프레임 수집", self)
        self.show_button = QPushButton("프레임 보기", self)
        self.stitch_button = QPushButton("스티칭", self)
        self.save_pano_button = QPushButton("저장", self)

        self.function_button_layout.addWidget(self.load_video_button)
        self.function_button_layout.addWidget(self.collect_from_video_button)
        self.function_button_layout.addWidget(self.show_button)
        self.function_button_layout.addWidget(self.stitch_button)
        self.function_button_layout.addWidget(self.save_pano_button)

        # 버튼 연결
        self.load_video_button.clicked.connect(self.load_video_function)
        self.collect_from_video_button.clicked.connect(self.collect_from_video)
        self.show_button.clicked.connect(self.show_function)
        self.stitch_button.clicked.connect(self.stitch_function)
        self.save_pano_button.clicked.connect(self.save_panorama_function)

        self.collect_from_video_button.setEnabled(False)
        self.show_button.setEnabled(False)
        self.stitch_button.setEnabled(False)
        self.save_pano_button.setEnabled(False)
        self.imgs = []

    def load_video_function(self):
        pass

    def collect_from_video(self):
        self.show_button.setEnabled(False)
        self.stitch_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.label.setText('c로 수집하고 끝나면 q로 끄기')

        self.cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit('카메라 연결 실패')

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            cv.imshow('video display', frame)

            key = cv.waitKey(1)
            if key==ord('c'):
                self.imgs.append(frame)
            elif key==ord('q'):
                self.cap.release()
                cv.destroyWindows('video display')
                break

        if len(self.imgs)>=2:
            self.show_button.setEnabled(True)
            self.stitch_button.setEnabled(True)
            self.save_button.setEnabled(True)

    def show_function(self):
        self.label.setText('수집된 영상은 '+ str(len(self.imgs)) +'장입니다.')
        stack = cv.resize(self.imgs[0], dsize=(0,0),fx=0.25,fy=0.25)
        for i in range(1,len(self.imgs)):
            stack=np.hstack((stack, cv.resize(self.imgs[i], dsize=(0,0), fx=0.25, fy=0.25)))
        cv.imshow('Image collection',stack)

    def stitch_function(self):
        pass

    def save_panorama_function(self):
        pass

    # --- 특수 효과 기능 ---
    def effect_function(self):
        self.label.setText("특수 효과 기능 선택됨")
        self.clear_function_button_layout()  # 기능별 버튼 지우기
        self.effect_ui()

    def effect_ui(self):
        # 함수 범위 내에 버튼 생성
        self.picture_button = QPushButton("열기", self)
        self.save_effect_button = QPushButton("저장", self)
        self.effect_combo = QComboBox(self)
        self.effect_combo.addItems(["엠보스", "카툰", "연필 스케치", "유화"])

        self.function_button_layout.addWidget(self.picture_button)
        self.function_button_layout.addWidget(self.save_effect_button)
        self.function_button_layout.addWidget(self.effect_combo)

        # 버튼 연결
        self.picture_button.clicked.connect(self.picture_open_function)
        self.save_effect_button.clicked.connect(self.save_function)
        self.effect_combo.currentIndexChanged.connect(self.apply_selected_effect)
        self.save_effect_button.setEnabled(False)  # 처음에는 저장 버튼 비활성화

    def picture_open_function(self):
        pass

    def emboss_function(self):
        pass

    def cartoon_function(self):
        pass

    def sketch_function(self):
        pass

    def oil_function(self):
        pass

    def save_function(self):
        pass

    def apply_selected_effect(self):
        pass

    def quit_program(self):
        cv.destroyAllWindows()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisionAgentGUI()
    sys.exit(app.exec_())
