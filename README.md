# opengauss-srcrpm

#### 介绍
用于打包适配好的riscv64平台的openGauss-server，同时兼容x86_64平台和aarch64平台

#### 软件架构
主要适配riscv64平台，同时兼容x86_64平台和aarch64平台


#### 准备

1.  准备一个riscv64架构的openEuler系统，或者一个使用riscv64架构的容器环境
    
    可以使用我们的[镜像](https://mirror.iscas.ac.cn/openeuler-sig-riscv/openEuler-RISC-V/preview/openEuler-22.03-V2-riscv64/openeuler-rootfs.tar.gz)跟文件系统搭建系统或者容器环境

2.  执行updatecode.sh脚本克隆打包openGauss-server master分支最新代码

    ```shell
      chmod +x ./updatecode.sh
      sh ./updatecode.sh
    ```

3.  将代码拷贝到rpmbuild所使用的SOURCE目录

#### 编译

1.  安装编译依赖

    ```shell
      yum-builddep opengauss-server.spec
    ```

2.  开始编译
    
    ```shell
      rpmbuild -ba opengauss-server.spec
    ```


#### 安装

1.  安装编译后生成的rpm包

    ```shell
      dnf install -y opengauss-master-1.full_no_mot.riscv64.rpm
    ```

