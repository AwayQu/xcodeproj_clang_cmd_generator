

import PBXConst
import buildSettings


class ClangOption(object):
    DriverOptions = ['-o',
                     '-Qunused-arguments'
                     ]


class FileInfo(object):
    file_path = None
    file_name = None
    file_relative_path = None
    name = None

    def __init__(self, file_path, file_name):
        super(FileInfo, self).__init__()
        import os
        self.file_relative_path = file_path
        self.file_path = os.path.abspath(file_path)
        self.file_name = file_name
        self.name = self.file_name.split('.')[0]


class ClangCMDGenerator(object):
    proj_proxy = None  # PBXProjProxy

    target_name = None  # str target
    configuration = None  # srt Debug Release

    def __init__(self, proj_proxy, **kwargs):
        super(ClangCMDGenerator, self).__init__()

        self.target_name = kwargs.get('target', None)
        self.configuration = kwargs.get('configuration', None)
        self.proj_proxy = proj_proxy
        self.build_settings = buildSettings.BuildSettings(**kwargs)


    def cmd(self, file_name_or_path):
        fn = None
        fp = None
        if self.is_filename(file_name_or_path):
            fn = file_name_or_path
            fp = self.get_path(fn)
        else:
            fp = file_name_or_path
            fn = self.get_name(fp)
        return self._cmd(FileInfo(fp, fn))

    def _cmd(self, fileinfo):
        args = []
        args += self.clang_path()
        args += self.x(fileinfo)
        args += self.arch()
        args += self.std()
        args += self.compiler_flags(fileinfo)
        args += self.O0()
        args += self.D()
        args += self.isysroot()
        args += self.fobjc_abi_version()
        args += self.fobjc_legacy_dispatch()
        args += self.iquote()
        args += self.F()
        args += self.MMD()
        args += self.MT()
        args += self.dependencies()
        args += self.MF(fileinfo)
        args += self.serialize_diagnostics(fileinfo)
        args += self.c(fileinfo)
        args += self.o(fileinfo)

        return args

    def get_name(self, file_path):
        try:
            return file_path.split('/')[-1]
        except:
            raise SystemError('not a path')


    def get_path(self, file_name):
        try:
            import os
            import fnmatch

            def iterfindfiles(path, fnexp):
                for root, dirs, files in os.walk(path):
                    for filename in fnmatch.filter(files, fnexp):
                        yield os.path.join(root, filename)
            for filename in iterfindfiles(self.proj_proxy.project_path, file_name):
                return filename
        except:
            raise SystemError('file not exist')

    def file_path_exist(self, file_path):
        import os
        return os.path.exists(file_path)

    def file_exist(self, file_name):
        path = self.get_path(file_name)
        if not path:
            return False
        import os
        return os.path.exists(path)

    def is_filename(self, file_name_or_path):
        if u'/' in file_name_or_path:
            return False
        return True

    def clang_path(self):
        return [u'clang']

    # Language Selection and Mode Options
    def x(self, file_info):
        opts = ['-x']

        ref = self.proj_proxy.get_ref_file_dic(self.target_name).get(file_info.file_name)
        if not ref:
            raise SystemError('no file')
        language_type = ref.language_type()
        if language_type == PBXConst.PBXConst_REFERENCE_FILE_TYPE_C:
            opts.append('c')
        elif language_type == PBXConst.PPBConst_REFERENCE_FILE_TYPE_OBJC:
            opts.append('objective-c')
        elif language_type == PBXConst.PPBConst_REFERENCE_FILE_TYPE_OBJCPP:
            opts.append('objective-c++')
        elif language_type == PBXConst.PPBConst_REFERENCE_FILE_TYPE_CPP:
            # TODO: cpp
            raise SystemError('no implement')
        else:
            raise SystemExit('unknown type')
        return opts

    def std(self):
        # TODO: check std type
        opts = ['-std=gnu99']
        return opts

    # Target Selection Options

    def arch(self):
        return ['-arch', 'i386']

    # Search Headers Options

    def iquote(self):
        import os
        build_header_path = self.proj_proxy.build_header_map_path(self.target_name)
        product_name = self.proj_proxy.product_name(self.target_name, self.configuration)
        opts = [u'-iquote', os.path.join(build_header_path, u'{}-generated-files.hmap'.format(product_name))]
        opts += [u'-iquote', os.path.join(build_header_path, u'{}-project-headers.hmap'.format(product_name))]
        return opts

    def isysroot(self):
        return [u'-isysroot',
                u'/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk']


    def I(self):
        import os
        build_header_path = self.proj_proxy.build_header_map_path(self.target_name)
        product_name = self.proj_proxy.product_name(self.target_name, self.configuration)
        opts = [u'-I' + os.path.join(build_header_path, u'{}-own-target-headers.hmap'.format(product_name))]
        opts += [u'-I' + os.path.join(build_header_path, u'{}-all-target-headers.hmap'.format(product_name))]
        opts += [u'-I'+ os.path.join(self.proj_proxy.build_path(), u'include')]

        # TODO: Pod Headers
        # TODO: DerivedSources
        return opts

    def include(self):
        return []

    # Framework Search Options


    def F(self):
        s = self.build_settings.get(buildSettings.FRAMEWORK_SEARCH_PATHS)
        ls = s.split(u' ')
        opts = []
        for l  in ls:
            opts.append(u'-F{}'.format(l[1:-1] if l[0]=='"' else l))
        return opts

    # Driver Options
    def o(self, fileinfo):
        import os
        return [u'-o', os.path.join(self.proj_proxy.intermediates_path(self.target_name), fileinfo.name + u'.o')]

    # Objective-C Options
    def compiler_flags(self, file_info):
        # fobjc-no-arc
        # -fobjc-arc
        ref_proxy = self.proj_proxy.get_ref_file_dic(self.target_name).get(file_info.file_name)
        s = ref_proxy.compiler_flags()
        opts = s.split(" ")
        return opts

    def fobjc_abi_version(self):
        return [u'-fobjc-abi-version=2']

    def fobjc_legacy_dispatch(self):
        return [u'-fobjc-legacy-dispatch']

    # Code Generation Options
    def O0(self):
        return [u'-O0']

    # Preprocessor Options
    def D(self):
        return []

    # Stage Selection Options
    def c(self, fileinfo):
        import os
        return [u'-c', fileinfo.file_path]

    # Anoyomus Options

    def MMD(self):
        return [u'-MMD']

    def MT(self):
        return [u'-MT']

    def dependencies(self):
        return [u'dependencies']

    def MF(self, fileinfo):
        import os
        return [u'-MF', os.path.join(self.proj_proxy.intermediates_path(self.target_name), fileinfo.name + u'.d')]

    def serialize_diagnostics(self, fileinfo):
        import os
        return [u'-serialize-diagnostics', os.path.join(self.proj_proxy.intermediates_path(self.target_name), fileinfo.name + u'.dia')]


