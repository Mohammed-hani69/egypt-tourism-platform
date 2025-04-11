{pkgs}: {
  deps = [
    pkgs.libmysqlclient
    pkgs.postgresql
    pkgs.openssl
  ];
}
