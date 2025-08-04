import tkinter as tk

print("🎉 첫 번째 GUI 프로그램을 만들어보자!")

# 1단계: 기본 창 만들기
root = tk.Tk()  # 새로운 창을 만듭니다
root.title("내 첫 번째 GUI 프로그램")  # 창 제목 설정
root.geometry("400x300")  # 창 크기 설정 (가로x세로)

# 2단계: 간단한 텍스트 추가
welcome_label = tk.Label(root, text="안녕하세요! GUI 세계에 오신 것을 환영합니다!")
welcome_label.pack(pady=20)  # 창에 추가하고 위아래 여백 20픽셀

# 3단계: 창 보여주기 (이것이 없으면 창이 안 보여요!)
print("창을 보여줍니다... 창을 닫으려면 X 버튼을 눌러주세요!")
root.mainloop()

print("프로그램이 종료되었습니다. 수고하셨습니다!")