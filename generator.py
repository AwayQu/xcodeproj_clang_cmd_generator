
class ClangOption(object):
    DriverOptions = ['-o',
                     '-Qunused-arguments'
                     ]



class ClangCMDGenerator(object):
    proj = None # PBXProj

    target_name = None # str target
    configuration = None #  srt Debug Release

    def __init__(self, proj, **kwargs):
        super(self)

        kwargs.get('target', None)


        self.proj = proj

    @property
    def project_file(self):
        if self.proj:
            return self.proj.project_file


    def cmd(self, file_name_or_path):
        fn = None
        fp = None
        if self.is_filename(file_name_or_path):
            fn = file_name_or_path
            fp = self.get_path(fn)
        else:
            fp = file_name_or_path
            fn = file_name_or_path(fp)
        return self._cmd(fp, fn)


    def _cmd(self, file_path, file_name):
        pass







    def get_name(self, file_path):
        return ""

    def get_path(self, file_name):
        return ""

    def file_path_exist(self, file_path):
        pass

    def file_exist(self, file_name):
        pass

    def is_filename(self, file_name_or_path):
        pass

    ### Target Selection Options
    @property
    def arch(self):
        return ['-arch', 'i386']
"""

clang
-###
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