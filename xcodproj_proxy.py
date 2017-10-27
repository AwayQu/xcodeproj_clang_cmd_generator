# coding=utf-8
from xcodeproj import xcodeproj
from xcodeproj.pbProj import PBX_Constants

from PBXConst import PBXConst_ISA_PBXSourcesBuildPhase, PPBConst_REFERENCE_FILE_TYPE_OBJC


class PBXFileReferenceProxy(object):
    ref = None
    build_file = None

    def __init__(self, ref, build_file):
        super(PBXFileReferenceProxy, self).__init__()
        self.ref = ref
        self.build_file = build_file

    def language_type(self):
        file_type = self.ref.get(PBX_Constants.kPBX_REFERENCE_lastKnownFileType)
        if not file_type:
            file_type = self.ref.get(PBX_Constants.kPBX_REFERENCE_explicitFileType)
        return file_type

    def path(self):
        return self.ref.get(PBX_Constants.kPBX_REFERENCE_path)

    def compiler_flags(self):
        settings = self.build_file.get(PBX_Constants.kPBX_BUILDFILE_settings)
        if settings:
            return settings.get(u"COMPILER_FLAGS", "")
        return ""

    def name(self):
        path = self.path()
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
    def project_path(self):
        paths = self.project_file.pbx_file_path.split('/')
        return '/'.join(paths[:-2])

    @property
    def project_name(self):
        """
        file name
        """
        paths = self.project_file.pbx_file_path.split('/')
        file_name = paths[-2]
        return file_name.split('.')[0]

    def product_name(self, target_name, configuration):
        self.get_target(target_name)
        xc_config_list = self.get_target(target_name).get(PBX_Constants.kPBX_TARGET_buildConfigurationList)
        if not xc_config_list:
            return None
        build_configs = xc_config_list.get(PBX_Constants.kPBX_XCCONFIGURATION_buildConfigurations)
        if not build_configs:
            return None
        for config in build_configs:
            if config.get(u"name") == configuration:
                build_settings = config.get(u"buildSettings")
                if not build_configs:
                    return None
                product_name = build_settings.get(u"PRODUCT_NAME")
                if product_name == u'$(TARGET_NAME)':
                    return target_name
        return None

    def info_plist_path(self, target_name, configuration):
        xc_config_list = self.get_target(target_name).get(PBX_Constants.kPBX_TARGET_buildConfigurationList)
        if not xc_config_list:
            return None
        build_configs = xc_config_list.get(PBX_Constants.kPBX_XCCONFIGURATION_buildConfigurations)
        if not build_configs:
            return None
        for config in build_configs:
            if config.get(u"name") == configuration:
                build_settings = config.get(u"buildSettings")
                if not build_configs:
                    return None
                return build_settings.get(u"INFOPLIST_FILE")
        return None

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
                    return PBXFileReferenceProxy(file_ref, f)
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
                dic[name] = PBXFileReferenceProxy(file_ref, f)
            except:
                pass
        return dic



if __name__ == '__main__':
    # proj = xcodeproj.xcodeproj('/Users/away/Desktop/analyzer/infer-0.12.0/examples/ios_hello/HelloWorldApp.xcodeproj')
    proj = xcodeproj.xcodeproj('./test_res/ios_hello/HelloWorldApp.xcodeproj')

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

    # project_path
    assert proxy.project_path == u'./test_res/ios_hello'

    # project name
    assert proxy.project_name == u'HelloWorldApp'


    # infoplist_file
    assert proxy.info_plist_path(hello_world_app_, u'Debug') == u'HelloWorldApp/Info.plist'
    assert proxy.info_plist_path(hello_world_app_, u'Release') == u'HelloWorldApp/Info.plist'

    # production_name
    assert proxy.product_name(hello_world_app_, u'Debug') == u'HelloWorldApp'
    assert proxy.product_name(hello_world_app_, u'Release') == u'HelloWorldApp'
    print ''
