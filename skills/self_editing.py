import os
import sys

class SelfEditingModule:
    def __init__(self, jarvis):
        self.jarvis = jarvis

    def edit_code(self, filepath, new_code):
        try:
            with open(filepath, 'w') as file:
                file.write(new_code)
            return True
        except Exception as e:
            print(f"Error editing code: {e}")
            return False

    def add_feature(self, feature_name, feature_code):
        filepath = f"./skills/{feature_name}.py"
        if not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                file.write(feature_code)
            return True
        else:
            print("Feature already exists.")
            return False

    def fix_bug(self, filepath, bug_fix_code):
        try:
            with open(filepath, 'w') as file:
                file.write(bug_fix_code)
            return True
        except Exception as e:
            print(f"Error fixing bug: {e}")
            return False

def main(jarvis):
    self_editing_module = SelfEditingModule(jarvis)
    while True:
        print("1. Edit code")
        print("2. Add feature")
        print("3. Fix bug")
        choice = input("Enter your choice: ")
        if choice == "1":
            filepath = input("Enter the filepath: ")
            new_code = input("Enter the new code: ")
            self_editing_module.edit_code(filepath, new_code)
        elif choice == "2":
            feature_name = input("Enter the feature name: ")
            feature_code = input("Enter the feature code: ")
            self_editing_module.add_feature(feature_name, feature_code)
        elif choice == "3":
            filepath = input("Enter the filepath: ")
            bug_fix_code = input("Enter the bug fix code: ")
            self_editing_module.fix_bug(filepath, bug_fix_code)
        else:
            break

if __name__ == "__main__":
    main(None)