if __name__ == '__main__':
    from xcodeproj import xcodeproj
    from xcodproj_proxy import PBXProjProxy
    proj = xcodeproj.xcodeproj('./test_res/ios_hello/HelloWorldApp.xcodeproj')

    proxy = PBXProjProxy(proj)

    cmd_generator = ClangCMDGenerator(proxy, target=u'HelloWorldApp', configuration=u'Debug')

    # is_filename
    assert cmd_generator.is_filename('main.m')
    assert not cmd_generator.is_filename('./ios_hello/HelloWorldApp/main.m')
    import os
    assert cmd_generator.get_path('main.m') == os.path.abspath(u'./test_res/ios_hello/HelloWorldApp/main.m')

    # file exists
    assert cmd_generator.file_exist('main.m')
    assert not cmd_generator.file_exist('ma.m')

    # file path exists
    assert not cmd_generator.file_path_exist('main.m')
    assert cmd_generator.file_path_exist(u'./test_res/ios_hello/HelloWorldApp/main.m')

    # -x
    x = cmd_generator.x(file_info=FileInfo(u'./test_res/ios_hello/HelloWorldApp/main.m', u'main.m'))
    assert ['-x', 'objective-c'] == x

    # compiler_args
    appdelegate_info = FileInfo(u'./test_res/ios_hello/HelloWorldApp/Appdelegate.m', u'AppDelegate.m')
    compile_args = cmd_generator.compiler_flags(appdelegate_info)
    assert [u'-fobjc-arc'] == compile_args

    # I
    I = cmd_generator.I()

    # iquote
    iquote = cmd_generator.iquote()

    # FM
    MF = cmd_generator.MF(appdelegate_info)

    # diagnostics
    diagnostics = cmd_generator.serialize_diagnostics(appdelegate_info)

    # c
    c = cmd_generator.c(appdelegate_info)

    # o
    o = cmd_generator.o(appdelegate_info)

    cmd = cmd_generator.cmd(u'./test_res/ios_hello/HelloWorldApp/main.m')


    cmd = cmd_generator.cmd(u'AppDelegate.m')

    print ' '.join(cmd)
    pass

