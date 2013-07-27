Date: 2013-07-01
Title: Compiling open source libraries with Android NDK: Part 2
Category: Software
Tags: android, ndk

_This is a repost from my old blog._

For the second part of this series, we will deal with the compiling of open
source libraries that have several makefiles.

Android NDK r5 added support for prebuilt libraries and also included
standalone toolchains that could be used to compile open-source libraries for
Android. These are very useful, and lets you tap into the pool of open-source
goodies that desktop developers enjoy. Essentially, we will be using the same
makefiles but with a cross-compiler.

I am using Mac OS X, but the steps should also work on a Linux machine. If you
are a Windows user and know how to compile open-source libraries for Android on
a Windows machine, please leave a comment.

Here, I will use the fftw3 library as an example. Get the library from the
[FFTW](http://www.fftw.org/download.html) website.

1. Use Eclipse to create a new Android project (let’s name it `FourierTest`) in
your workspace. This uses Android ADT to create the files required by
`ndk-build`.
1. Unpack the fftw3 library in a directory parallel to the project directory
that you have just created.
1. Inside the project directory, create a new `build.sh` file with the following
contents:

        :::sh
        #!/bin/sh
        # FourierTest/build.sh
        # Compiles fftw3 for Android
        # Make sure you have NDK_ROOT defined in .bashrc or .bash_profile

        INSTALL_DIR="`pwd`/jni/fftw3"
        SRC_DIR="`pwd`/../fftw-3.2.2"

        cd $SRC_DIR

        export
        PATH="$NDK_ROOT/toolchains/arm-linux-androideabi-4.4.3/prebuilt/darwin-x86/bin/:$PATH"
        export SYS_ROOT="$NDK_ROOT/platforms/android-8/arch-arm/"
        export CC="arm-linux-androideabi-gcc --sysroot=$SYS_ROOT"
        export LD="arm-linux-androideabi-ld"
        export AR="arm-linux-androideabi-ar"
        export RANLIB="arm-linux-androideabi-ranlib"
        export STRIP="arm-linux-androideabi-strip"

        mkdir -p $INSTALL_DIR
        ./configure --host=arm-eabi --build=i386-apple-darwin10.8.0
        --prefix=$INSTALL_DIR LIBS="-lc -lgcc"

        make
        make install

        exit 0

    At this point, your directory structure should look like the following:

        <workspace>/
            FourierTest/
                AndroidManifest.xml
                build.sh
                ...
                src/
            fftw-3.2.2/
                configure
                ...

    The `build.sh` script given above tells the makefile to use the Android
    cross-compiler instead of the system's compiler. In particular,

    - `INSTALL_DIR` tells make to install the compiled library in our project's jni directory
    - `PATH` tells make to look for our tool chain in the NDK directory. Note that
    you might have to change this value - explore your NDK directory to make sure
    that the path exists
    - `SYS_ROOT` tells make where to look for system libraries and header files
    - `./configure --host=arm-eabi --build=i386-apple-darwin10.8.0` tells make that
    we are cross-compiling using a i386 architecture for an ARM architecture.

    You most likely have to change the `PATH` variable and the `--build` parameter.

4. Open up Terminal and cd to your project directory
5. Run `build.sh`
6. The compiled library will be installed in `FourierTest/jni/fftw3`. To use this
library, create the following `Android.mk` file in `FourierTest/jni/fftw3`:

        :::Makefile
        # FourierTest/jni/fftw3/Android.mk
        LOCAL_PATH := $(call my-dir)

        include $(CLEAR_VARS)

        LOCAL_MODULE := fftw3

        LOCAL_SRC_FILES := lib/libfftw3.a
        LOCAL_EXPORT_C_INCLUDES := $(LOCAL_PATH)/include

        include $(PREBUILT_STATIC_LIBRARY)
