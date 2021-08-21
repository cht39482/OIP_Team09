import os
import pathlib

def change_order(directory,order):
    target=os.path.join(pathlib.Path().resolve(),directory)
    os.chdir(target)
    print("Current working directory is:", os.getcwd())
    for filename in os.listdir("."):
            if filename.endswith(".txt") and (filename.find("classes")==-1):
                updated_lines=[]
                with open(filename,"r") as openfile:
                    for line in openfile.readlines():
                        line_read=line.strip()
                        updated_line=str(order)+ " "+ line[3:]
                        updated_lines.append(updated_line)
                        print(line)
                    print(updated_lines)
                    openfile.close()
                with open(filename,"w") as openfile:
                    openfile.writelines(updated_lines)
                    openfile.close()
    
                    
                        

path="images_syringes\\dirty"

print("Current Directory:",os.path.join(pathlib.Path().resolve(),path))
change_order(path,0)
