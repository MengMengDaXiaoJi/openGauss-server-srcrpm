%define port 5432
%define datapath /var/lib/opengauss
%define apppath %{_prefix}/local/opengauss
%define gauss_version master
# Only NUMA topology can enable mot feature in openGauss.
# If your cpu is numa topology, you can change this value from false to true.
%define is_enable_mot false

Name:           opengauss
Version:        master
Release:        1
Summary:        opengauss is an open source relational database management system
Provides:       opengauss = %{version}-%{release}
License:        MulanPSL-2.0 and MIT and BSD and zlib and TCL and Apache-2.0 and BSL-1.0
Source0:        openGauss-server-%{gauss_version}.tar.gz
Source1:        openGauss-third_party_binarylibs_openEuler_2203_riscv64.tar.gz

Source5:        opengauss-bashprofile
Source6:        opengauss.service

Patch0:         0001-openGauss-server-support-riscv64.patch
Patch1:         0002-openGauss-server-enable-all-openeuler-release-compile.patch

BuildRequires:  cmake gcc gcc-c++ openssl-devel python tar wget
BuildRequires:  cjson lz4-devel zstd-devel boost-devel cjson-devel
BuildRequires:  libcgroup-devel libcurl-devel unixODBC-devel jemalloc-devel krb5-devel
BuildRequires:  java-1.8.0-openjdk-devel libedit-devel libaio-devel
BuildRequires:  bison flex
BuildRequires:  numactl-devel

Autoreqprov: 0

Requires: lsof 
Requires: libaio-devel

%if "%{is_enable_mot}" == "true"
Requires: numactl-devel
%endif

%description
opengauss kernel : opengauss is an open source relational database management system.

%global debug_package %{nil}

%prep
%setup -q -c -n %{name}-%{version}

%ifarch x86_64 aarch64 %{arm}

%ifarch x86_64
%define binarylibs_name openGauss-third_party_binarylibs_openEuler_2203_x86_64
%define gcc_version 10.3.0
%endif

%ifarch aarch64 %{arm}
%define binarylibs_name openGauss-third_party_binarylibs_openEuler_2203_arm
%define gcc_version 10.3.1
%endif

wget https://opengauss.obs.cn-south-1.myhuaweicloud.com/latest/binarylibs/gcc10.3/%{binarylibs_name}.tar.gz
tar -zxf %{binarylibs_name}.tar.gz -C %{_builddir}/%{name}-%{version}

%endif

%ifarch riscv64
%define binarylibs_name openGauss-third_party_binarylibs_openEuler_2203_riscv64
%define gcc_version 10.3.0
tar -zxf %{SOURCE1} -C %{_builddir}/%{name}-%{version}
%endif

chmod -R 755 %{_builddir}/%{name}-%{version}

### patch openGauss-server ##############
pushd openGauss-server-%{gauss_version}
%patch0 -p1
%patch1 -p1
popd

%build
GAUSS_THIRD_PATH=$(pwd)/%{binarylibs_name}
### export environment ##################
export GCC_PATH=$GAUSS_THIRD_PATH/buildtools/gcc10.3
export CC=$GCC_PATH/gcc/bin/gcc
export CXX=$GCC_PATH/gcc/bin/g++
export LD_LIBRARY_PATH=%{apppath}/lib:$GCC_PATH/gcc/lib64:$GCC_PATH/isl/lib:$GCC_PATH/mpc/lib/:$GCC_PATH/mpfr/lib/:$GCC_PATH/gmp/lib/:$LD_LIBRARY_PATH
export LIBRARY_PATH=%{apppath}/lib:$GCC_PATH/gcc/lib64:$GCC_PATH/isl/lib:$GCC_PATH/mpc/lib/:$GCC_PATH/mpfr/lib/:$GCC_PATH/gmp/lib/:$LIBRARY_PATH
export PATH=%{apppath}/bin:$GCC_PATH/gcc/bin:$PATH
########### build openGauss-server ################
pushd openGauss-server-%{gauss_version}
chmod +x ./configure
%if "%{is_enable_mot}" == "true"
./configure \
CC=g++ CFLAGS='-O2' \
--gcc-version=%{gcc_version} \
--prefix=%{apppath} \
--3rd=$GAUSS_THIRD_PATH \
--enable-thread-safety \
--with-readline \
--without-zlib \
--enable-mot
%else
./configure \
CC=g++ CFLAGS='-O2' \
--gcc-version=%{gcc_version} \
--prefix=%{apppath} \
--3rd=$GAUSS_THIRD_PATH \
--enable-thread-safety \
--with-readline \
--without-zlib
%endif

%make_build
popd

%install
%define _python_bytecompile_errors_terminate_build 0
### install openGauss-server ############
pushd openGauss-server-%{gauss_version}
make install DESTDIR=%{buildroot} -s %{?_smp_mflags}
mkdir -p %{buildroot}/var/lib/opengauss/data
mkdir -p %{buildroot}/%{apppath}/script
cp build/script/opengauss_config_file_mini %{buildroot}/%{apppath}/share/postgresql/
popd

