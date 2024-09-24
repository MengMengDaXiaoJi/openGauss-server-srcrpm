version=master
server_repo=https://gitee.com/opengauss/openGauss-server
third_party_repo=https://gitee.com/opengauss/openGauss-third_party

# clone openGauss-server and package it
server_name=openGauss-server-$version
if [ ! -f $server_name.tar.gz ]; then
    if [ ! -d $server_name ]; then
        git clone -b $version $server_repo $server_name
    else
        pushd $server_name
	git pull
	popd
    fi    
    tar -zcf "${server_name}.tar.gz" $server_name
    #rm -rf $server_name
fi

