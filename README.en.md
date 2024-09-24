# opengauss-srcrpm

#### Description
This project is used to build and package openGauss-server master code on riscv64 platform, also compatible with x86_64 and aarch64 architectures.

#### Software Architecture
Mainly for riscv64, also compatible with x86_64 and aarch64 architectures.

#### Prepare

1.  prepare a openeuler system on riscv64 platform or a container with openeuler system.

    You can use our [mirror rootfs openeuler22.03](https://mirror.iscas.ac.cn/openeuler-sig-riscv/openEuler-RISC-V/preview/openEuler-22.03-V2-riscv64/openeuler-rootfs.tar.gz)

2.  execute the updatecode.sh to clone and package latest openGauss-server master code.

    ```shell
    sh ./updatecode.sh
    ```

#### Install

1.  install the output rpm with follow script

    ```shell 
    dnf install -y opengauss-master-1.riscv64.rpm
    ```

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request