# opengauss datanode dir.
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/opengauss/data

# opengauss .bash_profile
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{?_localstatedir}/lib/opengauss/.bash_profile
# auto start files
install -m 644 %{SOURCE6} %{buildroot}/%{apppath}/script/opengauss.service

%pre
/usr/sbin/groupadd opengauss >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g opengauss -d %{datapath} -s /bin/bash \
        -c "opengauss Server" omm >/dev/null 2>&1 || :

# for install step
if [ $1 = 1 ]; then
    portinfo=$(lsof -i:%{port})
    if [ "${portinfo}" != "" ]; then
        echo "The port[%{port}] is occupied. Please use command 'lsof -i:%{port} to check it.'"
        exit 1
    fi
fi

%post
# set opengauss mini config parameters
set_mini_configparam(){
    config_mini_file=%{apppath}/share/postgresql/opengauss_config_file_mini

    # set guc parameters
    echo "port = %{port}" >> ${config_mini_file}
    echo "synchronous_commit = off" >> ${config_mini_file}
    echo "listen_addresses = '*'" >> ${config_mini_file}

    config_sample_file=%{apppath}/share/postgresql/postgresql.conf.sample
    if [[ -f $config_mini_file ]]
    then
        if [[ ! -f "$config_sample_file" ]]
        then
            echo "postgresql.conf.sample does not exist"
        else
            while IFS= read -r line; do
                SUBSTRING=$(echo $line | cut -d'=' -f 1)"= "
                if grep -q "$SUBSTRING" $config_sample_file ; then
                    sed -i "/$SUBSTRING/c$line" $config_sample_file
                else
                    echo $line >> $config_sample_file
                fi
            done < $config_mini_file
        fi
    fi

    sed -i "s/asp_sample_num/#asp_sample_num/" $config_sample_file
    sed -i "s/wal_insert_status_entries/#wal_insert_status_entries/" $config_sample_file
}

start_opengauss(){
    process_id=$(ps -ef | grep /usr/local/opengauss/bin/gaussdb | grep /var/lib/opengauss/data | grep -v grep | awk '{print $2}')
    if [ "$process_id" != "" ]; then
        echo "A process of opengauss already exists. Use command (ps -ef | grep /var/lib/opengauss/data) to confirm."
        echo "Please kill the process and reinstall opengauss."
        return 0
    fi

    if [ "`ls -A /var/lib/opengauss/data`" != "" ]; then
        echo "Datanode dir(/var/lib/opengauss/data) is not empty."
        echo "Please delete dir and reinstall opengauss."
        return 0
    fi

    result=`su - omm -c "source /var/lib/opengauss/.bash_profile; gs_initdb -D /var/lib/opengauss/data -U omm --nodename=single_node"`
    if [ $? -ne 0 ]; then
        echo "Init opengauss database failed."
        echo "Init opengauss database failed."
        echo $result
    else
        echo "Init opengauss database success."
        result=`systemctl start opengauss`
        if [ $? -ne 0 ]; then
            echo "Start opengauss database failed."
            echo $result
            echo $result
        else
            echo "Start opengauss database success."
        fi
    fi
}

add_service(){
    cp %{apppath}/script/opengauss.service /usr/lib/systemd/system/
    systemctl enable opengauss.service
}

set_conf(){
    echo "host  all  all 0.0.0.0/0 sha256" >> %{datapath}/data/pg_hba.conf
}

restart_opengauss(){
    result=`systemctl restart opengauss`
    if [ $? -ne 0 ]; then
        echo "Restart opengauss database failed."
        echo $result
        echo $result
        else
            echo "Restart opengauss database success."
    fi
}

# for install step
if [ $1 = 1 ]; then
    set_mini_configparam
    add_service
    start_opengauss
    set_conf
    restart_opengauss
fi

%postun
remove_service(){
    servicename=/usr/lib/systemd/system/opengauss.service
    if [ -f $servicename ]; then
        systemctl disable opengauss.service
        rm $servicename
    fi
}
clear_database(){
    pid=$(ps -ef | grep /usr/local/opengauss/bin/gaussdb | grep -v grep | awk '{print $2}')
    if [ "$pid" != "" ]; then
        kill -9 $pid
    fi
    if [ -d /var/lib/opengauss/data ]; then
        rm -rf /var/lib/opengauss/data
    fi
}
if [ "$1" = "0" ]; then
    remove_service
    clear_database
    # delete user omm
    /usr/sbin/userdel omm
    /usr/sbin/groupdel opengauss
fi

%files
%defattr (-,root,root)
%{apppath}
%doc
%{?_localstatedir}/lib/opengauss
%attr(700,omm,opengauss) %dir %{?_localstatedir}/lib/opengauss
%attr(700,omm,opengauss) %dir %{?_localstatedir}/lib/opengauss/data
%attr(644,omm,opengauss) %config(noreplace) %{?_localstatedir}/lib/opengauss/.bash_profile

%changelog
* Mon Sep 23 2024 huangji <huangji@iscas.ac.cn> - master
- Support riscv64 platform
