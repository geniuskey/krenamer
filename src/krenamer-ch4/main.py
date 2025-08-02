#!/usr/bin/env python3
"""
KRenamer Chapter 3: Drag & Drop Functionality
드래그 앤 드롭 기능을 추가한 GUI

이 챕터에서는 다음 기능을 배웁니다:
- tkinterdnd2를 사용한 드래그 앤 드롭 구현
- 파일 대화상자를 통한 파일 선택
- 실제 파일 경로 관리
- 파일 정보 표시 개선
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path

# tkinterdnd2 선택적 import
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class DragDropKRenamerGUI:
    """
    KRenamer Chapter 2: 드래그 앤 드롭 기능
    
    Chapter 1의 기본 구조에 실제 파일 처리 기능을 추가합니다:
    - 드래그 앤 드롭으로 파일 추가
    - 파일 대화상자로 파일 선택
    - 파일 경로와 정보 관리
    """
    
    def __init__(self):
        # tkinterdnd2가 사용 가능하면 DnD 윈도우 생성
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
        
        # 파일 경로를 저장할 리스트
        self.files = []
        
        self.setup_window()
        self.setup_widgets()
        self.setup_drag_drop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("KRenamer - Chapter 2: 드래그 앤 드롭")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.minsize(700, 500)
        
        self.center_window()
    
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_widgets(self):
        """GUI 위젯들 설정 및 배치"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 목록 라벨과 정보
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        files_label = ttk.Label(
            header_frame, 
            text="파일 목록:", 
            font=("맑은 고딕", 10, "bold")
        )
        files_label.pack(side=tk.LEFT)
        
        # 파일 개수 표시
        self.count_var = tk.StringVar()
        self.count_var.set("파일: 0개")
        count_label = ttk.Label(
            header_frame, 
            textvariable=self.count_var,
            font=("맑은 고딕", 9),
            foreground="blue"
        )
        count_label.pack(side=tk.RIGHT)
        
        # 파일 목록 프레임 (리스트박스 + 스크롤바)
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # 파일 리스트박스 (수평, 수직 스크롤 지원)
        self.files_listbox = tk.Listbox(
            listbox_frame, 
            height=18,
            font=("맑은 고딕", 9),
            selectmode=tk.EXTENDED  # 다중 선택 가능
        )
        
        # 스크롤바들
        scrollbar_y = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar_x = ttk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=self.files_listbox.xview)
        
        self.files_listbox.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 그리드 배치
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 리스트박스 프레임 그리드 설정
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        # 파일 추가 버튼
        self.add_button = ttk.Button(
            button_frame, 
            text="파일 추가", 
            command=self.add_files_dialog,
            width=12
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 폴더 추가 버튼
        self.add_folder_button = ttk.Button(
            button_frame, 
            text="폴더 추가", 
            command=self.add_folder_dialog,
            width=12
        )
        self.add_folder_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 선택 제거 버튼
        self.remove_button = ttk.Button(
            button_frame, 
            text="선택 제거", 
            command=self.remove_selected_files,
            width=12
        )
        self.remove_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 전체 지우기 버튼
        self.clear_button = ttk.Button(
            button_frame, 
            text="전체 지우기", 
            command=self.clear_all_files,
            width=12
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 이름 변경 버튼
        self.rename_button = ttk.Button(
            button_frame, 
            text="이름 변경", 
            command=self.rename_files,
            width=12
        )
        self.rename_button.pack(side=tk.LEFT)
        
        # 상태바 프레임
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 상태 메시지
        self.status_var = tk.StringVar()
        if DND_AVAILABLE:
            self.status_var.set("파일을 드래그 앤 드롭하거나 '파일 추가' 버튼을 클릭하세요.")
        else:
            self.status_var.set("tkinterdnd2가 설치되지 않음. '파일 추가' 버튼을 사용하세요.")
        
        status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            font=("맑은 고딕", 9),
            foreground="gray"
        )
        status_label.pack(side=tk.LEFT)
        
        # DnD 상태 표시
        dnd_status = "DnD: 사용가능" if DND_AVAILABLE else "DnD: 사용불가"
        dnd_label = ttk.Label(
            status_frame,
            text=dnd_status,
            font=("맑은 고딕", 9),
            foreground="green" if DND_AVAILABLE else "red"
        )
        dnd_label.pack(side=tk.RIGHT)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # 파일 목록 영역이 확장
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 초기 버튼 상태 설정
        self.update_button_states()
    
    def setup_drag_drop(self):
        """드래그 앤 드롭 설정"""
        if DND_AVAILABLE:
            # 리스트박스에 드래그 앤 드롭 등록
            self.files_listbox.drop_target_register(DND_FILES)
            self.files_listbox.dnd_bind('<<Drop>>', self.on_drop)
            
            # 메인 윈도우에도 드래그 앤 드롭 등록 (전체 영역)
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """드래그 앤 드롭 이벤트 처리"""
        try:
            # 드롭된 파일들 경로 파싱
            files = self.parse_drop_data(event.data)
            if files:
                self.add_files(files)
        except Exception as e:
            self.status_var.set(f"드래그 앤 드롭 처리 중 오류: {e}")
    
    def parse_drop_data(self, data):
        """드롭 데이터 파싱 (다양한 형식 지원)"""
        files = []
        
        # tkinter의 splitlist 사용
        try:
            raw_files = self.root.tk.splitlist(data)
            for file_path in raw_files:
                # 중괄호로 감싸진 경로 처리
                if file_path.startswith('{') and file_path.endswith('}'):
                    file_path = file_path[1:-1]
                
                if os.path.exists(file_path):
                    files.append(file_path)
        except Exception:
            # splitlist 실패 시 문자열 직접 파싱
            if isinstance(data, str):
                file_path = data.strip('{}')
                if os.path.exists(file_path):
                    files.append(file_path)
        
        return files
    
    def add_files_dialog(self):
        """파일 선택 대화상자"""
        try:
            files = filedialog.askopenfilenames(
                title="파일 선택",
                filetypes=[
                    ("모든 파일", "*.*"),
                    ("텍스트 파일", "*.txt"),
                    ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                    ("문서 파일", "*.pdf *.doc *.docx *.hwp"),
                    ("음악 파일", "*.mp3 *.wav *.flac"),
                    ("비디오 파일", "*.mp4 *.avi *.mkv *.mov")
                ]
            )
            if files:
                self.add_files(files)
        except Exception as e:
            messagebox.showerror("오류", f"파일 선택 중 오류가 발생했습니다: {e}")
    
    def add_folder_dialog(self):
        """폴더 선택 대화상자"""
        try:
            folder = filedialog.askdirectory(title="폴더 선택")
            if folder:
                # 폴더 내 모든 파일 찾기
                folder_files = []
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        folder_files.append(file_path)
                
                if folder_files:
                    self.add_files(folder_files)
                else:
                    self.status_var.set("선택한 폴더에 파일이 없습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"폴더 선택 중 오류가 발생했습니다: {e}")
    
    def add_files(self, file_paths):
        """파일 추가 처리"""
        added_count = 0
        skipped_count = 0
        
        for file_path in file_paths:
            try:
                # 실제 파일인지 확인
                if os.path.isfile(file_path):
                    # 중복 확인
                    if file_path not in self.files:
                        self.files.append(file_path)
                        
                        # 파일명과 경로 정보 표시
                        file_name = os.path.basename(file_path)
                        file_size = os.path.getsize(file_path)
                        size_str = self.format_file_size(file_size)
                        
                        display_text = f"{file_name} ({size_str}) - {file_path}"
                        self.files_listbox.insert(tk.END, display_text)
                        added_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            except Exception:
                skipped_count += 1
        
        self.update_file_count()
        self.update_button_states()
        
        # 상태 메시지 업데이트
        if added_count > 0:
            message = f"{added_count}개 파일이 추가되었습니다."
            if skipped_count > 0:
                message += f" ({skipped_count}개 건너뜀)"
            self.status_var.set(message)
        elif skipped_count > 0:
            self.status_var.set(f"{skipped_count}개 파일을 건너뛰었습니다. (중복 또는 유효하지 않은 파일)")
        else:
            self.status_var.set("추가할 파일이 없습니다.")
    
    def format_file_size(self, size_bytes):
        """파일 크기를 읽기 쉬운 형태로 변환"""
        if size_bytes == 0:
            return "0B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{int(size_bytes)}{unit}"
                else:
                    return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f}TB"
    
    def remove_selected_files(self):
        """선택된 파일들 제거"""
        selection = self.files_listbox.curselection()
        if selection:
            removed_count = len(selection)
            
            # 뒤에서부터 제거 (인덱스 변경 방지)
            for index in reversed(selection):
                self.files_listbox.delete(index)
                del self.files[index]
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"{removed_count}개 파일이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일을 선택해주세요.")
    
    def clear_all_files(self):
        """모든 파일 제거"""
        if self.files:
            count = len(self.files)
            self.files.clear()
            self.files_listbox.delete(0, tk.END)
            
            self.update_file_count()
            self.update_button_states()
            self.status_var.set(f"모든 파일({count}개)이 제거되었습니다.")
        else:
            self.status_var.set("제거할 파일이 없습니다.")
    
    def update_file_count(self):
        """파일 개수 업데이트"""
        count = len(self.files)
        self.count_var.set(f"파일: {count}개")
    
    def update_button_states(self):
        """버튼 상태 업데이트"""
        has_files = len(self.files) > 0
        
        # 파일이 있을 때만 활성화되는 버튼들
        state = tk.NORMAL if has_files else tk.DISABLED
        self.remove_button.config(state=state)
        self.clear_button.config(state=state)
        self.rename_button.config(state=state)
    
    def rename_files(self):
        """파일명 변경 (다음 챕터에서 구현)"""
        if self.files:
            self.status_var.set("이름 변경 기능은 Chapter 3에서 구현됩니다.")
            
            # 간단한 정보 표시
            total_size = sum(os.path.getsize(f) for f in self.files if os.path.exists(f))
            size_str = self.format_file_size(total_size)
            
            messagebox.showinfo(
                "파일 정보",
                f"선택된 파일: {len(self.files)}개\\n총 크기: {size_str}\\n\\n"
                "실제 이름 변경 기능은 Chapter 3에서 구현됩니다."
            )
        else:
            self.status_var.set("변경할 파일이 없습니다.")
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n프로그램이 사용자에 의해 종료되었습니다.")
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


def main():
    """메인 함수"""
    print("KRenamer Chapter 2: 드래그 앤 드롭 기능")
    print("=" * 40)
    print("이 예제에서 배우는 내용:")
    print("• tkinterdnd2를 사용한 드래그 앤 드롭")
    print("• 파일 대화상자를 통한 파일 선택")
    print("• 실제 파일 경로 관리")
    print("• 파일 정보 표시 (크기, 경로)")
    print("• 폴더 내 파일 일괄 추가")
    
    if not DND_AVAILABLE:
        print()
        print("⚠️  tkinterdnd2가 설치되지 않았습니다.")
        print("드래그 앤 드롭 기능을 사용하려면 다음 명령어로 설치하세요:")
        print("pip install tkinterdnd2")
        print()
    
    print("GUI 윈도우를 시작합니다...")
    
    try:
        app = DragDropKRenamerGUI()
        app.run()
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {e}")
        return 1
    
    print("KRenamer Chapter 2 완료!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())