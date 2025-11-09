
class FolderSelector:
    def __init__(self):
        self.folder_path = ""

    def select_folder(self, folder_name):
        # フォルダ選択のロジックをここに実装
        self.folder_path = folder_name
        print(f"Selected folder: {self.folder_path}")
        