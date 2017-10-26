# coding=utf-8
from xcodeproj import xcodeproj

if __name__ == '__main__':
    proj = xcodeproj.xcodeproj('/home/administrator/下载/infer/examples/ios_hello/HelloWorldApp.xcodeproj')
    projs = proj.projects()

    proj.targets()
    proj.project_file.targets()



    print projs
