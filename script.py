import os

screenshot_count = 0

for root, dirs, files in os.walk('/'):

    for file in files:

        if file.endswith(('.png', '.jpg', '.jpeg')) and 'screenshot' in file.lower():

            screenshot_count += 1

print(f'You have {screenshot_count} screenshots on your device')