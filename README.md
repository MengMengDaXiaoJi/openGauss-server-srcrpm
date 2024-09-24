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
      sh ./updatecode.sh
    ```

#### 安装

1.  安装编译后生成的rpm包

    ```shell
      dnf install -y opengauss-master-1.riscv64.rpm
    ```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
