import tkinter as tk
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title("Entry 입력값 검증")
root.geometry("500x400")

# 입력 필드들
tk.Label(root, text="이름:", font=("맑은 고딕", 12)).pack(pady=5)
name_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
name_entry.pack(pady=5)

tk.Label(root, text="나이 (숫자만):", font=("맑은 고딕", 12)).pack(pady=5)
age_entry = tk.Entry(root, font=("맑은 고딕", 12), width=30)
age_entry.pack(pady=5)

# 입력값 처리 함수
def process_input():
    name = name_entry.get()
    age = age_entry.get()
    
    # 입력값 검증
    if not name:
        msgbox.showwarning("입력 오류", "이름을 입력해주세요!")
        return
    
    if age and not age.isdigit():
        msgbox.showerror("입력 오류", "나이는 숫자만 입력해주세요!")
        return
    
    # 결과 표시
    result = f"안녕하세요, {name}님!"
    if age:
        result += f"\n나이: {age}세"
    
    msgbox.showinfo("입력 결과", result)

# 버튼과 기능
tk.Button(root, text="입력 처리", command=process_input, 
          font=("맑은 고딕", 12), bg="lightgreen").pack(pady=10)

def clear_all():
    name_entry.delete(0, tk.END)  # Entry 내용 지우기
    age_entry.delete(0, tk.END)

tk.Button(root, text="모두 지우기", command=clear_all,
          font=("맑은 고딕", 12), bg="lightcoral").pack(pady=5)

# Enter 키로 입력 처리
root.bind('<Return>', lambda event: process_input())

root.mainloop()