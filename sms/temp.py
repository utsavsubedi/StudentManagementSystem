from pathlib import Path 


temp = Path(r'C:\Users\Hp\Desktop\MyGithub\StudentManagement').joinpath('random.json')
temp.touch(exist_ok=True)

# temp = Path(r"C:\Users\Hp\AppData\Roaming\sms\database").joinpath("sms_db.json")
# temp.touch(exist_ok=True)
