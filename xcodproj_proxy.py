# coding=utf-8
from xcodeproj import xcodeproj
from xcodeproj.pbProj import PBX_Constants

from PBXConst import PBXConst_ISA_PBXSourcesBuildPhase, PPBConst_REFERENCE_FILE_TYPE_OBJC


class PBXFileReferenceProxy(object):
    ref = None

    def __init__(self, ref):
        super(PBXFileReferenceProxy, self).__init__()
        self.ref = ref

    def language_type(self):
        file_type = self.ref.get(PBX_Constants.kPBX_REFERENCE_lastKnownFileType)
        if not file_type:
            file_type = self.ref.get(PBX_Constants.kPBX_REFERENCE_explicitFileType)
        return file_type

    def name(self):
        path = self.ref.get(PBX_Constants.kPBX_REFERENCE_path)
        try:
            name = path.split('/')[-1]
            return name
        except:
            pass
        return None

class PBXProjProxy(object):
    proj = None

    def __init__(self, proj):
        super(PBXProjProxy, self).__init__()
        self.proj = proj  # type xcodeproj

    @property
    def project_file(self):
        return self.proj.project_file  # type PBXProj

    @property
    def project(self):
        return self.project_file.pbx_root_object

    def targets(self):  # type list<>

        return self.project.get(PBX_Constants.kPBX_PROJECT_targets)

    def get_target(self, name):  # type PBXNativeTarget
        for target in self.targets():
            if target.get(PBX_Constants.kPBX_TARGET_name) == name:
                return target
        return None

    def get_source_build_phase(self, target_name):
        target = self.get_target(target_name)
        if not target:
            return None

        build_phases = target.get(PBX_Constants.kPBX_TARGET_buildPhases)
        if not build_phases:
            return None
        for phase in build_phases:
            if phase.isa == PBXConst_ISA_PBXSourcesBuildPhase:
                return phase
        return None

    def get_build_file_ref(self, target_name, file_name):
        phase = self.get_source_build_phase(target_name)
        if not phase:
            return None
        files = phase.get(PBX_Constants.kPBX_PHASE_files)
        if not files:
            return None
        for f in files: # type PBXBuildFile
            file_ref = f.get(PBX_Constants.kPBX_BUILDFILE_fileRef)
            if not file_ref:
                continue
            path = file_ref.get(PBX_Constants.kPBX_REFERENCE_path)
            try:
                name = path.split('/')[-1]
                if name == file_name:
                    return PBXFileReferenceProxy(file_ref)
            except:
                pass
        return None

    def get_ref_file_dic(self, target_name):
        dic = {}
        phase = self.get_source_build_phase(target_name)
        if not phase:
            return None
        files = phase.get(PBX_Constants.kPBX_PHASE_files)
        if not files:
            return None
        for f in files:  # type PBXBuildFile
            file_ref = f.get(PBX_Constants.kPBX_BUILDFILE_fileRef)
            if not file_ref:
                continue
            path = file_ref.get(PBX_Constants.kPBX_REFERENCE_path)
            try:
                name = path.split('/')[-1]
                if not name:
                    continue
                dic[name] = PBXFileReferenceProxy(file_ref)
            except:
                pass
        return dic





if __name__ == '__main__':
    proj = xcodeproj.xcodeproj('/Users/away/Desktop/analyzer/infer-0.12.0/examples/ios_hello/HelloWorldApp.xcodeproj')
    # proj = xcodeproj.xcodeproj('/home/administrator/下载/infer/examples/ios_hello/HelloWorldApp.xcodeproj')

    proxy = PBXProjProxy(proj)
    proxy.targets()

    # target

    hello_world_app_ = u'HelloWorldApp'
    target = proxy.get_target(hello_world_app_)
    assert target

    # phase
    phase = proxy.get_source_build_phase(hello_world_app_)

    # file_ref
    delegate_m = 'AppDelegate.m'
    file_ref = proxy.get_build_file_ref(hello_world_app_, delegate_m)

    assert file_ref
    assert delegate_m in file_ref.name()

    file_ref_dic = proxy.get_ref_file_dic(hello_world_app_)

    # ref_dic
    assert len(file_ref_dic.keys()) == 4

    # file_type
    for v in file_ref_dic.values():
        assert PPBConst_REFERENCE_FILE_TYPE_OBJC == v.language_type()
    print ''
