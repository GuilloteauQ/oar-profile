with (import <nixpkgs>{});

python37Packages.buildPythonPackage rec {
  name = "oar-profile";
  version = "1.0";

  # src = fetchTarball("https://github.com/GuilloteauQ/oar-profile/tarball/main");
  src = ./.;
  propagatedBuildInputs = with python37Packages; [
  ];

  doCheck = false;

  postInstall = ''
    cp -r app/ $out
  '';
}