"""

clang
-#
-x
objective-c
-arch
i386
-fmessage-length=0
-fdiagnostics-show-note-include-stack
-fmacro-backtrace-limit=0
-std=gnu99
-fobjc-arc
-fmodules
-fmodules-prune-interval=86400
-fmodules-prune-after=345600
-fbuild-session-file=/var/folders/tf/zbcpj6qx6p13pj_dm_w9k1_h0000gn/C/org.llvm.clang/ModuleCache/Session.modulevalidation
-fmodules-validate-once-per-build-session
-Wnon-modular-include-in-framework-module
-Werror=non-modular-include-in-framework-module
-Wno-trigraphs
-fpascal-strings
-O0
-Wno-missing-field-initializers
-Wno-missing-prototypes
-Werror=return-type
-Wunreachable-code
-Wno-implicit-atomic-properties
-Werror=deprecated-objc-isa-usage
-Werror=objc-root-class
-Wno-arc-repeated-use-of-weak
-Wduplicate-method-match
-Wno-missing-braces
-Wparentheses
-Wswitch
-Wunused-function
-Wno-unused-label
-Wno-unused-parameter
-Wunused-variable
-Wunused-value
-Wempty-body
-Wconditional-uninitialized
-Wno-unknown-pragmas
-Wno-shadow
-Wno-four-char-constants
-Wno-conversion
-Wconstant-conversion
-Wint-conversion
-Wbool-conversion
-Wenum-conversion
-Wshorten-64-to-32
-Wpointer-sign
-Wno-newline-eof
-Wno-selector
-Wno-strict-selector-match
-Wundeclared-selector
-Wno-deprecated-implementations
-DDEBUG=1
-DOBJC_OLD_DISPATCH_PROTOTYPES=0
-isysroot
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.2.sdk
-fasm-blocks
-fstrict-aliasing
-Wprotocol
-Wdeprecated-declarations
-mios-simulator-version-min=8.2
-g
-Wno-sign-conversion
-Wno-infinite-recursion
-fobjc-abi-version=2
-fobjc-legacy-dispatch
-iquote
/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/HelloWorldApp-generated-files.hmap
-I/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/HelloWorldApp-own-target-headers.hmap
-I/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/HelloWorldApp-all-target-headers.hmap
-iquote
/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/HelloWorldApp-project-headers.hmap
-I/Users/away/Desktop/ios_hello/build/Debug-iphonesimulator/include
-I/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/DerivedSources/i386
-I/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/DerivedSources
-F/Users/away/Desktop/ios_hello/build/Debug-iphonesimulator
-MMD
-MT
dependencies
-MF
/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/Objects-normal/i386/ViewController.d
--serialize-diagnostics
/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/Objects-normal/i386/ViewController.dia
-c
/Users/away/Desktop/ios_hello/HelloWorldApp/ViewController.m
-o
/Users/away/Desktop/ios_hello/build/HelloWorldApp.build/Debug-iphonesimulator/HelloWorldApp.build/Objects-normal/i386/ViewController.o
-fno-cxx-modules
-Qunused-arguments
-Wno-ignored-optimization-argument

"""
